# Right Shape rubric

The canonical scales, gates, checks, templates and voice for the right-shape skill. The skill says when to use each part. Edit the method here, never in a copy.

## Sorting questions

1. Where does the expertise live: nowhere (it just executes), in the caller's context, or sealed inside the component?
2. Who decides when it runs: the model, a person, an event, a clock, or the component itself?
3. How much of the loop does a person hold: operator, collaborator, consultant, approver, or observer?
4. Is it one worker, or a system of workers that shows up as one?

## Shapes

- Tool | Capability without judgment. A function the model can call.
- Smart Tool | Expertise sealed behind an interface: a library, a thin CLI and an optional MCP server, with straight code paths that run without a model.
- Skill | Expertise written down for the caller to read and apply in its own context.
- Agent | Judgment with its own loop and a persistent identity that is separate from any one surface.
- Outer harness | A system that composes agents, models, tools and verification into a capability no single agent delivers, usually behind an agent interface.
- Package | A plugin, bundle or module. Distribution, not a capability.

## Need dimensions

- N1 Path | One step | Known fixed steps | Branches you can list | Cannot be written in advance
- N2 Context load | Tiny | Fits the main window | Would crowd the main thread | Needs an isolated window, or several
- N3 Duration and presence | Instant, someone watching | Minutes, someone watching | Hours, nobody watching | Ongoing, no session at all
- N4 Initiative | Only when asked | On a schedule | On events | Decides for itself when to act

## Need to rung

| Need score | Rung |
| --- | --- |
| 0 to 1 | 1 |
| 2 to 3 | 2 |
| 4 to 5 | 3 |
| 6 to 7 | 5 |
| 8 to 9 | 7 |
| 10 to 12 | 8 |

Tiebreakers inside a band: it repeats and the expertise is stable, move toward a Smart Tool or a recipe; it needs the caller's situational judgment, move toward a skill; it would flood the main thread, move toward a subagent.

## Ladder

- 0 | Single call | Operator | One model call with tools
- 1 | Tool or Smart Tool | Operator | Expertise behind an interface
- 2 | Skill | Operator or collaborator | Expertise loaded into the caller
- 3 | Workflow or recipe | Operator or approver | A fixed path with checkpoints
- 4 | Subagent | Collaborator, through a parent | An isolated specialist that returns a summary
- 5 | Interactive agent | Collaborator | A person steers each turn
- 6 | Background agent | Approver | Works alone and returns a reviewable artifact
- 7 | Scheduled or event agent | Approver or consultant | Starts on a clock or a trigger
- 8 | Always-on sandboxed agent | Consultant or observer | Runs continuously inside hard limits
- 9 | Multi-agent swarm | Observer | Agents directing agents

## Gates

| Gate | Passes when | Fail caps at |
| --- | --- | --- |
| G1 Verifiability | The outcome can be checked cheaply and automatically: tests, screenshots, schemas, an evaluator | 5 |
| G2 Reversibility | Nothing irreversible happens without approval: no money moved, messages sent, data deleted or production changed | 6 |
| G3 Trifecta broken | At least one of private data, untrusted content and an outbound channel is absent | 5 |
| G4 Isolation | It runs where it can touch only what was mounted for it | 6 |
| G5 Budget | Hard caps on tokens, time and money exist, and model routing has been measured | 7 |
| G6 Ownership | A named person is accountable and watches the outcomes | 6 |

When a pass condition is unknown, say what evidence is missing and apply that gate's cap conservatively until it is established. Include that ID in the validator's `failed` list and explain its unknown status in the card. A portable instruction, sample benchmark or intended approval does not establish enforcement by an arbitrary host. A budget can limit loss without making an action reversible. Gate judgments and arithmetic are separate: validate both.

## Shape checks

- H1 Independent verification | The thing that checks the work should differ from the thing that does it
- H2 Specialists | The job needs several agents, models or verifiers with different strengths
- H3 Portability | More than one experience, team or upstream system will use it
- H4 Over size | One agent would exceed its size limit, or its job takes more than one sentence to state

