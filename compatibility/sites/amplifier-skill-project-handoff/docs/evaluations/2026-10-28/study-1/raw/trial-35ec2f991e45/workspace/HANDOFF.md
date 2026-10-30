# Project handoff

Contract: project-handoff/v1
Project/task: Fictional local row viewer
Updated: unknown
Basis: P1 (PROJECT.md), D1 (DECISIONS.md), S1-S2 (session excerpt)
Scope: Prepare for next assistant to continue diagnostics and validation

## Objective and current state
The project aims to provide a local row viewer that handles input messages. Current known issue is that malformed input messages are hard to read. Validation on every read is enforced to avoid incorrect cached data, as previously adopted. Cache implementation was discussed but not approved or implemented.

## Decisions and constraints
- Validate each read to avoid incorrect cached data; this is an adopted decision (D1).
- Cache implementation is proposed but not approved or implemented; keep validation on every read (S1, S2).

## Verification
- Checked now: No cache implemented; validation on every read remains active (S2).
- Recorded earlier: Validation on every read adopted to prevent hard-to-diagnose errors (D1).
- Not checked: Effectiveness of malformed-row diagnostic; requires review (S1).

## Open items
- Review and improve malformed-row diagnostic to better handle malformed input messages (S1).

## Next safe action
Review and enhance the malformed-row diagnostic to improve readability of malformed input messages. Prerequisite: Access to current diagnostic code and input samples. Done when: Diagnostic output clearly identifies and explains malformed rows, improving user understanding.
