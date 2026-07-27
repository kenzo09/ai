---
name: import-claude-config
description: Use when the user gives a public GitHub repo URL and wants its .claude/ config (skills, agents, hooks, rules, CLAUDE.md) installed or merged into the current project
---

# Importing Claude Config From GitHub

## Overview

Fetches the `.claude/` directory tree from a public GitHub repo via the GitHub REST API (no `git clone`, no local git history pulled) and reports each file as NEW, CONFLICT, or IDENTICAL against the current project's `.claude/`. You then apply the changes, asking the user before overwriting anything.

The scripts are pure-Python stdlib (`urllib`, no `curl`/`bash`/`mktemp` dependency) so they run the same way on Linux, macOS, and Windows — anywhere `python3` (or `python` on Windows if `python3` isn't on PATH) is available.

The script never writes into the real `.claude/` directory itself — it only downloads to a temp staging dir and reports. Copying into place is a separate, deliberate step so conflicts are never silently overwritten.

## When to Use

- User pastes/names a public GitHub repo ("owner/repo" or a full URL) and asks to pull in its skills, agents, hooks, rules, or CLAUDE.md.
- User wants to sync/update an existing local `.claude/` setup from a repo they follow.

Not for: private repos requiring auth beyond a personal `GITHUB_TOKEN`, or repos that don't use the `.claude/` layout at all (see Non-standard layouts below).

## Workflow

1. **Parse the input.** Normalize to `owner/repo`. Strip `https://github.com/` if given a full URL. Ask the user only if the repo string is genuinely ambiguous.

2. **List what's available before downloading anything:**
   ```
   python3 ~/.claude/skills/import-claude-config/scripts/list_claude_tree.py <owner/repo> [ref] [subpath]
   ```
   (use `python` instead of `python3` if that's what resolves on the current machine, e.g. some Windows setups)
   - `ref` — leave empty (`""`) to auto-resolve the repo's default branch.
   - `subpath` — defaults to `.claude`, which normally covers CLAUDE.md, skills/, agents/, hooks/, and rules/ in one listing (they all nest under it in the standard layout).

   This prints each top-level entry under the subpath (e.g. `DIR .claude/skills/ (7 files)`) with its immediate children indented (e.g. individual skill names, agent files). If it reports "No files found", see Non-standard layouts below.

3. **Ask the user what to import** — everything, or specific entries from the listing (e.g. "só as skills `foo` e `bar`, e o CLAUDE.md" vs "tudo"). Don't assume "import everything" by default; the listing exists so the user can pick.

4. **Run the fetch script with the selected paths:**
   ```
   python3 ~/.claude/skills/import-claude-config/scripts/fetch_claude_config.py <owner/repo> [ref] [root_subpath] [target_dir] [selected...]
   ```
   - `root_subpath` — same value used for `subpath` in step 2 (default `.claude`).
   - `target_dir` — defaults to `./.claude` (the current project). Run from the project root.
   - `selected...` — one or more paths from the listing the user chose (e.g. `.claude/skills/foo .claude/CLAUDE.md`). Omit entirely to import everything under `root_subpath`.

   Set `GITHUB_TOKEN` in the environment first if you hit GitHub's unauthenticated rate limit (60 req/hr).

5. **Read the report.** Output ends with lines like:
   ```
   NEW       skills/foo/SKILL.md
   CONFLICT  agents/bar.md
   IDENTICAL rules/baz.md
   STAGING_DIR=/tmp/tmp.XXXXXX
   ```

6. **Apply NEW and IDENTICAL entries** by copying straight from `STAGING_DIR/.claude/<path>` to `target_dir/<path>` (IDENTICAL needs no copy, it's already the same). Use your file tools (read the staged file, write it to the target path) rather than a shell-specific copy command — this keeps the step working the same on any OS. No need to ask — there's nothing to lose.

7. **For every CONFLICT, ask the user before touching it** — show the path and offer: overwrite with the remote version, keep the local version, or view a diff first (read both `STAGING_DIR/.claude/<path>` and `target_dir/<path>` and compare). Never batch-overwrite conflicts without a per-file (or explicit "overwrite all") confirmation.

8. **Clean up:** delete `STAGING_DIR` once everything is applied (it's an OS temp directory either way — safe to leave if deletion is inconvenient on the current platform).

## Non-standard layouts

If step 2 reports "No files found under .claude/" the source repo may not use the standard layout (e.g., top-level `skills/`, `hooks/` instead of nested under `.claude/`). Don't guess — ask the user which subpath(s) to fetch, then re-run the script once per subpath with a matching `target_dir` (e.g. `subpath=skills`, `target_dir=.claude/skills`).

## Common Mistakes

| Mistake | Why it's wrong |
|---|---|
| Using `git clone` instead of the script | Pulls full history and everything else in the repo; the script fetches only the relevant subtree via the GitHub API + raw file URLs. |
| Running fetch directly without listing first | Skips the user's chance to pick a subset; always run `list_claude_tree.py` and ask before `fetch_claude_config.py`. |
| Overwriting CONFLICT files automatically | Destroys local edits with no way back locally. Always ask first. |
| Assuming a `.claude/` folder exists | Some repos use their own layout (see Non-standard layouts) — check the script's output before assuming. |
| Forgetting to clean up `STAGING_DIR` | Leaves temp dirs behind; delete it after applying changes (it lives under the OS temp dir, so leaving it isn't harmful, just untidy). |
