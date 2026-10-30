# HANDOFF.md

## Project Overview
This project is a fictional local row viewer designed to handle and display rows of data. A key challenge is dealing with malformed input messages, which are currently difficult to read and diagnose.

## Key Decisions
- Validation is performed on every read operation to ensure data correctness. This approach was adopted because incorrect cached data is hard to diagnose.
- Although caching was discussed, it has not been implemented or approved. All reads currently bypass any cache and validate data directly.

## Current Focus
- Maintain strict validation on every data read.
- Improve diagnostics for malformed rows to make errors easier to identify and understand.

## Next Steps for the Assistant
- Review and enhance the malformed-row diagnostic capabilities.
- Avoid implementing caching unless explicitly approved.

## Notes
- Refer to DECISIONS.md for rationale behind validation strategy.
- Refer to PROJECT.md for project context and challenges.

Please continue with improving error diagnostics and maintain the current validation approach on reads.