# Runtime provider probe

Last verified: 2026-09-07 (Asia/Shanghai)

## Privacy-safe result

| Credential path | Status | Confirmed model IDs relevant to routing |
| --- | --- | --- |
| DeepSeek official API `/models` | OK | `deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` |
| GLM official API `/models` | Key not exposed to this process | None confirmed through the official endpoint |
| Configured OpenAI-compatible gateway `/models` | OK | `GLM-5.2`, `glm-5.1`, `glm-5`, `glm-5-turbo`, `glm-5-code`, `DeepSeek-V4-Flash`, `DeepSeek-V4-Pro`, and older variants |

The snapshot omits credentials, account identifiers, and gateway hostnames. Provider catalog visibility does not prove that every listed alias has quota, identical behavior, native reasoning controls, or current pricing.

## Capability and price interpretation

DeepSeek's official documentation identifies `deepseek-v4-flash` as DeepSeek-V4-Flash-0731 and `deepseek-v4-pro` as DeepSeek-V4-Pro-0813. Both expose a 1M context window, tool calls, Responses API, JSON output, and thinking/non-thinking modes. At the verification date, the official price table listed per-million-token cache-hit/cache-miss/output prices of `$0.0028/$0.14/$0.28` for Flash and `$0.003625/$0.435/$0.87` for Pro. Recheck before cost-sensitive routing because prices are explicitly mutable.

The gateway confirms that `GLM-5.2` is addressable on this machine. Its exact reasoning-control syntax and gateway price were not returned by `/models`, so the router may name the model but must not invent an effort setting or price. Probe a model-specific metadata or billing endpoint before calling it the value choice.

## Current routing consequence

- `deepseek-v4-flash / thinking`: eligible for high-volume extraction and inexpensive first-pass analysis.
- `deepseek-v4-pro / thinking`: eligible for more demanding DeepSeek reasoning and agentic work.
- `GLM-5.2`: catalog-confirmed through the gateway, but effort and price remain unverified.
- GPT models from the local Codex cache remain host-catalog entries; current-turn identity is separate.
