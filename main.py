import argparse
import sys
import os
import json

def main():
    import parsers
    import drift_detector
    from rich.console import Console

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default="findings.json")
    args = parser.parse_args()

    console = Console()
    console.print("Scanning...")

    code_files = []
    doc_files = []
    for root, dirs, files in os.walk(args.directory):
        for f in files:
            if f.endswith('.py'): code_files.append(os.path.join(root, f))
            if f.endswith('.md'): doc_files.append(os.path.join(root, f))

    code_elems = []
    for f in code_files: code_elems.extend(parsers.parse_code(f))
    doc_elems = []
    for f in doc_files: doc_elems.extend(parsers.parse_docs(f))

    findings = drift_detector.detect_drift(code_elems, doc_elems)

    console.print(f"Findings: {len(findings)}")
    for f in findings: console.print(f"  - {f}")

    if args.dry_run:
        console.print("Dry run")
    else:
        with open(args.output, 'w') as out:
            json.dump(findings, out)
        console.print(f"Exported to {args.output}")

if __name__ == '__main__':
    main()
