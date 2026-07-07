#!/usr/bin/env python3
"""
Zoe school AI checker — runs in GitHub Actions on the Claude Agent SDK.

For each school it:
  1. fetches the page text (browser UA + SSL fallback, same as check_schools.py),
  2. runs the Agent SDK `record_findings` tool to get clean, schema-validated
     JSON of K1 admission dates (open day / application / interview / results),
  3. confidence-gates the results:
       high     -> writes openDay / appDateConfirmed (+ note, status) into
                   schools.json, and collects NEW high-confidence dates for email,
       med/low  -> surfaces as a `crawlerHint` (verify) only; never overwrites
                   the curated openDay / appDateConfirmed fields,
  4. diffs against ai-state.json so only genuinely new dates trigger an email,
  5. emails mk@leary.hk via Microsoft Graph when new high-confidence dates appear.

Auth: in CI the Agent SDK runs on the subscription credit via the
CLAUDE_CODE_OAUTH_TOKEN env var (generate locally with `claude setup-token`).
Model: ZOE_AI_MODEL env (default claude-sonnet-4-6) — a cheap, CJK-capable
choice for this extraction.

Email is sent only when ZOE_AI_EMAIL=1 and MS_* credentials are present.
"""
import asyncio
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

HKT = timezone(timedelta(hours=8))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHOOLS_FILE = os.path.join(ROOT, "zoe-school", "data", "schools.json")
AI_STATE_FILE = os.path.join(ROOT, "zoe-school", "data", "ai-state.json")
MODEL = os.environ.get("ZOE_AI_MODEL", "claude-sonnet-4-6")
RECIPIENT = "mk@leary.hk"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-HK,zh;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

FINDINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "found": {"type": "boolean"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "event": {"type": "string",
                              "description": "Open Day, Application, Interview, Briefing, or Results"},
                    "date": {"type": "string", "description": "ISO date YYYY-MM-DD"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "quote": {"type": "string", "description": "exact sentence the date came from"},
                },
                "required": ["event", "date", "confidence", "quote"],
            },
        },
    },
    "required": ["found", "items"],
}

# The entry level a school admits at drives what dates we ask the model to find.
# Not hardcoded to K1 any more: a school's `category` in schools.json selects the
# right grade + cohort so kindergartens surface K1 dates and primary schools
# surface P1 (小一) dates from the same crawl.
LEVELS = {
    "kindergarten": {
        "grade": "K1 (nursery / 幼兒班)",
        "cohort": "the 2027/2028 school year (child entering K1 in Sep 2027)",
    },
    "primary": {
        "grade": "Primary One (P1 / 小一)",
        "cohort": "September 2027 entry (2027/2028 school year)",
    },
}


def level_of(school):
    """Map a school's category to a known admission level (default kindergarten)."""
    return "primary" if school.get("category") == "primary" else "kindergarten"


def system_for(level):
    spec = LEVELS.get(level, LEVELS["kindergarten"])
    grade, cohort = spec["grade"], spec["cohort"]
    return (
        "You are a data-extraction backend for a Hong Kong school admission "
        "tracker. You read page text and call the record_findings tool exactly "
        f"once with {grade} admission dates for {cohort}: open days / briefings "
        "(簡介會), application periods, interviews, and result-announcement dates. "
        "For an application period, report the CLOSING / deadline (截止) date as the "
        "'Application' date. Normalise every date to ISO YYYY-MM-DD. Ignore unrelated "
        "dates (copyright, past events, other grades or year levels, other cohorts). "
        f"Mark confidence 'high' only when the date is explicit and clearly tied to "
        f"{grade} admission for {cohort}. Some primary schools admit through the "
        "government Primary One Admission (POA / 自行分配學位 · 統一派位) system with no "
        "separate school application — if so, still capture any published key dates "
        "but mark them 'medium'. You MUST call record_findings — never answer in prose."
    )

# ---------------------------------------------------------------- pure helpers

ISO_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def normalize_date(value):
    """Return YYYY-MM-DD if the string contains a clean ISO date, else None."""
    if not isinstance(value, str):
        return None
    m = ISO_RE.search(value)
    if not m:
        return None
    y, mo, d = m.groups()
    if not ("2026" <= y <= "2029"):
        return None
    return f"{y}-{mo}-{d}"


def map_event(event):
    """Classify an event label into the schools.json field it maps onto."""
    e = (event or "").lower()
    if any(k in e for k in ("open day", "開放日", "簡介", "briefing", "info", "visit")):
        return "openDay"
    if any(k in e for k in ("application", "報名", "申請", "enrol", "register", "招生")):
        return "appDateConfirmed"
    if any(k in e for k in ("result", "放榜", "公佈", "公布", "取錄", "announce", "notification")):
        return "resultDate"
    # interview etc. — informative, but not a primary date field
    return "note"


