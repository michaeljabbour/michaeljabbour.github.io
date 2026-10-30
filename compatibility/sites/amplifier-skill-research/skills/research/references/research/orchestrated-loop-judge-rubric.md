# Orchestrated-Loop Judge Rubric

This is the rubric the `judge-satisfaction` step in `recipes/orchestrated-loop.yaml` uses to decide whether a given round's results satisfy the loop's convergence criteria. Loaded by reference (`@research:context/orchestrated-loop-judge-rubric.md`) at recipe execution time.

The judge is selected by `provider_preferences: class: reasoning` with a cross-vendor requirement enforced via `behaviors/cross-vendor-judge.md` — the judge MUST be from a different vendor family than the SUT.

## What this judge decides

A single satisfaction score in [0.0, 1.0], plus a structured rationale. The score is compared to the loop's `closure_target` (default 0.50) by the recipe engine's `satisfaction_threshold` mechanism.

The judge does NOT decide:
- Whether individual residuals are closed (that's `recipes/residual-adjudicator.yaml`'s job, in a separate blinded sub-session).
- Whether the no-op arm's residuals closed (same — that's the adjudicator's job).
- Whether the loop should continue or stop (that's the recipe engine's `while_condition` based on the satisfaction score AND the closure-rate-vs-no-op gate).

## Score dimensions (5 axes, each 0-1, weighted average)

```
satisfaction = 0.30 * closure_evidence
             + 0.20 * severity_weighted_closure
             + 0.20 * ratio_to_no_op
             + 0.15 * knowledge_tracking_alignment
             + 0.15 * residual_freshness
```

| Dimension | What to look at | Score 1.0 means | Score 0.0 means |
|---|---|---|---|
| **closure_evidence** | newly_closed list from this round's adjudicator output | At least 30% of round-start open_residuals are now closed with quoted evidence | Zero new closures, or closures without concrete evidence quotes |
| **severity_weighted_closure** | sum(w_severity * count) where w₁=1, w₂=2, w₃=4 | Severity-weighted closure rate ≥ 2× the count-based rate (i.e., load-bearing residuals dominated) | Severity-weighted ≤ count-based (i.e., only cosmetic residuals closed) |
| **ratio_to_no_op** | Loop arm's per-round closure ÷ no-op arm's per-round closure | Ratio ≥ 2.0 (the v3 paper's H3 first-conjunct pass criterion) | Ratio ≤ 1.0 (loop is no better than drift) |
| **knowledge_tracking_alignment** | Specialist accuracy on date-stamped questions vs corpus update timing | Accuracy on post-update questions rises this round AND was not present pre-update | Accuracy uncorrelated with corpus update timing, or constant-correct (= pre-training contamination) |
| **residual_freshness** | Whether the loop is finding NEW residuals AND closing OLD ones (the ratchet) | Both new findings AND closures present; no oscillation | Either zero new findings (loop has stopped exploring) OR oscillation (residuals reopen as fast as they close) |

## Hard fail conditions (override the weighted score)

If ANY of these is observed, set `satisfaction = 0.0` regardless of the dimensional scores:

1. **Pre-registration hash mismatch.** The parent loop's `state.preregistration_hash` does not match the recomputed hash of the residual-schema + closure-rule + no-op-arm-spec + adjudication-contract. This is recipe-level deviation — `honest-pivot` must fire.
2. **Adjudicator-proposer collusion detected.** Adjudicator's residual_ids match proposer's residual_ids 1:1 with identical timing (suggests blinding failed). Flag and escalate.
3. **Same-vendor judge accidentally selected.** If the resolved judge model is in the same vendor family as the SUT (reflexivity-hazard #1 violation), abort the judging step and re-resolve with the cross-vendor constraint enforced.

## Output format

```yaml
judge_satisfaction:
  satisfaction: 0.62                        # weighted score in [0,1]
  threshold_pass: true                      # satisfaction >= closure_target
  rationale:
    closure_evidence:
      score: 0.7
      quote: "5 of 12 open residuals closed with concrete evidence"
    severity_weighted_closure:
      score: 0.4
      quote: "Severity-weighted closure 0.36, count-based 0.42 — cosmetic
              residuals dominated"
    ratio_to_no_op:
      score: 0.8
      quote: "Loop arm 0.42, no-op arm 0.20, ratio 2.1"
    knowledge_tracking_alignment:
      score: 0.5
      quote: "Round 3 accuracy on June-update questions rose; pre-update
              questions stable"
    residual_freshness:
      score: 0.6
      quote: "3 new residuals named, 5 old closed, no oscillation detected"
  hard_fails: []                            # populated if any hard-fail triggered
  cross_vendor_judge_resolved:
    sut_vendor: anthropic
    judge_vendor: openai
    judge_model: gpt-5.5-2026-04-01
    constraint_satisfied: true
```

## What the parent loop does with this output

The parent `orchestrated-loop.yaml` Stage 3 step `update-loop-state` reads the satisfaction score and, combined with the residual-adjudicator's closure counts and the no-op arm's metrics, computes:

```
converged = (satisfaction >= closure_target) AND
            (severity_weighted_closure_rate >= 2 * no_op_closure_rate)
```

The loop exits when `converged == true` OR `rounds_remaining <= 0`. The synthesis stage then computes the H3 verdict.

## Notes on calibration

This judge inherits the same calibration warning that applies to all LLM-as-judge usage in the bundle: see `behaviors/cross-vendor-judge.md` for the cross-vendor requirement and `agents/ml-paper-reviewer.md` for the explicit warning about LLM-judge inflation. The cross-vendor selection mitigates same-vendor leniency; it does not eliminate the general LLM-judge-vs-human-judge gap. The v3 paper's F1 falsifier (human-DBA κ-tracking) is the load-bearing replication for THIS judge stack as well as for PSE's primary judge stack.
