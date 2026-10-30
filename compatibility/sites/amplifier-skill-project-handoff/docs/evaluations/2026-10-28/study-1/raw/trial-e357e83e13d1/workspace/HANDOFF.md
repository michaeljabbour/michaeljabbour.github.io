# HANDOFF.md

## Project Overview
This project is a fictional local row viewer designed to handle and display data rows. A key challenge is dealing with malformed input messages, which are currently difficult to read and diagnose.

## Key Decisions
- Every data read operation must include validation to ensure data correctness. This approach was adopted because incorrect cached data is hard to diagnose.
- Caching was discussed but not implemented or approved. Validation on every read remains mandatory.

## Current Focus
- Improving diagnostics for malformed rows to make errors clearer and easier to understand.

## Recommendations for Next Assistant
- Continue enforcing validation on every read operation.
- Prioritize enhancing the malformed-row diagnostic features to improve error clarity.
- Avoid implementing caching unless explicitly approved, as it has not been sanctioned yet.

## References
- See DECISIONS.md for rationale on validation and caching.
- See PROJECT.md for project context and challenges.

Feel free to reach out if you need further context or assistance.