"""简历式精简 README 的内容契约（2026-11-12 起，配合治理 §8.2）。

历史契约要求两张 HTML 精选卡片与「全部公开项目」完整表格，导致主页仓
被写成软件项目说明书。治理 §8.2 为 `delivery=content` 的 profile 仓定义
了简历式模板后，本脚本改为校验该模板的最低要求：

  1. 一屏可读（行数 / 字节数上限）；
  2. 必含四块信息与两个入口（治理引用行、平台 repositories 索引）；
  3. 不得回退为长模板（展示图、HTML 卡片、完整英文镜像、软件项目章节）；
  4. 代表项目表格仍受 7 条结构不变量约束，数量限 5–10 个；
  5. 过期仓库名 / 徽章串仍禁止出现。

完整公开项目清单不再由 README 维护，交给 GitHub 账号 repositories 页；
链接真实性由 check_public_index.py 校验。

Must be run from the repository root (reads README.md by relative path).
"""

import re
from pathlib import Path
from urllib.parse import urlparse


OWNER = "ReSerendipity"
MAX_LINES = 80
MAX_BYTES = 8000
MIN_FEATURED = 5
MAX_FEATURED = 10

raw = Path("README.md").read_bytes()
readme = raw.decode("utf-8")
lines = readme.splitlines()

if len(lines) > MAX_LINES:
    raise SystemExit(
        f"README.md is {len(lines)} lines; the profile resume template caps it at {MAX_LINES} (governance 8.2)"
    )
if len(raw) > MAX_BYTES:
    raise SystemExit(
        f"README.md is {len(raw)} bytes; the profile resume template caps it at {MAX_BYTES} (governance 8.2)"
    )

required = (
    "## 专注领域",
    "## 代表项目",
    "## 协作方式",
    "**常用技术栈**",
    "https://github.com/ReSerendipity/.github/tree/main/governance",
    "https://github.com/ReSerendipity?tab=repositories",
    "*English:",
)
for text in required:
    if text not in readme:
        raise SystemExit(f"README.md is missing required profile-resume content: {text}")

forbidden = (
    "![",  # 展示图 / 徽章墙
    "<table",  # HTML 精选卡片
    "## English\n",  # 完整英文镜像段
    "### FAQ",
    "### 快速开始",
    "### 系统要求",
    "### 使用示例",
    "### 全部公开项目",
)
for text in forbidden:
    if text in readme:
        raise SystemExit(
            f"README.md contains long-template content that 8.2 exempts: {text!r}. "
            "Keep the profile page to one screen."
        )

for stale in (
    "github.com/ReSerendipity/TTS_MultiModel",
    "github.com/ReSerendipity/SeedVR2-lite",
    "open%20source-Apache--2.0",
):
    if stale in readme:
        raise SystemExit(f"README.md contains stale or misleading content: {stale}")


# 「代表项目」表格的 7 条结构不变量（与旧契约一致，只是不再要求覆盖全部公开仓）
LINK_ROW_RE = re.compile(r"^\|\s*\[([^\]\|]+)\]\(([^)\|]+)\)\s*\|\s*([^|]*?)\s*\|\s*$")
SEPARATOR_CELL_RE = re.compile(r":?-{3,}:")
REPO_LINK_RE = re.compile(r"https://github\.com/ReSerendipity/([A-Za-z0-9._-]+)")


def is_separator_row(stripped_line: str) -> bool:
    cells = [cell.strip() for cell in stripped_line.strip("|").split("|")]
    return bool(cells) and all(SEPARATOR_CELL_RE.fullmatch(cell) for cell in cells)


seen_slugs: dict[str, int] = {}
row_count = 0
for lineno, line in enumerate(lines, start=1):
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
                f'expected "| [名称](URL) | 说明 |": {stripped}'
            )
        continue  # header and non-project table rows
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

if not MIN_FEATURED <= row_count <= MAX_FEATURED:
    raise SystemExit(
        f"README.md has {row_count} featured projects; 8.2 requires {MIN_FEATURED}-{MAX_FEATURED}"
    )

# 表格以外的项目链接也要计入总数，避免把清单藏在散文里绕开数量上限
linked_slugs = set(REPO_LINK_RE.findall(readme)) - {OWNER, ".github"}
if len(linked_slugs) > MAX_FEATURED:
    raise SystemExit(
        f"README.md links to {len(linked_slugs)} project repos; 8.2 caps the profile page at {MAX_FEATURED}"
    )

print(
    f"README profile-resume contract OK; {row_count} featured projects, "
    f"{len(lines)} lines, {len(raw)} bytes"
)
