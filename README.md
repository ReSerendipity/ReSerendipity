# ReSerendipity

主要维护多模态 AI 应用与工具方向的开源项目。

## 项目

| 仓库 | 简介 |
|---|---|
| [Image_MultiModel](https://github.com/ReSerendipity/Image_MultiModel) | 多引擎统一文生图/图生图后端服务 + 轻量 Web UI |
| [TTS_MultiModel](https://github.com/ReSerendipity/TTS_MultiModel) | 多引擎语音合成（TTS）工具 |
| [SeedVR2-lite](https://github.com/ReSerendipity/SeedVR2-lite) | 图片/视频修复增强（SeedVR2 轻量版） |
| [MiniMax-H3-lite](https://github.com/ReSerendipity/MiniMax-H3-lite) | 视频生成时间线工作台（轻量 Web 壳） |
| [SpiritPal](https://github.com/ReSerendipity/SpiritPal) | 桌面宠物应用（Tauri） |
| [DraftPeek](https://github.com/ReSerendipity/DraftPeek) | Android 草稿预览编辑器 |
| [ComfyUI-BatchPromptLoader](https://github.com/ReSerendipity/ComfyUI-BatchPromptLoader) | ComfyUI 自定义节点：从 TXT 批量加载提示词（固定 / 递增 / 递减 / 随机） |
| [Multi-Tracker](https://github.com/ReSerendipity/Multi-Tracker) | 多平台视频创作者工具箱：B 站 / 抖音 / 快手 / 小红书 视频下载、飞书同步、评论与 AI 转写 |
| [Unfading-Wall](https://github.com/ReSerendipity/Unfading-Wall) | 教师节「黑板上的话」师生印象墙，零后端链接分享 |

## 治理约定

所有仓库共用 [.github](https://github.com/ReSerendipity/.github) 中的默认社区健康文件（贡献指南 / 行为准则 / 安全披露 / 支持渠道），由账号级自动回退生效，项目定制以各自仓库文件为准。

其中 Image_MultiModel、TTS_MultiModel、SeedVR2-lite、MiniMax-H3-lite 四个 Python 仓库额外共用家族级 CI 质量门禁（可复用 workflow）。

许可证以各仓库 `LICENSE` 为准，多数为 **Apache-2.0**。另有 ComfyUI-Manager 为上游项目的 fork，不在上表列出。
