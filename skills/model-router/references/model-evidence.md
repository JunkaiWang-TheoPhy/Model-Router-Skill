# Model-routing evidence register

Last reviewed: 2026-09-07

## Supported model-family slots

The router accepts provider/model identifiers for GPT, Kimi, DeepSeek, GLM, Doubao, Seedance, Gemini, and Grok. These are routing slots, not claims of equal quality. Each slot must carry its own measured quality, price, latency, modality, and tool-support fields before it can become a preferred route.

This register supports routing decisions; it is not a universal ranking. Scores from different evaluations are not directly interchangeable. Update entries with the retrieval date, evaluation conditions, and a link to the primary source.

## Evidence currently used

| Dimension | Source | What it supports | Limit |
| --- | --- | --- | --- |
| General reasoning, coding, agentic workflows, computer use | [OpenAI GPT-5.4 announcement](https://openai.com/index/introducing-gpt-5-4/) | The vendor reports GPT-5.4 combines reasoning, coding, and agentic workflows, including native computer-use capabilities in Codex/API; it reports MMMU-Pro 81.2% without tools versus GPT-5.2 79.5%. | Vendor-reported; not a neutral cross-model comparison. |
| Human preference and coding | [Arena coding leaderboard](https://arena.ai/leaderboard?category=coding) | Useful live, preference-based comparison for coding responses; retain rank and uncertainty interval at retrieval time. | Preference data is prompt/population dependent and does not measure long-horizon execution directly. |
| Agentic tool/browser/computer workflows | [BenchLM agentic leaderboard](https://benchlm.ai/agentic) | A task-specific signal for tool use and agentic workflows. | Methodology and model coverage can change; snapshot rather than ground truth. |
| Multimodal-agent benchmark catalog | [Awesome multimodal agent benchmarks](https://github.com/PhiloLabs/awesome-multimodal-agent-benchmarks) | Discovery index for multimodal-agent evaluations and their task definitions. | A catalog is not itself a score or validation result. |

## Source inventory for recurring collection

The router tracks several complementary public sources instead of collapsing everything into one leaderboard. A future snapshot should record the retrieval date, model identifier, effort/tool settings, raw score, rank, uncertainty interval, and source type for each row.

| Family | Source | Primary signal |
| --- | --- | --- |
| Preference | [Arena overall](https://arena.ai/leaderboard) | Human preference across general prompts |
| Preference | [Arena coding](https://arena.ai/leaderboard?category=coding) | Human preference on coding prompts |
| Composite + price | [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/leaderboards/models) | Multi-benchmark intelligence, cost-per-task, price, latency, and speed context |
| Coding | [SWE-bench](https://www.swebench.com/) | Repository issue resolution by agents |
| Coding | [LiveCodeBench](https://livecodebench.github.io/) | Contamination-resistant competitive coding |
| Agentic | [GAIA benchmark](https://huggingface.co/gaia-benchmark) | General assistant tool use and multi-step tasks |
| Agentic | [τ-bench](https://github.com/sierra-research/τ-bench) | Tool-calling policy adherence and stateful interaction |
| Browser/research | [BrowseComp](https://openai.com/index/browsecomp/) | Difficult web retrieval and synthesis |
| Multimodal reasoning | [MMMU-Pro](https://mmmu-benchmark.github.io/) | Visual and cross-domain reasoning |
| Science/reasoning | [Humanity's Last Exam](https://lastexam.ai/) | Broad expert-level knowledge and reasoning |

Coverage statistic for this revision: 10 source families (3 preference/composite, 2 coding, 3 agentic/browser, 1 multimodal, 1 science/reasoning). This is source coverage, not a claim that one model leads all families.

## Price and efficiency accounting

Track price as a first-class routing signal, but keep these quantities separate:

- input, cached-input, cache-write, reasoning, and output token prices;
- tool or search charges and any priority/fast-mode surcharge;
- estimated cost per task, not only cost per million tokens;
- latency, throughput, and retry/failure cost.

[Artificial Analysis](https://artificialanalysis.ai/models/) publishes cost-per-task calculations that combine token categories and benchmark token usage, while its [data API](https://artificialanalysis.ai/data-api) exposes benchmark, pricing, latency, and throughput fields. Use those as external comparison inputs. For Codex aliases, prefer current host usage telemetry or invoice data; if unavailable, mark price as `unknown` and avoid pretending that a public family price applies.

The router should select by a quality–cost frontier: choose the least costly route whose expected quality and risk satisfy the task, then switch to a better-fitting route when verification fails. For repeated workloads, report median and p95 cost per completed task, including retries, rather than a single optimistic token estimate.

## Claim ledger

| Claim ID | Claim | Evidence count | Status | Routing treatment |
| --- | --- | ---: | --- | --- |
| H-001 | Astra may improve agentic and multimodal work more than Sol while offering a smaller pure-reasoning gain. | 0 direct public measurements of the exact aliases; 1 user-reported hypothesis | Provisional | Use only as a prior; require local A/B evaluation before changing a default route. |
| F-001 | GPT-5.4 vendor materials report combined reasoning, coding, agentic, and computer-use capabilities. | 1 primary source | Observed, vendor-reported | Supports considering a frontier route for complex agentic tasks, with a vendor-bias caveat. |
| M-001 | Public leaderboards are task- and population-dependent and can disagree. | 4 source families in the current register | Methodological conclusion | Weight the benchmark family matching the inferred task; do not use a universal rank. |

## How to aggregate

1. Separate dimensions into reasoning, coding, agentic execution, multimodal understanding, latency, cost, and reliability.
2. Normalize only within the same benchmark family and evaluation conditions. Keep raw values and ranks alongside any normalized score.
3. Weight the dimension that matches the inferred task. Do not let a general leaderboard override a directly relevant task evaluation.
4. Require at least two independent sources before turning a claim into a routing rule. Label one-source or anecdotal claims as provisional.
5. Recheck volatile rankings before high-stakes routing. Retire stale entries rather than silently carrying them forward.

## Interpretation policy

Claims such as “Astra improves agentic and multimodal work more than Sol, while reasoning gains are small” may be a useful hypothesis, but are not established until exact model variants, effort settings, prompts, tools, and sample sizes are recorded. Public boards often expose model families rather than internal Codex aliases, so the router should use such claims as a prior and local task outcomes as the deciding evidence.
