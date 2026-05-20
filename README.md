# DocGuard CLI

A CLI tool to detect documentation drift in Python projects.

## Usage
```bash
python main.py --directory ./path/to/project --dry-run --output findings.json
```

## Features
- Scans Python files and Markdown docs.
- Detects undocumented functions/classes.
- Detects references in code that are missing from docs.
- Outputs findings in a Rich terminal table.
- Exports results to JSON.
