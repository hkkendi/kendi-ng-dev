"""
POC: replace the Zoe checker's regex date-hunt with a `claude -p` call.

Takes ONE school, downloads its page, cleans the text, then asks Claude
(via the Claude Code CLI in print mode) to find any real K1 2026/27
admission or open-day date. Prints a side-by-side of the old regex result
vs. Claude's structured answer.

This is throwaway. It touches nothing in C:\\Automation\\zoe-school-checker.
Usage:  python check_ai_poc.py [school_id]
"""
import json
import re
import shutil
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

SCHOOLS_JSON = (
    "https://raw.githubusercontent.com/hkkendi/kendi-ng-dev/master/"
    "zoe-school/data/schools.json"
)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ZoeSchoolCheckerPOC/1.0"

# --- the OLD way: regex (copied from check.py, trimmed) ---------------------
DATE_PATTERNS = [
    re.compile(r"\b\d{1,2}\s*[/\-\.]\s*\d{1,2}\s*[/\-\.]\s*202[6-7]\b"),
    re.compile(r"\b202[6-7]\s*[年\-/\.]\s*\d{1,2}\s*[月\-/\.]\s*\d{1,2}\b"),
]


def regex_dates(text: str) -> list[str]:
    out, seen = [], set()
    for pat in DATE_PATTERNS:
        for m in pat.finditer(text):
            d = m.group(0).strip()
            if d.lower() not in seen:
                seen.add(d.lower())
                out.append(d)
    return out


# --- the NEW way: ask Claude via `claude -p` -------------------------------
PROMPT = """Extract K1 (nursery) admission info for the 2026/2027 school year \
from the Hong Kong kindergarten page text on stdin. Include application dates, \
open-day/briefing dates, interview and result dates. Ignore unrelated dates \
(copyright years, past events, other grades).

CRITICAL OUTPUT CONTRACT — follow exactly:
- Your ENTIRE response must be ONE JSON object and nothing else.
- The FIRST character you output must be `{` and the LAST must be `}`.
- No preamble, no explanation, no markdown, no code fences, no trailing text.
- Schema: {"found": <bool>, "items": [{"event": <str>, "date": <str>, \
"confidence": "high"|"medium"|"low", "quote": <str>}]}
- If nothing relevant: {"found": false, "items": []}

Begin your response with { now."""

# A system prompt is the strongest lever for format compliance: it overrides
# the model's instinct to be chatty/helpful and forces machine output.
SYSTEM_PROMPT = (
    "You are a data-extraction endpoint, not a chat assistant. "
    "Respond with EXACTLY ONE valid JSON object and NOTHING else — "
    "no prose, no explanation, no markdown code fences. "
    "If the page has no relevant K1 2026/27 admission dates, return "
    '{"found": false, "items": []}.'
)


def _extract_json(s: str) -> dict | None:
    """Pull the first balanced {...} object out of a string and parse it.
    Survives stray prose or ``` fences around the JSON."""
    s = s.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    start = s.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(s[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def claude_extract(text: str) -> dict:
    # keep the payload sane for a POC
    snippet = text[:6000]
    # On Windows the npm shim is claude.cmd; subprocess needs the full name.
    claude_bin = shutil.which("claude.cmd") or shutil.which("claude") or "claude"
    # Pass the instruction via -p, the page text via stdin. Stuffing a big
    # multi-line string into argv gets mangled by the Windows .cmd shim.
    proc = subprocess.run(
        [claude_bin, "-p", PROMPT,
         "--system-prompt", SYSTEM_PROMPT,   # REPLACE the coding-agent persona
         "--output-format", "json"],
        input=snippet,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=180,
    )
    if proc.returncode != 0:
        return {"_error": f"claude exited {proc.returncode}: {proc.stderr[:300]}"}
    # `--output-format json` wraps the reply; the model's text is in .result
    try:
        raw = json.loads(proc.stdout).get("result", proc.stdout)
    except json.JSONDecodeError:
        raw = proc.stdout
    parsed = _extract_json(raw)
    return parsed if parsed is not None else {"_unparseable": raw}


def main() -> int:
    school_id = sys.argv[1] if len(sys.argv) > 1 else "spk"
    schools = requests.get(SCHOOLS_JSON, timeout=30).json()["schools"]
    school = next((s for s in schools if s["id"] == school_id), None)
    if not school:
        print(f"No school with id {school_id!r}. Try one of:",
              ", ".join(s["id"] for s in schools[:8]), "...")
        return 1

    url = school["website"]
    print(f"School : {school['nameEn']} ({school['nameZh']})")
    print(f"URL    : {url}\n")

    r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
    r.encoding = r.apparent_encoding or r.encoding
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ")).strip()
    print(f"Page text length: {len(text)} chars\n")

    print("=" * 60)
    print("OLD (regex) — every 2026/2027 date on the page:")
    print("=" * 60)
    rd = regex_dates(text)
    print("  " + ("\n  ".join(rd) if rd else "(none found)"))

    print("\n" + "=" * 60)
    print("NEW (claude -p) — Claude judges what's actually K1 admissions:")
    print("=" * 60)
    result = claude_extract(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
