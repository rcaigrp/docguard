import argparse
import os
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

from parsers import parse_code, parse_docs
from drift_detector import find_drift

console = Console()

def scan_directory(directory):
    code_files = []
    doc_files = []
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise ValueError(f"Invalid directory: {directory}")
    for root, dirs, files in os.walk(directory):
        for f in files:
            full_path = os.path.join(root, f)
            if f.endswith('.py'):
                code_files.append(full_path)
            elif f.endswith('.md'):
                doc_files.append(full_path)
    return code_files, doc_files

def main():
    parser = argparse.ArgumentParser(description="DocGuard CLI")
    parser.add_argument('--directory', required=True, help="Directory to scan")
    parser.add_argument('--dry-run', action='store_true', help="Run without saving output")
    parser.add_argument('--output', type=str, help="Output file for JSON findings")
    args = parser.parse_args()

    console.print(f"[bold cyan]Scanning directory: {args.directory}[/bold cyan]")
    
    code_files, doc_files = scan_directory(args.directory)
    
    code_elements = []
    for f in code_files:
        code_elements.extend(parse_code(f))
        
    doc_sections = []
    for f in doc_files:
        doc_sections.extend(parse_docs(f))
        
    drifts = find_drift(code_elements, doc_sections)
    
    # Build rich table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Type", style="dim")
    table.add_column("Element", style="cyan")
    table.add_column("Message", style="yellow")
    
    for d in drifts:
        table.add_row(d['type'], d['element'], d['message'])
        
    console.print(table)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(drifts, f, indent=2)
        console.print(f"[green]Findings exported to {args.output}[/green]")
    elif args.dry_run:
        console.print("[yellow]Dry run mode. No output saved.[/yellow]")
    else:
        console.print("[yellow]No output file specified. Use --output to save findings.[/yellow]")

if __name__ == "__main__":
    main()
