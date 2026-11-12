# ReSerendipity

独立开发者 · 本地优先的 AI 媒体工具与端侧应用作者。
做语音、图像、视频的生成与修复，也写 Android 原生工具和离线可跑的单页实验；偏好可自托管、不依赖云端、能在本机闭环的完整工具链。

> 治理规范：[ReSerendipity/.github/governance](https://github.com/ReSerendipity/.github/tree/main/governance)

## 专注领域

| 方向 | 主要工作 |
|---|---|
| 语音 / 音频 | 多引擎 TTS 统一调度、声音克隆与设计、多角色配音 |
| 图像 / 视频 | 本地超分与修复、多模型图像生成、ComfyUI 工作流工程化 |
| 端侧应用 | Android 原生工具、Tauri 桌面壳、离线优先的文件与编辑器 |
| Web 实验 | 单文件零构建交互演示、Three.js 可视化 |
| 工程治理 | 账号级仓库规范、CI 门禁、可复现的发布与证据链 |

**常用技术栈**：Python / FastAPI · Kotlin (Android) · Tauri v2 / Rust · TypeScript / Vite / Three.js · CUDA 本地推理 · GitHub Actions

## 代表项目

| 项目 | 说明 |
|---|---|
| [TTS-MultiModel](https://github.com/ReSerendipity/TTS-MultiModel) | 六引擎本地 TTS 工作台：声音克隆、声音设计、多角色配音，Windows / Linux / Docker（Apache-2.0） |
| [SeedVR2-Lite](https://github.com/ReSerendipity/SeedVR2-Lite) | 视频 / 图像超分：桌面版 + 网页版，批量修复，无需 ComfyUI（Apache-2.0） |
| [Image-DuoModel](https://github.com/ReSerendipity/Image-DuoModel) | 多模型图像生成与编辑：LoRA 叠加、超分、批量生成、水印溯源 |
| [DraftPeek](https://github.com/ReSerendipity/DraftPeek) | Android 原生代码 / 文本编辑器：内置终端、Markdown 预览、40+ 语言高亮 |
| [GameShell](https://github.com/ReSerendipity/GameShell) | Android 视觉小说运行器：引擎识别 + 原生 / 模拟智能路由 |
| [SpiritPal](https://github.com/ReSerendipity/SpiritPal) | Tauri 桌面 AI 伙伴：Live2D 角色、本地记忆与专注工具 |
| [dsh-superagent](https://github.com/ReSerendipity/dsh-superagent) | 把 GitHub / 收件目录 / 群聊事件转成隔离执行的工单并回贴结果 |

完整项目索引见 [Repositories](https://github.com/ReSerendipity?tab=repositories)（含归档与实验项目，由 GitHub 自动更新，无需手工维护清单）。

## 协作方式

- **许可**：各仓独立授权，以仓库自身 LICENSE 为准；本主页仓是内容页，保留所有权利。
- **反馈**：功能建议与问题请到对应项目开 Issue；安全漏洞按 [SECURITY.md](https://github.com/ReSerendipity/.github/blob/main/SECURITY.md) 私下报告。
- **治理**：命名、README、发布与 CI 的公共条款统一在 [.github/governance](https://github.com/ReSerendipity/.github/tree/main/governance)。

---

*English: Independent developer building local-first AI media tooling (TTS, image/video restoration and generation) and offline-capable Android, desktop and web apps. Selected work is above; [all repositories](https://github.com/ReSerendipity?tab=repositories).*
