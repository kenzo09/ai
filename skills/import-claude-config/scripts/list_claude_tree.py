#!/usr/bin/env python3
"""Lists what exists under a subpath (default .claude) of a public GitHub repo,
one level deep (with a second level for directories), so the caller can ask
the user which parts to import before downloading anything.

Usage: list_claude_tree.py <owner/repo> [ref] [subpath]
  ref     default: repo's default branch
  subpath default: .claude; pass "." to list the REPO ROOT instead - do that whenever
          .claude/ turns up empty, to see a non-standard layout. Use "." and not "/":
          Git Bash on Windows rewrites a bare "/" into the Git install path.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict


def api_get(url):
    req = urllib.request.Request(url)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"GitHub API error {e.code} for {url}: {e.read().decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error for {url}: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: list_claude_tree.py <owner/repo> [ref] [subpath]", file=sys.stderr)
        sys.exit(1)

    repo = args[0]
    ref = args[1] if len(args) > 1 and args[1] else ""
    raw_subpath = args[2] if len(args) > 2 else ""
    subpath = (raw_subpath if raw_subpath else ".claude").rstrip("/")
    at_root = subpath in ("", ".")  # "/" or "." asked for the repo root

    if not ref:
        info = api_get(f"https://api.github.com/repos/{repo}")
        ref = info.get("default_branch", "")
        if not ref:
            print(f"Could not resolve default branch for {repo} (repo missing/private/rate-limited?)", file=sys.stderr)
            sys.exit(1)

    tree = api_get(f"https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1")

    print(f"REF={ref}")

    prefix = "" if at_root else subpath + "/"
    top_files = defaultdict(int)
    second_level = defaultdict(lambda: defaultdict(int))
    found = False

    for entry in tree.get("tree", []):
        if entry.get("type") != "blob":
            continue
        path = entry.get("path", "")
        if not path.startswith(prefix):
            continue
        found = True
        rel = path[len(prefix):]
        parts = rel.split("/")
        top = parts[0]
        top_files[top] += 1
        if len(parts) > 1:
            second_level[top][parts[1]] += 1

    if not found:
        print(f"No files found under {subpath}/ in this repo/ref.")
        print('Re-run with subpath "." to list the repo root and spot a non-standard layout.')
        return

    for top in sorted(top_files):
        if top not in second_level:
            print(f"FILE  {prefix}{top}")
        else:
            print(f"DIR   {prefix}{top}/  ({top_files[top]} files)")
            for second in sorted(second_level[top]):
                print(f"        - {prefix}{top}/{second}  ({second_level[top][second]} files)")


if __name__ == "__main__":
    main()
