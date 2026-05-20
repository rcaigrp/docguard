import argparse
import sys
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

from parsers import parse_code, parse_markdown, extract_references
from drift_detector import detect_drift


def scan_directory(directory):
    """Scan the specified directory recursively."""
    files = list(Path(directory).rglob('*'))
    return [f for f in files if f.is_file()]


def parse_files(files):
    """Parse code comments and markdown documentation files."""
    code_elements = {}
    doc_sections = {}
    for f in files:
        content = f.read_text()
        if f.suffix == '.py':
            code_elements[f.name] = parse_code(content)
        elif f.suffix in ('.md', '.txt'):
            doc_sections[f.name] = parse_markdown(content)
    return code_elements, doc_sections


def generate_table(findings):
    """Output a formatted rich terminal table with findings."""
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Type", style="dim")
    table.add_column("Element/Reference", style="bold")
    table.add_column("File", style="cyan")
    table.add_column("Message", style="green")
    
    for f in findings:
        table.add_row(f['type'], f.get('element', f.get('reference', '')), f['file'], f['message'])
    console.print(table)


def main():
    parser = argparse.ArgumentParser(description='DocGuard CLI')
    parser.add_argument('--directory', required=True, help='Directory to scan')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    parser.add_argument('--export', help='Export findings to JSON')
    
    args = parser.parse_args()
    
    files = scan_directory(args.directory)
    code_elements, doc_sections = parse_files(files)
    findings = detect_drift(code_elements, doc_sections)
    
    generate_table(findings)
    
    if not args.dry_run and args.export:
        with open(args.export, 'w') as f:
            json.dump(findings, f)


if __name__ == '__main__':
    main()
