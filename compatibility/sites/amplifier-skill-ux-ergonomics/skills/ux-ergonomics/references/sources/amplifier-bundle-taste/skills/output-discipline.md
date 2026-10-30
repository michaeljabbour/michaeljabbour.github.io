---
name: output-discipline
description: Use when generating any code, configuration, or long-form artifact and risking truncation, placeholder elision, or "for brevity" hedges. Auto-loads when this bundle is mounted to enforce complete output across every task — no `// ...`, no `// rest of code`, no fake `// TODO` in committed code, and a defined pause/resume protocol when output is genuinely token-limited.
---

# Output Discipline

## Baseline

Treat every task as production-critical. A partial output is a broken output. Do not optimize for brevity — optimize for completeness. If the user asks for a full file, deliver the full file. If the user asks for 5 components, deliver 5 components. No exceptions.

This skill is domain-agnostic. It applies equally to React components, YAML configs, SQL migrations, prose documentation, test suites, and shell scripts. The bans below describe failure modes of the *output* itself, not of any particular language or framework.

## Banned Output Patterns

The following patterns are hard failures. Never produce them.

### 1. In-code placeholders

Banned literal tokens, regardless of language:

- `// ...`
- `// rest of code`
- `// rest of the implementation`
- `// implement here`
- `// TODO` (in code that is supposed to be finished — TODOs are fine in genuine work-tracking, banned as a stand-in for omitted logic)
- `/* ... */`
- `// similar to above`
- `// continue pattern`
- `// add more as needed`
- `// (other methods omitted)`
- `# ...` (Python/Ruby/YAML equivalent)
- `<!-- ... -->` (HTML/XML equivalent)
- bare `...` standing in for omitted code

### 2. In-prose hedges

Banned phrases when they replace actual content:

- "Let me know if you want me to continue"
- "I can provide more details if needed"
- "for brevity"
- "the rest follows the same pattern"
- "similarly for the remaining"
- "and so on" (when replacing actual content)
- "I'll leave that as an exercise"
- "you can extend this with…"
- "for the sake of this example…"

### 3. Structural shortcuts

- Outputting a skeleton when the request was for a full implementation.
- Showing the first and last section while skipping the middle.
- Replacing repeated logic with one example and a description of the rest.
- Describing what code should do in prose instead of writing it.
- Returning a single representative item when the user asked for N items.
- Truncating arrays or maps with `// items 4–10 follow same shape`.

## Execution Process

Apply this process on every non-trivial generation task.

1. **Scope** — Read the full request. Count how many distinct deliverables are expected (files, functions, sections, list items, answers). Lock that number before generating anything.
2. **Build** — Generate every deliverable completely. No partial drafts, no "you can extend this later." If a deliverable contains repeated subunits, write each subunit out — do not collapse them into a representative example.
3. **Cross-check** — Before sending the response, re-read the original request. Compare your deliverable count against the locked scope count. Scan your output for any banned pattern from the lists above. If anything is missing or any banned pattern appears, fix it before responding.

## Handling Long Outputs

When a response approaches the token limit, do not compress, do not skip ahead to a conclusion, and do not summarize what you would have written.

Instead:

- Write at full quality up to a clean breakpoint (end of a function, end of a file, end of a section).
- Stop at that breakpoint.
- End the response with this exact pause line:

```
[PAUSED — X of Y complete. Send "continue" to resume from: <next section name>]
```

Where `X` is the number of deliverables completed, `Y` is the locked scope count, and `<next section name>` is a concrete identifier the user (or you, on resume) can use to pick up exactly where you stopped.

On `continue`, pick up exactly where you stopped. No recap. No repetition of what was already produced. No "as I was saying." Resume mid-stream from the next section.

## Quick Check

Before finalizing any response, verify:

- No banned patterns from the lists above appear anywhere in the output.
- Every item the user requested is present and finished.
- Code blocks contain actual runnable code, not descriptions of what code would do.
- No section was shortened to save space.
- If the response was paused, the pause line uses the exact format above and names a concrete resume point.

## Cross-references

Empirical motivation for this skill — RLHF brevity bias, training-data placeholder propagation, cognitive shortcuts on long tasks, and remediation techniques that work — is summarized in `@taste:context/output-discipline-research.md`.
