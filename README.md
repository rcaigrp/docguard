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
