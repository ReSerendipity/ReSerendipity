"""Check that featured-project links on the profile README are still live.

Since governance 8.2 (2026-11-12), the README is a one-screen profile resume:
it lists a short selection of representative projects, and the complete index
is GitHub's own repositories tab (always current, no hand-maintained table).
Accordingly this script no longer requires the README to enumerate every
public repository. It now verifies that every project link on the page still
resolves to a real, public, non-fork, non-archived repo of this account.

Runs locally (reusing the signed-in gh CLI) and as a CI step of the
"README integrity" job using the job's GITHUB_TOKEN.

Exit codes: 0 = all featured links resolve, 1 = broken/stale link or too few
projects, 2 = cannot decide (gh unavailable / unauthenticated / network
failure). 2 is deliberately not a pass; CI turns it into a warning, but a
warning still needs a manual re-check.

Must be run from the repository root (reads README.md by relative path).
"""

import io
import re
import subprocess
import sys

OWNER = "ReSerendipity"
MIN_FEATURED = 5
FULL_INDEX = f"https://github.com/{OWNER}?tab=repositories"

# Not projects: the profile repo itself and the governance/community-health hub.
EXCLUDED = {OWNER, ".github"}

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
    if FULL_INDEX not in readme:
        print(f"README.md must link to the platform-maintained full index: {FULL_INDEX}")
        return 1
    repos = list_public_repos()
    if repos is None:
        return 2

    featured = set(ROW_URL_RE.findall(readme)) - EXCLUDED
    stale = sorted(featured - repos)

    print(f"live public repos: {len(repos)} | featured links on README: {len(featured)} | excluded: {sorted(EXCLUDED)}")
    for name in stale:
        print(f"STALE featured link: {name} -> https://github.com/{OWNER}/{name} (no longer public/active)")

    if len(featured) < MIN_FEATURED:
        print(f"GAP: only {len(featured)} featured projects; 8.2 requires at least {MIN_FEATURED}")
        return 1
    if stale:
        print(f"GAP: {len(stale)} featured link(s) no longer resolve to a live public repo")
        return 1
    print(f"index OK: all {len(featured)} featured projects resolve; full list at {FULL_INDEX}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
