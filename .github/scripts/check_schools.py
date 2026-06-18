#!/usr/bin/env python3
"""
Zoe K1 school checker.

Reads the live school list from zoe-school/data/schools.json (so it never goes
stale), fetches each school website, extracts admission-related snippets + date
tokens, and compares them against the previous run stored in
zoe-school/data/crawl-state.json.

When something changes (a new open day, application date, or admission notice),
it:
  - prints a summary to the Actions log,
  - writes a human-readable zoe-school/data/crawl-log.md,
  - updates crawl-state.json (so the same change isn't flagged twice),
  - sets the GitHub Actions output `changes=true` and writes an issue body to
    $GITHUB_STEP_SUMMARY and issue-body.md so the workflow can open an issue.

Exit code is always 0 on a completed crawl; "changes detected" is signalled via
the `changes` output, not the exit code.
"""

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

import requests
from bs4 import BeautifulSoup

# Ensure emoji/CJK output works regardless of console encoding (Windows cp1252).
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

HKT = timezone(timedelta(hours=8))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHOOLS_FILE = os.path.join(ROOT, "zoe-school", "data", "schools.json")
STATE_FILE = os.path.join(ROOT, "zoe-school", "data", "crawl-state.json")
LOG_FILE = os.path.join(ROOT, "zoe-school", "data", "crawl-log.md")
ISSUE_BODY_FILE = os.path.join(ROOT, "issue-body.md")

# A realistic browser UA — several school sites 403 on obvious bot UAs.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-HK,zh;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Words that flag a line as admission / open-day relevant (zh + en).
KEYWORDS = [
    "開放日", "簡介會", "報名", "申請", "入學", "招生", "註冊", "面試", "收生",
    "open day", "info session", "information session", "admission", "application",
    "apply", "enrol", "enroll", "register", "registration", "interview", "k1",
]

