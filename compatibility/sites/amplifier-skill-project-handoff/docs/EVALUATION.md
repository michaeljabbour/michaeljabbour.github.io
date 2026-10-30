# Running the Project Handoff evaluation

This harness is optional development tooling. Using Project Handoff requires no model key, service or benchmark package. The harness uses Python's standard library.

## Recorded result — 2026-10-28

**No credible effectiveness conclusion is supported.** [study-1](evaluations/2026-10-28/study-1/REPORT.md) completed 60 fictional transfer trials and 180 provider calls. The frozen automated labels report correct resumption in 20/20 skill, 20/20 baseline and 17/20 placebo attempts. One placebo judgment failed strict literal-quotation validation and remains ungraded in the denominator; invalid grading is not evidence that the participant handoff failed.

The [secondary semantic quality review](evaluations/2026-10-28/study-1/STUDY-QUALITY-REVIEW.md) inspected 17 trials across all ten fixtures. It disputes both automatic critical-execution labels, finds unsupported missing-feature or approval claims in some passing skill outputs, and disputes a clean-case evidence penalty. These are provisional automatic rates, not validated reliability estimates. The reported skill-minus-baseline difference is zero. The +15-point placebo difference and descriptive [0, 30]-point interval use disputed labels and cannot support a benefit or safety claim. The sampled [0, 0] skill/baseline interval is not a population guarantee.

The nominal uncached token estimate for study-1 is USD 0.7910956, not an invoice. Only Capture-to-neutral-resumer transfer in a virtual text/file interface was tested. Actual host actions, direct Resume/Check effects, time saved, adoption and return use were not measured. [Pilot semantic review](evaluations/2026-10-28/pilot-3/SEMANTIC-SPOT-REVIEW.md) and the blocked instrument-development pilots remain retained; no raw response or label was silently repaired.

[Local validation](VALIDATION.md) and the [Right Shape application record](RIGHT-SHAPE-REVIEW.md) distinguish code/install checks from behavioral outcomes and from unreliable reviewer certification.

## Validate and run a new record

```sh
python3 evals/run.py --validate
python3 -m unittest discover -s tests -p 'test_evals.py'
python3 evals/run.py --offline-smoke --run-id plumbing-1
```

Offline smoke uses canned responses; it cannot establish behavior. It writes a dated record with behavioral metrics set to null.

Live requests read OPENAI_API_KEY and ANTHROPIC_API_KEY from the execution environment. Never put their values in files, arguments or logs. Choose explicit supported model snapshots from your account. The initial transport/model configuration was checked against official APIs; it does not silently choose newer versions.

```sh
python3 evals/run.py --pilot --model gpt-4.1-mini-2025-04-14 --judge claude-sonnet-4-6 --run-id pilot-3
python3 evals/run.py --run --model gpt-4.1-mini-2025-04-14 --judge claude-sonnet-4-6 --repeats 2 --budget-usd 5 --run-id study-1
```

Those are the recorded pilot/main commands. Their run IDs already exist and must not be reused for a fresh run. Choose a new explicit ID and freeze any changed protocol or source before another live call.

Read docs/BENCHMARK.md and commit the treatment/protocol first. Pilot observations are separate from main estimates. Any pilot-driven change requires another frozen run. A repeated --run-id refuses overwrite; --resume only continues exact matching source/configuration and keeps failed trials rather than retrying them. Change a budget or method only in a new run ID. Date defaults to America/New_York, and --date YYYY-MM-DD is explicit if needed.

Records live at docs/evaluations/<date>/<run-id>/. Start with REPORT.md and summary.json. Inspect manifest.json, snapshots/, trials/, blind-map.json and raw/ to audit what happened. A live report is still a curated fictional Capture-transfer study; direct Resume/Check method effects and human outcomes remain unmeasured. Read the failures, controls and limitations before quoting a rate.

Pilot-1 and pilot-2 are retained blocked instrumentation records. They are not valid behavioral comparisons and are not repaired by trimming or re-scoring their raw responses. The protocol documents each instrumentation revision and the explicit judge change before pilot-3. A successful pilot needs six valid judgments; the skill may still fail behavioral gates.

Transport references: [OpenAI Responses](https://developers.openai.com/api/reference/resources/responses/methods/create), [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [OpenAI pricing](https://developers.openai.com/api/docs/pricing), [Anthropic Messages](https://platform.claude.com/docs/en/api/messages/create), [Anthropic Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing). Price metadata in the runner is dated and nominal; refresh it explicitly for a later study rather than silently changing a frozen record.
