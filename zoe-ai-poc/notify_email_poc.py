"""
POC (A): the mk@leary.hk notification — self-contained.

It does two things:
  1. Builds the "schools updated this week" HTML email and writes it to a
     preview file you can open in a browser. (Runs anywhere, no credentials.)
  2. Sends it for real via the Microsoft Graph API (`sendMail`) using the
     app-registration credentials in the project .env (client-credentials
     flow). Credentials are read at runtime — never hard-coded here.

Usage:
  python notify_email_poc.py            # preview only (no send)
  python notify_email_poc.py --check    # verify Graph auth (acquire token, no mail)
  python notify_email_poc.py --send     # actually deliver to mk@leary.hk
"""
import json
import os
import sys
import webbrowser

import requests

RECIPIENT = "mk@leary.hk"
PREVIEW_PATH = os.path.expanduser("~/zoe_email_preview.html")

GRAPH_TOKEN_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
GRAPH_SENDMAIL_URL = "https://graph.microsoft.com/v1.0/users/{sender}/sendMail"

# The data the AI extractor (POC B) produced for True Light Kowloon.
UPDATES = [
    {"nameEn": "Kowloon True Light KG", "nameZh": "九龍真光中學（幼稚園部）",
     "event": "Briefing 簡介會", "date": "2025-09-13", "confidence": "high",
     "url": "https://www.ktlks.edu.hk"},
    {"nameEn": "Kowloon True Light KG", "nameZh": "九龍真光中學（幼稚園部）",
     "event": "Interview 面試", "date": "2025-11-01", "confidence": "high",
     "url": "https://www.ktlks.edu.hk"},
    {"nameEn": "Kowloon True Light KG", "nameZh": "九龍真光中學（幼稚園部）",
     "event": "Results 公佈結果", "date": "2025-11-12", "confidence": "high",
     "url": "https://www.ktlks.edu.hk"},
]


def load_env(path: str = None) -> dict:
    """Parse the project .env (KEY=value or KEY = "value"); real env overrides."""
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    env = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    for k in list(env):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def build_html(updates: list) -> str:
    rows = "".join(
        f"<tr>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>{u['nameEn']}<br>"
        f"<span style='color:#666'>{u['nameZh']}</span></td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>{u['event']}</td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'><b>{u['date']}</b></td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>{u['confidence']}</td>"
        f"<td style='padding:6px 12px;border:1px solid #ddd'>"
        f"<a href='{u['url']}'>site</a></td></tr>"
        for u in updates
    )
    return f"""\
<div style="font-family:Arial,sans-serif;font-size:14px;color:#222">
  <p>Hi Mum &amp; Dad 👶,</p>
  <p>The Zoe school checker found <b>{len(updates)} new date(s)</b> this week:</p>
  <table style="border-collapse:collapse;margin:12px 0">
    <tr style="background:#f3f3f3">
      <th style="padding:6px 12px;border:1px solid #ddd;text-align:left">School</th>
      <th style="padding:6px 12px;border:1px solid #ddd;text-align:left">Event</th>
      <th style="padding:6px 12px;border:1px solid #ddd;text-align:left">Date</th>
      <th style="padding:6px 12px;border:1px solid #ddd;text-align:left">Confidence</th>
      <th style="padding:6px 12px;border:1px solid #ddd;text-align:left">Link</th>
    </tr>{rows}
  </table>
  <p>Full tracker:
     <a href="https://kendi-ng.com/zoe-school/">kendi-ng.com/zoe-school</a></p>
  <p style="color:#888;font-size:12px">Auto-extracted by Claude — confirm against
     the school site before relying on a date.</p>
</div>"""


def get_graph_token(env: dict) -> str:
    for k in ("MS_TENANT_ID", "MS_CLIENT_ID", "MS_CLIENT_SECRET"):
        if not env.get(k):
            raise RuntimeError(f"Missing {k} in .env")
    r = requests.post(
        GRAPH_TOKEN_URL.format(tenant=env["MS_TENANT_ID"]),
        data={
            "client_id": env["MS_CLIENT_ID"],
            "client_secret": env["MS_CLIENT_SECRET"],
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        },
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Token request failed: HTTP {r.status_code} {r.text[:300]}")
    return r.json()["access_token"]


def send_via_graph(subject: str, html: str, env: dict = None) -> None:
    env = env or load_env()
    sender = env.get("SENDER_EMAIL")
    if not sender:
        raise RuntimeError("Missing SENDER_EMAIL in .env")
    token = get_graph_token(env)
    message = {
        "subject": subject,
        "body": {"contentType": "HTML", "content": html},
        "toRecipients": [{"emailAddress": {"address": RECIPIENT}}],
    }
    if env.get("BCC_EMAIL"):
        message["bccRecipients"] = [{"emailAddress": {"address": env["BCC_EMAIL"]}}]
    r = requests.post(
        GRAPH_SENDMAIL_URL.format(sender=sender),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps({"message": message, "saveToSentItems": True}),
        timeout=30,
    )
    if r.status_code not in (200, 202):
        raise RuntimeError(f"Graph sendMail failed: HTTP {r.status_code} {r.text[:400]}")


def main() -> int:
    env = load_env()

    if "--check" in sys.argv:
        # Verify the Graph app credentials work (acquire a token; send no mail).
        try:
            tok = get_graph_token(env)
            print(f"Graph auth OK — token acquired ({len(tok)} chars). "
                  f"Sender: {env.get('SENDER_EMAIL', '?')}")
            print("Note: sendMail also requires the app to have the Mail.Send "
                  "APPLICATION permission (admin-consented) in the tenant.")
            return 0
        except Exception as e:
            print(f"Graph auth FAILED: {e}")
            return 1

    if not UPDATES:
        print("No updates — no email needed.")
        return 0

    subject = f"Zoe school tracker — {len(UPDATES)} new date(s) this week"
    html = build_html(UPDATES)

    with open(PREVIEW_PATH, "w", encoding="utf-8") as f:
        f.write(f"<h3 style='font-family:Arial'>To: {RECIPIENT} &nbsp;|&nbsp; "
                f"Subject: {subject}</h3><hr>{html}")
    print(f"Preview written: {PREVIEW_PATH}")

    if "--send" in sys.argv:
        send_via_graph(subject, html, env)
        print(f"SENT to {RECIPIENT} via Microsoft Graph (from {env.get('SENDER_EMAIL')}).")
    else:
        try:
            webbrowser.open(f"file:///{PREVIEW_PATH.replace(os.sep, '/')}")
        except Exception:
            pass
        print("Preview only. Re-run with --send to deliver to mk@leary.hk via Graph "
              "(or --check to validate Graph auth without sending).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