# Date-ish tokens worth surfacing at a glance: zh dates, dd/mm/yyyy, "18 Jul 2026", ranges.
DATE_PATTERNS = [
    r"202[6-9]\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日",       # 2026年9月15日
    r"202[6-9]\s*年\s*\d{1,2}\s*月",                       # 2026年9月
    r"\d{1,2}\s*[\/\-\.]\s*\d{1,2}\s*[\/\-\.]\s*202[6-9]",  # 15/9/2026
    r"\d{1,2}\s*月\s*\d{1,2}\s*日",                         # 9月15日
    r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+202[6-9]",  # 18 Jul 2026
]


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def extract_relevant(html):
    """Return (snippets, dates) for admission-relevant content on the page."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    snippets = []
    for ln in lines:
        low = ln.lower()
        if any(kw.lower() in low for kw in KEYWORDS):
            # Keep it readable; drop noisy menu-length lines.
            if 2 <= len(ln) <= 200:
                snippets.append(ln)

    dates = []
    for pat in DATE_PATTERNS:
        for m in re.findall(pat, text):
            tok = re.sub(r"\s+", "", m) if re.search(r"[年月日]", m) else m.strip()
            if tok not in dates:
                dates.append(tok)

    # Dedupe snippets, keep order.
    seen = set()
    uniq = []
    for s in snippets:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    return uniq[:40], dates[:20]


def check_school(school):
    sid = school["id"]
    url = school.get("website")
    name = school.get("nameEn") or school.get("nameZh") or sid
    if not url:
        return {"id": sid, "name": name, "status": "skip", "reason": "no website"}
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or r.encoding
        snippets, dates = extract_relevant(r.text)
        fingerprint = hashlib.sha256(
            ("\n".join(snippets) + "|" + "|".join(sorted(dates))).encode("utf-8")
        ).hexdigest()
        return {
            "id": sid,
            "name": name,
            "url": url,
            "status": "ok",
            "snippets": snippets,
            "dates": dates,
            "fingerprint": fingerprint,
            "checked_at": datetime.now(HKT).isoformat(timespec="seconds"),
        }
    except Exception as e:
        return {"id": sid, "name": name, "url": url, "status": "error", "error": str(e)}


def set_output(name, value):
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"{name}={value}\n")


def main():
    data = load_json(SCHOOLS_FILE, None)
    if not data or "schools" not in data:
        print(f"❌ Could not read {SCHOOLS_FILE}")
        sys.exit(1)

    schools = data["schools"]
    prev = load_json(STATE_FILE, {"schools": {}})
    prev_schools = prev.get("schools", {})

    now = datetime.now(HKT)
    stamp = now.strftime("%Y-%m-%d %H:%M HKT")
    print(f"\n{'='*64}\nZoe School Checker — {stamp}\n{'='*64}\n")

    new_state = {"lastCrawl": now.isoformat(timespec="seconds"), "schools": {}}
    changed = []
    errors = []

    for school in schools:
        res = check_school(school)
        sid = res["id"]
        name = res["name"]

        if res["status"] == "error":
            errors.append(res)
            print(f"❌  {name} ({sid}): {res['error']}")
            # Preserve previous good state on error so we don't lose the baseline.
            if sid in prev_schools:
                new_state["schools"][sid] = prev_schools[sid]
            continue
        if res["status"] == "skip":
            print(f"⏭️   {name} ({sid}): {res['reason']}")
            continue

        new_state["schools"][sid] = {
            "fingerprint": res["fingerprint"],
            "dates": res["dates"],
            "snippets": res["snippets"],
            "checked_at": res["checked_at"],
        }

        old = prev_schools.get(sid)
        if old is None:
            print(f"🆕  {name} ({sid}): baseline captured ({len(res['dates'])} date tokens)")
        elif old.get("fingerprint") != res["fingerprint"]:
            new_dates = [d for d in res["dates"] if d not in old.get("dates", [])]
            old_snips = set(old.get("snippets", []))
            new_snips = [s for s in res["snippets"] if s not in old_snips]
            res["new_dates"] = new_dates
            res["new_snippets"] = new_snips
            changed.append(res)
            print(f"⚠️   {name} ({sid}): CHANGED — {len(new_dates)} new date(s), {len(new_snips)} new line(s)")
            for d in new_dates:
                print(f"        📅 {d}")
        else:
            print(f"✅  {name} ({sid}): no change")

    # Write updated state.
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_state, f, ensure_ascii=False, indent=2)

    # Human-readable log.
    write_log(stamp, schools, changed, errors, new_state)

    print(f"\n{'='*64}")
    print(f"Summary: {len(changed)} school(s) changed, {len(errors)} error(s)")
    print(f"{'='*64}\n")

    if changed:
        write_issue_body(stamp, changed)
        set_output("changes", "true")
    else:
        set_output("changes", "false")


def write_log(stamp, schools, changed, errors, state):
    lines = [f"# Zoe school crawl log", "", f"_Last crawl: {stamp}_", ""]
    if changed:
        lines.append("## ⚠️ Changes detected this run")
        lines.append("")
        for c in changed:
            lines.append(f"### {c['name']} ([site]({c['url']}))")
            if c.get("new_dates"):
                lines.append(f"- **New date tokens:** {', '.join(c['new_dates'])}")
            for s in c.get("new_snippets", [])[:10]:
                lines.append(f"  - {s}")
            lines.append("")
    else:
        lines.append("## ✅ No changes detected this run")
        lines.append("")
    if errors:
        lines.append("## ❌ Errors (sites unreachable)")
        lines.append("")
        for e in errors:
            lines.append(f"- **{e['name']}** ({e['url']}): {e['error']}")
        lines.append("")
    lines.append("## Current snapshot per school")
    lines.append("")
    for sid, info in state["schools"].items():
        dates = ", ".join(info.get("dates", [])) or "—"
        lines.append(f"- **{sid}**: {dates}  _(checked {info.get('checked_at','?')})_")
    lines.append("")
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_issue_body(stamp, changed):
    lines = [
        f"Automated weekly crawl detected possible admission updates on **{len(changed)}** school site(s).",
        f"_Crawl: {stamp}_",
        "",
        "Please review and update `zoe-school/data/schools.json` (`openDay`, `appDateConfirmed`, `status`) if confirmed.",
        "",
    ]
    for c in changed:
        lines.append(f"### {c['name']}")
        lines.append(f"{c['url']}")
        if c.get("new_dates"):
            lines.append(f"- **New date tokens found:** {', '.join(c['new_dates'])}")
        for s in c.get("new_snippets", [])[:10]:
            lines.append(f"  - {s}")
        lines.append("")
    body = "\n".join(lines)
    with open(ISSUE_BODY_FILE, "w", encoding="utf-8") as f:
        f.write(body)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(body)


if __name__ == "__main__":
    main()