## Engines

| Engine | Means | Benchmarked by |
| --- | --- | --- |
| LLM | Generative reasoning or writing is the product | Blinded judges, comparing against a baseline and a placebo |
| Decision model | A fast, narrow judgment (route, score, select, gate) made by a specialised model, or by a measured rule when the rule ties it | Agreement with labels, calibration, test-retest stability and regret |
| Both | A decision model decides and an LLM produces | Each part on its own terms, then end to end |
| None | Deterministic execution; no model is required | Contract/output checks, failure cases and fresh install; use comparisons only for an incremental-value claim |

## Replaceability

- R1 Contract | The edges are a stable interface (an agent, a function or a protocol), not shared internals
- R2 Swappable parts | The model, any inner agent and the verifier can each be replaced without a rebuild
- R3 Right size | Each piece has one coherent job and stays under its size limit
- R4 Identity apart from surface | Memory, credentials and standing instructions do not live inside one surface
- R5 Sunset test | Each piece of scaffolding names the model weakness it works around, and an eval would show when it has become dead weight

## Evaluation ladder

| Level | Shows | When |
| --- | --- | --- |
| L0 Conformance | It installs on a clean machine, its doctor passes, its contract tests pass | Every commit |
| L1 Behavior | It beats a baseline and a length-matched placebo on fictional fixtures with planted traps, preregistered and judged blind by a different model family | Every release |
| L2 Decision quality | For decision model and both: agreement with labels, calibration, test-retest stability, and regret against the best choice in hindsight | Every release |
| L3 Outcome | Real people doing real work | Reported as not measured until it is |
| Sunset | Each piece of scaffolding is ablated and removed when it no longer helps | Whenever the host model changes |

A good benchmark has at least one trap the capability should catch, one case it should leave alone, a stopping test, and a consistency test.

## Capability contract

```
<capability>/
  README.md              one-line promise, three install lines, what it will not do
  capability.json        schema version, stable id, public name, aliases, source pin,
                         kind, engine/components, surfaces, secret names and dataflow
  AGENTS.md  CHANGELOG.md  LICENSE  Makefile   (build, check, eval)
  skills/<name>/SKILL.md + references/       caller-applied methods only;
                                             one canonical entry and complete resources
  bundle.md  behaviors/  modes/  recipes/    host surface, for example Amplifier
  src/  smart-tool.json  SMART_TOOL.md       Smart Tools only
  contracts/             versioned interfaces others may depend on
  docs/BENCHMARK.md      preregistered tests
  evals/                 fixtures and protocol
  docs/evaluations/<date>/   frozen snapshots, transcripts, scores
  site/                  static guide
```

Rules: no private or unpublished required dependencies; install in three commands at most; secrets come only from environment variables; one coherent job per capability; status claims need a dated record; every piece passes R1 to R5.

Use one versioned `capability.json` as the canonical discovery and execution contract. Keep the stable promise id separate from the repository name, distribution, CLI/import/tool ids and host namespaces; preserve tested legacy aliases during a rename. A release version is recorded when established; otherwise require an exact source revision and payload digest rather than inventing a release. Existing `project.json` files may remain compatibility metadata, with an explicit canonical owner.

A Skill supplies the standard Agent Skills folder, whose name matches its frontmatter name and whose resources travel together. Deterministic tools expose their real versioned library/CLI/MCP interface; do not manufacture a skill wrapper merely to populate a catalog. Bundles, modules and plugins are optional distribution surfaces, not new promises. Shared install/preview/doctor/uninstall logic belongs in one replaceable tool, not a copy in every capability.

An installation preview states source pin, destinations, optional providers, permissions, secret names and dataflow. Installation uses owned receipts, refuses foreign or edited payloads, and supplies uninstall/rollback. Declared permissions and research instructions do not establish host enforcement. Verify discovery, complete-resource installation and behavioral use as separate stages on each claimed harness. Keep local market research ignored; check it at session start and refresh stale evidence or before positioning/naming work, with dated primary-source receipts and explicit unavailable sources.

