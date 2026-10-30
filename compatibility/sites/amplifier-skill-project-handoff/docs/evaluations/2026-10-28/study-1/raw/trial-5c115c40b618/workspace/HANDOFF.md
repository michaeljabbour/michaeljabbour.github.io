# Project handoff

Contract: project-handoff/v1
Project/task: Fictional offline list reader
Updated: unknown
Basis: session excerpt S1, S2; PROJECT.md P1; previous HANDOFF.md H0
Scope: prepare next assistant to continue development

## Objective and current state
The project is an offline list reader currently using CSV format as source data. The previous plan to switch to a database has been rejected to maintain compatibility. The current task is to add support for parsing quoted commas in CSV entries.

## Decisions and constraints
- Adopted decision: Keep the CSV format; do not move to a database to preserve offline reader compatibility. Reason: maintain existing compatibility. Source: S1.
- Proposed change: Add a quoted-comma parser case to the CSV reader. Source: S1.

## Verification
- Checked now: None; the quoted-comma parser case is still pending. Source: S2.
- Recorded earlier: None.
- Not checked: Implementation and testing of quoted-comma parser case.

## Open items
- Implement and verify the quoted-comma parser case. Source: S1, S2.

## Next safe action
Implement the quoted-comma parser case in the CSV reader. Prerequisite: understanding of current CSV parsing code. Done when: the parser correctly handles quoted commas and passes relevant tests.