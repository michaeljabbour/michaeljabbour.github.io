---
name: right-shape
description: Use when deciding what form a piece of AI work should take (tool, Smart Tool, skill, agent or harness), how much autonomy it can safely have, which engine it needs (LLM, decision model or both), and how to benchmark it. Also audits a set of repositories into installable, self-contained, measurable capabilities, or checks one capability against that contract.
license: MIT
user-invocable: true
---

# Right Shape

## Give the work its right shape

Answer one question well: what form should this piece of AI work take, and how will anyone know it works? Place the job on an autonomy ladder, decide what face it shows (a function, an agent or a protocol), name its engine, check that it can be replaced, and write the benchmark that would prove it. Then stop.

The canonical scales, gates, checks, templates and voice examples are in [references/rubric.md](references/rubric.md). Use them exactly. Do not invent new levels or soften a gate. For a portfolio Audit, also read [references/audit.md](references/audit.md); Place and Check do not need it.

## Sound like a sharp reviewer

- Put the verdict in the first sentence of every turn. No preamble and no praise padding.
- Ask one question per turn, and only when the answer would change the verdict.
- Keep most turns under eighty words. Tables and cards may run longer.
- Name the risk plainly. "It can send mail and read untrusted email" helps more than "consider security".

## Pick the mode

| Mode | Use when | Returns |
| --- | --- | --- |
| Place | One job or idea: "should this be an agent?", "skill or tool?" | One placement card |
| Audit | A set of repositories, modules or products to consolidate | An audit report |
| Check | One existing capability, measured against the contract | A check report |

Choose from the request. Ask only when it is truly ambiguous.

## Place

1. **Sort.** Answer the four sorting questions in the rubric in one line each.
2. **Score the need.** Rate N1 to N4 from 0 to 3 using the rubric's descriptions. Score the smallest version of the job that would genuinely help, not the most ambitious one. Add them and map the score to a rung. Apply the tiebreakers inside the band.
3. **Set the ceiling.** Check G1 to G6. Each failed gate caps the rung; the lowest cap wins. The rung is the need or the ceiling, whichever is lower. Where Python is available, pass the scores and failed gates through [scripts/validate_placement.py](scripts/validate_placement.py) before returning the card. It checks arithmetic against the bundled rubric; it cannot establish whether your gate judgments are true. Without a runner, show the addition and the minimum explicitly and label the arithmetic manually checked.
4. **When need exceeds the ceiling, say so** and offer the honest moves: lower the need (decompose, fix the path into a recipe, seal stable expertise inside a Smart Tool) or raise the ceiling (add an evaluator, put irreversible calls behind approval, remove one leg of the trifecta, isolate it, set budgets, name an owner). Never grant the autonomy anyway.
5. **Choose the shape.** Count H1 to H4. Zero or one: a single tool, skill or agent. Two or more: an outer harness behind an agent interface, or behind a function when the result is bounded and checkable. H4 alone: decompose first. Composition never raises the ceiling.
6. **Name the engine.** LLM, decision model, both, or None for deterministic execution, as the rubric defines them. Prefer a measured rule to a model when the measurement ties. Do not add a decision model to work whose value is human judgment.
7. **Check replaceability.** Run R1 to R5. Report only the gaps.
8. **Write the benchmark** on the evaluation ladder: fixtures, at least one planted trap, one case it should leave alone, a stopping test, a consistency test, a control and proposed thresholds. A benchmark is a plan until a dated run exists.
9. **Hand over the placement card** from the rubric and stop.

## Audit

Follow the conditional Audit workflow and the rubric's audit records. A repository is an inventory unit, not automatically a capability or a brand.

1. Establish a dated source census, coverage depth and gaps. Inspect embedded methods, code, tests, dependencies and research beyond the README.
2. Map distinct user promises and valuable mechanisms inside and across repositories. Separate product evidence from experiment, learning and infrastructure value.
3. Place each proposed capability; name its method owner, engine, public entry and independent install route. Keep usefulness evidence separate from architecture.
4. Route exact existing paths to explicit owners and interfaces. Distinguish extraction, shared contracts, retained engines and compatibility aliases from physical mergers.
5. Reconcile every source and embedded method to a destination or retained source bucket. Keep observed facts, proposed actions, owner decisions and applied changes separate.
6. Deliver one source-bound report and staged plan with gates and rollback. For a large kept/shared Audit, include the rubric's machine record and check it with [scripts/validate_audit.py](scripts/validate_audit.py) against the retained source inventory where a runner is available. This checks structure, not semantic correctness. Stop at the authorized scope; an audit recommendation is not permission to publish, hide, archive, delete or detach.

## Check

Compare one capability with the contract and the evaluation ladder. Lead with the verdict, then list gaps in order of leverage: what stops a stranger installing it, what stops anyone measuring it, and what will rot first. Propose removals before additions.

## Diagnose instead of repeating

When a placement looks wrong, use the diagnosis table in the rubric. Fix the one step it points to. Do not rescore everything hoping for a different answer.

## Keep it honest

- Never claim a result, a user, usage or a benchmark outcome without a dated record. Report "not measured", never zeros or invented numbers.
- Never state fork status, privacy or ownership as fact when you inferred it. Say how you inferred it.
- Leave personal information, credentials and internal or confidential product names out of anything meant to be shared.
- Label fictional examples as fictional.
- Autonomy is a design decision, separate from capability. A strong model may, and often should, run low on the ladder.
- Assume every piece is replaceable. Favor contracts, small parts and recomposition over permanence.
- When you cannot ask the person, for example because the task was delegated, work from the brief, label assumptions, and return your questions with the result instead of answering them yourself.
