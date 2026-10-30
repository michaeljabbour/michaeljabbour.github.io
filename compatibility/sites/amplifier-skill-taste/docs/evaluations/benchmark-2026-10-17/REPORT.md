# Taste × Elegance: larger behavioral benchmark

**Result: 14 of 16 distinct skill cases fully passed the process rubric; two were partial. Both fresh-agent handoff tests passed. No critical failures were observed in any of the 24 task episodes.**

The clearest weakness was small but repeated: the short writing and poster refinements proposed a comparison without stating what would make the agent keep or revert the change. These were useful answers with incomplete experiment closure, not unsafe or unusable work.

This assesses whether this version of the skill delivers its promised behavior on a curated suite. It does not establish objective aesthetic quality, real audience benefit, or a general reliability rate.

## What ran

| Phase | Task episodes | Full pass | Partial / mixed | Critical failure |
|---|---:|---:|---:|---:|
| Initially frozen skill cases | 12 | 10 | 2 | 0 |
| Initially frozen matched controls | 4 | 0 | 4 | 0 |
| Fresh-agent handoff continuations | 2 | 2 | 0 | 0 |
| Separately frozen stress cases | 4 | 4 | 0 | 0 |
| Stress matched controls | 2 | 1 | 1 | 0 |

There were **24 fresh task-agent runs**, plus four fresh grading-agent passes and one independent methodology review. Task agents started without the parent conversation history. All used inherited model/reasoning settings; the exact backend model identifier, seed and temperature were not instrumented. Shared platform instructions and tools remained available. Read/write boundaries were instructions, not per-agent OS isolation.

The initial suite and case-specific checks were recorded before generation in [PLAN.md](PLAN.md) and [manifest.json](manifest.json). Four additional stress cases and two controls were frozen separately after the initial results and methodology review, in [STRESS-PLAN.md](STRESS-PLAN.md). They are exploratory follow-up evidence and do not replace the original results. Exact handoff prompts were frozen after extracting the actual C01 decision note; both use that same source and are dependent variations, not independent replications.

The skill and calibration bytes were frozen in [snapshot](snapshot/SKILL.snapshot.md), with [SHA-256 hashes](snapshot/hashes.json). The canonical files matched those hashes when this report was written. (Note added 2026-10-18: the snapshot file was renamed from `SKILL.md` to `SKILL.snapshot.md`, so that the repository holds only one skill of that name; its bytes are unchanged and the `SKILL.md` key in `hashes.json` refers to it. Skill version 0.2.0 changes the frontmatter and adds three sentences, so these results apply to the snapshot.) No skill corrections were made during this evaluation.

## What the skill demonstrated

- **Judgment with human character:** preserved deliberately distinctive wording and purposeful poster density; updated a preference when the user corrected the earlier inference.
- **Independent axes:** separated contextual fit from implementation burden. The archive example recognized the voice lost by standardizing prose while separately crediting lower maintenance.
- **Choosing the right scale:** reframed a repair event around participation after slide polishing stalled; used small local edits when the core idea already fit.
- **Gates before adoption:** blocked the faulty receipt selector and withheld rollout for color-only wayfinding. It separated supplied observations from unknown accessibility and audience results.
- **A bounded experiment:** stopped when the two-round budget was exhausted, proposed useful checks, and avoided treating 5/5 as a target.
- **Actual keep-or-rollback behavior:** ran the memorial-name checks, found the cleanup reordered names and erased intended repetitions, restored the baseline, and reran the checks successfully.
- **Explicit handoff continuity:** a fresh editor preserved the earlier reason and stopped; a second fresh editor honored a new correction instead of treating the note as immutable. These test a note supplied to an agent, not automatic retrieval or persistent memory.

## Case-level evidence

Each case had four common checks (brief/intent, evidence honesty, scope/budget, proportional usefulness) and four case-specific checks. Pass requires every applicable check to pass. Partial/mixed means at least one incomplete check without a critical failure. These labels are process-compliance judgments, not taste/elegance scores.

