# Provider and model-family catalog

Last reviewed: 2026-09-07. This is a routing inventory, not a leaderboard. A provider enters the preferred set only after recording current model ID, modality, tool support, benchmark conditions, price, and reliability.

| Family | Official model/pricing source | Evaluation sources to collect | Initial routing hypothesis |
| --- | --- | --- | --- |
| GPT | [OpenAI models and pricing](https://openai.com/api/pricing/) | Arena, SWE-bench, Terminal-Bench, BrowseComp, MMMU-Pro, Artificial Analysis | Frontier reasoning, coding, and agentic baseline; verify effort-dependent cost. |
| Claude | [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) | Arena, SWE-bench, GDPval, Terminal-Bench, Artificial Analysis | Strong long-form coding and knowledge work candidate; verify cache and long-context pricing. |
| Kimi | [Moonshot API docs](https://platform.moonshot.cn/docs) | Arena coding, SWE-bench, BrowseComp, Terminal-Bench | Long-context and coding candidate; require direct API price and reliability data. |
| DeepSeek | [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/) | LiveCodeBench, SWE-bench, GPQA, Artificial Analysis | Cost-sensitive reasoning/coding candidate; account for peak/off-peak price changes. |
| GLM | [Z.ai pricing](https://bigmodel.cn/pricing) | Arena, Chinese-language evals, SWE-bench, Artificial Analysis | Chinese-language and general reasoning candidate; verify tool-call behavior. |
| Doubao | [Volcengine Ark documentation](https://www.volcengine.com/product/ark) | Chinese instruction following, multimodal evals, latency and cost tests | China-region availability and cost candidate; use provider-specific measurements. |
| Seedance | [ByteDance Seedance](https://seed.bytedance.com/en/seedance2_0) | Video Arena, VBench, image/video consistency and instruction tests | Generative-video specialist, not a drop-in text/agent replacement; price per generation. |
| Gemini | [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) | MMMU-Pro, BrowseComp, SWE-bench, Arena, Artificial Analysis | Multimodal, long-context, and fast-model candidate; separate grounding/search charges. |
| Grok | [xAI API pricing](https://docs.x.ai/developers/pricing) | Arena, SWE-bench, Terminal-Bench, BrowseComp, Artificial Analysis | Real-time/web and coding candidate; verify tool access, latency, and service-tier price. |

## Collection and scoring rules

For each family, retain a dated row with `model_id`, `provider`, `benchmark`, `score`, `rank`, `uncertainty`, `input_price`, `cached_input_price`, `output_price`, `tool_cost`, `latency`, `modality`, and `source_url`. Normalize scores only inside the same benchmark and conditions. Compute a task-weighted quality score, then report cost per successful completed task and a quality/cost Pareto frontier. Do not compare Seedance video-generation costs with text token costs without a separate unit model.

Current evidence status: the family slots are registered, but exact preferred routes remain `unverified` until provider-level measurements and reproducible snapshots are added. User-facing recommendations should summarize this uncertainty naturally instead of exposing the catalog schema.
