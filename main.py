import argparse
import sys
import json
import pathlib

from rich.console import Console
from rich.table import Table

def main():
    parser = argparse.ArgumentParser(description='DocGuard CLI')
    parser.add_argument('--directory', required=True, help='Directory to scan')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    parser.add_argument('--output', type=str, help='Export findings to file (e.g., json)')
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("Dry run mode enabled.")
        return
    
    from parsers import parse_code, parse_docs
    from drift_detector import detect_drift
    
    code = parse_code(args.directory)
    docs = parse_docs(args.directory)
    findings = detect_drift(code, docs)
    
    console = Console(force_terminal=False)
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Type", style="dim")
    table.add_column("Element", style="cyan")
    table.add_column("Issue", style="red")
    
    for f in findings:
        table.add_row(f['type'], f['element'], f['issue'])
    
    console.print(table)
    
    if args.output:
        output_path = pathlib.Path(args.output)
        output_path.write_text(json.dumps(findings))

if __name__ == '__main__':
    main()