def apply_findings(school, items, prev_seen, now):
    """Apply the confidence gate to one school (mutates it). Pure & testable.

    Returns (new_high, hint) where new_high is a list of {event, date} that are
    high-confidence AND not previously seen, and hint is a crawlerHint dict (or
    None) for the medium/low-confidence findings.
    """
    today = now.strftime("%Y-%m-%d")
    new_high = []
    hint_dates, hint_lines = [], []
    notes = []
    for it in items or []:
        ev = (it.get("event") or "").strip()
        conf = it.get("confidence", "low")
        iso = normalize_date(it.get("date", ""))
        if not iso:
            continue
        field = map_event(ev)
        if conf == "high":
            if field == "openDay" and school.get("openDay") != iso:
                school["openDay"] = iso
                school["openDayNote"] = f"\U0001F916 AI-detected {iso} — verify ({ev})"
            elif field == "appDateConfirmed" and school.get("appDateConfirmed") != iso:
                school["appDateConfirmed"] = iso
                school["appDateNote"] = f"\U0001F916 AI-detected {iso} — verify ({ev})"
                school["status"] = "confirmed"
            elif field == "resultDate" and school.get("resultDate") != iso:
                school["resultDate"] = iso
                school["resultDateNote"] = f"\U0001F916 AI-detected {iso} — verify ({ev})"
            elif field == "note":
                notes.append(f"{ev}: {iso}")
            if (school["id"], ev, iso) not in prev_seen:
                new_high.append({"event": ev, "date": iso})
        else:
            hint_dates.append(iso)
            hint_lines.append(f"{ev}: {iso}")
    if notes:
        existing = school.get("appDateNote") or ""
        extra = " · ".join(notes)
        school["appDateNote"] = (existing + " · " if existing else "") + "\U0001F916 " + extra
    hint = None
    if hint_dates or hint_lines:
        hint = {"detectedAt": today, "dates": hint_dates[:4], "lines": hint_lines[:2]}
    return new_high, hint


# ---------------------------------------------------------------- fetch + LLM

def fetch_text(url):
    try:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        except requests.exceptions.SSLError:
            r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True, verify=False)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or r.encoding
        soup = BeautifulSoup(r.text, "html.parser")
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        return re.sub(r"\s+", " ", soup.get_text(" ")).strip()
    except Exception as e:
        print(f"   fetch error: {str(e)[:80]}")
        return None


def urls_for(school):
    """Homepage plus any extra admission/news sub-pages to crawl for this school.

    Many HK school sites keep the actual open-day/application dates on an
    admissions or news sub-page (or behind a JS redirect), not the homepage —
    so `crawlUrls` lets a school point the crawler straight at them.
    """
    out = []
    for u in [school.get("website")] + list(school.get("crawlUrls", [])):
        if u and u not in out:
            out.append(u)
    return out


def fetch_combined(school):
    """Fetch every URL for a school and join the page text (sub-pages first,
    as they carry the dates; homepage last)."""
    parts = []
    for u in urls_for(school):
        t = fetch_text(u)
        if t and len(t) >= 30:
            parts.append(t)
    return "\n\n----\n\n".join(parts) if parts else None


_captured = {}


