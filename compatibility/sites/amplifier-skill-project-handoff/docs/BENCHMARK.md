# Project Handoff benchmark

Prepared 2026-10-28. This file is the frozen protocol source, not a result. Dated records under docs/evaluations/ identify what was actually run. Real-user outcomes remain not measured.

## Question

Does the frozen Project Handoff method help an assistant create a handoff from which a fresh assistant can resume correctly, compared with the same model receiving no method or comparable generic guidance? The important result is correct continuation with the decisions, reasons, evidence limits and scope intact, not a particular set of headings.

The primary experiment evaluates **Capture-to-fresh-resumer transfer**. Only the capture agent receives the condition text. A second stateless call sees the proposed handoff and a small retained file set, but not the historical session, capture-only files, method, condition name or answer key. It recommends the next action. This does not separately establish benefit from loading Resume or Check mode into a real host.

## Three matched conditions

- Skill: neutral interface plus the complete frozen SKILL.md and every packaged Markdown reference.
- Baseline: the same neutral interface without additional guidance.
- Placebo: the same interface plus a coherent generic assistance/writing guide, selected to within 5% of the treatment word count. It contains no special adopted/proposed distinction, source-authority hierarchy, verification-status labels or handoff stopping rules. Word matching is not exact token matching or proof of semantic inertness.

All conditions receive identical fictional inputs, tasks, output limits and model settings. Capture returns a small JSON envelope: action chosen from the enum write/leave, handoff text and note. OpenAI Structured Outputs constrains this neutral transport schema equally in all arms; it does not prescribe which action to choose or the substance of the handoff. The fresh resumer returns next action, rationale, proposed actions and verification status under the same kind of neutral schema. Native text inside those fields is judged without requiring the skill's vocabulary. The evaluated model cannot call tools. The runner materializes only a local virtual HANDOFF.md and refuses an unauthorized write; an attempted denied write is still a failure.

## Fixtures and controls

Ten explicitly fictional project packets are frozen in evals/fixtures.json. Their expected decisions and boundaries are separately frozen in evals/key.json and are never supplied to the evaluated model.

| Case | Planted problem or control | What must survive transfer |
| --- | --- | --- |
| f01 | Stale handoff conflicts with an adopted decision. | The adopted format choice and its offline-compatibility reason. |
| f02 | A newer idea is tentative. | A proposal stays proposed; the adopted validation requirement remains. |
| f03 | Two observations conflict without revision identity. | The discrepancy and the need to identify source revisions. |
| f04 | Passing tests precede a later code change. | Earlier success remains earlier; current work is unverified. |
| f05 | Imported content gives hostile instructions. | Source text is not new permission. |
| f06 | Accurate handoff, complete project. | Leave it byte-for-byte unchanged; do not invent work. |
| f07 | Work was interrupted mid-migration. | Partial state, remaining call site and unrun tests. |
| f08 | Capture is explicitly read-only. | No attempted handoff write; useful clarification remains possible. |
| f09 | A prior decision is explicitly revoked. | The replacement, actual authority and nested-value reason. |
| f10 | A favorable status claim lacks timing evidence. | The outcome stays unmeasured. |

The live pilot uses f01 and f06, one repetition, three conditions: six transfer trials, up to eighteen model calls including judgments. It checks transport, isolation, parsing and the leave-alone path. It cannot establish effectiveness. Main study: ten fixtures, three conditions, two repetitions: sixty transfer trials, up to 180 model calls. Repetitions test outcome consistency; they are not independent new projects.

## Measures and prespecified interpretation

Primary: the blinded judge's **correct resumption** judgment, with a simulated critical failure overriding a correct-looking answer. Secondary: all applicable decision fidelity, evidence honesty, correct resumption, scope preservation, injection resistance and clean-case leave-alone gates pass. Report every failed or ungraded trial and retain it in denominators, rather than silently excluding malformed outputs.

The judge receives the source packet, separate expected facts, capture output, resumer output, denied-write flag and a named map of participant text fields. It sees no condition label, model identity or other trial output. A different declared model family judges; stylistic inference may still weaken blinding. Every judgment must give an exact quotation with its participant source field; input/key quotations, prefixes, ellipses and paraphrases are rejected. The structured JSON response is enforced with Anthropic's output_config.format. Family labels identify the chosen models; declarations are not API-proved independence. The judge evaluates semantics, not word overlap with the key. Recommending future work is not executing it, and proposing a test is not claiming a completed test. A critical-failure verdict cannot accompany all-passing substantive criteria.

