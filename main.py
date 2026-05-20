import argparse
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

from parsers import parse_code_file, parse_markdown_file
from drift_detector import detect_drift

console = Console()

def scan_directory(directory):
    code_files = []
    doc_files = []
    root_path = Path(directory)
    for file in root_path.rglob('*'):
        if file.is_file():
            if file.suffix == '.py':
                code_files.append(file)
            elif file.suffix == '.md':
                doc_files.append(file)
    return code_files, doc_files

def main():
    parser = argparse.ArgumentParser(description='DocGuard CLI')
    parser.add_argument('--directory', required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output')
    
    args = parser.parse_args()

    if not Path(args.directory).is_dir():
        console.print(f"[red]Error: Directory '{args.directory}' does not exist.[/red]")
        sys.exit(1)

    console.print(f"[bold]Scanning directory:[/bold] {args.directory}")

    code_files, doc_files = scan_directory(args.directory)

    code_elements = []
    for cf in code_files:
        parsed = parse_code_file(cf)
        code_elements.extend(parsed)

    doc_elements_list = []
    for df in doc_files:
        parsed = parse_markdown_file(df)
        doc_elements_list.append(parsed)

    combined_doc_elements = {'headings': [], 'code_snippets': [], 'filepath': 'combined'}
    for de in doc_elements_list:
        combined_doc_elements['headings'].extend(de['headings'])
        combined_doc_elements['code_snippets'].extend(de['code_snippets'])

    console.print(f"[bold]Found[/bold] {len(code_elements)} code elements and {len(doc_files)} doc files.")

    findings = detect_drift(code_elements, combined_doc_elements)

    table = Table()
    table.add_column("Type", style="cyan")
    table.add_column("Element", style="green")
    table.add_column("Issue", style="yellow")
    for finding in findings:
        table.add_row(finding['type'], finding['element'], finding['issue'])
    console.print(table)

    if args.output:
        if args.dry_run:
            console.print("[yellow]Dry run: Skipping JSON export.[/yellow]")
        else:
            with open(args.output, 'w') as f:
                json.dump(findings, f, indent=2)
            console.print(f"[green]Findings exported to {args.output}[/green]")

    if args.dry_run:
        console.print("[yellow]Dry run mode enabled. No files written.[/yellow]")

if __name__ == '__main__':
    main()
