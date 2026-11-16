# .githooks（入库正本）

本目录是随仓分发的 git 钩子正本；`local/hooks/` 是本机包装层，不入库（§13.1）。

## 安装（换机 / 重克隆后必做一次）

```sh
git config core.hooksPath .githooks
```

## pre-push 行为

1. **main 保护**（始终生效）：禁止删除 `main`、禁止非快进推送 `main`（私有仓无服务器侧保护的替代控制，ADR-0004）。逃生阀：`SKIP_GOVERNANCE_HOOKS=1 git push ...`。
2. **家族台账闸**（可选）：设置 `GOVERNANCE_HOME` 指向 `ReSerendipity/.github` 的本地克隆后，pre-push 会调用其 `check-ledger-append.ps1`（代码变更须 GOTCHAS 新行、AGENTS.md 变更须 REVISION_LOG 新行，ADR-0012/0019）。未设置时仅打印提示，不阻断。

PowerShell 示例（写入用户环境变量，重开终端生效）：

```powershell
[Environment]::SetEnvironmentVariable('GOVERNANCE_HOME', 'C:\Users\<你>\APP\repository\.github', 'User')
```
