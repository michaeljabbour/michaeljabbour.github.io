# Right Shape

[Open the guide and get the skill](https://michaeljabbour.github.io/amplifier-skill-right-shape/). [Watch the 86-second film](https://michaeljabbour.github.io/amplifier-skill-right-shape/#film) (captioned, with a transcript and a 15-second cut).

**What it is for.** You have a job you want AI to help with. Before anyone builds anything, Right Shape answers three questions: what form should it take, how much should it do on its own, and what kind of AI, if any, does it need. It explains each answer in plain words and gives you a test that shows whether the result works. Most of the time the right answer is smaller than you expected.

It works on one job ("should our support inbox get an agent?") or on a whole set of code repositories you want to tidy into installable, measurable pieces. It recommends; it does not build. It never gives an AI more freedom than its safety checks allow.

## First use

Bring one AI job, an existing capability or a repository portfolio. You get a placement card or an audit with source routes, limits and the next test.

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-right-shape.git
cd amplifier-skill-right-shape
python3 scripts/capability.py install --dest ~/.agents/skills
```

Requires Git and Python 3.11+. Use the skills directory supported by your agent. Ask for Right Shape in a new session and supply one real task. The [install guide](docs/INSTALL.md) explains the complete ZIP alternative and safe updates.

## The three choices

People often mix these up. "Let's build an agent" quietly answers all three at once. Right Shape answers each one separately, so you can see which choice is driving the result.

| Choice | The question | The options |
| --- | --- | --- |
| **Shape** | What form should it take? | Tool, Smart Tool, Skill, Agent, or a Team (outer harness) |
| **Freedom** | How much should it do on its own? | From "you ask, it answers" (rungs 0 to 2) through "it follows a set route" (3) and "it works alongside you" (4 to 5) to "it works without you" (6 to 9) |
| **Engine** | What kind of AI, if any, does it need? | A writer (an LLM), a referee (a decision model that makes one narrow call fast and consistently), both, or no model for fixed code |

### The five shapes, side by side

Listed from the least independent to the most. Pick the first one that does the job.

| Shape | In plain words | Like | Pick it when | Who is in charge |
| --- | --- | --- | --- | --- |
| **Tool** | Does one fixed thing when asked. No judgment of its own. | A calculator | The steps never change and a wrong answer is easy to spot | You, every time |
| **Smart Tool** | A specialist you hand a request to. The expertise stays inside; you get a finished result back. | A tax-prep service | The job repeats and the know-how is stable | You, at the hand-off |
| **Skill** | Know-how written down for your assistant to read and apply with its own judgment. | A playbook or recipe card | Your assistant needs your team's way of doing something, but situations vary | You, alongside it |
| **Agent** | A worker you delegate to. It plans its own steps, keeps going without you, and remembers. | A colleague you hand a task to | The steps can't be written in advance, and the result can be checked | You approve the result |
| **Team (outer harness)** | Several workers and checkers behind one point of contact. | A small team with a manager | The work needs a separate checker, several specialists, or many groups will use it | You approve at set checkpoints |

Plugins and bundles are not on the list on purpose: they are the box a capability ships in, not a kind of capability.

### How the freedom is decided

**Need** is how much freedom the job wants: how open its path is, how much it has to keep in mind, how long it runs without anyone watching, and whether it acts on its own. **The ceiling** is how much freedom can safely be given, set by six safety checks: can the result be checked, can it be undone, is the "lethal trifecta" broken (private data plus untrusted content plus a way to send data out), is it isolated, is there a budget, and is someone accountable. The recommendation is whichever is lower.

This project pairs the [`right-shape` skill](skills/right-shape/SKILL.md) and its [rubric](skills/right-shape/references/rubric.md) with an explanatory static website that includes a placement calculator. The [full controlled benchmark plan](docs/BENCHMARK.md) has not been run. A separate fictional Audit application failed substantive checks; [local validation](docs/VALIDATION.md) records it alongside passing arithmetic conformance.

## Use the skill

Give an agent the skill and the work: a job description, an idea, one repository, or a list of repositories. Say which mode you want, or let it choose. Expect a verdict in the first sentence, one question at most, and a card or report at the end.

If your tool supports reusable skills, copy the complete `skills/right-shape/` directory according to that tool's instructions. Keep `references/`, the optional Python validator in `scripts/`, and the MIT notice intact. The method works without Python; the validator checks placement arithmetic when Python is available.

## Audit a whole portfolio

Audit reads inside repositories and groups distinct user promises across them. It returns exact existing source paths, proposed owners and targets, interfaces, source coverage, install blockers, research provenance and staged changes with gates and rollback. A public entry, a reusable engine and a learning experiment can have different destinations. Useful experiments do not need product grades to justify retaining them.

The [Audit workflow](skills/right-shape/references/audit.md) explains collection depth, promise and mechanism boundaries, optional market-fit/usefulness evidence, code routing and retirement after verified replacement. The [rubric](skills/right-shape/references/rubric.md) remains the single source for report records and dispositions. An audit plan does not authorize publication, visibility changes or source retirement. Already authorized work and owner decisions remain in force.

> Audit these repositories beyond their READMEs. Find the distinct promises, embedded methods and useful mechanisms. Give every source an exact route or retained bucket, distinguish evidence from hypotheses, and show a reversible implementation sequence. Keep learning experiments and confirmed owner decisions intact.

To check a placement's arithmetic, give the bundled validator one JSON object. For example, from this checkout:

```sh
python3 skills/right-shape/scripts/validate_placement.py --input placement.json
```

The input uses `need` (four integers), `failed` (gate IDs), `checks` (shape-check IDs), `engine`, and optional `rung`, `need_score`, `need_rung`, `ceiling`, `tiebreak` and `honest_move`. A false ceiling or a placement above it exits with an error. This checks arithmetic and recognized labels; it cannot establish that the gate judgments or utility claims are true.

For a kept/shared portfolio, write the rubric’s `right-shape-audit/v1` companion record and check its structural coverage against the retained inventory:

```sh
python3 skills/right-shape/scripts/validate_audit.py audit.json --inventory census.json
```

The inventory can use `sources` with ID, revision, paths and embedded-method paths, or fixture-style `repositories` with ID, revision and a files map. This catches omissions and invalid paths/interfaces/placements; it cannot certify a proposed merger, license determination or user claim.

## In Amplifier

This repository is also an Amplifier bundle (`right-shape`). Add its behavior to your current host:

```bash
amplifier bundle add "git+https://github.com/michaeljabbour/amplifier-skill-right-shape@main#subdirectory=behaviors/right-shape.yaml" --app
```

For a local checkout that stays in step with your edits, use `file:///<path-to-checkout>/behaviors/right-shape.yaml` instead. Remove with `amplifier bundle remove right-shape-behavior --app`. Start a new session, then:

- **Skill:** `/right-shape`, or ask for it by name. Nothing loads until it is used.
- **Mode:** `/shape` sets a reviewing posture for the session: verdict first, gates before ambition, and every file edit asks you first. `/mode off` leaves it.
- **Recipe:** `@right-shape:recipes/right-shape-audit.yaml` runs one bounded audit that pauses for you after the inventory and again after the placements, then writes a report to `.right-shape/` in your working directory. It never edits anything in scope.

The skill is registered through `tool-skills`. If no other bundle in your host configures skill sources, Amplifier stops scanning its default skill directories (`.amplifier/skills` in the workspace and `~/.amplifier/skills`); add them to your own skills configuration if you need them. Don't also keep a hand-copied `right-shape` in `~/.amplifier/skills`, or two copies will compete.

Example requests:

> Use right-shape on this idea: an agent that watches our support inbox and refunds orders under fifty dollars. Place it.

> Use right-shape to audit the repositories in repos.txt. Follow the layout of our newest skill repository. Ask me before deciding anything about forks.

> Use right-shape to check this Smart Tool against the contract. What stops a stranger installing it?

See [worked examples](docs/EXAMPLES.md): three placements and one audit, all fictional.

## How it works

1. **Sort.** Where does the expertise live, who starts it, how much of the loop a person holds, and whether it is one worker or many.
2. **Score the need.** Four dimensions from 0 to 3 map to a rung on a ten-rung ladder, from a single call to a swarm.
3. **Set the ceiling.** Six gates. Each failure caps the rung. The placement is the lower of need and ceiling, and the skill says what would raise the ceiling honestly.
4. **Choose the shape and engine.** Four composition checks decide between a single worker and an outer harness behind an agent interface. The engine is LLM, decision model, both, or None for deterministic execution.
5. **Check replaceability.** Five checks, from a stable contract to a sunset test that shows when scaffolding has become dead weight.
6. **Write a benchmark that can fail.** A planted trap, a case to leave alone, a stopping test, a consistency test and a control.

## Local development

The site follows the family's small Python static-builder approach: HTML, CSS and JavaScript with no backend or runtime dependencies. Use Python 3.11 or later; no package installation is required.

From the project directory:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check site/site.js   # optional JavaScript syntax check; needs Node.js
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open <http://127.0.0.1:8000> in your browser. Stop the server with `Ctrl+C`. Re-run the build after source changes. `_site/` is generated output.

The build reads the ladder, need dimensions, gates, shape checks, engines, replaceability checks, evaluation ladder and dispositions straight from the rubric, and the benchmark rows from `docs/BENCHMARK.md`, so the page never forks the method. It also recomputes every fictional placement in `site/site.json` from the rubric and refuses one that does not follow it. The check verifies local links and fragments, that the page and downloads match the canonical skill byte for byte, and the ZIP contents. See [site details](site/README.md).

The Pages workflow builds and checks `_site/` on pushes to `main`, then publishes only that static output. It uses GitHub's official actions pinned to fixed commits and needs no project secrets.

## Project contents

- `skills/right-shape/SKILL.md`: the method.
- `skills/right-shape/references/rubric.md`: the scales, gates, checks, engines, contract, dispositions, diagnosis table, card templates and voice.
- `skills/right-shape/references/audit.md`: the conditional portfolio workflow, with source-depth, ownership, evidence and reversible-migration guidance.
- `skills/right-shape/scripts/validate_placement.py`: the portable arithmetic validator; the site imports the same parser.
- `bundle.md`, `behaviors/right-shape.yaml`: the Amplifier bundle and its installable behavior.
- `modes/shape.md`: the `/shape` mode.
- `recipes/right-shape-audit.yaml`: one staged, human-gated audit.
- `docs/EXAMPLES.md`: fictional worked placements and a fictional audit.
- `docs/BENCHMARK.md`: the tests the skill has to pass. Not yet run.
- `scripts/build.py`, `scripts/check.py`: dependency-free build and integrity checks.
- `site/`: page template, metadata, styles, local assets (including the film, its captions, poster and 15-second cut) and interaction code.
- `_site/`: generated website and downloadable skill assets.

## Background

The method draws on public work: Anthropic's *Building effective agents* (workflows versus agents), Feng, McDonald and Zhang's *Levels of Autonomy for AI Agents* (autonomy as a design decision separate from capability), Simon Willison's *lethal trifecta*, Anthropic's *Scaling Managed Agents* (stable interfaces, and scaffolding that becomes dead weight), and Rich Sutton's *The Bitter Lesson*.

## A few terms

- **Rung:** one step on the ten-step ladder of how much an AI does on its own.
- **Gate:** a safety check that lowers the ceiling when it fails.
- **Harness:** the code that runs an AI. An outer harness organizes many workers into a team.
- **Smart Tool:** a tool that carries its own expertise and works without a model wherever it can.
- **Decision model:** a small, fast model, or a measured rule, that makes one narrow decision consistently.
- **Benchmark:** a test set up in advance, with traps to catch and cases to leave alone.

## Limits

This is a structured judgment aid, not a security review, a compliance process or a guarantee. Rung thresholds and gate caps are design choices to argue with, and two careful reviewers may place the same job a rung apart. An audit sees only what it can read; private repositories and anything nothing links to may be missing. The examples on the site and in the docs are invented.

## License and provenance

MIT; see [LICENSE](LICENSE). The family theme snapshot keeps its own [MIT notice](site/theme/LICENSE). The page follows the Amplifier Smart Tools family site as a design and implementation reference.

## Repository migration

This repository was renamed from `amplifier-skill-right-shape` to `amplifier-capability-right-shape`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.
