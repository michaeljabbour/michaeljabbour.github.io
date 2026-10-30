# Project handoff v1

This is the canonical plain-file interface for a new Project Handoff record. It is ordinary Markdown, readable without software. Existing project formats may remain when they preserve the same information. Missing evidence is written as unknown or not checked; do not invent it to complete the format.

## Minimum information

| Field | Must communicate |
| --- | --- |
| Identity and basis | Project/task, record version, update date if known, inspected revision or other source basis, and scope of this pass. |
| Objective and current state | What is being attempted and what the evidence currently supports. Separate intended behavior from observed implementation. |
| Decisions and constraints | Adopted choices with their recorded reasons and source references; distinguish proposed or disputed changes. Preserve authorization boundaries. |
| Verification | What was checked now, recorded earlier or not checked, with the result's source and scope. Never silently upgrade one category to another. |
| Open items | Unresolved conflicts, unknowns, blockers and dependencies that affect resumption. |
| Next safe action | One action within the stated authorization, its prerequisite and its completion check. A resolving question is an action when the project is blocked. |

Source references belong beside the claim they support. Use project-relative paths, known sections/lines, revision IDs or supplied source IDs. A handoff may link deeper records; it should not duplicate an entire journal or transcript.

## Minimal template

```markdown
# Project handoff

Contract: project-handoff/v1
Project/task: <known name or supplied identifier>
Updated: <known date, or unknown>
Basis: <inspected revision or supplied records; limits>
Scope: <request and permitted destination/actions>

## Objective and current state
<The job and the state supported by sources.>

## Decisions and constraints
- <Adopted decision; recorded reason; source.>
- <Proposed/disputed change, when relevant; source.>

## Verification
- Checked now: <result and source, or none.>
- Recorded earlier: <result, time/scope and source, or none.>
- Not checked: <material limits.>

## Open items
<Conflicts, unknowns or blockers; source where available.>

## Next safe action
<One action. Prerequisite: ... Done when: ...>
```

Omit empty detail rather than pad the record, but keep material verification limits explicit. The source document or supplied source ID is the evidence; the template heading itself proves nothing.

## Compatibility

Version 1 does not prescribe a directory, database, model, API or host. `HANDOFF.md` is a suggested filename only. Reading, writing or checking the record must not require the semantic Memory capability. Generated project records remain independently usable when this skill is removed.

Changes that alter a field's meaning require a new contract version. Additional optional detail may be added without reinterpreting an existing decision or verification label. Consumers should read the documented meaning, not rely on exact heading spelling or formatting. Export/import must preserve decisions, their status and reasons, supporting references and unresolved conflicts.

## Leave-alone test

A record meets the interface when a fresh collaborator can identify the current job, preserve its adopted choices, tell what was actually verified, see material uncertainty and choose the stated next safe action. An accurate record in a different heading style does not need conversion. No tool may treat the presence of this version string as authorization to edit or execute anything.