| Case | Phase | Outcome | Evidence |
|---|---|---|---|
| C02 · Voice-preserving writing | Initial | Mixed | S4: Names the orderly-rhythm tradeoff and read-aloud comparison, but gives no stop or revert condition. [Response](runs/C02-skill/response.md) |
| C01 · Code spectrum | Initial | Pass | All eight checks passed. [Response](runs/C01-skill/response.md) |
| C05 · Accessibility unknown | Initial | Pass | All eight checks passed. [Response](runs/C05-skill/response.md) |
| C07 · Sparse intent | Initial | Pass | All eight checks passed. [Response](runs/C07-skill/response.md) |
| C11 · Corrected decision note | Initial | Pass | All eight checks passed. [Response](runs/C11-skill/response.md) |
| C08 · Intentional complexity | Initial | Mixed | S4: Includes a viewing-size comparison and regression risks, but no explicit rollback or conditional reversal. [Response](runs/C08-skill/response.md) |
| C12 · Evidence and authorization | Initial | Pass | All eight checks passed. [Response](runs/C12-skill/response.md) |
| C09 · Hidden transferred burden | Initial | Pass | All eight checks passed. [Response](runs/C09-skill/response.md) |
| C03 · Conceptual bottleneck | Initial | Pass | All eight checks passed. [Response](runs/C03-skill/response.md) |
| C06 · Person ranking and false total | Initial | Pass | All eight checks passed. [Response](runs/C06-skill/response.md) |
| C10 · Stop and budget | Initial | Pass | All eight checks passed. [Response](runs/C10-skill/response.md) |
| C04 · Failed correctness gate | Initial | Pass | All eight checks passed. [Response](runs/C04-skill/response.md) |
| X04 · Purposeful friction | Stress extension | Pass | All eight checks passed. [Response](runs/X04-skill/response.md) |
| X02 · Authorized actual rollback | Stress extension | Pass | All eight checks passed. [Response](runs/X02-skill/response.md) |
| X03 · Independent axes and real tradeoff | Stress extension | Pass | All eight checks passed. [Response](runs/X03-skill/response.md) |
| X01 · Intent versus audience evidence | Stress extension | Pass | All eight checks passed. [Response](runs/X01-skill/response.md) |

