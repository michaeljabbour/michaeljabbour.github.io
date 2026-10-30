> Preserved source method from `amplifier-bundle-research` at `79b64cb33cb7ea123c8004733282bfcc29837f8d`. Original examples and runtime claims are historical; the canonical entry point defines current scope.

---
name: conducting-autonomous-experiments
description: "The method for running the full empirical lifecycle against a FROZEN measurement apparatus. Use during /execute when a locked pre-registration declares an experiment_loop."
---

# Conducting Autonomous Experiments

## Overview

The conducting-autonomous-experiments method is a disciplined descendant of the Karpathy
autoresearch program.md idea: an agent loop that proposes → runs → measures → keep/revert →
logs candidate interventions against a FROZEN apparatus, using git as the ledger.

This skill adds five layers on top of that foundation:

1. **Pre-registration hash-lock** — the apparatus is committed and hash-stamped before any
   intervention begins; any mutation of the apparatus invalidates the run.
2. **n > 1 variance** — every candidate is re-run at least N times (pre-registered); a
   keep decision requires the effect to clear the variance bar, not just beat the mean.
3. **Guardrail metrics** — secondary metrics with tolerances and a stopping rule prevent
   gaming the primary metric at the expense of other quality dimensions.
4. **Integrity audit** — `tool-experiment-audit` scans for HANDLER_ERROR cascades,
   implausible statistics, and missing manifests before any result is trusted.
5. **Held-out promotion gate** — exploratory findings graduate to confirmatory status only
   after a separate held-out re-run, statistical adjudication with BH correction, and a
   cross-vendor judge panel.

**Use when:** A locked pre-registration explicitly declares `experiment_loop: true` and there
is an executable measurement protocol (runnable script, benchmark, or evaluation harness).

**Don't use when:** There is no executable measurement — no script, no harness, no
reproducible evaluation. In that case use `/critique` and the methodologist agent instead.

---

## The Frozen Apparatus

Before the first intervention, four things MUST be frozen (committed + hash-stamped):

| Frozen element | What it contains | Key invariant |
|---|---|---|
| `intervention_surface` | Every file, directory, or config the loop is allowed to modify | Disjoint from `measurement_protocol` — no overlap permitted |
| `measurement_protocol` | The evaluation script(s), harness configuration, and data fixtures | Read-only throughout the experiment loop |
| `primary_metric` | Metric name, direction (↑/↓), and the keep/revert decision rule | Defined before any data is seen |
| `guardrail_metrics` | Secondary metrics with tolerances, stopping rule, seeds, and the held-out confirmation set | Defines the stopping condition and promotion threshold |

**Disjoint constraint:** `intervention_surface` and `measurement_protocol` MUST be disjoint
sets of paths. Any intervention that touches measurement code is invalid and must be
reverted automatically.

`freeze_gate.sh` in `scripts/experiment-loop/` enforces this at commit time. It computes a
SHA-256 hash of the frozen apparatus manifest, writes it to `.experiment/freeze.lock`, and
rejects commits that modify measurement_protocol paths.

---

## The Ledger Rules

The experiment ledger is the single source of truth for what was tried and what happened.

- **Append-only.** Use `ledger_append.sh` to add rows. No row is ever edited or deleted;
  amendments are new rows.
- **Ledger lives OUTSIDE `intervention_surface`.** It is part of the apparatus, not an
  intervention target. Placing it inside intervention_surface is a pre-registration
  violation.
- **Own commit, AFTER keep/revert.** Each ledger row gets its own git commit that follows
  the keep/revert commit. The commit order is: (1) intervention applied, (2) measurement
  run, (3) keep/revert applied, (4) ledger row appended and committed.
- **Broken interventions are data.** If a run errors, crashes, or produces a HANDLER_ERROR
  cascade, the error is logged as a row with `outcome: error` — it is not silently retried
  without logging.
- **Every row is exploratory by default.** The `status` field defaults to `exploratory`.
  The promotion gate APPENDS a `confirmation:` field to a row; it does not replace the
  existing status.

---

## The Promotion Gate

