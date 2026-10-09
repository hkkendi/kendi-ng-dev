"""Check that backdoor/pages.json lists every page of this site, and nothing that is gone.

Run from the repo root:  python tools/check_site_index.py
Exit 0 = in sync. Exit 1 = prints what to add or remove. Used by .github/workflows/site-index-check.yml.

A "page" is every .html file in the repo, except files under assets/ and hidden folders.
Subdomains (the "hosts" list) live on Cloudflare, not in this repo, so they are checked for shape only.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "backdoor" / "pages.json"
SKIP_DIRS = {"assets", "tools", "node_modules"}


def site_pages():
    found = set()
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(".") or part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        found.add(rel.as_posix())
    return found


def path_for(file):
    if file == "index.html":
        return "/"
    if file.endswith("/index.html"):
        return "/" + file[: -len("index.html")]
    return "/" + file


def main():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    errors = []

    listed = {}
    for i, page in enumerate(data.get("pages", [])):
        for key in ("path", "file", "description", "linked"):
            if not page.get(key):
                errors.append(f"pages[{i}] is missing '{key}'")
        f = page.get("file", "")
        if f in listed:
            errors.append(f"{f} is listed twice")
        listed[f] = page
        if f and page.get("path") and page["path"] != path_for(f):
            errors.append(f"{f}: path should be {path_for(f)}, not {page['path']}")

    on_disk = site_pages()
    for f in sorted(on_disk - set(listed)):
        errors.append(f"NOT LISTED: {f} exists but is missing from backdoor/pages.json (add it, path {path_for(f)})")
    for f in sorted(set(listed) - on_disk):
        errors.append(f"GONE: {f} is listed in backdoor/pages.json but no longer exists (remove it)")

    hosts = data.get("hosts", [])
    if not any(h.get("host") == "kendi-ng.com" for h in hosts):
        errors.append("hosts must include kendi-ng.com")
    for i, h in enumerate(hosts):
        for key in ("host", "description", "access"):
            if not h.get(key):
                errors.append(f"hosts[{i}] is missing '{key}'")
        if h.get("host") and not (h["host"] == "kendi-ng.com" or h["host"].endswith(".kendi-ng.com")):
            errors.append(f"hosts[{i}]: {h['host']} is not under kendi-ng.com")

    if errors:
        print("Site index out of date:")
        for e in errors:
            print("  - " + e)
        return 1
    print(f"Site index OK: {len(listed)} pages, {len(hosts)} hosts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
