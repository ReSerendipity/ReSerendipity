# GOTCHAS（坑点台账）

> 本文件由自进化协议维护：每次踩坑 / 修 bug 后追加到表尾，不删不改历史行。
> 路径优先 `local/agents/GOTCHAS.md`；存量 `docs/agents/GOTCHAS.md` 视为历史分片。
> 不得写密钥 / token / 口令 / 连接串；限制级内容只写指路，不摘正文。

| # | 坑点标题 | 触发场景 | 现象/报错 | 正确做法 | 首次发现日期 |
|---|---|---|---|---|---|
| 1 | 示例：把「探测不到」写成「缺失即故障」 | 干净检出 / CI 里读本地文件 | 报「文件缺失」，实际是设计上不入库 | 先查 `.gitignore` 与 `git ls-files`，再判定 | YYYY-MM-DD |
| 2 | .gitignore 变更触发 ledger-gate | 文档收口同步本地忽略注释 | push 被拦「代码/配置/脚本变更，但 GOTCHAS 未新增行」 | 追加本行；本次无代码踩坑 | 2026-11-04 |
| 3 | 只精简 README 会把 CI 判红 | 主页仓从 260 行改成简历式 | `check_readme.py` 逐字要求两张 HTML 精选卡片与 Apache-2.0 恰好 2 次；`check_public_index.py` 要求覆盖全部公开仓，删文案即失败 | 识别为「契约变更」而非文案改动：治理 §8.2 先立精简模板，再同步改两个脚本的断言与本地 AGENTS.md §3，最后跑两条校验 | 2026-11-12 |
| 4 | 中文 override 在 PowerShell 台账门禁里失效 | pre-push hook 调 `check-ledger-append.ps1`，commit message 已写「本次无踩坑」 | 仍报「代码/配置/脚本变更，但 GOTCHAS 未新增行」，且报错中文全为问号；说明 `$msg` 从 git 读回时中文乱码，`$override` 匹配失败 | 兜底关键词用 ASCII `[skip-ledger]`；或按自进化铁律真实追加 GOTCHAS 行使 `gotchasAdded=true`。不要为了绕门禁去改断言或跳过 hook | 2026-11-12 |
| 5 | 台账被父目录级 ignore 挡住，`!` 反包含写了不生效 | 本仓 `.gitignore` 原为 `/local/`，按 ledger-gate 要求往台账补行后执行 `git add` | `git check-ignore -v` 仍命中 `/local/`，`git add -n` 报 paths are ignored；台账长期只存在于本机，远端无该文件 | 按 ADR-0019 改四段式：`/local/*` → `!/local/agents/` → `/local/agents/*` → `!/local/agents/GOTCHAS.md` → `!/local/agents/REVISION_LOG.md`；验收以 `git add -n` 成功为准，且同目录 `.ledger-baseline.json` 等内部件必须仍被忽略 | 2026-11-12 |
