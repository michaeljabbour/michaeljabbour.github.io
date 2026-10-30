> Preserved source method from `amplifier-bundle-ergonomics` at `8a6b9a0a5189b5572ea5d5c933f7956227a711fb`. Original examples and runtime claims are historical; the canonical entry point defines current scope.

---
name: ux-acceptance-criteria
description: Convert UX and ergonomic recommendations into observable, testable acceptance criteria without inventing arbitrary thresholds.
---

# UX acceptance criteria

Use this pattern:

`Given <user and context>, when <task or event>, the user can <observable outcome> without <critical failure>, while the system provides <necessary feedback, control, or recovery>.`

Add a numerical threshold only when baseline, risk, contractual requirement, or decision power justifies it. Otherwise define the measurement and decision rule first.

Each criterion must trace to a finding and include test method, required state, evidence captured, and failure interpretation.
