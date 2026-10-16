# AGENTS.md — ReSerendipity

## 仓库定位

这是 GitHub **个人账号**主页仓库（profile repo，账号 `ReSerendipity` 是 user 而非 org，
枚举公开仓库要走 `users/ReSerendipity/repos`，`orgs/...` 会 404），内容以 `README.md` 的主页卡片为主。
本仓库唯一的**远端**自动门禁是 `.github/workflows/ci.yml`，它在 **push 到 `main`** 和**所有 PR** 上运行两步检查：

1. `README.md` 存在且非空（`test -f` / `test -s`）；
2. `python3 .github/scripts/check_readme.py` —— 校验精选卡片字符串、许可证表述、过期串，以及「全部公开项目」表格的**结构**不变量。

除 ci.yml 外没有其他 CI/CD 门禁。另有一条**只能本地跑**的清单完整性检查 `check_public_index.py`（见下），它需要访问 GitHub API，而本 CI 无出网权限，因此**不在远端强制执行**。修改 README 或脚本前，先在本地复现这两项校验。

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
- `check_public_index.py`：需要 GitHub API（复用本机已登录的 `gh`，仓库内不存任何凭据）。退出码 `0` = 清单与公开仓库集合一致，`1` = 发现缺项或已失效条目，`2` = 无法判定（`gh` 缺失、未登录或网络失败）。**`2` 不是通过**，不要把它当绿灯。
- 该检查声明的排除项为 `ReSerendipity`（本主页仓库自身）与 `.github`（治理与社区健康文件，README 末尾已单独给出入口）；除此之外新增公开仓库必须入表。

## 编辑守则

- 改动 `README.md` 中精选卡片区域时，保持上表字符串逐字不变；只改卡片描述文案等不受契约约束的部分。
- **「全部公开项目」表格区同样受契约约束**：受 `check_readme.py` 的 7 条结构不变量限制，并受 `check_public_index.py` 的完整性约束。新增公开仓库必须补一行；显示名要等于 slug、简介不能空、链接必须在 `github.com/ReSerendipity/` 下。简介取自该仓库自身的 GitHub `description`，不要代拟文案。
- **不要为了让 CI 通过而放宽或修改 `check_readme.py` / `check_public_index.py` / `ci.yml` 的断言**；门禁是契约的一部分。
- 新增/删除精选卡片属于契约变更，需同步修改 `check_readme.py` 并相应核对 Apache-2.0 出现次数。
- 改动 `README.md` 或任一脚本后，两条本地校验都要跑；提交信息里应能对应到跑过的检查结论。