async def _extract(text, level="kindergarten", urls=None):
    """Run the Agent SDK record_findings tool and return its validated args.

    Plain `requests` can't see dates on JavaScript-rendered school sites (the
    content loads client-side after the HTML). When `urls` are given we also let
    the agent use WebFetch — which renders those pages — so it can read dates the
    pre-fetched text is missing, then record them. WebFetch is additive: if it
    fails (e.g. a geo-blocked HK site with the VPN down) the agent still has the
    pre-fetched text to fall back on."""
    from claude_agent_sdk import (
        AssistantMessage, ClaudeAgentOptions, ResultMessage, ToolUseBlock,
        create_sdk_mcp_server, query, tool,
    )

    _captured.clear()

    grade = LEVELS.get(level, LEVELS["kindergarten"])["grade"]

    @tool("record_findings", f"Record extracted {grade} admission dates.", FINDINGS_SCHEMA)
    async def record_findings(args):
        _captured.clear()
        _captured.update(args)
        return {"content": [{"type": "text", "text": "recorded"}]}

    server = create_sdk_mcp_server("zoe", tools=[record_findings])
    allowed = ["mcp__zoe__record_findings"]
    if urls:
        allowed.append("WebFetch")
    options = ClaudeAgentOptions(
        model=MODEL,
        system_prompt=system_for(level),
        mcp_servers={"zoe": server},
        allowed_tools=allowed,
        permission_mode="bypassPermissions",
        max_turns=6 if urls else 3,
    )
    prompt = f"Extract {grade} admission dates from this page text:\n\n" + text[:12000]
    if urls:
        prompt += (
            "\n\n----\nIf the text above is missing clear, explicit "
            f"{grade} admission dates (or shows only a JS/loading shell), use the "
            "WebFetch tool to read the official page(s) below, which render the "
            "live dates, then extract from what you read:\n" + "\n".join(urls[:3])
        )
    last_result = None
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, ResultMessage):
                last_result = msg
            elif isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, ToolUseBlock) and block.name.endswith("record_findings"):
                        pass
    except Exception as e:
        # The CLI emits a result with is_error=True then exits non-zero on an
        # API error (401/429/5xx); the raised error only carries the subtype.
        # Surface the real HTTP status the CLI reported so failures are diagnosable.
        status = getattr(last_result, "api_error_status", None)
        errs = getattr(last_result, "errors", None)
        if status or errs:
            raise RuntimeError(
                f"API error (HTTP {status or '?'}) from Claude CLI: {errs or e}"
            ) from e
        raise
    return dict(_captured)


def extract(text, level="kindergarten", urls=None):
    return asyncio.run(_extract(text, level, urls))


# ---------------------------------------------------------------- email (Graph)

def load_creds():
    env = {}
    for k in ("MS_TENANT_ID", "MS_CLIENT_ID", "MS_CLIENT_SECRET", "SENDER_EMAIL", "BCC_EMAIL"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def build_html(updates):
    rows = "".join(
        f"<tr>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>{u['nameEn']}<br>"
        f"<span style='color:#666'>{u['nameZh']}</span></td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>{u['event']}</td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'><b>{u['date']}</b></td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'><a href='{u['url']}'>site 校網</a></td></tr>"
        for u in updates
    )
    return (
        "<div style=\"font-family:Arial,sans-serif;font-size:14px;color:#222\">"
        "<p>Hi Mum &amp; Dad \U0001F476,</p>"
        f"<p>The Zoe school checker found <b>{len(updates)} new date(s)</b> this week:<br>"
        f"<span style=\"color:#555\">Zoe 學校檢查器今週發現 <b>{len(updates)} 個新日期</b>：</span></p>"
        "<table style=\"border-collapse:collapse;margin:12px 0\">"
        "<tr style=\"background:#f3f3f3\">"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">School 學校</th>"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">Event 項目</th>"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">Date 日期</th>"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">Link 連結</th>"
        f"</tr>{rows}</table>"
        "<p>Full tracker 完整追蹤器：<a href=\"https://kendi-ng.com/zoe-school/\">kendi-ng.com/zoe-school</a></p>"
        "<p style=\"color:#888;font-size:12px\">Auto-extracted by Claude — confirm against the school site "
        "before relying on a date. 由 Claude 自動擷取，報名前請以官方網站核實。</p></div>"
    )


def send_email(updates):
    env = load_creds()
    for k in ("MS_TENANT_ID", "MS_CLIENT_ID", "MS_CLIENT_SECRET", "SENDER_EMAIL"):
        if not env.get(k):
            print(f"   email skipped: missing {k}")
            return False
    tok = requests.post(
        f"https://login.microsoftonline.com/{env['MS_TENANT_ID']}/oauth2/v2.0/token",
        data={
            "client_id": env["MS_CLIENT_ID"], "client_secret": env["MS_CLIENT_SECRET"],
            "scope": "https://graph.microsoft.com/.default", "grant_type": "client_credentials",
        }, timeout=30,
    )
    if tok.status_code != 200:
        print(f"   email token failed: HTTP {tok.status_code}")
        return False
    token = tok.json()["access_token"]
    message = {
        "subject": f"Zoe school tracker 學校追蹤 — {len(updates)} new date(s) 個新日期 this week",
        "body": {"contentType": "HTML", "content": build_html(updates)},
        "toRecipients": [{"emailAddress": {"address": RECIPIENT}}],
    }
    if env.get("BCC_EMAIL"):
        message["bccRecipients"] = [{"emailAddress": {"address": env["BCC_EMAIL"]}}]
    r = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{env['SENDER_EMAIL']}/sendMail",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps({"message": message, "saveToSentItems": True}), timeout=30,
    )
    if r.status_code in (200, 202):
        print(f"   emailed {RECIPIENT} ({len(updates)} new date(s))")
        return True
    print(f"   email send failed: HTTP {r.status_code} {r.text[:200]}")
    return False


