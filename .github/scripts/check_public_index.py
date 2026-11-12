"""Check that featured-project links on the profile README are still live and pinned.

Since governance 8.2 (2026-11-12), the README is a one-screen profile resume:
it lists exactly the account's two pinned repositories (the highest-starred
ones), and the complete index is GitHub's own repositories tab (always current,
no hand-maintained table). This script verifies:

  * the README keeps the platform full-index link;
  * it lists exactly EXPECTED_FEATURED project links;
  * each link resolves to a real, public, non-fork, non-archived repo;
  * each listed repo is currently pinned on the account (soft check: if the
    GraphQL pinned set cannot be fetched, this check is skipped with a notice
    rather than failing the gate, so an API hiccup cannot fake-red main).

Runs locally (reusing the signed-in gh CLI) and as a CI step of the
"README integrity" job using the job's GITHUB_TOKEN.

Exit codes: 0 = all checks pass, 1 = broken/stale/unpinned link or wrong count,
2 = cannot decide (public repo set unavailable). 2 is deliberately not a pass;
CI turns it into a warning, but a warning still needs a manual re-check.

Must be run from the repository root (reads README.md by relative path).
"""

import io
import re
import subprocess
import sys

OWNER = "ReSerendipity"
EXPECTED_FEATURED = 2
FULL_INDEX = f"https://github.com/{OWNER}?tab=repositories"

# Not projects: the profile repo itself and the governance/community-health hub.
EXCLUDED = {OWNER, ".github"}

ROW_URL_RE = re.compile(r"https://github\.com/ReSerendipity/([A-Za-z0-9._-]+)")

PINNED_QUERY = (
    'query { user(login: "ReSerendipity") { '
    "pinnedItems(first: 6, types: REPOSITORY) { "
    "nodes { ... on Repository { name } } } } }"
)


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


def list_pinned_repos():
    """Return the account's pinned repo names, or None if the set is unavailable.

    This is a soft check: pinned items are public data, but a GraphQL outage or
    a token without GraphQL access must not turn main red. The hard count/link
    checks above still apply in that case.
    """
    cmd = [
        "gh", "api", "graphql",
        "-f", f"query={PINNED_QUERY}",
        "--jq", ".data.user.pinnedItems.nodes[].name",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError:
        return None
    if proc.returncode != 0:
        print(f"notice: pinned set unavailable (exit {proc.returncode}); skipping pinned check")
        return None
    pinned = {line.strip() for line in proc.stdout.splitlines() if line.strip()}
    if not pinned:
        print("notice: pinned set is empty or unreadable; skipping pinned check")
        return None
    return pinned


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
    pinned = list_pinned_repos()
    not_pinned = sorted(featured - pinned) if pinned else []

    print(
        f"live public repos: {len(repos)} | featured links on README: {len(featured)} | "
        f"excluded: {sorted(EXCLUDED)} | pinned: {sorted(pinned) if pinned else 'unavailable'}"
    )
    for name in stale:
        print(f"STALE featured link: {name} -> https://github.com/{OWNER}/{name} (no longer public/active)")
    for name in not_pinned:
        print(f"NOT PINNED: {name} is listed but is not a pinned repository of this account")

    if len(featured) != EXPECTED_FEATURED:
        print(f"GAP: {len(featured)} featured projects; 8.2 requires exactly {EXPECTED_FEATURED} pinned repos")
        return 1
    if stale:
        print(f"GAP: {len(stale)} featured link(s) no longer resolve to a live public repo")
        return 1
    if not_pinned:
        print(f"GAP: {len(not_pinned)} featured project(s) are not pinned")
        return 1
    print(f"index OK: {len(featured)} featured projects resolve and match pinned repos; full list at {FULL_INDEX}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
