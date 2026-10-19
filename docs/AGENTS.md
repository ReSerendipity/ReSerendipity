# AGENTS.md — ReSerendipity

## 仓库定位

这是 GitHub **个人账号**主页仓库（profile repo，账号 `ReSerendipity` 是 user 而非 org，
枚举公开仓库要走 `users/ReSerendipity/repos`，`orgs/...` 会 404），内容以 `README.md` 的主页卡片为主。
本仓库唯一的**远端**自动门禁是 `.github/workflows/ci.yml`，它在 **push 到 `main`** 和**所有 PR** 上运行三步检查：

1. `README.md` 存在且非空（`test -f` / `test -s`）；
2. `python3 .github/scripts/check_readme.py` —— 校验精选卡片字符串、许可证表述、过期串，以及「全部公开项目」表格的**结构**不变量；
3. `python3 .github/scripts/check_public_index.py` —— 校验清单**完整性**（缺项/失效条目判红；API 无从判定时只告警）。

除 ci.yml 外没有其他 CI/CD 门禁。清单完整性检查 `check_public_index.py`（见下）已作为同一个
job 的步骤在远端运行，但它对 GitHub API 的依赖意味着**结论可能是"无法判定"**——这种情形只告警
不判红。修改 README 或脚本前，先在本地复现这两项校验。

## check_readme.py 强制的内容契约

脚本（`.github/scripts/check_readme.py`）要求 `README.md` **必须逐字包含**以下字符串：

| # | 必须存在的字符串 | 含义 |
|---|---|---|
| 1 | `<b style="font-size:17px;">TTS-MultiModel</b>` | 精选卡片 1 标题 |
| 2 | `href="https://github.com/ReSerendipity/TTS-MultiModel"` | 卡片 1 仓库链接 |
| 3 | `<b style="font-size:17px;">SeedVR2-Lite</b>` | 精选卡片 2 标题 |
| 4 | `href="https://github.com/ReSerendipity/SeedVR2-Lite"` | 卡片 2 仓库链接 |
| 5 | `href="https://reserendipity.github.io/SeedVR2-Lite/docs/"` | 卡片 2 文档链接 |

外加两条约束：

- **许可证表述**：` · Apache-2.0</p>` 必须**恰好出现 2 次**（两张精选卡片各一处）；多或少都会失败。
- **禁止出现的过期字符串**（出现即失败）：
  - `github.com/ReSerendipity/TTS_MultiModel`（旧名，下划线）
  - `github.com/ReSerendipity/SeedVR2-lite`（旧名，小写 lite）
  - `open%20source-Apache--2.0`（旧 badge URL）

### 「全部公开项目」表格的结构不变量

脚本会遍历所有以 `|` 开头的行（跳过表头与分隔行），对形如 `| [名称](URL) | 简介 |`
的项目行强制以下 7 条，任一违规即退出非零并报出**具体 README 行号**：

1. 行格式必须是 `| [名称](URL) | 简介 |`；以 `| [` 开头却不合此格式 → 直接判失败；
2. 链接 host 必须为 `github.com`；
3. 链接路径必须位于 `github.com/ReSerendipity/` 之下；
4. 显示名必须与 URL 末段 slug **完全相等**；
5. 简介单元格非空；
6. slug 不得重复；
7. 至少存在一行项目。

注意：这些是**格式**约束，脚本无法知道某个公开仓库是否被漏列——那由
`check_public_index.py` 负责。

## 本地校验命令

必须在**仓库根目录**运行（两个脚本都用相对路径 `README.md` 读取，其他目录下运行会找不到文件）：

```bash
python3 .github/scripts/check_readme.py
python3 .github/scripts/check_public_index.py
```

Windows 上若无 `python3` 命令，把 `python3` 换成 `python` 等效。

- `check_readme.py`：通过时打印 `README featured-project content OK; <N> public-project rows well-formed and unique`（`<N>` 是当前项目行数，会随清单变化）；失败时以缺失/违规的具体字符串或行号报错并退出非零（CI 红色）。
- `check_public_index.py`：需要 GitHub API。本地复用本机已登录的 `gh`（仓库内不存任何凭据）；CI 里用作业自带的 `GITHUB_TOKEN`。退出码 `0` = 清单与公开仓库集合一致，`1` = 发现缺项或已失效条目，`2` = 无法判定（`gh` 缺失、未登录或网络失败）。**`2` 不是通过**：本地要当阻塞处理，CI 里则只发 `::warning::` 不判红（避免 API 抖动把主干变成假失败），但看到该 warning 必须手工复查一次清单。
- 该检查声明的排除项为 `ReSerendipity`（本主页仓库自身）与 `.github`（治理与社区健康文件，README 末尾已单独给出入口）；除此之外新增公开仓库必须入表。

## 编辑守则

- 改动 `README.md` 中精选卡片区域时，保持上表字符串逐字不变；只改卡片描述文案等不受契约约束的部分。
- **「全部公开项目」表格区同样受契约约束**：受 `check_readme.py` 的 7 条结构不变量限制，并受 `check_public_index.py` 的完整性约束。新增公开仓库必须补一行；显示名要等于 slug、简介不能空、链接必须在 `github.com/ReSerendipity/` 下。简介取自该仓库自身的 GitHub `description`，不要代拟文案。
- **不要为了让 CI 通过而放宽或修改 `check_readme.py` / `check_public_index.py` / `ci.yml` 的断言**；门禁是契约的一部分。
- 新增/删除精选卡片属于契约变更，需同步修改 `check_readme.py` 并相应核对 Apache-2.0 出现次数。
- 改动 `README.md` 或任一脚本后，两条本地校验都要跑；提交信息里应能对应到跑过的检查结论。

