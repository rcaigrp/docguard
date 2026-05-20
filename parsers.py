import ast
import re
from pathlib import Path

def parse_code(directory):
    code_elements = []
    for file in Path(directory).rglob('*.py'):
        with open(file) as f:
            content = f.read()
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                code_elements.append({
                    'name': node.name,
                    'type': node.__class__.__name__,
                    'file': str(file)
                })
    return code_elements

def parse_docs(directory):
    docs = []
    for file in Path(directory).rglob('*.md'):
        with open(file) as f:
            content = f.read()
        headers = re.findall(r'^# (.+)', content, re.M)
        for h in headers:
            docs.append({'name': h, 'file': str(file)})
    return docs
