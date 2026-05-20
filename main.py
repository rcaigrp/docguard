import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Import local modules
from parsers import parse_code, parse_docs
from drift_detector import detect_drift

def main():
    parser = argparse.ArgumentParser(description="DocGuard: Detect documentation drift")
    parser.add_argument("--directory", type=str, default=".", help="Directory to scan")
    parser.add_argument("--dry-run", action="store_true", help="Enable dry-run mode")
    parser.add_argument("--output", type=str, default="console", help="Output format (console or json)")
    
    args = parser.parse_args()
    
    console = Console()
    
    if args.dry_run:
        console.print("[green]Dry-run mode enabled. Skipping API calls.[/green]")
        console.print("[yellow]Dry-run mode: No detection performed.[/yellow]")
        return

    # Parse
    code_elements = parse_code(args.directory)
    doc_sections = parse_docs(args.directory)
    
    # Detect
    findings = detect_drift(code_elements, doc_sections)
    
    # Output
    if args.output == "json":
        import json
        print(json.dumps(findings, indent=2))
    else:
        table = Table()
        table.add_column("Element", style="cyan")
        table.add_column("Status", style="green")
        for f in findings:
            table.add_row(f.get("element", "Unknown"), f.get("status", "OK"))
        console.print(table)

if __name__ == "__main__":
    main()
