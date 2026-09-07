---
name: model-router
description: Infer the user's task intent from conversation and workspace context, then recommend or route to the best available Codex model and reasoning effort. Use when model choice, delegation, latency, or quality tradeoffs need to be decided; do not use it as a substitute for domain-specific execution skills.
---

# Model Router Skill

Select the least expensive model that is likely to satisfy the actual task, switching models when ambiguity, risk, or reasoning depth makes another fit more appropriate. This skill is a routing aid: it may recommend a model for the current response or set an explicit model when creating/delegating a Codex task, but it cannot change the model already running the current turn.

## Runtime model discovery

Before recommending a route, identify two separate facts:

1. **Current model** — use the model identifier exposed by the current system/app turn, if present. If it is not exposed, report `unknown`; never infer it from the requested reasoning effort or from a model name mentioned in the conversation.
2. **Known supported models** — inspect the current host's advertised model capabilities first, then non-secret local configuration and environment metadata. The bundled helper `scripts/detect_runtime.py` performs a conservative scan and emits JSON without printing tokens or private prompt content.

Treat a configured model as *available in configuration*, not proof that the account or current host can invoke it. Treat an API model-list response as account/API availability, not proof that the Codex app exposes the same model. Record the source and timestamp for every discovered item.

## 1. Build a minimal task profile

Read only context needed for routing:

- User goal and deliverable (answer, code change, review, research, document, visual, automation).
- Ambiguity: whether requirements, boundaries, or acceptance criteria are missing.
- Complexity: number of dependent steps, cross-file reasoning, algorithms, and synthesis breadth.
- Risk: security, privacy, legal/medical/financial impact, destructive or externally visible actions.
- Workspace signals: current working directory, relevant files, repository status, available tools/skills, and recent errors. Do not dump unrelated file contents or secrets into the routing rationale.
- Interaction constraints: latency sensitivity, requested depth, and whether parallel delegation is allowed.

Treat explicit user model requests as preferences, subject to availability and safety. Treat the latest user message and fresh tool output as authoritative.

## 2. Choose a route

Use this practical model map (names are case-insensitive):

| Situation | Preferred route | Why |
| --- | --- | --- |
| Large synthesis, novel architecture, high-stakes reasoning, difficult debugging, or subtle tradeoffs | **Astra max** | Highest reasoning headroom; accept higher latency/cost |
| Complex implementation, multi-file refactor, rigorous review, or research synthesis | **Terra high** | Strong general reasoning with good execution reliability |
| Normal coding, analysis, tool use, or a response needing balanced quality | **Sol medium** | Default balanced route |
| Straightforward lookup, formatting, small edit, classification, or latency-sensitive step | **Sol light** | Fast and economical; switch if uncertainty changes the task fit |
| Broad but repetitive scanning, enumeration, summarization, or batch triage | **Luna max** | High-throughput context handling; use a stronger model for novel decisions |

Adjust the initial choice as follows:

1. For high ambiguity, irreversible actions, security/privacy concerns, or an unmet verification gate, select the model with the reasoning and verification capacity that best fits the risk; do not describe this as an upgrade.
2. For deterministic, well-specified work with a narrow acceptance test, prefer the route with lower latency or cost when quality remains sufficient.
3. Choose Terra high rather than Astra max when the task is complex but conventional and implementation-oriented; these are different fits, not levels in a ladder.
4. Choose Luna max when breadth/volume dominates originality; do not use it for a critical architectural decision solely because it is efficient at scanning.
5. If a requested model or effort is unavailable on the target host, choose the nearest supported combination and state the substitution.

Reasoning-effort labels map directly to the host capability (`light` → `low`, `media`/`medium` → `medium`, `high` → `high`, `max` → `max`). Never invent support for a model/effort pairing; inspect the current host's advertised capabilities when routing a delegated task.

## 3. Route safely

- For the current reply, provide a recommendation; do not imply that the active model changed.
- For a delegated Codex task, pass the selected `model` and `thinking` only when an explicit override improves the outcome; otherwise inherit the destination's settings.
- Keep routing separate from authorization. A stronger model does not grant permission for external, destructive, or sensitive actions.
- Invoke domain skills after routing when their trigger applies (for example, documents, spreadsheets, security review, or web research). Model choice never replaces those skills.
- If the profile is genuinely underdetermined, choose a safe balanced route (Sol medium) and name the single uncertainty that could change the decision; do not interrogate the user for trivial distinctions.

## 4. Response style and contract

Default to a natural, human-readable answer. Unless the user explicitly asks for one model, always give at least two viable candidates, each with an independent fit score from 0% to 100%. Scores do not need to add up to 100%; multiple models may each score 100% when they fit different aspects of the task. Displayed candidates must differ by at least 5 percentage points. If the evidence is nearly tied, use a secondary task-fit factor such as cost, latency, tool support, or verification burden to make the decision margin explicit. Scores are evidence-based judgments of task fit, not measured probabilities. Explain the tradeoff conversationally rather than exposing a rigid template.

Mention the main reason, the likely upgrade trigger, and any meaningful uncertainty in one or two short paragraphs. Keep the tone conversational and decisive, not bureaucratic. Do not mention hidden workspace details merely to make the answer sound analytical.

Only when the user explicitly asks for an audit trail, JSON, or a structured decision record, return:

```text
Intent: <one-sentence inferred goal>
Route: <model> / <effort>
Confidence: <high|medium|low>
Signals: <2–4 concrete context signals>
Why: <short tradeoff explanation>
Fallback: <nearest alternative and trigger>
Action: <recommend current reply, or specify delegated-task override>
```

When using the structured format, include `Candidates: <model / effort — fit: percentage>` with at least two entries unless the user explicitly requested a single model. Each fit score must be between 0% and 100%; scores are independent and must not be normalized or summed. Ensure every displayed pair differs by at least 5 percentage points.

Use `Confidence: low` when intent or environment evidence is incomplete. Distinguish observed facts from inference, and never expose credentials, private content, or irrelevant workspace details merely to justify a route.

## 5. Evidence maintenance

For model-quality claims, read [references/model-evidence.md](references/model-evidence.md) when the task needs a nontrivial comparison. Treat it as a dated evidence register, not a permanent ranking. Prefer multiple independent leaderboards and task-specific evaluations over one aggregate score. Record benchmark conditions, confidence intervals when available, publication date, and whether a result is vendor-reported, third-party, or anecdotal. Exact Codex aliases such as Sol, Terra, Luna, and Astra may not appear on public boards; do not fabricate equivalences—mark the mapping as an internal hypothesis until measured locally.

For provider-specific routing and price discovery, read [references/provider-catalog.md](references/provider-catalog.md). It defines the supported-family slots without treating availability, quality, or price as permanent.
