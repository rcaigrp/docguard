# DocGuard CLI

A CLI tool to detect documentation drift in software projects.

## Usage
```bash
python main.py --directory ./src --dry-run
python main.py --directory ./src --output json > findings.json
```

## Components
- `main.py`: CLI entry point.
- `parsers.py`: Parses code and documentation.
- `drift_detector.py`: Identifies drift.

## Acceptance Criteria
1. Scan specified directory recursively.
2. Parse code comments and markdown documentation files.
3. Identify potential drift (e.g., undocumented functions, outdated references).
4. Output a formatted rich terminal table with findings.
5. Support dry-run mode.
6. Export findings to JSON.
