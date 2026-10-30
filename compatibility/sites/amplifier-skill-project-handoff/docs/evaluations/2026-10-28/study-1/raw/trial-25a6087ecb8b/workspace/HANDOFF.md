# HANDOFF

## Project Overview
This project is a fictional local row viewer designed to handle and display rows of data. A key challenge is dealing with malformed input messages, which are currently hard to read and diagnose.

## Key Decisions
- Validation is performed on every read operation to ensure data correctness. This approach was adopted because incorrect cached data is difficult to diagnose.
- Although caching was discussed, it has not been implemented or approved.

## Current Focus
- Maintain validation on every read as per the decision.
- Improve diagnostics for malformed rows to enhance readability and troubleshooting.

## Next Steps for the Assistant
- Continue enforcing validation on each read.
- Review and enhance the malformed-row diagnostic features.
- Avoid implementing caching unless explicitly approved.

## References
- See DECISIONS.md for rationale on validation.
- See PROJECT.md for project context and challenges.

Please maintain these guidelines to ensure data integrity and ease of debugging.