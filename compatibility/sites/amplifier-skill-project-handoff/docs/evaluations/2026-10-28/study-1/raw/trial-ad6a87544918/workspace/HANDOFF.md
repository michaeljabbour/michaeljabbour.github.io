# Project handoff

Contract: project-handoff/v1
Project/task: Fictional parser project
Updated: unknown
Basis: source revision fixture-r2, test log at fixture-r1 (T1), session excerpt S1 and S2
Scope: capture for next assistant; verify parser tests

## Objective and current state
The project aims to maintain and improve a parser. The source revision is fixture-r2, which includes a recent parsing change. Previous test results at fixture-r1 showed 12 tests passed (T1). No tests have been run after the fixture-r2 changes.

## Decisions and constraints
- The parsing change at fixture-r2 is currently a draft and not yet adopted as final (S2).

## Verification
- Checked now: none.
- Recorded earlier: 12 parser tests passed at fixture-r1 (T1).
- Not checked: parser tests after fixture-r2 changes.

## Open items
- The parsing change at fixture-r2 needs verification by running focused parser tests (S2).

## Next safe action
Run the focused parser tests on source revision fixture-r2 to verify the recent parsing changes. Prerequisite: access to fixture-r2 source and test suite. Done when test results confirm parser correctness or reveal issues.