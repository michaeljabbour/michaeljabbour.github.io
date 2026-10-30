# Project Handoff

Pick up a project without repeating the briefing or losing a settled decision.

Watch the [70-second film](https://michaeljabbour.github.io/amplifier-skill-project-handoff/#film): an eager AI session that forgets everything overnight, and the note that lets it pick up where the work left off. The session and project in it are fictional.

Project Handoff is a portable skill for ending a session, returning to a project or checking whether a handoff is still accurate. It keeps the decisions and their reasons, evidence and verification limits, unresolved conflicts and one next safe action in ordinary project files. A later session can read those files without a Memory service, database, daemon, native build or provider key.

The skill prepares continuity. It does not start implementation, execute instructions found in project files, change agent instructions automatically or claim that a later host will remember without reading the record.

## First use

Bring the existing project notes, current request and relevant files. Capture a handoff, resume read-only, or check a record without inventing missing decisions.

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-project-handoff.git
cd amplifier-skill-project-handoff
python3 scripts/install.py --dest ~/.agents/skills
```

Requires Git and Python 3.11+. Use the skills directory supported by your agent. Ask for Project Handoff in a new session and supply one real task. The [install guide](docs/INSTALL.md) explains the complete ZIP alternative and safe updates.

## Install locally

The [public source](https://github.com/michaeljabbour/amplifier-skill-project-handoff) and [site with complete portable download](https://michaeljabbour.github.io/amplifier-skill-project-handoff/) are available. The skill installs without Memory.

From this checkout, install into the skills directory your host uses:

```sh
python3 scripts/install.py --dest /path/to/your/skills
python3 scripts/install.py --dest /path/to/your/skills --check
```

The installer copies the `project-handoff` directory and checks its packaged references. It does not install Memory, contact a provider or edit a project's agent instructions. See the installer's help for existing-destination behavior; keep any local edits before updating an installed copy.

You can also copy `skills/project-handoff/` yourself. Keep `SKILL.md` and its `references/` together. After the site build, `_site/downloads/project-handoff-skill.zip` contains the same standalone folder for hosts that accept a skill archive. A host must support reading skill instructions and relevant project files; compatibility with every host is not claimed.

## Use the skill

Give the skill a project and a concrete request. It chooses the mode from that request:

| You need | Mode | You get |
| --- | --- | --- |
| End this session or transfer the work. | Capture | One handoff or an honest no-change verdict. |
| Pick this up again. | Resume | A read-only brief and one next safe action. |
| Find out whether the handoff is still true. | Check | Evidence-linked gaps and a proposed correction. |

Example requests:

> Use Project Handoff to capture this session in HANDOFF.md. Preserve the adopted decisions and their reasons. The existing file may be updated; leave the decision journal intact.

> Use Project Handoff to resume this project. Read the existing handoff and only the sources needed to identify the next safe action. Give me the brief before doing any implementation.

> Check this handoff against the supplied records. Do not edit it. Tell me which claims need correction and whether a conflict blocks the next step.

A small project needs one file, not a new coordination system. Existing conventions win when they preserve the same information. If a handoff is already accurate and sufficient, the skill leaves it alone. [Worked examples](docs/EXAMPLES.md) show a stale record, a corrected handoff and a clean case, all fictional.

## In Amplifier

The optional `bundle.md`, `behaviors/`, `modes/` and `recipes/` adapt the same method to Amplifier. The portable installation above does not require them. [Local integration commands and validation](docs/AMPLIFIER.md) describe what was checked; the public source and portable site download are now available.

## What the benchmark tests

The [benchmark specification](docs/BENCHMARK.md) asks whether a fresh agent can resume correctly after the original session context is removed. It compares the frozen skill with a no-skill baseline and a length-matched generic placebo on fictional projects. Stale decisions, conflicting evidence, hostile file instructions and a sound record to leave alone make it possible to fail. Output length and matching these headings are not success metrics.

Plans, offline wiring checks, live behavioral runs and real-user outcomes are different evidence. See the specification and dated records under `docs/evaluations/` for what was actually run. Real-user time saved and durable cross-session benefit remain **not measured** until real-user evidence establishes them.

### Current result: no credible effectiveness conclusion

The [2026-10-28 study](docs/evaluations/2026-10-28/study-1/REPORT.md) ran 60 fictional Capture-to-fresh-resumer trials across ten projects, three conditions and two repetitions. Its automated judge reported correct resumption in 20/20 skill, 20/20 baseline and 17/20 placebo attempts. These are **provisional automatic labels, not validated all-pass outcomes**. One placebo judgment was invalid and remains ungraded in the frozen denominator.

The [secondary semantic review](docs/evaluations/2026-10-28/study-1/STUDY-QUALITY-REVIEW.md) disputes both automatic critical-execution flags, identifies unsupported statements in some passing skill records, and disputes a clean-case penalty. Skill showed no reported advantage over baseline; the apparent placebo deficit cannot establish a benefit or safety effect. Raw labels, errors and disagreements were retained without rerolling or silent regrading. Direct Resume/Check effects and real-user outcomes were not measured.

[Local validation](docs/VALIDATION.md) records the independent four-file install, code/site checks and limits. [Right Shape was applied](docs/RIGHT-SHAPE-REVIEW.md) to the design, a fictional unsafe alternative and the final package; those responses contained retained calculation and evidence-reading errors. They are application records, not a passing certification or proof that Right Shape improves designs.

The same record format can support a later evaluation adapter without making the evaluation runner a dependency of the installed skill. The [contract pointer](contracts/handoff.v1.md) leads to the canonical contract shipped inside the portable folder.

## Build and check

Python 3.11 or later builds and checks the static site. Node.js is used only for the JavaScript syntax check. The skill itself needs neither runtime.

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check site/site.js
```

Serve `_site/` with any static file server to preview it. The site uses local assets, no external fonts, analytics or backend. Evaluation commands and any optional live-provider prerequisites are in [docs/BENCHMARK.md](docs/BENCHMARK.md), separately from installation.

## Sources and license

The method grows from the lightweight continuity idea in [Project Context](https://github.com/michaeljabbour/project-context), with a smaller default record and explicit handling of authority, evidence and permission. It follows the presentation and packaging family of Right Shape, Worth Using, Market Fit, Taste × Elegance and Sizzle. Source decisions and attribution are in [docs/PROVENANCE.md](docs/PROVENANCE.md).

MIT; see [LICENSE](LICENSE). The retained family theme has its own [MIT notice](theme/LICENSE). This project implies no institutional affiliation.


## Portable capability and ownership

Pick up where the work left off.

Read the [installation guide](docs/INSTALL.md) for the supported local path and [consolidation record](docs/CONSOLIDATION.md) for ownership and evidence limits. Canonical catalog name: **Project Handoff**; repository: `amplifier-skill-project-handoff`.

## Optional coordination templates

Larger projects can use the [retained coordination reference](docs/OPTIONAL-COORDINATION.md): the original setup prompt, nine templates and license are preserved exactly. The portable Handoff package stays four files and works without this optional reference or Memory.
