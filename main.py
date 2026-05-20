import argparse
import json
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from drift_detector import scan

def main():
    parser = argparse.ArgumentParser(description='DocGuard CLI: Detect documentation drift')
    parser.add_argument('directory', help='Directory to scan')
    parser.add_argument('--dry-run', action='store_true', help='Run without modifying files')
    parser.add_argument('--output', help='Export findings to JSON file')
    
    args = parser.parse_args()
    
    console = Console()
    console.print(f"Scanning directory: {args.directory}")
    
    findings = scan(args.directory)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status", style="bold")
    table.add_column("Element")
    table.add_column("File")
    
    for f in findings:
        table.add_row(f['status'], f['element'], f['file'])
        
    console.print(table)
    
    if args.output:
        with open(args.output, 'w') as out:
            json.dump(findings, out, indent=2)
        console.print(f"[green]Findings exported to {args.output}[/green]")
        
    return findings

if __name__ == '__main__':
    main()
