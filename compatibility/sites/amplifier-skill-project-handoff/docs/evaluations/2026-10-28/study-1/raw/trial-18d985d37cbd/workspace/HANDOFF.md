# HANDOFF

## Current Status
- The offline list reader continues to use the CSV format for compatibility.
- The plan to switch to a database has been abandoned.

## Next Steps
- Implement the quoted-comma parser case to handle CSV entries with quoted commas.
- Add tests to verify the new parser case.

## Notes
- Ensure backward compatibility with existing CSV files.
- Review existing parser code before adding new cases.