# DocGuard CLI

## Goal
Detect documentation drift in software projects by comparing code comments and documentation files against code structure.

## Acceptance Criteria
1. Scan specified directory recursively.
2. Parse code comments and markdown documentation files.
3. Identify potential drift (e.g., undocumented functions, outdated references).
4. Output a formatted `rich` terminal table with findings.
5. Support dry-run mode.
6. Export findings to JSON.

## Status
- All criteria implemented.
- Tests passing.

## Next Steps
- Deploy to production.
