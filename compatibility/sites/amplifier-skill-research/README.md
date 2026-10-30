# Research

Make the answer traceable to the evidence.

Watch the [66-second film](https://michaeljabbour.github.io/amplifier-skill-research/#film): nine crashed runs that vanish from a score, and how the skill keeps them in the count. The example in it is fictional.

A research skill for decisions, experiments and papers. Build a claim-to-source chain, keep contradictions visible and use a study design that can support the conclusion you want to make.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-research/) · [Read the method](skills/research/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Answer the bounded question.** Choose a focused investigation, a justified experiment or a claim-linked manuscript.
- **Keep the evidence inspectable.** Retain source locators, methods, populations, applicability and the reasoning between them.
- **Learn from an honest comparison.** Freeze the protocol, preserve errors and failed trials, and separate exploratory findings from confirmation.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-research.git
cd amplifier-skill-research
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/research` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use Research to assess whether the fictional document-retrieval change improves source coverage. First propose a bounded question, treatment and baseline, coverage measure, error handling, budget and stop rule. Prepare a protocol; do not run paid calls.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Define what the answer changes.** Name the question, audience, competing explanations, needed evidence and budget.
2. **Gather or measure.** Read primary sources, or freeze the experiment and measurement rules before outcomes.
3. **Write what the evidence permits.** Link claims to records, include disagreement and uncertainty, and identify the smallest useful next check.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional protocol: retrieval coverage
Question: does the change surface required evidence?
Baseline and treatment: frozen versions
Unit: source-question pair
Errors: retained under the declared denominator
Judge: calibrated against literal source evidence
Conclusion: pending measurements; no improvement claim yet
```

## What is checked

174 native integrity-tool tests and ten synthetic experiment-loop shell checks passed. They check software controls, not research novelty, an empirical treatment effect or an outside-user outcome. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Retained implementation and references

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.
