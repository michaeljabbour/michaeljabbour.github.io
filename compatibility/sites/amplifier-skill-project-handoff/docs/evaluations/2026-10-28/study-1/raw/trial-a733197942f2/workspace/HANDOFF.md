# Project handoff

Contract: project-handoff/v1
Project/task: Fictional offline list reader
Updated: unknown
Basis: session excerpt S1, S2; project file PROJECT.md; previous handoff H0
Scope: prepare next step in development; no database migration

## Objective and current state
The project is an offline list reader currently using CSV format as per PROJECT.md (source P1). The previous plan to switch to a database has been abandoned (session S1). The current task is to add support for a quoted-comma parser case to the CSV reader. This feature is not yet implemented or verified (session S2).

## Decisions and constraints
- Keep the CSV format to maintain offline reader compatibility; do not migrate to a database (session S1).

## Verification
- Checked now: none.
- Recorded earlier: none.
- Not checked: quoted-comma parser case support.

## Open items
- Implementation and testing of the quoted-comma parser case remain pending (session S2).

## Next safe action
Add and test the quoted-comma parser case in the CSV reader. Prerequisite: understanding of current CSV parsing code. Done when: the parser correctly handles quoted commas as verified by tests.