"""Check that README's "全部公开项目" index covers every public repository.

check_readme.py verifies row *format* only; it cannot know whether a public
repository is missing from the list, because that needs the live repo set.
This script supplies that missing invariant. It runs both locally (before
committing README edits, reusing the signed-in gh CLI) and as a CI step of the
same "README integrity" job using the job's GITHUB_TOKEN.

Exit codes: 0 = index matches the public repo set, 1 = gap found,
2 = cannot decide (gh unavailable / unauthenticated / network failure).
2 is deliberately not a pass; CI turns it into a warning rather than a red, so
an API hiccup cannot fake-fail main -- but that warning still needs a manual
re-check of the list.

Must be run from the repository root (reads README.md by relative path).
"""

import io
import json
import re
import subprocess
import sys

OWNER = "ReSerendipity"

# Declared exclusions: not members of "全部公开项目". Rationale is documented in
# AGENTS.md so the decision is not re-litigated on every run.
EXCLUDED = {
    OWNER,  # this profile repo is the page itself
    ".github",  # governance/community-health files, linked at README "治理与社区健康文件"
}

# Same row shape check_readme.py accepts: | [name](url) | summary |
ROW_URL_RE = re.compile(r"https://github\.com/ReSerendipity/([A-Za-z0-9._-]+)")


def read_readme() -> str:
    try:
        return io.open("README.md", encoding="utf-8").read()
    except OSError as exc:
        print(f"cannot read README.md from the current directory: {exc}")
        print("run this script from the repository root")
        return None


def list_public_repos():
    """Enumerate public repos via the users endpoint (returns public repos only)."""
    cmd = [
        "gh", "api",
        f"users/{OWNER}/repos?per_page=100",
        "--paginate",
        "--jq", ".[] | [.name, .private, .fork, .archived] | @tsv",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError:
        print("gh CLI not found; the public repo set cannot be enumerated")
        return None
    if proc.returncode != 0:
        print(f"gh api failed (exit {proc.returncode}): {proc.stderr.strip()[:400]}")
        return None
    repos = set()
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 4:
            continue
        name, private, fork, archived = parts
        if private == "false" and fork == "false" and archived == "false":
            repos.add(name)
    if not repos:
        print("gh returned no public repositories; refusing to treat that as a clean result")
        return None
    return repos


def main() -> int:
    readme = read_readme()
    if readme is None:
        return 2
    repos = list_public_repos()
    if repos is None:
        return 2

    listed = set(ROW_URL_RE.findall(readme))
    missing = sorted(repos - listed - EXCLUDED)
    stale = sorted(listed - repos - EXCLUDED)

    print(f"public repos (non-fork, non-archived): {len(repos)} | README-covered: {len(listed)} | excluded: {sorted(EXCLUDED)}")
    for name in missing:
        print(f"MISSING from 全部公开项目: {name} -> https://github.com/{OWNER}/{name}")
    for name in stale:
        print(f"LISTED but no longer public/active: {name}")

    if missing or stale:
        print(f"GAP: {len(missing)} missing, {len(stale)} stale")
        return 1
    print(f"index OK: all {len(repos - EXCLUDED)} public projects are listed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
