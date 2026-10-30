> Preserved source method from `amplifier-bundle-ergonomics` at `8a6b9a0a5189b5572ea5d5c933f7956227a711fb`. Original examples and runtime claims are historical; the canonical entry point defines current scope.

---
name: task-analysis
description: Build an evidence-aware model of a user's real task, including triggers, goals, prerequisites, decisions, actions, feedback, interruptions, errors, recovery, handoffs, and completion evidence.
---

# Task analysis

Use when the product surface is known but the actual human job or failure sequence is unclear.

## Procedure

1. State the actor, triggering condition, desired outcome, context, frequency, expertise, constraints, and consequence of failure.
2. Trace prerequisites, decisions, actions, system responses, waiting, interruptions, handoffs, errors, recovery, and completion evidence.
3. Mark hidden state, recall demand, attention switching, ambiguity, motor burden, irreversible actions, and external coordination.
4. Separate the nominal flow from common variants and exceptions.
5. Identify evidence for each claimed breakdown.

## Output

Return a task model, critical path, variants, failure points, evidence levels, and unknowns. Do not redesign during task modeling.