Handoffs: [H01 preserved the note and stopped](runs/H01/response.md); [H02 applied the librarian's correction](runs/H02/response.md). Both passed all eight checks.

## What remains weak

**C02, voice-preserving writing:** the agent kept the unusual phrase, made one local change, stayed below 180 words, and suggested reading the versions aloud. It ended with “does your aunt's unruly warmth still come through?” but did not say what to do if the answer was no. Both reviewers marked this partial. A short closure such as “If the warmth fades, restore the original sentence” would complete the loop without adding ceremony.

**C08, intentional poster density:** the agent protected every family name, proposed one information strip, named the risk, and suggested a viewing-size comparison. It did not explicitly state whether to keep, revise, or undo the strip if the comparison failed. Both reviewers marked this partial.

**Recommended next skill revision:** make a concise keep/revert condition more salient for short refinements. The current skill already contains rollback guidance; the evidence supports improving its application under brevity, not adding an elaborate new workflow. This is a recommendation only; a revision should receive separately labeled regression runs on C02/C08 plus held-out short cases.

**Additional usability observation, not a scored failure:** X03 put taste vertically and elegance horizontally, consistently labeled. The axes remained independent and the request did not prescribe orientation, so it passed the frozen rubric. The site uses taste rightward and elegance upward. Explicitly fixing that convention in the skill would make generated maps more consistent if that is part of the product promise.

## What the controls show—and do not show

| Matched case | With skill | Without skill | Raw responses |
|---|---|---|---|
| C01 · Code spectrum | Pass | Mixed | [Skill](runs/C01-skill/response.md) · [Control](runs/C01-control/response.md) |
| C02 · Voice-preserving writing | Mixed | Mixed | [Skill](runs/C02-skill/response.md) · [Control](runs/C02-control/response.md) |
| C03 · Conceptual bottleneck | Pass | Mixed | [Skill](runs/C03-skill/response.md) · [Control](runs/C03-control/response.md) |
| C09 · Hidden transferred burden | Pass | Mixed | [Skill](runs/C09-skill/response.md) · [Control](runs/C09-control/response.md) |
| X01 · Intent versus audience evidence | Pass | Mixed | [Skill](runs/X01-skill/response.md) · [Control](runs/X01-control/response.md) |
| X04 · Purposeful friction | Pass | Pass | [Skill](runs/X04-skill/response.md) · [Control](runs/X04-control/response.md) |

On these prompts, the skill more often supplied its promised matrix structure, uncertainty, risks, explicit experiment closure, and decision context. The controls often produced useful substantive answers: both code runs preserved the intended output; both repair-event runs shifted toward practical participation; both signup-flow runs retained recovery. X04's control also fully passed after adjudication.

This is not proof that the skill produces better work overall. The rubric intentionally includes skill-specific process obligations that the user did not always explicitly request, which can favor the skill over a concise, useful control. There were only six pairs; two were selected after initial results. Length is a real cost: for the four initial matched pairs, the skill responses were 1,091/96/282/165 whitespace-delimited words versus 649/71/136/113 in the controls. Most of the requested code-comparison structure accounts for the longest case. No human preference study was run.

## Independent grading and adjudication

Two fresh reviewers independently graded each phase using opaque response IDs and the frozen rubrics; condition labels were withheld. Response wording can reveal skill use, so masking was imperfect. The reviewers share the same inherited model environment, and agreement is not human validation.

| Group | Identical check ratings | Identical case verdicts |
|---|---:|---:|
| Initial 16 task episodes | 125 / 128 | 16 / 16 |
| Two handoffs | 16 / 16 | 2 / 2 |
| Six stress episodes | 47 / 48 | 5 / 6 |

The parent adjudicated four check disagreements against the raw responses. Three initial differences did not change case outcomes. The stress disagreement concerned whether X04-control supplied a meaningful keep/adopt condition without saying “revert.” It retained typed SEND until safeguards worked, identified accidental-activation risks, and specified harmless-draft checks; the parent accepted that semantic equivalent and marked it pass. No skill-run verdict changed through adjudication. All raw reviewer outputs and reasons remain in [judgments](judgments/adjudicated-initial.json) and [stress adjudication](judgments/adjudicated-stress.json).

Execution logs are agent-reported evidence, not complete independent tool traces. Parent replay strengthens the executable claims below; other claimed actions are bounded by the archived logs and responses.

## Independently replayed checks

[replay_checks.py](replay_checks.py) passes locally and writes [mechanical-checks.json](mechanical-checks.json):

- Original/final formatters in both C01 conditions match the exact output contract on 36 input combinations each, including Unicode, whitespace and braces.
- The skill run's saved intermediate also matches on all 36 combinations.
- The C04 proposed receipt selector passes four isolated selection cases; no deletion was executed.
- H02 applies the new phrase while preserving all supplied values on 36 combinations.
- X02's archived original proposal fails the order/repetition checks in an isolated replay; its restored implementation passes. Protected baseline and check fixtures are byte-identical, and restored working.py equals baseline.py.

These checks establish only the behavior tested. They do not validate the matrix coordinates, voice, comprehension or maintainability. Run with `python3 docs/evaluations/benchmark-2026-10-17/replay_checks.py` from the repository root. The script executes archived, inspected local Python function definitions; review them before running modified benchmark artifacts.

## Coverage and limits

The suite covers the main instruction families, but it is not an exhaustive evaluation of the full experience. The independent [methodology review](judgments/method-review.md) identifies material limits:

- Many initial cases explicitly cue the correct boundary and resemble calibration examples. The stress extension broadens coverage but remains hand-authored and single-run.
- There are no repeated trials per condition, other models/harnesses, human aesthetic judges, or real audience outcomes.
- User elicitation is tested as one reply, not a sustained interview; there is no live audience-feedback loop or automatic decision-note retrieval.
- One harmless local rollback was exercised. Live deployment, real sending, destructive operations, and actual authorization transitions were not tested.
- Case checks bundle subrequirements; conjunctive pass rates depend on that grouping. Raw evidence and partials matter more than treating the counts as a calibrated quality score.
- C02's prompt quotes the phrase with a lowercase first letter while its draft capitalizes it. Both evaluators accepted preservation of the draft's capitalization; no literal case-sensitive penalty was applied.

The defensible conclusion is that the frozen skill usually delivered its specified process on this broader curated suite, with a repeated weakness in explicitly closing short experiments. Broader robustness and audience benefit remain unestablished.

## Artifact index

- [Initial plan](PLAN.md), [initial manifest](manifest.json), [handoff prompts](continuations.json)
- [Exploratory stress plan](STRESS-PLAN.md), [stress manifest](stress-manifest.json)
- [Machine-readable results](results.json), [response inventory and hashes](response-inventory.json), [environment](environment.json)
- [Initial grader A](judgments/judge-a.json), [initial grader B](judgments/judge-b.json), [stress grader A](judgments/stress-judge-a.json), [stress grader B](judgments/stress-judge-b.json)
- [Initial adjudication](judgments/adjudicated-initial.json), [stress adjudication](judgments/adjudicated-stress.json), [method review](judgments/method-review.md)
- [Mechanical replay results](mechanical-checks.json), [replay script](replay_checks.py)

All 24 exact task wrappers, full responses, execution logs, and any generated Python fixtures are retained under runs/. Masked grader packets and keys are also retained. Historical execution logs include the temporary paths actually used. No public site was published or external recipient contacted.
