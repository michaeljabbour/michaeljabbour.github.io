# HANDOFF

## Project Overview
This project is an offline list reader that currently uses CSV files as its data source. The decision has been made to retain the CSV format to maintain compatibility with existing workflows and avoid migrating to a database.

## Current Status
- The reader continues to use CSV files.
- A new parser case to handle quoted commas in CSV entries is planned but not yet implemented.

## Next Steps
- Implement and test the quoted-comma parser case to correctly handle CSV fields containing commas enclosed in quotes.

## Notes
- Avoid switching to a database as per the latest project direction.
- Ensure backward compatibility with existing CSV files.

Please refer to the project documentation and source code comments for further details.