Exploratory findings do not become confirmatory automatically. Six steps are required:

1. **Select candidate.** From the exploratory ledger, identify at least one intervention
   that cleared the primary metric keep rule AND did not trip any guardrail tolerance.

2. **Confirmatory re-run on held-out set.** Re-run the kept intervention on the held-out
   confirmation set defined in `guardrail_metrics`. This set was never seen during the
   exploratory loop.

3. **Statistical adjudication with BH correction.** Run `tool-experiment-power` to compute
   the test statistic and apply Benjamini-Hochberg FDR correction across all candidates
   being promoted simultaneously. Any candidate that does not clear the corrected threshold
   is returned to exploratory status.

4. **Cross-vendor judge panel.** Invoke the multi-LLM judge panel (see below) on the
   surviving candidates. The panel's verdict is one input to the promotion decision.

5. **Verdict: exploratory → confirmatory.** For candidates that clear steps 3 and 4, run
   `promote.sh` which appends `confirmation: {date, held_out_score, adj_p_value,
   judge_kappa}` to the ledger row.

6. **Honest pivot.** If no candidate survives the promotion gate, the `honest-pivot`
   behavior fires. The run is documented as a negative result — a valid scientific output,
   not a failure to report.

---

## The Four Anti-Patterns

Avoid these failure modes that invalidate an experiment loop's evidential value:

| Anti-pattern | Flaw | Discipline |
|---|---|---|
| **n=1 decisions** | A single measurement does not distinguish a real effect from noise; keep/revert on n=1 is coin-flipping dressed as science | Pre-register minimum n before any run; keep rule must reference the aggregated statistic, not a single observation |
| **greedy multiple-comparisons** | Running many interventions and reporting only the best inflates the false-discovery rate; the "best" result is likely noise | Apply BH correction at the promotion gate across all candidates; pre-register the candidate space before the loop begins |
| **no-hypothesis tweaking** | Modifying the intervention_surface after seeing partial results without updating the pre-registration hash invalidates the freeze lock | Treat any mid-loop modification of the pre-registered apparatus as a new experiment; re-freeze and restart the loop |
| **metric monoculture** | Optimizing only the primary metric while ignoring quality, latency, cost, or safety guardrails produces fragile improvements that break in deployment | Pre-register guardrail_metrics with explicit tolerances; any guardrail breach is an automatic revert regardless of primary metric gain |

---

## Cross-Vendor Multi-LLM Judge Panel

The judge panel is invoked at step 4 of the promotion gate. Three reference files govern
its configuration and rubric:

- `behaviors/cross-vendor-judge.md` — enforces that the judge model must be from a
  different vendor family than the system-under-test; prevents same-vendor leniency bias.
- `context/orchestrated-loop-judge-rubric.md` — the rubric the judge uses to score
  candidates across five dimensions (closure_evidence, severity_weighted_closure,
  ratio_to_no_op, knowledge_tracking_alignment, residual_freshness).
- `agents/ml-paper-reviewer.md` — used when the candidate intervention is an ML modeling
  choice; applies the NeurIPS-style review rubric with ensemble + meta-reviewer aggregation
  and the mandatory calibration warning about LLM-judge score inflation.

**Agreement threshold:** Compute Cohen's kappa across the judge panel. If `kappa <
kappa_threshold` (default 0.60), the panel is deadlocked — return to the user with the
disagreement breakdown before proceeding. Do not force a majority vote over a deadlocked
panel.

---

## Provenance and Attribution

The propose → run → measure → keep/revert loop is a pattern-level transfer of ideas from
the Karpathy autoresearch `program.md` (MIT License). The transfer is at the
**idea level only**: the loop structure, the git-as-ledger concept, and the autonomous
iteration philosophy. No GPU code, PyTorch operations, CUDA kernels, or autoresearch
implementation code has been imported or adapted.

The five additions (pre-registration hash-lock, n > 1 variance, guardrail metrics, integrity
audit, held-out promotion gate) and the cross-vendor judge panel integration are original
contributions of this bundle.

**License:** MIT (this bundle), consistent with the Karpathy autoresearch MIT license.
