# Project handoff

Contract: project-handoff/v1
Project/task: Fictional local row viewer
Updated: 2024-06-01
Basis: P1 (PROJECT.md), D1 (DECISIONS.md), S1-S2 (session excerpt)
Scope: Prepare for next assistant to review malformed-row diagnostic; no cache implementation authorized

## Objective and current state
The project is a fictional local row viewer application. The current focus is on improving diagnostics for malformed input messages, which are hard to read. Validation on every data read is enforced to avoid issues from incorrect cached data.

## Decisions and constraints
- Validation on every read is adopted to prevent errors from stale or incorrect cached data; cache implementation is not approved and remains only discussed (D1, S1, S2).

## Verification
- Checked now: No cache implemented; validation on every read remains active (S2).
- Recorded earlier: Validation decision adopted (D1).
- Not checked: Diagnostic improvements for malformed rows are pending review.

## Open items
- Malformed-row diagnostic needs review and potential enhancement (S1).
- Cache implementation remains a proposed but unapproved idea (S1).

## Next safe action
Review and improve the malformed-row diagnostic to enhance readability and error detection. Prerequisite: Access to current diagnostic code and sample malformed inputs. Done when diagnostic output clearly identifies and explains malformed rows with improved clarity.