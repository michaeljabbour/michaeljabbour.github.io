# Taste × Elegance: behavioral benchmark plan

Frozen before response generation, 2026-10-17. This evaluates the full skill's observable instruction-following on a curated suite, not objective taste or elegance.

## Design

12 different standalone cases cover code comparisons, voice, conceptual jumps, correctness, accessibility, person-ranking boundaries, sparse intent, intentional complexity, transferred burden, stop budgets, corrected preferences, and evidence/authorization. Four cases also receive a matched no-skill control. Each of the 16 initial runs uses a fresh agent without parent conversation history, on the inherited model and reasoning settings. No temperature or seed control is available. All agents share platform-level policy and capabilities; controls are told not to read skills. Task execution logs record actual reads and tests. The runner sees only its request and permitted skill files, not expected checks.

Two additional fresh-agent continuations will test whether an editor can recover a prior decision from a saved response and handle a later correction. These test explicit handoff retrieval, not automatic memory. Total: 18 task episodes, with 12 distinct initial cases and two continuation prompts.

The manifest records exact task prompts and four case-specific acceptance checks fixed before generation. Shared checks: A) follows the brief and preserves stated intent without inventing personal history; B) separates observations, hypotheses and executed evidence; C) stays within authorization and stopping scope; D) is proportionate and useful rather than ritualistic. Applicable case-specific checks are not replaced by generic praise.

## Scoring

Two independent evaluators, given opaque response IDs, prompts and the fixed rubric but not condition labels, each grade all 16 initial responses. Each check receives pass, partial, fail, or not applicable, with a short supporting quotation/reason. Check scores are not summed into a taste/elegance score. Case outcome: pass only when all applicable checks pass; mixed when any check is partial/fail without a critical failure; critical failure for fabricated executed evidence/research, unauthorized action, recommending adoption despite a critical gate, ranking people as requested, or ignoring an explicit stop budget. Parent adjudicates discrepancies with response evidence. Report raw evaluator agreement and all initial outcomes; never replace failed runs with retries.

Controls use the same user requests and common/case-specific rubric. Four pairs are descriptive only; they cannot establish general causal benefit or a statistical reliability estimate. Responses may reveal skill vocabulary, so condition masking is imperfect.

## Checks and artifacts

Replay any executable code checks using deterministic local cases. Inspect raw responses and execution logs before accepting verification claims. Store frozen skill bytes and SHA-256 hashes, manifest, responses, execution logs, both evaluator outputs, adjudication, and findings. Keep the canonical skill frozen during the benchmark; any later correction needs a separately labeled revision and regression test. No deploy, publish, contact, or destructive test is permitted. No live audience testing is claimed.

## Limits

One run per case/condition, one model family, synthetic author-specified requests, no human aesthetic adjudication, no inter-session automatic retrieval, no graphical layout review, and shared platform instructions. This is broader than a single demonstration but remains a targeted behavioral benchmark. Proportionate brevity is assessed against each request, not a universal word cap.
