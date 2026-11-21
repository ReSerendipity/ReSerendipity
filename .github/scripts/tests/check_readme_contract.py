"""check_readme.py 的契约反例测试：正例必须绿，负例必须红。

用法：python .github/scripts/tests/check_readme_contract.py
退出码：0=全部符合预期；1=有用例不符合；2=环境不可用。
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECK = ROOT / ".github" / "scripts" / "check_readme.py"

BASE = """# ReSerendipity

独立开发者 · 本地优先的 AI 媒体工具与端侧应用作者。

## 专注领域

| 方向 | 主要工作 |
|---|---|
| 语音 / 音频 | 多引擎 TTS 统一调度 |

**常用技术栈**：Python / FastAPI · Kotlin

## 代表项目

| 项目 | 说明 |
|---|---|
| [SeedVR2-Lite](https://github.com/ReSerendipity/SeedVR2-Lite) | 视频 / 图像超分 |
| [TTS-MultiModel](https://github.com/ReSerendipity/TTS-MultiModel) | 六引擎本地 TTS 工作台 |

其余项目见 [Repositories](https://github.com/ReSerendipity?tab=repositories)。

## 协作方式

- 治理：[.github/governance](https://github.com/ReSerendipity/.github/tree/main/governance)

*English: Independent developer building local-first AI media tooling.*
"""

PASS = 0
FAIL = 0


def run_case(name: str, content: str, expected: int) -> None:
    global PASS, FAIL
    with tempfile.TemporaryDirectory(prefix="readme-contract-") as tmp:
        Path(tmp, "README.md").write_text(content, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(CHECK)],
            cwd=tmp,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    actual = proc.returncode
    if actual == expected:
        print(f"PASS  {name:<32} rc={actual}")
        PASS += 1
    else:
        print(f"FAIL  {name:<32} 期望 rc={expected}，实际 rc={actual}")
        for line in (proc.stdout + proc.stderr).splitlines()[:3]:
            print(f"      {line}")
        FAIL += 1


def main() -> int:
    if not CHECK.is_file():
        print(f"ERROR: 找不到 {CHECK}", file=sys.stderr)
        return 2

    run_case("T1 合规简历式模板", BASE, 0)
    run_case("T2 超过 80 行", BASE + "\n" * 60, 1)
    run_case("T3 超过 8000 字节", BASE + "x" * 9000, 1)
    run_case("T4 缺协作方式", BASE.replace("## 协作方式", "## 其它"), 1)
    run_case("T5 禁止展示图", BASE.replace("## 专注领域", "![badge](x)\n\n## 专注领域"), 1)
    run_case(
        "T6 过期仓库名",
        BASE.replace("TTS-MultiModel", "TTS_MultiModel"),
        1,
    )
    run_case(
        "T7 项目行缺说明列",
        BASE.replace(
            "| [SeedVR2-Lite](https://github.com/ReSerendipity/SeedVR2-Lite) | 视频 / 图像超分 |",
            "| [SeedVR2-Lite](https://github.com/ReSerendipity/SeedVR2-Lite) |",
        ),
        1,
    )
    run_case(
        "T8 代表项目多于 2 个",
        BASE.replace(
            "| [TTS-MultiModel](https://github.com/ReSerendipity/TTS-MultiModel) | 六引擎本地 TTS 工作台 |",
            "| [TTS-MultiModel](https://github.com/ReSerendipity/TTS-MultiModel) | 六引擎本地 TTS 工作台 |\n"
            "| [Other](https://github.com/ReSerendipity/Other) | 另一个项目 |",
        ),
        1,
    )
    run_case(
        "T9 表格外多一个项目链接",
        BASE + "\n另见 https://github.com/ReSerendipity/Other\n",
        1,
    )

    print(f"\n结果：PASS={PASS} FAIL={FAIL}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
