import argparse
import ast
import json
import sys
from pathlib import Path
import rich
from parsers import parse_code, parse_docs
from drift_detector import detect_drift

def scan_directory(directory):
    code = parse_code(directory)
    docs = parse_docs(directory)
    return code, docs

def detect_drift_logic(code, docs):
    return detect_drift(code, docs)

def main():
    parser = argparse.ArgumentParser(description='DocGuard CLI')
    parser.add_argument('--directory', required=True, help='Directory to scan')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    parser.add_argument('--output', default=None, help='Export findings to JSON file')
    
    args = parser.parse_args()
    
    code, docs = scan_directory(args.directory)
    drifts = detect_drift_logic(code, docs)
    
    if args.dry_run:
        print("Dry run complete.")
        return
    
    # Format output
    table = rich.table.Table()
    table.add_column("Type", style="bold")
    table.add_column("Element")
    table.add_column("Issue")
    for d in drifts:
        table.add_row(d['type'], d['element'], d['issue'])
    
    console = rich.console.Console()
    console.print(table)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(drifts, f)

if __name__ == '__main__':
    main()
