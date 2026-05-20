import ast
import os
import re

def parse_python_code(file_path):
    """Parse Python file and extract function/class definitions."""
    with open(file_path, 'r') as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    
    elements = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            elements.append({
                'name': node.name,
                'docstring': docstring,
                'type': 'function' if isinstance(node, ast.FunctionDef) else 'class'
            })
    return elements

def parse_markdown_docs(directory):
    """Parse Markdown files in directory and extract documentation sections."""
    docs = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.md'):
                file_path = os.path.join(root, f)
                with open(file_path, 'r') as fp:
                    content = fp.read()
                # Simple heuristic: extract headings as keys
                for match in re.finditer(r'^# (.*?)$', content, re.MULTILINE):
                    heading = match.group(1)
                    docs[heading] = True
    return docs
