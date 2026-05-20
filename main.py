import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

def main():
    parser = argparse.ArgumentParser(description="DocGuard CLI - Detect documentation drift")
    parser.add_argument("--directory", type=str, required=True, help="Directory to scan recursively")
    parser.add_argument("--dry-run", action="store_true", help="Run in dry-run mode")
    parser.add_argument("--output", type=str, help="Export findings to JSON file")
    
    args = parser.parse_args()
    
    console = Console()
    
    if not Path(args.directory).is_dir():
        console.print(f"[red]Error: Directory {args.directory} does not exist.[/red]")
        sys.exit(1)
        
    from parsers import parse_code, parse_docs
    from drift_detector import find_drift
    
    code_elements = parse_code(args.directory)
    docs = parse_docs(args.directory)
    
    findings = find_drift(code_elements, docs)
    
    if args.dry_run:
        console.print("[yellow]Dry-run mode enabled. No output generated.[/yellow]")
        return
    
    console.print("\n[bold]DocGuard Findings:[/bold]")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Element", style="green")
    table.add_column("Issue", style="red")
    
    for finding in findings:
        table.add_row(finding["type"], finding["element"], finding["issue"])
        
    console.print(table)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(findings, f, indent=2)
        console.print(f"[green]Findings exported to {args.output}[/green]")

if __name__ == "__main__":
    main()
