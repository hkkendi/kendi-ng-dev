#!/usr/bin/env python3
"""
Zoe school date reminders — the date-driven counterpart to ai_check.py.

Where ai_check.py emails when a NEW date is *discovered* (news), this script
emails as a recorded date *approaches*. It runs daily, reads the curated dates
already in zoe-school/data/schools.json (openDay / appDateConfirmed /
resultDate) and emails mk@leary.hk a reminder 7 days before and again 1 day
before each date.

Each (school, field, date, lead) milestone is emailed once — tracked in
zoe-school/data/reminder-state.json — so a date never nags twice for the same
lead. The "days until" is computed in HKT so "tomorrow" means tomorrow in HK.

Robust to a missed daily run: a lead fires when days_until <= lead (not just
== lead), and every lead that has effectively passed is marked sent in the same
pass, so a skipped day never drops a reminder or sends a duplicate.

Email is sent only when ZOE_REMINDER_EMAIL=1 and MS_* credentials are present;
otherwise it prints what it *would* send (safe dry-run for local testing).
"""
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta, date

import requests

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

HKT = timezone(timedelta(hours=8))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHOOLS_FILE = os.path.join(ROOT, "zoe-school", "data", "schools.json")
STATE_FILE = os.path.join(ROOT, "zoe-school", "data", "reminder-state.json")
RECIPIENT = "mk@leary.hk"

# Days before a date to nudge. Fires at each threshold, once per milestone.
LEADS = [7, 1]

# The recorded date fields we count down to, with their display label.
DATE_FIELDS = [
    ("openDay", "Open Day"),
    ("appDateConfirmed", "Application"),
    ("resultDate", "Results"),
]

ISO_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def to_iso_date(value):
    """Pull a YYYY-MM-DD date out of a field even if wrapped in other text."""
    if not isinstance(value, str):
        return None
    m = ISO_RE.search(value)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def when_phrase(days):
    if days == 0:
        return "today"
    if days == 1:
        return "tomorrow"
    return f"in {days} days"


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def collect_due(schools, today, prev_sent):
    """Return (due, newly_sent).

    `due` is a list of reminder rows for dates whose 7-day / 1-day threshold has
    arrived and not yet been sent. `newly_sent` is the set of milestone keys to
    persist so they don't fire again.
    """
    due = []
    newly_sent = set(prev_sent)
    for s in schools:
        name = s.get("nameEn") or s.get("nameZh") or s["id"]
        for field, label in DATE_FIELDS:
            d = to_iso_date(s.get(field))
            if not d:
                continue
            days = (d - today).days
            if days < 0:
                continue  # date already passed
            fired = [L for L in LEADS
                     if days <= L and (s["id"], field, d.isoformat(), L) not in prev_sent]
            if not fired:
                continue
            for L in fired:
                newly_sent.add((s["id"], field, d.isoformat(), L))
            due.append({
                "nameEn": name, "nameZh": s.get("nameZh", ""),
                "event": label, "date": d.isoformat(),
                "days": days, "when": when_phrase(days),
                "url": s.get("website", ""),
            })
    # Soonest first.
    due.sort(key=lambda r: r["days"])
    return due, newly_sent


# ---------------------------------------------------------------- email (Graph)

def load_creds():
    env = {}
    for k in ("MS_TENANT_ID", "MS_CLIENT_ID", "MS_CLIENT_SECRET", "SENDER_EMAIL", "BCC_EMAIL"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def build_html(rows):
    body = "".join(
        f"<tr>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>{r['nameEn']}<br>"
        f"<span style='color:#666'>{r['nameZh']}</span></td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>{r['event']}</td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'><b>{r['date']}</b></td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'><b>{r['when']}</b></td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'><a href='{r['url']}'>site</a></td></tr>"
        for r in rows
    )
    return (
        "<div style=\"font-family:Arial,sans-serif;font-size:14px;color:#222\">"
        "<p>Hi Mum &amp; Dad \U0001F476,</p>"
        f"<p>Reminder — <b>{len(rows)} of Zoe's school date(s)</b> are coming up:</p>"
        "<table style=\"border-collapse:collapse;margin:12px 0\">"
        "<tr style=\"background:#f3f3f3\">"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">School</th>"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">Event</th>"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">Date</th>"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">When</th>"
        "<th style=\"padding:6px 12px;border:1px solid #ddd;text-align:left\">Link</th>"
        f"</tr>{body}</table>"
        "<p>Full tracker: <a href=\"https://kendi-ng.com/zoe-school/\">kendi-ng.com/zoe-school</a></p>"
        "<p style=\"color:#888;font-size:12px\">Dates are AI-detected — confirm against "
        "the school site before relying on one.</p></div>"
    )


def send_email(rows):
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
    soonest = min(r["days"] for r in rows)
    subject = f"Zoe school reminder — {len(rows)} date(s) coming up ({when_phrase(soonest)})"
    message = {
        "subject": subject,
        "body": {"contentType": "HTML", "content": build_html(rows)},
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
        print(f"   emailed {RECIPIENT} ({len(rows)} reminder row(s))")
        return True
    print(f"   email send failed: HTTP {r.status_code} {r.text[:200]}")
    return False


# ---------------------------------------------------------------- main

def main():
    data = load_json(SCHOOLS_FILE, None)
    if not data or "schools" not in data:
        print(f"Could not read {SCHOOLS_FILE}")
        return 1
    state = load_json(STATE_FILE, {"sent": []})
    prev_sent = {tuple(x) for x in state.get("sent", [])}
    now = datetime.now(HKT)
    today = now.date()

    due, newly_sent = collect_due(data["schools"], today, prev_sent)

    print(f"Zoe reminders — {now.strftime('%Y-%m-%d %H:%M HKT')}")
    if not due:
        print("No dates hit a 7-day or 1-day threshold today.")
        return 0

    for r in due:
        print(f"  {r['nameEn']} — {r['event']} {r['date']} ({r['when']})")

    sent_ok = False
    if os.environ.get("ZOE_REMINDER_EMAIL") == "1":
        try:
            sent_ok = send_email(due)
        except Exception as e:
            print(f"   email error: {str(e)[:160]}")
    else:
        print("   dry-run (ZOE_REMINDER_EMAIL != 1) — not emailing, not marking sent")

    # Only persist milestones as "sent" once the email actually went out, so a
    # failed/skip send retries next run instead of silently swallowing a date.
    if sent_ok:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"updatedAt": now.isoformat(timespec="seconds"),
                       "sent": sorted(list(newly_sent))}, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
