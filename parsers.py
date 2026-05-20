import ast
import re
from pathlib import Path

def parse_code(directory: str):
    code_elements = []
    for path in Path(directory).rglob("*.py"):
        with open(path) as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                code_elements.append({
                    "name": node.name,
                    "file": str(path),
                    "doc": docstring
                })
    return code_elements

def parse_docs(directory: str):
    docs = []
    for path in Path(directory).rglob("*.md"):
        with open(path) as f:
            content = f.read()
        headers = re.findall(r"^##\s+(.*)", content, re.M)
        refs = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        docs.append({
            "file": str(path),
            "headers": headers,
            "refs": refs
        })
    return docs
