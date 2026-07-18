"""
POC (B): reliable structured extraction via the Claude Agent SDK.

The bare `claude -p` CLI gave great *content* but always wrapped it in prose,
no matter how we prompted. The Agent SDK fixes that the right way: we define a
tool (`record_findings`) whose arguments are SCHEMA-VALIDATED, then force the
model to call it. Whatever the model "says" is irrelevant — we read the clean,
typed arguments it passed to the tool. That's guaranteed JSON we can write
straight into schools.json.

Same engine as `claude -p`, so it runs on the $100 Agent SDK credit.

Usage:  python extract_sdk_poc.py [school_id]
"""
import asyncio
import json
import re
import sys

import requests
from bs4 import BeautifulSoup
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ToolUseBlock,
    create_sdk_mcp_server,
    query,
    tool,
)

SCHOOLS_JSON = (
    "https://raw.githubusercontent.com/hkkendi/kendi-ng-dev/master/"
    "zoe-school/data/schools.json"
)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ZoeSchoolCheckerPOC/1.0"

# The schema the model MUST conform to. These keys map onto schools.json:
#   open day  -> openDay
#   application period -> appDateConfirmed / appDateNote
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
                              "description": "e.g. Open Day, Application, Interview, Briefing"},
                    "date": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "quote": {"type": "string",
                              "description": "exact sentence the date came from"},
                },
                "required": ["event", "date", "confidence", "quote"],
            },
        },
    },
    "required": ["found", "items"],
}

# Closure to capture what the model passes to the tool.
_captured: dict = {}


@tool("record_findings", "Record the extracted K1 admission dates.", FINDINGS_SCHEMA)
async def record_findings(args):
    _captured.clear()
    _captured.update(args)
    return {"content": [{"type": "text", "text": "recorded"}]}


SYSTEM = (
    "You are a data-extraction backend for a Hong Kong kindergarten admission "
    "tracker. You read page text and call the record_findings tool exactly once "
    "with K1 (nursery) 2026/2027 admission dates: open days, application periods, "
    "briefings, interviews, result dates. Ignore unrelated dates (copyright, past "
    "events, other grades). You MUST call record_findings — do not answer in prose."
)


async def extract(text: str) -> dict:
    server = create_sdk_mcp_server("zoe", tools=[record_findings])
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM,
        mcp_servers={"zoe": server},
        allowed_tools=["mcp__zoe__record_findings"],
        permission_mode="bypassPermissions",
        max_turns=3,
    )
    prompt = "Extract K1 admission dates from this page text:\n\n" + text[:6000]

    tool_was_called = False
    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, ToolUseBlock) and block.name.endswith("record_findings"):
                    tool_was_called = True
    return {"_tool_called": tool_was_called, **_captured}


def main() -> int:
    school_id = sys.argv[1] if len(sys.argv) > 1 else "truelight_kln"
    schools = requests.get(SCHOOLS_JSON, timeout=30).json()["schools"]
    school = next((s for s in schools if s["id"] == school_id), None)
    if not school:
        print("Unknown id. Try:", ", ".join(s["id"] for s in schools[:8]))
        return 1

    print(f"School : {school['nameEn']} ({school['nameZh']})")
    print(f"URL    : {school['website']}\n")
    r = requests.get(school["website"], headers={"User-Agent": UA}, timeout=20)
    r.encoding = r.apparent_encoding or r.encoding
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ")).strip()
    print(f"Page text length: {len(text)} chars\n")

    print("=" * 60)
    print("Agent SDK — clean, schema-validated JSON (tool arguments):")
    print("=" * 60)
    result = asyncio.run(extract(text))
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Prove it's real JSON we can use programmatically:
    if result.get("items"):
        print("\n--- proof it's usable: first item's date field ---")
        print("openDay/appDate candidate ->", result["items"][0]["date"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