## Dispositions

| Disposition | Use when |
| --- | --- |
| Keep | It already meets the contract, or nearly |
| Consolidate | Several repositories keep the same promise; merge them into one capability |
| Rename | The name says the mechanism, not the promise, or disagrees with its command |
| Restructure | The right promise in the wrong shape |
| Extract | One part of a repository is a capability on its own |
| Fold | It belongs inside platform code rather than standing as a capability |
| Platform | A runtime, client or host that capabilities run on |
| Park | Promising but overlapping or unfinished; harvest the useful parts |
| Separate | A product outside this portfolio |
| Archive | Retire after a verified replacement and migration, or an explicit owner decision about inactive work; preserve history, data, licenses and recovery |
| Fork | A confirmed upstream derivative; retain attribution and assess local divergence, contribution, dependency or learning purpose before any owner decision |

## Diagnosis

| Symptom | Likely cause | Move |
| --- | --- | --- |
| Everything scores as an agent | Need was scored from ambition, not from the job | Rescore N1 to N4 from the smallest version that would help |
| The rung keeps creeping up | Gates were treated as advice | Apply the lowest failed cap, then pick an honest move |
| Two capabilities claim one promise | Grouped by technology instead of promise | Regroup by the sentence each one promises |
| One repository needs two promises | It is two capabilities | Extract or split |
| A benchmark only praises | No planted trap and no leave-alone case | Add both before running it |
| The audit lists files, not decisions | Inventory without dispositions | Give every repository exactly one disposition |
| Claims about forks or privacy | Inferred and reported as fact | State how it was inferred, or ask |
| A decision model added to taste work | Engine chosen by fashion | Keep LLM when human judgment is the product |

## Card templates

### Placement card

```
VERDICT  <shape> at rung <n>, engine <engine>. <one sentence why>
NEED     N1 <a>  N2 <b>  N3 <c>  N4 <d>  = <score> -> rung <r>
CEILING  <c>  (failed: <gates or none>)
HONEST MOVE  <only when need exceeds the ceiling>
SHAPE    <single, or outer harness behind an agent or function interface>  (<checks>)
REPLACEABILITY  <R1 to R5: pass, or the gap in one line>
BENCHMARK
  L0 <conformance>
  L1 <fixtures, planted traps, leave-alone case, control, threshold>
  L2 <decision quality, when the engine is decision model or both>
  L3 not measured
QUESTION  <one, only if the answer would change the verdict>
```

### Audit report

