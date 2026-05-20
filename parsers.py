import ast
from pathlib import Path
import re

def parse_code(directory):
    code_elements = []
    for path in Path(directory).rglob("*.py"):
        try:
            with open(path, "r") as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    doc = ast.get_docstring(node) or ""
                    code_elements.append({
                        "name": node.name,
                        "file": str(path),
                        "doc": doc[:50] + "..." if len(doc) > 50 else doc
                    })
        except Exception as e:
            pass
    return code_elements

def parse_docs(directory):
    doc_sections = {}
    for path in Path(directory).rglob("*.md"):
        with open(path, "r") as f:
            content = f.read()
        for match in re.finditer(r"^(#+)\s+(.*)", content, re.M):
            level, title = match.groups()
            doc_sections.setdefault(str(path), []).append({
                "level": level,
                "title": title
            })
    return doc_sections
