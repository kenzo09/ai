#!/usr/bin/env python3
"""Downloads selected paths from a public GitHub repo into a staging
directory, then reports each file as NEW, IDENTICAL, EOL-ONLY (same content,
different line endings) or CONFLICT (exists locally with different content)
versus a target directory inside the CURRENT project. Never writes into the
target itself - the caller (agent) decides what to do with conflicts.

Run list_claude_tree.py first to see what's available and let the user
pick which of SELECTED... to import (or the root itself for everything).

Usage: fetch_claude_config.py <owner/repo> [ref] [root_subpath] [target_dir] [selected...]
  ref          default: repo's default branch
  root_subpath default: .claude - the local target_dir corresponds to this repo path
  target_dir   default: .claude - ALWAYS relative to the current working directory;
               a path resolving outside the cwd is refused (exit 2). Run from the
               project root.
  selected...  one or more repo paths to import, each equal to root_subpath or nested
               under it (e.g. ".claude/skills", ".claude/agents/reviewer.md",
               ".claude/CLAUDE.md"). Defaults to [root_subpath] - i.e. import everything.
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


def _request(url):
    req = urllib.request.Request(url)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    return req


def api_get(url):
    try:
        with urllib.request.urlopen(_request(url), timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"GitHub API error {e.code} for {url}: {e.read().decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error for {url}: {e.reason}", file=sys.stderr)
        sys.exit(1)


def download(url, dest: Path):
    with urllib.request.urlopen(_request(url), timeout=30) as resp:
        dest.write_bytes(resp.read())


def same_but_eol(a: Path, b: Path):
    """True when two files differ only in line endings - a constant false-positive
    source on Windows, where a CRLF checkout diffs against LF raw GitHub content."""
    norm = lambda p: p.read_bytes().replace(b"\r\n", b"\n")
    return norm(a) == norm(b)


def under(path, sel):
    sel = sel.rstrip("/")
    return path == sel or path.startswith(sel + "/")


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: fetch_claude_config.py <owner/repo> [ref] [root_subpath] [target_dir] [selected...]", file=sys.stderr)
        sys.exit(1)

    repo = args[0]
    ref = args[1] if len(args) > 1 and args[1] else ""
    root = (args[2] if len(args) > 2 and args[2] else ".claude").rstrip("/")
    target_dir = args[3] if len(args) > 3 and args[3] else ".claude"
    selected = args[4:] if len(args) > 4 else []
    if not selected:
        selected = [root]

    # target_dir is always resolved inside the current project. This skill imports
    # into the project you are standing in, never into a global config dir.
    project = Path.cwd().resolve()
    target_path = (project / target_dir).resolve()
    if target_path != project and project not in target_path.parents:
        print(
            "REFUSED: target_dir must stay inside the current project.\n"
            f"  project (cwd): {project}\n"
            f"  target_dir:    {target_path}\n"
            "Run this script from the project root and pass a RELATIVE target_dir such as\n"
            "'.claude' or '.claude/skills'. Importing into a global config dir (~/.claude)\n"
            "is not what this skill does - ask the user first if that is really wanted.",
            file=sys.stderr,
        )
        sys.exit(2)

    if not ref:
        info = api_get(f"https://api.github.com/repos/{repo}")
        ref = info.get("default_branch", "")
        if not ref:
            print(f"Could not resolve default branch for {repo} (repo missing/private/rate-limited?)", file=sys.stderr)
            sys.exit(1)

    staging = Path(tempfile.mkdtemp())
    tree = api_get(f"https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1")

    if tree.get("truncated"):
        print("WARNING: repo tree was truncated by the GitHub API (very large repo) - some files may be missing", file=sys.stderr)

    blobs = [
        entry
        for entry in tree.get("tree", [])
        if entry.get("type") == "blob"
        and under(entry.get("path", ""), root)
        and any(under(entry["path"], sel) for sel in selected)
    ]
    paths = [entry["path"] for entry in blobs]

    if not paths:
        print(f"No files found under the selected path(s) in {repo}@{ref}: {' '.join(selected)}", file=sys.stderr)
        shutil.rmtree(staging, ignore_errors=True)
        sys.exit(1)

    for entry in blobs:
        p = entry["path"]
        dest = staging / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        raw_url = f"https://raw.githubusercontent.com/{repo}/{ref}/{p}"
        download(raw_url, dest)
        # GitHub marks executables as mode 100755. write_bytes() creates 0644, which
        # silently breaks an imported hook script on Linux/macOS. No-op on Windows,
        # which has no exec bit - copy the file with shutil.copy (not copyfile) to keep it.
        if entry.get("mode") == "100755" and os.name != "nt":
            dest.chmod(dest.stat().st_mode | 0o111)

    print(f"Downloaded {len(paths)} file(s) from {repo}@{ref} (selected: {' '.join(selected)}) into {staging}")
    print()
    print(f"=== STATUS vs {target_path} ===")
    root_prefix = root + "/"
    for p in paths:
        rel = p[len(root_prefix):] if p.startswith(root_prefix) else p
        local_file = target_path / rel
        staged_file = staging / p
        if not local_file.exists():
            print(f"NEW      {rel}")
        elif filecmp.cmp(local_file, staged_file, shallow=False):
            print(f"IDENTICAL {rel}")
        elif same_but_eol(local_file, staged_file):
            print(f"EOL-ONLY {rel}")
        else:
            print(f"CONFLICT {rel}")

    print()
    print(f"STAGING_DIR={staging}")
    print(f"(staged files are under $STAGING_DIR/{root}/...)")


if __name__ == "__main__":
    main()
