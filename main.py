import argparse
import sys
import os
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

def main():
    parser = argparse.ArgumentParser(description='DocGuard CLI')
    parser.add_argument('--directory', required=True, help='Directory to scan')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    parser.add_argument('--output', help='Output JSON file')
    args = parser.parse_args()
    
    from parsers import parse_python_code, parse_markdown_docs
    from drift_detector import detect_drift
    
    console = Console()
    console.print(f"Scanning {args.directory}...")
    
    code_files = []
    for root, dirs, files in os.walk(args.directory):
        for f in files:
            if f.endswith('.py'):
                code_files.append(os.path.join(root, f))
                
    code_elements = []
    for f in code_files:
        code_elements.extend(parse_python_code(f))
        
    docs = parse_markdown_docs(args.directory)
    
    findings = detect_drift(code_elements, docs, args.dry_run)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(findings, f)
            
    table = Table(title="DocGuard Findings")
    table.add_column("Type", style="cyan")
    table.add_column("Name")
    for f in findings:
        table.add_row(f['type'], f['name'])
    console.print(table)

if __name__ == '__main__':
    main()
