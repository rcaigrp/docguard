import ast
import re

def parse_code(file_path):
    """Parse Python code files to extract function and class definitions with docstrings."""
    elements = []
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node)
                elements.append({
                    'name': node.name,
                    'type': node.__class__.__name__,
                    'docstring': docstring,
                    'file': file_path,
                    'lineno': node.lineno
                })
    except Exception:
        pass
    return elements

def parse_docs(file_path):
    """Parse Markdown documentation files to extract section headers and references."""
    sections = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Extract markdown headers
        headers = re.findall(r'^# (.+)$', content, re.MULTILINE)
        for h in headers:
            sections.append({
                'name': h.strip(),
                'file': file_path,
                'type': 'HEADER'
            })
        # Extract code references (e.g., `func_name` or `module.func`)
        refs = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', content)
        for ref in refs:
            if ref not in [s['name'] for s in sections]:
                sections.append({
                    'name': ref,
                    'file': file_path,
                    'type': 'REFERENCE'
                })
    except Exception:
        pass
    return sections