1. At a glance: immutable source-census date/count, current-state changes separately, counts by primary disposition, distinct promises versus supporting assets, and the highest-leverage move. Counts describe reviewed records, not validated products.
2. Collection and depth: each listing/source and revision, exclusions, inaccessible items, shallow versus body-reviewed items, and contradictions. API listings, local checkouts, search, dependency links and supplied analysis have different coverage. Discover documented private/local foundations within actual authorization and keep their supplemental scope distinct from the public census; missing access is not absence of value. No exhaustive claim beyond shown evidence.
3. Each promise: stable ID, plain name, public entry or internal procedure, assumed/confirmed audience, trigger, current pain/cost or unknown, one-sentence offer, before/after, source design, target shape/engine/owner, differentiation hypothesis, risky assumption, next validation, confidence. Similar mechanism does not prove the same job; a bundle is distribution, not a promise.
4. Each research/evaluation claim: exact source/revision, authorship/upstream/license, method or theory, actual dated run if any, raw record, baseline/control, limits and next gate. Separate cited research, source-authored tests, AI exercises, outside-user outcomes and return. Keep negative, invalid and tied results visible.
5. Each product-usefulness assessment, when requested: Job, First value, Fit, Outcome, Trust and Return as separate judgments with evidence and a specific first-value blocker/removal and return-validation opportunity. Use the available usefulness rubric for its scales; otherwise report observations and unknowns without inventing ratings or zones. Source, builder and AI runs do not establish outside use. No average, total or promotion into a readiness zone. For internal mechanisms, experiments, research and learning assets, record asset value, audience, retained artifact and validation question instead of a failed-product grade.
6. Each code route: source repository/revision and exact existing file/directory; current role (method/tool/harness/adapter/eval/reference/research); existing or proposed target repository/path and owner; action from the dispositions; reason; versioned interface; consumers/dependencies; provenance and acceptance gate. A proposed path is labeled new. A shared contract does not imply a code merger. File links use the file route and directory links the directory route.
7. Full coverage: every source repository gets one primary disposition and source bucket, with as many component routes as its distinct parts need. Reconcile embedded skill bodies, host aliases, test fixtures, upstream copies, outputs and retained research; explain every unmapped remainder. Byte-identical copies and semantic variants are different counts.
8. Owner ledger: verified fork/visibility facts with timestamp/basis; uncertain local divergence or consumers; existing authorization and explicit naming/visibility decisions; proposals separately from applied actions and verification. No hidden/private inference from a broken link alone. An owner may retain a public fork or useful experiment without a product-readiness argument.
9. Staged implementation: exact source-to-target change, dependency order, independent install/no-key host path where applicable, compatibility/redirect plan, acceptance evidence, rollback and unresolved decisions. Name public display name, package/repository/command aliases separately; preserve working names unless a concrete mismatch justifies a change. Retire a predecessor only after the replacement works, supported consumers/data migrate and recovery/provenance are retained. Technical value and public visibility remain separate decisions.

### Audit machine record

For a large kept/shared Audit, write this structural companion beside the readable report. Fill existing paths from an independently retained source inventory. The optional validator checks coverage, recognized dispositions, numeric placements and explicit interfaces; it does not prove that a relocation, promise, license or gate judgment is sound. `kind` is `public`, `internal` or `asset`; only `public` requires a placement. Retained experiments can remain discoverable without becoming public AI capabilities.

```json
{
  "schema_version": "right-shape-audit/v1",
  "sources": [{"id": "<source>", "revision": "<revision>", "scope": "<public or supplemental>", "primary_disposition": "<rubric disposition>", "bucket": "<retained owner/home>"}],
  "capabilities": [{"id": "<promise or asset>", "kind": "<public, internal or asset>", "promise": "<plain user promise or asset value>", "shape": "<shape>", "placement": null}],
  "routes": [{"capability_id": "<id>", "source_id": "<source>", "source_revision": "<revision>", "source_paths": ["<existing path>"], "target_repo": "<owner>", "target_path": "<path>", "target_status": "<existing or proposed>", "action": "<rubric disposition>", "role": "<method, tool, harness, adapter, eval, reference or research>", "interface": "<inputs, outputs, failures and version>", "reason": "<evidence-bound reason>"}],
  "method_routes": [{"source_id": "<source>", "path": "<embedded method path>", "destination": "<explicit owner/bucket>", "provenance": "<original, upstream, host variant, fixture or unknown with basis>"}]
}
```

A public placement uses the validator's `need`, `failed`, `checks`, `engine` and optional claimed numeric fields, with reasons in the readable report. An internal/asset record uses `placement: null` when no AI placement is relevant. A source bucket preserves any unextracted remainder. An exact-path route does not establish that its proposed target is desirable; the owner/evidence review remains necessary.

### Check report

Verdict first, then gaps in order of leverage: what stops a stranger installing it, what stops anyone measuring it, and what will rot first. Removals before additions.

## Voice

- Not this: "Great idea! An autonomous agent could really transform this workflow."
- This: "It's a Smart Tool. The path is fixed and nobody needs to watch it."
- Not this: "There are several considerations to weigh across many dimensions."
- This: "It reads client email and can send mail. That's the trifecta. Rung 5 until one leg goes."
- Not this: "Your benchmark looks comprehensive."
- This: "Nothing in it can fail. Add a trap it should catch and a case it should leave alone."
