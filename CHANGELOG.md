# Changelog

本仓库的显著变更记录于此文件，格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)；
一旦出现可发布产物，版本号将遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。
本口径依据 `ReSerendipity/.github` 的 `REPOSITORY_GUIDELINES.md` §10.2。

## [Unreleased]

- 本仓为与账号同名的 GitHub Profile 主页仓，**尚未建立版本化发布**：无 tag、无 Release，亦无可分发产物（详见 `docs/release-governance.md`）。本文件于 2026-10-18 建立。
- 此后按 §10.2 口径执行：每次合并 `main` 在 `[Unreleased]` 追加（`feat→Added`、`fix→Fixed`、`refactor→Changed`）；发版时 `[Unreleased]` → `[VERSION] - YYYY-MM-DD`。

### Changed

- 2026-11-12：根 `README.md` 由「仓库说明书」改为治理 §8.2 的**简历式精简模板**（260 行 / 24 KB → 42 行 / 3.1 KB）：去掉展示图、HTML 精选卡片、完整双语镜像、快速开始 / 系统要求 / 使用示例 / FAQ 等软件项目章节，以及手工维护的全部公开项目表；完整索引改由 GitHub `?tab=repositories` 承载。`check_readme.py` / `check_public_index.py` 同步换成精简契约，CI 步骤名同步。