# ---------------------------------------------------------------- main

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def cache_path(school):
    d = os.environ.get("ZOE_CACHE_DIR")
    return os.path.join(d, f"{school['id']}.txt") if d else None


def page_text(school):
    """Read page text from the cache dir if present, else fetch live.

    The cache lets us split the run in two: fetch pages while the HK VPN is
    up (some HK school sites geo-block non-HK IPs), then run the Claude API
    with the VPN down (Anthropic does not serve Hong Kong — a HK exit IP
    gets every API call 403'd). Local runs with no cache just fetch live.
    """
    cp = cache_path(school)
    if cp and os.path.exists(cp):
        with open(cp, "r", encoding="utf-8") as f:
            return f.read()
    return fetch_combined(school)


def fetch_phase(data):
    """Download every school page to the cache dir; no extraction. Run with VPN up."""
    cache_dir = os.environ.get("ZOE_CACHE_DIR")
    os.makedirs(cache_dir, exist_ok=True)
    n = 0
    for school in data["schools"]:
        url = school.get("website")
        name = school.get("nameEn") or school.get("nameZh") or school["id"]
        if not url:
            continue
        print(f"- {name} ({school['id']})")
        text = fetch_combined(school)
        if text and len(text) >= 50:
            with open(cache_path(school), "w", encoding="utf-8") as f:
                f.write(text)
            n += 1
        else:
            print("   (no usable text — skipped)")
    print(f"\nFetched {n}/{len(data['schools'])} page(s) to {cache_dir}")
    return 0


def main():
    data = load_json(SCHOOLS_FILE, None)
    if not data or "schools" not in data:
        print(f"Could not read {SCHOOLS_FILE}")
        return 1

    if "--fetch-only" in sys.argv:
        return fetch_phase(data)

    state = load_json(AI_STATE_FILE, {"seen": []})
    prev_seen = {tuple(x) for x in state.get("seen", [])}
    now = datetime.now(HKT)

    all_new = []
    new_seen = set(prev_seen)
    hints = 0
    for school in data["schools"]:
        url = school.get("website")
        name = school.get("nameEn") or school.get("nameZh") or school["id"]
        if not url:
            continue
        level = level_of(school)
        print(f"- {name} ({school['id']}) [{level}]")
        text = page_text(school)
        if not text or len(text) < 50:
            continue
        try:
            # WebFetch (renders JS pages) is enabled only for schools flagged
            # with crawlUrls — the JS-rendered sites plain requests can't read —
            # so the rest keep the cheaper text-only extraction.
            fetch_urls = urls_for(school) if school.get("crawlUrls") else None
            result = extract(text, level, fetch_urls)
        except Exception as e:
            print(f"   extract error: {str(e)[:120]}")
            continue
        items = result.get("items", []) if isinstance(result, dict) else []
        new_high, hint = apply_findings(school, items, prev_seen, now)
        if hint:
            school["crawlerHint"] = hint
            hints += 1
        for nh in new_high:
            new_seen.add((school["id"], nh["event"], nh["date"]))
            all_new.append({
                "nameEn": name, "nameZh": school.get("nameZh", ""),
                "event": nh["event"], "date": nh["date"], "url": url,
            })
        if new_high:
            print(f"   {len(new_high)} new high-confidence date(s)")

    data["lastCrawl"] = now.strftime("%Y-%m-%d")
    with open(SCHOOLS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nSummary: {len(all_new)} new high-confidence date(s), {hints} hint(s)")

    # Advance the "seen" set only for dates we've actually notified about. If the
    # email fails (or emailing is disabled), keep the previous seen set so those
    # dates are retried next run — otherwise a failed send silently marks them
    # seen and they're never emailed. (schools.json already holds the new dates
    # regardless, so the tracker UI still shows them.)
    seen_to_persist = new_seen
    if all_new:
        if os.environ.get("ZOE_AI_EMAIL") == "1":
            sent_ok = False
            try:
                sent_ok = send_email(all_new)
            except Exception as e:
                print(f"   email error: {str(e)[:160]}")
            if not sent_ok:
                print("   email not confirmed — keeping these dates unseen; will retry next run.")
                seen_to_persist = prev_seen
        else:
            print("   emailing disabled (ZOE_AI_EMAIL != 1) — not marking new dates seen.")
            seen_to_persist = prev_seen

    with open(AI_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"updatedAt": now.isoformat(timespec="seconds"),
                   "seen": sorted(list(seen_to_persist))}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
