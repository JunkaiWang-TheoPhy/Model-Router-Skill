<p align="center">🇺🇸 <a href="README.md">English</a> | 🇨🇳 <a href="README.zh.md">中文</a></p>

<h1 align="center">Model Router Skill</h1>

<p align="center"><a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-blue.svg" alt="AGPL-3.0 许可证"></a> <img src="https://img.shields.io/badge/status-experimental-purple.svg" alt="实验状态"></p>

![Model Router Skill 路由示意图](assets/model-router-banner.png)

## 引言

Model Router Skill 是一个 Codex Skill，用于从对话和工作区上下文推断任务意图，并选择合适的模型与推理强度。它把公开榜单视为带日期的证据，不把任何榜单当成永久排名。

路由维度包括推理、编码、智能体执行、多模态任务、延迟、成本和可靠性。技能会区分当前回复的建议与委派任务时的显式模型覆盖。

## 仓库结构

- `skills/model-router/` — 可安装的 Codex Skill
- `skills/model-router/references/model-evidence.md` — 带日期的榜单与来源登记
- `skills/model-router/SECURITY.md` — 公开、可 Fork 仓库的安全策略
- `COPYRIGHT.md` 和 `NOTICE` — 版权与第三方归属登记
- `assets/model-router-banner.png` — 仓库 Banner

## 使用

将 `skills/model-router` 复制到 Codex 技能目录，安装后也可以显式调用 `$model-router`。技能会输出简洁的决策记录，包括推断意图、路由、置信度、证据信号、备选方案和行动建议。

## 证据策略

尽量使用多个相互独立且与任务相关的评测。没有实测证据时，不要把 Sol、Terra、Luna、Astra 等内部别名直接等同于公开模型系列。详见[证据登记](skills/model-router/references/model-evidence.md)。

## 许可证

项目贡献者保留版权。代码和 Skill 采用 GNU Affero General Public License v3.0；再分发时请保留版权与许可证声明，并标注修改内容。详见 [COPYRIGHT.md](COPYRIGHT.md)、[NOTICE](NOTICE) 和 [LICENSE](LICENSE)。
