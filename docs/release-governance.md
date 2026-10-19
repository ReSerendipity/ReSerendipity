# 发布 / 回滚 规范（本仓本地化）

> **来源与权威**：公共条款见 `ReSerendipity/.github` 的 `REPOSITORY_GUIDELINES.md` §10（发布 / 分发统一规范）。
> 本文件由同仓 `RELEASE_GOVERNANCE_TEMPLATE.md` 复制而来，只填**本仓特有**内容，**不重写、不抵触 §10 的公共条款**。
> 占位符已逐项替换为本仓真值；未确定项标注「待定（负责人 + 触发条件）」。

---

## 0. 远端优先（根原则，不可改写）

发布链的构建、打包、扫描、上传、推送**全部在 GitHub Actions 远端完成**；本地只做三件事：改版本位、落 CHANGELOG、`git tag` + `git push`。本地不执行打包 / 镜像构建 / 发布上传。

> 本仓当前**无发布链**（见 §3 与文末「发布链现状判定」）；一旦未来建链，必须同样遵守本条**远端优先**原则。

## 1. 版本号规范

- 遵循 **SemVer** `MAJOR.MINOR.PATCH`；预发布用 `-alpha.N` / `-beta.N` / `-rc.N`（**仅在本仓未来出现可发布产物时适用**）。
- **唯一权威版本位**：**无**。本仓为账号主页 profile 仓，不维护任何版本位——仓内不存在 `pyproject.toml` / `package.json` / `Cargo.toml` / `go.mod` / `config.yaml` / `Tauri.conf.json` 等版本声明文件。
- 必须同步的其它版本位：**无**（无版本位，故无多点漂移可言）。
- 版本位漂移校验：**无**。无版本位可钉，暂无 `tests/test_version_consistency.py` 一类入口。
- 自动化方式：**无 release-please、无 tag 驱动发版**（本仓当前无发布产物，见文末判定）。

## 2. CHANGELOG 管理

- 公共口径仍为 **Keep a Changelog**（`Added / Changed / Fixed / Deprecated / Removed / Security`），`feat→Added`、`fix→Fixed`、`refactor→Changed`，发版时 `[Unreleased]` → `[VERSION] - YYYY-MM-DD`。
- **本仓现状**：根级 `CHANGELOG.md` 按 §10.2 要求已于 2026-10-18 建立（Keep a Changelog 结构，仅维护 `[Unreleased]`）；本仓仍无版本号与发版节奏，故尚无版本化条目。
- 追加触发条件：此后每次合并 `main` 在 `[Unreleased]` 追加；发版时再 `[Unreleased]` → `[VERSION] - YYYY-MM-DD`（**负责人：ReSerendipity（账号所有者）**）。

## 3. 发布流程（远端）

**本仓暂无发布产物，发布链待需要时再建。** 本节保留公共流程骨架，待建链时直接套用：

1. 确认 `[Unreleased]` 条目完整；
2. 同步版本位（见 §1 清单）；
3. 本地打 tag 并推送：`git tag v<X.Y.Z>` → `git push origin v<X.Y.Z>`；
4. 远端凭 tag 触发 `release.yml` 构建产物；
5. 远端建 **draft Release** 并挂资产 → 人工审核后 `published`；
6. 盯到终态：`gh run list` 确认成功；红了当场修或 revert 止损。

> 当前 `.github/workflows/` 下**没有** `release.yml`，也**不会**为本仓硬建该 workflow（理由见文末「发布链现状判定」）。唯一现存 workflow 是 `ci.yml`，只跑 README 静态门禁，不属于发布链。

## 4. 分发产物与完整性

| 产物 | 构建位置 | 标签 / 命名 | 完整性手段 |
|---|---|---|---|
| **无**（本仓无可分发产物） | 不适用 | 不适用 | 不适用 |

- 本仓**不产出** wheel / sdist / 容器镜像 / APK / 安装包等任何可分发物。
- **不使用 `latest` 作为发布基线**（§10.3 反模式）；未来若建镜像链，tag 只取不可变标签（semver + sha）。
- **不使用 GPG 分离签名**（2026-10-18 裁决撤掉）；未来若有桌面分发，防伪造仅由 Tauri ed25519 更新器签名承担，`SHA256SUMS.txt` 仅用于防传输损坏。
- 未来若推镜像：统一 `ghcr.io`、`packages: write`、镜像引用全小写、Trivy `CRITICAL,HIGH`（`ignore-unfixed`）默认阻断、开 `provenance: true` + `sbom: true`——以上均在出现镜像产物时落实，当前无对象。