## 合入流程（main 受 ruleset 保护）

`main` 上启用了仓库 ruleset「main: CI 必需检查 + 禁止直推/强推/删除」（enforcement=active，
仅作用于 `refs/heads/main`）：禁止直推、禁止删除分支、禁止非快进（强推），改动必须经 PR 合入，
且 PR 必须先通过必需检查 **`README integrity`**。所需批准人数为 **0**，因此单人为仓库可由作者
自行合并自己的 PR；`strict_required_status_checks_policy=false`，即不强制分支先同步到最新 main。

对 agent 的实际含义：**`git push origin main` 会被远端拒绝**，这不是本地配置问题，也不要试图
绕过（不 force-push、不改保护、不 `--no-verify`）。正确路径是推功能分支再开 PR：

```bash
git switch -c <branch>
git push origin <branch>        # 之后在 GitHub 上开 PR，等 README integrity 变绿后合并
```

若本地 main 因故领先于 origin/main 而推不上去，用 `git reset --soft origin/main` 收回提交对象
（改动仍留在工作树），再按上面路径重做——不要为此改写已推送历史。

### 合并方式与提交身份（红线 #4 操作细则，2026-10-18 增补，同日完成根治）

红线 #4 要求所有提交「身份固定为 `ReSerendipity <259081123+ReSerendipity@users.noreply.github.com>`（noreply），禁止个人邮箱身份」。历史上经 GitHub API/UI 执行的合并**不满足**这条：

- `gh pr merge --squash`：服务端生成的 squash 提交，author 邮箱 = PR 作者的**账号公开邮箱**（实测 PR #2 → `eef084f`，author 为 `ReSerendipity@outlook.com`）；
- `gh pr merge --merge`：合并提交同理（TTS 仓实测 `9870016`）；
- `pulls/{n}/update-branch`：平台生成的合并提交既无签名也无 noreply（SpiritPal 仓实测）。

**根治状态：已于 2026-10-18 完成。** 账号已开启 "Keep my email addresses private"，两个 outlook 地址在 Settings → Emails 均已被标记为 Private，web 端 Git 操作统一挂到上述 noreply 地址。实证：`.github` PR #8 的服务端 squash 提交 `4edce6f`，API 回读 `commit.author.email` == noreply（同一操作在变更前产出的是 outlook 邮箱）。

**规则**：

1. **三种服务端合并已解除禁令、恢复可用**（生成的提交 author 已天然 noreply）。单条 noreply 提交的 PR 仍优先用 `gh pr merge --rebase`：它同时保真 author、committer 与 `Signed-off-by`，而 squash/merge 会把 committer 盖成 `GitHub <noreply@github.com>`。
2. **回退条件**：若 Settings → Emails 的 "Keep my email addresses private" 变回 Off，立即恢复本节原先对三种服务端合并的禁令，改走 `--rebase` 或本地 `git merge --squash` + `git commit -s`。
3. **"Block command line pushes that expose my email" 刻意保持 Off**：SpiritPal `main` 历史含 866 条账号主邮箱提交，开启该闸会硬拒任何重放这段历史的推送，而 9 仓本地 `user.email` 已全部固定为 noreply，该闸边际收益为零。不要顺手打开它。
4. 已落库的个人邮箱提交用根目录 `.mailmap` 归一**显示**（不改写历史）。两个已知局限：`commit.author.email` 原文在 API 上仍公开可读；`.mailmap` 自身是被跟踪的公开文件，所以完整个人邮箱地址只写在 `.mailmap` 一处，本节与其他文档一律用「账号主邮箱」指代，避免同一地址在仓内多份文件里重复出现。
5. 2026-10-18 补漏：`ReSerendipity`、`.github`、`Image-DuoModel` 三仓的 `.mailmap` 原先只覆盖 `ReSerendipity@outlook.com`，而账号主邮箱已是另一个 outlook 地址（实测三仓 committer 字段各泄漏 1 笔），已各补一行归一。

## Harness 复核的证据边界

Better Harness 的会话证据按「工作区根的绝对路径」派生会话库标识，本账号下其他项目
（例如 `ComfyUI-Experiment-Toolbox`）都有各自按此规则命名的会话库。实测本仓**没有**对应
的会话库，且所有会话库中也不存在指向本仓路径的任何别名——即本目录从未作为工作区根被
打开过，因此没有可回溯的 Task Episode。由此有两条必须遵守的口径：

- 分析器可能报出「N 个会话 / M 条 Episode」这类数字。**那是账号级全局口径**，覆盖本机
  所有其他项目，**不得归属到本仓**；本仓的行为类结论只能写成「无会话证据」，不能写成
  「无重复劳动」，两者含义不同。
- 要让复核能判断重复劳动与改进效果，需以本目录为工作区根正常开展任务、积累至少两个可比
  Task Episode 后，再只读重跑 `evidence-bundle`。判定来源根是否存在，用只读的
  `session-analysis sources` 路由，不要靠猜测路径。

本仓的报告与中间产物都写在 `.qoder/` 下（已被 `.gitignore` 排除，不入库）。