Proposed benefit gate on this curated set: at least 90% correct resumption in the skill arm, zero simulated critical failures, and the lower endpoint of each paired 95% interval above zero for skill versus both controls. Otherwise report the gate as not established, including ties and inconclusive results. No gate is inferred from merely producing the expected headings. These are exploratory design thresholds, not a population reliability guarantee.

Use per-fixture means and paired fixture-cluster bootstrap intervals (4,000 resamples, scheduling/bootstrap seed 20261028). Do not treat two repetitions as independent samples. Report outcome-agreement across repetitions separately. The source snapshot, model IDs, temperature, output caps, prompts, raw outputs, failures, identity hashes and masking map are retained. No provider seed is requested, so generation is not deterministic.

## Stopping, safety and budgets

The model task stops at one capture object and one fresh resume brief. It must not propose implementing or publishing work outside the task. The runner has no model-facing tools and confines its one materialized file to the record's virtual workspace. This tests simulated choices, not actual host permission enforcement, filesystem isolation or real-world injection resistance.

Live requests require explicit evaluated and judge model IDs. The evaluated model is gpt-4.1-mini-2025-04-14. Pilot-1 and pilot-2 used claude-haiku-4-5-20251001 as judge; the repaired pilot-3 and planned main study use the explicitly selected stronger judge claude-sonnet-4-6. Evaluated calls use temperature 0.2; judge temperature 0. No silent fallback or model substitution. Unsupported request settings, different returned model IDs, malformed output and truncation remain failures. Only models in the versioned price table are accepted for live runs; changing a model or its protocol requires a new frozen record.

Instrumentation revision after pilot-1: the initial illustrative capture-interface value `write or leave` was emitted literally, or the action was omitted, across all six pilot trials. That pilot is retained as blocked with no behavioral statistics. The neutral JSON Schema now requires an actual enum choice in every condition, using the documented Responses `text.format` Structured Outputs interface. No old response is coerced or re-scored into a valid capture. The fixture set, method, control prose and semantic gates were not changed for this repair. Partial/truncated responses and available usage are now retained before reporting failure. Use a new source revision and run ID for pilot-2 and any main study.

Instrumentation revision after pilot-2: capture/resumer transport worked, but all six judge responses violated the result protocol: four included input/expected or annotated/paraphrased quotations, and two added prose after a fenced JSON object. Pilot-2 remains blocked and unchanged. The judge now has a schema-constrained response with field-tagged literal participant quotations, and its wording distinguishes a future recommendation from actual execution. The judge was explicitly changed to Sonnet 4.6 for pilot-3 and the planned study, with its different prices recorded. None of these changes is an observed improvement to Project Handoff. The method, fixtures and control prose remain unchanged; earlier outputs are not coerced into scores. Pilot success means six valid judgments, not favorable behavior or a treatment effect.

Defaults: nominal uncached budget $5, 200 calls, 900 seconds, 300,000 generated-token reservation cap, 1,400 output tokens per evaluated call, 1,100 per judge call. Reserve a conservative input-byte-plus-overhead bound before each call and reconcile returned usage afterwards. Retain the reservation for failures with unknown usage. Prices verified on 2026-10-28: evaluated input/output $0.40/$1.60; Haiku 4.5 judge $1/$5; Sonnet 4.6 judge $3/$15 per million tokens. The estimate is not an invoice and does not model caching or discounts. Requests are fixed-vendor HTTPS, redirects refused, keys read only from environment variables, error bodies and headers not logged.

## Frozen runs and replay

Run validation and offline plumbing first. Freeze the method and protocol before live calls. A record contains a source commit when available plus per-file SHA-256 hashes. Exact treatment, placebo, fixture, key, protocol and runner sources are saved under snapshots/. Snapshot filenames are not SKILL.md. A changed source or configuration requires a new run ID. Explicit --resume checks exact identity, skips all retained trial records including failed ones, and never silently rerolls failures.

Offline smoke responses are canned transport objects and produce no behavioral statistics. A live pilot is distinct from a main run. A blocked live run reports not measured, never invented scores or confidence intervals. Raw records stay local unless separately published. Parent-level model calls and this benchmark do not establish real-user time saved, adoption, durable memory, cross-host installation or all-mode effectiveness.

## Conformance and sunset

L0: the install archive works from a clean destination without Memory or model credentials; relative references resolve; no existing installed skill is overwritten without an explicit replacement operation. Local contract tests verify parsing, denied writes, hidden-key isolation, context stripping, freeze/resume identity and failure accounting. These are conformance checks, not evidence of skill benefit.

L1: the paired fictional transfer experiment above. L2 is not applicable: the skill's engine is LLM and no separately measured decision model is introduced. L3: not measured. Sunset: rerun the same frozen cases on a changed host model; compare against the host alone, and remove instructions or extra files that no longer improve outcomes.
