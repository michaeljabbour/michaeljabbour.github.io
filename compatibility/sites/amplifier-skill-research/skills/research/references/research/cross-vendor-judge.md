---
bundle:
  name: research-cross-vendor-judge
  version: 0.1.0
  description: |
    Codifies the v3 program paper's reflexivity-hazard #1 mitigation: the
    LLM judge in any evaluation must be from a DIFFERENT vendor family
    than the system-under-test. Promotes "cross-vendor by class" from a
    discretionary best-practice to a first-class behavior with an explicit
    enforcement gate that any evaluation recipe can opt into.
---

# Behavior: cross-vendor-judge

**Default:** opt-in (per-recipe via `judge_cross_vendor_required: true`)
**Applies to:** any recipe that uses an LLM judge for grading, with a known SUT vendor

---

## What it does

When a recipe declares `judge_cross_vendor_required: true`, the bundle enforces:

1. The judge's `provider_preferences` MUST list at least one vendor family OTHER than the SUT's vendor family.
2. If the SUT is `claude-*`, the judge cannot be `claude-*`. If the SUT is `gpt-*`, the judge cannot be `gpt-*`. If the SUT is `gemini-*`, the judge cannot be `gemini-*`. Same for any open-weights family (e.g., `llama-*`, `qwen-*`, `gpt-oss-*`).
3. The judge is expressed as a fallback chain of explicit `provider:`/`model:` entries spanning multiple vendor families. The schema does NOT support `class: reasoning` inside `provider_preferences:` (the validator rejects this; v0.8.3 schema-discovery correction); cross-vendor enforcement is via the explicit fallback chain alone.
4. If no non-overlapping judge is available in the routing matrix, the recipe halts with an explicit error rather than silently falling back to a same-vendor judge.

## Why this exists

PSE-PG14 Layer 2 measured a real cross-judge sensitivity: the `claude-opus-4-7` judge graded `claude-*`-family agents 3 to 10 percentage points more leniently than `gpt-5.5` did, across three Anthropic agents on the same 30 items. **Same-vendor judging produces a measurable leniency bias.** The v3 program paper (§"Reflexivity hazards") names this as the #1 hazard a reflexive evaluation must mitigate.

The bundle has the primitive (`provider_preferences: class: reasoning` resolves across vendor families). What was missing was an enforcement gate: a recipe could declare a same-vendor judge by accident, and nothing would catch it. This behavior makes the cross-vendor constraint architectural rather than discretionary.

## Recipe-level usage

```yaml
# In any evaluation recipe:
context:
  judge_cross_vendor_required: true     # opt-in to enforcement

# Then the judge step:
- id: judge-rubric-grading
  type: llm_judge
  provider_preferences:
    - { provider: openai,    model: "gpt-5*" }
    - { provider: anthropic, model: "claude-opus-4-7" }
    - { provider: google,    model: "gemini*" }
  enforce_cross_vendor: "{{judge_cross_vendor_required}}"
  sut_vendor: "{{sut_vendor}}"          # supplied by recipe context
```

When `enforce_cross_vendor: true` AND `sut_vendor: "anthropic"`, the resolver removes Anthropic providers from the preference list before resolving. If the resulting list is empty, the recipe halts.

## Hard rules

- **Never silently degrade.** If cross-vendor enforcement cannot be satisfied, the recipe MUST halt rather than fall back to a same-vendor judge. The whole point of the enforcement is that the alternative is the wrong answer.
- **Never use ensemble averaging to "wash out" the bias.** If three same-vendor judges are used, the average is still same-vendor-biased. This is a confound, not noise.
- **Always record the resolved judge identity.** The `judge_model` field in the run JSON must be specific (e.g., `gpt-5.5-2026-04-01`), not just the family. This is what enables Layer 2 cross-judge sensitivity replays.

## Integration with the orchestrated loop

The `orchestrated-loop.yaml` recipe uses this behavior in its `judge-satisfaction` step (Stage 3). The judge is selected from `{openai/gpt-5*, anthropic/claude-opus-4-7, google/gemini*}` with explicit `class: reasoning`; if the SUT bundle's primary model is in any of those families, the resolver excludes that family. A loop that runs against an Anthropic SUT therefore uses an OpenAI or Google judge; an OpenAI SUT uses an Anthropic or Google judge; etc.

This is the substrate-level reflexivity mitigation that the v3 paper §"Reflexivity hazards" calls for. With the behavior on, the loop's H3 evidence cannot be vacated by the F4 falsifier (cross-vendor replication failure) due to a cross-vendor judge being absent.

## Companion: layer-2 sensitivity reporting

When this behavior is on, a follow-on recipe stage (`layer-2-cross-judge-sensitivity`) can re-run the same judging on a stratified subsample with each available cross-vendor judge in turn, producing the per-(SUT-vendor × judge-vendor) cross-tabulation that the v3 paper's H2 hypothesis requires. This is the operational form of "vendor-family matrix off-diagonal cells" from the H2 disconfirmation criteria.
