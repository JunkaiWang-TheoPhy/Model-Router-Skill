<p align="center">🇺🇸 <a href="README.md">English</a> | 🇨🇳 <a href="README.zh.md">中文</a></p>

<h1 align="center">Model Router Skill</h1>

<p align="center"><a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-blue.svg" alt="AGPL-3.0 license"></a> <img src="https://img.shields.io/badge/status-experimental-purple.svg" alt="Experimental"></p>

![Model Router Skill banner](assets/model-router-banner.png)

## Introduction

Model Router Skill is a Codex skill for inferring task intent from conversation and workspace context, then selecting a suitable model and reasoning effort. It treats public benchmark results as dated evidence rather than a permanent ranking.

The router covers reasoning, coding, agentic execution, multimodal work, latency, cost, and reliability. It distinguishes an advisory recommendation for the current turn from an explicit model override for delegated tasks.

## Repository layout

- `skills/model-router/` — installable Codex skill
- `skills/model-router/references/model-evidence.md` — dated benchmark and source register
- `skills/model-router/SECURITY.md` — public/forkable repository security policy
- `COPYRIGHT.md` and `NOTICE` — copyright and third-party attribution records
- `assets/model-router-banner.png` — repository banner

## Use

Copy `skills/model-router` into your Codex skills directory, or invoke it explicitly as `$model-router` after installation. The skill emits a compact decision record with inferred intent, route, confidence, evidence signals, fallback, and action.

## Evidence policy

Use multiple independent, task-specific evaluations where possible. Do not equate internal aliases such as Sol, Terra, Luna, or Astra with public model families without measured evidence. See the [evidence register](skills/model-router/references/model-evidence.md).

## License

Copyright is retained by the project contributors. The code and skill are licensed under the GNU Affero General Public License v3.0; preserve notices and mark modifications when redistributing. See [COPYRIGHT.md](COPYRIGHT.md), [NOTICE](NOTICE), and [LICENSE](LICENSE).
