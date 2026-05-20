import argparse
import json
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from parsers import parse_code_file, parse_markdown_file
from drift_detector import detect_drift

def run(args):
    console = Console()
    code_elements = []
    doc_sections = {}

    # 1. Scan specified directory recursively
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                functions, classes = parse_code_file(filepath)
                code_elements.extend([{'name': f['name'], 'type': 'function', 'path': filepath} for f in functions])
                code_elements.extend([{'name': c['name'], 'type': 'class', 'path': filepath} for c in classes])
            elif file.endswith(".md"):
                filepath = os.path.join(root, file)
                sections = parse_markdown_file(filepath)
                doc_sections.update(sections)

    # 3. Identify potential drift
    drifts = detect_drift(code_elements, doc_sections)

    # 5. Support dry-run mode
    if args.dry_run:
        console.print("[bold]DRY-RUN MODE[/] - No output or export.")
        return drifts

    # 4. Output a formatted rich terminal table
    table = Table(title="DocGuard Findings")
    table.add_column("Element", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Status", style="red")
    table.add_column("Path", style="dim")

    for d in drifts:
        table.add_row(d['element'], d['type'], d['status'], d['path'])

    console.print(table)

    # 6. Export findings to JSON
    if args.export:
        with open(args.export, 'w') as f:
            json.dump(drifts, f, indent=2)

    return drifts

def main():
    parser = argparse.ArgumentParser(description="DocGuard CLI")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--dry-run", action="store_true", help="Enable dry-run mode")
    parser.add_argument("--export", type=str, help="Export findings to JSON file")
    
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
