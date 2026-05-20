import ast
import os
import re
from pathlib import Path

def get_code_elements(directory):
    code_elements = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        source = file.read()
                        tree = ast.parse(source)
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                                code_elements.append({
                                    'name': node.name,
                                    'type': type(node).__name__,
                                    'file': path,
                                    'line': node.lineno
                                })
                except Exception:
                    pass
    return code_elements

def get_doc_refs(directory):
    doc_refs = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        headings = re.findall(r'^##\s+(.*)', content, re.M)
                        code_blocks = re.findall(r'```python\s*([^`]+)`', content, re.S)
                        doc_refs.extend(headings)
                        doc_refs.extend(code_blocks)
                except Exception:
                    pass
    return doc_refs
