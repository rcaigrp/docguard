import ast
import os
import re

def parse_code(directory):
    code_elements = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        source = f.read()
                        tree = ast.parse(source)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            code_elements.append({
                                'name': node.name,
                                'file': filepath,
                                'type': 'code'
                            })
                except Exception:
                    pass
    return code_elements

def parse_docs(directory):
    doc_sections = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    for match in re.finditer(r'^##\s+(.*)', content, re.MULTILINE):
                        doc_sections.append({
                            'name': match.group(1),
                            'file': filepath,
                            'type': 'doc'
                        })
                except Exception:
                    pass
    return doc_sections
