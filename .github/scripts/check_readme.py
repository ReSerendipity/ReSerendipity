import re
from pathlib import Path
from urllib.parse import urlparse


OWNER = "ReSerendipity"
readme = Path("README.md").read_text(encoding="utf-8")
required = (
    '<b style="font-size:17px;">TTS-MultiModel</b>',
    'href="https://github.com/ReSerendipity/TTS-MultiModel"',
    '<b style="font-size:17px;">SeedVR2-Lite</b>',
    'href="https://github.com/ReSerendipity/SeedVR2-Lite"',
    'href="https://reserendipity.github.io/SeedVR2-Lite/docs/"',
)
for text in required:
    if text not in readme:
        raise SystemExit(f"README.md is missing expected featured-project content: {text}")

if readme.count(" · Apache-2.0</p>") != 2:
    raise SystemExit("README.md must state Apache-2.0 separately for both featured repositories")

for stale in (
    "github.com/ReSerendipity/TTS_MultiModel",
    "github.com/ReSerendipity/SeedVR2-lite",
    "open%20source-Apache--2.0",
):
    if stale in readme:
        raise SystemExit(f"README.md contains stale or misleading content: {stale}")


# Structural invariants for the "全部公开项目" tables (offline-decidable only;
# live link checks need egress, which this CI does not have — add separately
# once network access is authorized).
LINK_ROW_RE = re.compile(r"^\|\s*\[([^\]\|]+)\]\(([^)\|]+)\)\s*\|\s*([^|]*?)\s*\|\s*$")
SEPARATOR_CELL_RE = re.compile(r":?-{3,}:")


def is_separator_row(stripped_line: str) -> bool:
    cells = [cell.strip() for cell in stripped_line.strip("|").split("|")]
    return bool(cells) and all(SEPARATOR_CELL_RE.fullmatch(cell) for cell in cells)


seen_slugs: dict[str, int] = {}
row_count = 0
for lineno, line in enumerate(readme.splitlines(), start=1):
    stripped = line.strip()
    if not stripped.startswith("|"):
        continue
    if is_separator_row(stripped):
        continue
    match = LINK_ROW_RE.match(stripped)
    if match is None:
        if stripped.startswith("| ["):
            raise SystemExit(
                f"README.md line {lineno}: malformed project-table row, "
                f'expected "| [名称](URL) | 简介 |": {stripped}'
            )
        continue  # header and other non-project rows
    name, url, summary = match.groups()
    parsed = urlparse(url if "://" in url else f"https://{url}")
    if parsed.netloc.lower() != "github.com":
        raise SystemExit(f"README.md line {lineno}: project URL host must be github.com: {url}")
    segments = [seg for seg in parsed.path.split("/") if seg]
    if not segments or segments[0] != OWNER:
        raise SystemExit(f"README.md line {lineno}: project URL must live under github.com/{OWNER}/: {url}")
    slug = segments[-1]
    if slug != name:
        raise SystemExit(f"README.md line {lineno}: row name {name!r} must match URL slug {slug!r}")
    if not summary:
        raise SystemExit(f"README.md line {lineno}: project {name} has an empty summary")
    if slug in seen_slugs:
        raise SystemExit(
            f"README.md line {lineno}: duplicate project row for {slug} "
            f"(first seen at line {seen_slugs[slug]})"
        )
    seen_slugs[slug] = lineno
    row_count += 1

if row_count == 0:
    raise SystemExit("README.md contains no project rows under 全部公开项目")

print(f"README featured-project content OK; {row_count} public-project rows well-formed and unique")
