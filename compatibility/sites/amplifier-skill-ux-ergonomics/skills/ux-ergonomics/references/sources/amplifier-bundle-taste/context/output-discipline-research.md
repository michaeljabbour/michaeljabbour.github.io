# Output Discipline — Research Backing

Distilled motivation for the `output-discipline` skill and behavior. Source: the four root-cause notes and three remediation notes in `taste-skill/research/laziness/` (RLHF + compute, training-data bias, cognitive shortcuts, output limits, prompt engineering, architectural patterns, parameter tuning).

This document is a summary, not a citation list. It captures the empirical claims as they appeared in the source notes; check the originals for primary references.

---

## Why models default to truncation

### 1. RLHF brevity bias

Token generation costs GPU compute. To control cost, providers use RLHF and post-training alignment to reward shorter, more confident outputs. The model is not silently lazy — it has been *trained* to prefer brief, summary-shaped responses over rigorous multi-step ones, because brief responses scale.

Two related signals come from this training pressure:

- **Stopping pressure.** Autoregressive models have no inherent sense of task completion, so training induces a learned tendency to conclude. Recent iterations have calibrated this aggressively, leading to mid-task halts ("let me know if you want me to continue") and skipped fields in long structured outputs.
- **Dynamic throttling.** During peak demand, providers may scale back generation depth on top of the base alignment, producing even shorter outputs when server load is high.

### 2. Training-data placeholder propagation

LLMs imitate patterns. A large slice of training data — Stack Overflow answers, GitHub READMEs, tutorial blogs, framework docs — uses abbreviated code as a *legitimate* answer format:

```python
def complex_logic():
    # implement auth here
    pass
```

The model treats this pattern as professional. When asked for a complete implementation, it faces competing signals: the explicit instruction (full code) versus the deeply embedded distribution (tutorial-style abbreviation). Without aggressive prompting, the tutorial pattern wins because it appears far more often in the training distribution.

This is also why the `// ...`, `// rest of code`, "similarly for the remaining" patterns show up on different models — they are inherited from the same shared corpus, not from any one alignment policy.

### 3. Cognitive shortcuts on complex tasks

Late-2024 benchmarks ("LazyBench" and similar) showed measurable cognitive shortcutting in frontier models including Gemini Pro and GPT-4o: when the task looks easy or the context looks long, the model reduces its internal computational effort. This is not memory loss — the model retains the input and chooses not to process it at full depth.

Two compounding effects:

- **Error-avoidance truncation.** Longer outputs increase the surface area for hallucinations and compounding mistakes. The model has learned that shorter outputs reduce blame, so truncation also functions as risk mitigation.
- **Context-driven brevity drift.** Even arbitrary contextual signals shift output length — the documented late-2023 "December effect," where ChatGPT became measurably terser in winter because the training corpus contains more out-of-office and short holiday content. Inserting "It is May" into the system prompt measurably restored length.

### 4. Output-limit asymmetry

Modern models have huge input windows (1–2M tokens) but tightly capped outputs (typically 8K). When the model estimates that a complete response would exceed its output budget, it preemptively *compresses* — abbreviating sections it would otherwise have written in full — rather than risking a hard cutoff at an awkward point.

Consumer-facing apps add a second layer: history capping (~32K), context pruning, and retrieval-based recall that silently drops earlier system instructions. Direct API and CLI access bypass this middleware and produce longer, more complete outputs from the same underlying model.

---

## Remediation techniques that work

The remediation notes cluster into three families. The `output-discipline` skill draws from all three.

### A. Explicit anti-truncation prompting

- **Hard ban lists.** Enumerate the placeholder strings (`// ...`, `// rest of code`, "for brevity") and instruct the model to scan its own output for them before sending. This is the core of the `output-discipline` skill body.
- **Scope-then-build-then-cross-check.** Force the model to count expected deliverables *before* generating, then verify the count *after* generating. This consumes the model's capacity for shortcutting and removes plausible deniability.
- **Pause/resume protocol.** When the response genuinely exceeds the output budget, give the model a clean exit ("write to a breakpoint, end with a structured pause line, resume on `continue`") rather than letting it improvise — improvisation is where compression happens.

### B. Architectural constraints

- **Lazy-loaded skill files.** Keep the rule body out of the system prompt by default; load it only when relevant. Reduces context dilution that triggers the cognitive shortcut described above. Specific YAML descriptions (a sentence describing exactly when to load) push discovery from ~68% to ~90%.
- **Chunked task execution.** For tasks that genuinely exceed the output budget, request architecture first, components individually, then integration — instead of asking the model to estimate total length and self-compress.
- **MCP / tool-grounded answers.** When facts come from a live source rather than weights, the model has less incentive to hallucinate or truncate to avoid factual claims.

### C. Parameter tuning

- **Lower temperature + lower top-p** for code and structured output. Amplifies the highest-confidence continuation and makes the model more deterministic — useful in combination with explicit hard bans, because the bans land more reliably when sampling is concentrated.
- **Thinking-level / reasoning-effort tuning** on models that expose it (Gemini 3 `thinking_level`, Claude/GPT extended-reasoning toggles). Set to `medium` or `high` for code generation and complex analysis. Avoid combining extreme low temperature with `high` thinking — that combination can induce internal reasoning loops.

---

## What this skill actually leverages

`output-discipline` is a Family-A intervention: explicit bans + scope-build-cross-check + a structured pause protocol. It does not require harness-level support for parameter tuning or MCP grounding to work — those are upstream concerns. The skill assumes the model has been told to follow it (via auto-load behavior) and that the harness routes long outputs through the pause/resume contract rather than auto-summarizing.

The empirical claim behind shipping it always-on rather than per-task: brevity bias and placeholder propagation are *defaults*, not reactions to specific prompts. Any task that produces code or long-form artifacts is at risk. Loading the skill on session start removes the per-prompt invocation step, which is itself a place where the user often forgets and the truncation reappears.
