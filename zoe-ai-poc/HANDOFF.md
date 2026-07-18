# Zoe School Checker — AI upgrade handoff

Goal: make the **Open Day & Application Tracker** tab self-updating, and email
`mk@leary.hk` (me + husband) whenever a new date is found — funded by the
$100/month Agent SDK credit (programmatic Claude usage, not subscription).

## What was proven (POCs in this folder)

1. **`claude -p` extracts brilliantly but won't emit strict JSON.**
   It read True Light Kowloon's page and found the K1 briefing/interview/result
   dates the old regex missed — but always replied in prose/markdown, even with
   `--system-prompt` fully replacing the coding-agent persona. So the bare CLI
   is the wrong tool for feeding a database. (`check_ai_poc.py`)

2. **The Agent SDK gives clean, schema-validated JSON — the fix.**
   `extract_sdk_poc.py` defines a `record_findings` tool with a JSON schema and
   forces the model to call it; we read the validated tool arguments. Output for
   True Light Kowloon (dates even normalized to ISO):
   ```json
   {"found": true, "items": [
     {"event":"Briefing 簡介會","date":"2025-09-13","confidence":"high","quote":"..."},
     {"event":"Interview 面試","date":"2025-11-01","confidence":"high","quote":"..."},
     {"event":"Results 公佈結果","date":"2025-11-12","confidence":"high","quote":"..."}
   ]}
   ```
   Same engine as `claude -p` → runs on the credit. `pip install claude-agent-sdk`
   (done in anaconda env; v0.2.110).

3. **Email notifier works as a preview.** `notify_email_poc.py` builds the
   "schools updated" HTML and opens a browser preview. Send path is stubbed —
   SEE BELOW, use Graph API instead of the SMTP stub.

## Target architecture (the loop to build)

```
weekly Task Scheduler run:
  1. crawl each school page            (existing check.py logic)
  2. Agent SDK record_findings tool →  clean JSON per school   [extract_sdk_poc.py]
  3. write into schools.json fields:
       openDay / appDateConfirmed / appDateNote / status
       - high confidence  → fill + status="confirmed"
       - low confidence   → leave a PR for manual review
  4. git commit + push  →  kendi-ng.com tracker tab updates itself
  5. email mk@leary.hk via Graph API  →  "True Light K1 interview 1 Nov 2025"
```

`schools.json` fields that map to the tracker tab:
`openDay`, `openDayNote`, `appDateConfirmed`, `appDateNote`, `status`
(repo: hkkendi/kendi-ng-dev, path: `zoe-school/data/schools.json`, 23 schools).

## NEW feature request: "Add to Calendar" column on the tracker tab

Add a new column with a 📅 button per row that adds that school's date/info to
our calendar. Use a client-side **.ics download** (no backend, no auth, works
on the static site; opens in Google / Outlook / Apple Calendar alike).

Each tracker row already has: school name, event type, date (ISO from the AI
extractor), and the school URL — that's everything an event needs. Treat the
dates as all-day events. Drop-in JS for the static tracker page:

```js
function pad(n){ return String(n).padStart(2,'0'); }
function icsDate(iso){ const d=new Date(iso); return `${d.getFullYear()}${pad(d.getMonth()+1)}${pad(d.getDate())}`; }

function addToCalendar(school, event, isoDate, url){
  const start = icsDate(isoDate);
  const endD = new Date(isoDate); endD.setDate(endD.getDate()+1);  // all-day = next-day DTEND
  const end = `${endD.getFullYear()}${pad(endD.getMonth()+1)}${pad(endD.getDate())}`;
  const ics = [
    'BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//kendi-ng//zoe-school//EN',
    'BEGIN:VEVENT',
    `UID:${school}-${event}-${start}@kendi-ng.com`,
    `DTSTART;VALUE=DATE:${start}`,
    `DTEND;VALUE=DATE:${end}`,
    `SUMMARY:${school} — ${event}`,
    `DESCRIPTION:Zoe school tracker. Confirm on the school site: ${url}`,
    `URL:${url}`,
    'END:VEVENT','END:VCALENDAR'
  ].join('\r\n');
  const blob = new Blob([ics], {type:'text/calendar'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `${school}-${event}.ics`.replace(/[^\w.-]+/g,'_');
  a.click(); URL.revokeObjectURL(a.href);
}
```
```html
<!-- new column cell, per row -->
<td><button onclick="addToCalendar('True Light KG','K1 Interview','2025-11-01','https://www.ktlks.edu.hk')">📅 Add</button></td>
```

Optional alternative if you prefer a one-click web link over a download:
- Google: `https://calendar.google.com/calendar/render?action=TEMPLATE&text=<title>&dates=<YYYYMMDD>/<YYYYMMDD>&details=<...>`
- Outlook: `https://outlook.office.com/calendar/0/deeplink/compose?subject=<title>&startdt=<ISO>&enddt=<ISO>&body=<...>`
(.ics is recommended — one button covers everyone, including Apple Calendar.)

## TODO in personal-github session

- [ ] Add the **📅 Add to Calendar** column to the tracker tab (.ics snippet above).
- [ ] Swap email send from the Gmail-SMTP stub to **Microsoft Graph
      `sendMail`** using my personal email's app registration (I have access).
      Replace `send_via_gmail()` in `notify_email_poc.py` with a Graph call:
      POST `https://graph.microsoft.com/v1.0/me/sendMail` (or `/users/{id}/sendMail`)
      with the HTML body from `build_html()`. Auth via MSAL client-credentials
      or my existing token.
- [ ] Wire `extract_sdk_poc.extract()` into the real `check.py` per school
      (replace/augment the regex `extract_findings()`), keeping the
      first-run-baseline and fingerprint-diff behavior.
- [ ] Add the confidence gate: high → auto-write schools.json; low → PR only.
- [ ] Map extracted `event` types onto the right schools.json field
      (Open Day → openDay; Application/Interview → appDateConfirmed/appDateNote).
- [ ] Keep all of it on the credit (Agent SDK / claude -p only; NOT the raw
      Anthropic API, which bills separately).

## Notes / gotchas
- Windows: call `claude.cmd` (not `claude`) from subprocess; pass page text via
  stdin, not argv (the .cmd shim mangles big multi-line args).
- Force UTF-8 for Chinese output: `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`.
- 4 school sites fail with SSLError (spcc_prep, shck, hkbuas, gskd); several are
  near-empty (JS-rendered) — handle/skip gracefully.
- Python: C:\Users\KendiNg\anaconda3\python.exe