## 5. 回滚

- **判定（触发阈值）**：本仓无线上运行服务、无发布产物，故**无 SLA 类回滚阈值**。文档 / 配置类变更若出错，直接走本节回滚。
- **执行**：`git revert <bad-commit>`（保历史、可再 forward）；不重定向 / 删除 tag、不移动任何远端 ref。
- **破坏性动作**：重定向 / 删除 tag、移动任何远端 ref **须仓库所有者单独授权**（本仓当前无 tag，故不涉及）。
- **回滚后验证**：在仓库根目录跑
  ```bash
  python3 .github/scripts/check_readme.py
  python3 .github/scripts/check_public_index.py
  ```
  两步全绿即说明 README 门禁未被破坏；`check_public_index.py` 返回 2（GitHub API 不可达）时按 `ci.yml` 口径只告警、不判红。

## 6. SLA / 错误预算

- **不适用**。本仓是静态主页仓库（纯 Markdown + 远端 YAML 门禁），无运行时服务、无在线发布物，不设可用性目标与错误预算。

## 7. 发布前检查清单

- [ ] 版本位全部同步（见 §1 清单）——**N/A（无版本位）**
- [ ] CHANGELOG `[Unreleased]` 已改版本 + 日期——**N/A（无发版）**
- [ ] 测试 / 覆盖率门禁命令通过——**N/A（本仓无测试套件；CI 门禁为 README 完整性检查）**
- [ ] lint / format 全绿——**N/A（无代码）**
- [ ] 镜像类仓：Trivy 阻断通过、豁免已登记——**N/A（无镜像）**
- [ ] 镜像类仓：`provenance: true` + `sbom: true` 已开——**N/A（无镜像）**
- [x] **本地未产出任何发布交付物**（当前成立；未来建链后也必须保持全部远端构建）

---

## 发布链现状判定（本仓关键决策）

**决定：本仓不建发布链（不新增 `release.yml`、不挂 `SHA256SUMS` 产物），文档记录为「暂无发布产物，发布链待需要时再建」。**

判断依据（均可在本仓现场复核）：

1. **无任何构建 / 打包 / 清单文件**：根目录仅 `README.md`、`.mailmap`、`.gitignore`（`AGENTS.md` 已归置 `docs/`，根目录若出现同名文件按 `.gitignore` 不入库）；不存在 `pyproject.toml`、`package.json`、`Cargo.toml`、`go.mod`、`Dockerfile`、`Tauri.conf.json`、`requirements*.txt` 等任何可分发物的构建入口。
2. **唯一 workflow 是 README 静态门禁**：`.github/workflows/ci.yml` 只跑三步——`README.md` 存在且非空、`check_readme.py`（精选卡片字符串 / 许可表述 / 链接结构）、`check_public_index.py`（公开项目索引完整性，API 不可达时只告警）；**没有任何 build / package / release / publish job**。
3. **无 tag、无 Release**：`git tag` 为空、`gh release list` 为空，本仓历史上从未打过 tag 或发过 Release。
4. **README 所列项目不在本仓分发**：首页卡片与索引表格指向的 `TTS-MultiModel`、`SeedVR2-Lite`、`Image-DuoModel` 等均为**其它独立仓库**，本仓仅做链接索引，不在此构建或打包它们。
5. **内容性质**：本仓是与账号同名的 GitHub profile 主页仓，对外产出就是一份静态 Markdown 主页，本身不存在"可分发产物"。

**触发条件（何时再建链）**：当且仅当本仓未来出现可分发产物时——典型情形为 (a) 把静态主页发布到 GitHub Pages 形成可部署站点，或 (b) 本仓开始承担某包 / 镜像 / 安装包的构建分发职责——再由账号所有者授权，按 §10 建最小发布链：`push: tags: v*` 触发的 `release.yml` + 产物 `SHA256SUMS.txt`，**不引入 `latest`、不建 / 保留任何 GPG 签名流程**。负责人：**ReSerendipity（账号所有者）**。

## 禁止事项

- 不重写 §10 的公共条款（远端优先、tag 驱动、版本位一致、不可变标签、扫描阻断、无 GPG）。
- 不引入 `latest` 作发布基线；不保留或新建 GPG 签名流程。
- 不留空占位符、不编造阈值；本仓不适用项一律写明「N/A / 无」并给依据，而非留空。
