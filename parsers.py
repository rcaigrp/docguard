import ast
import re
from pathlib import Path

def parse_code_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        elements = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                elements.append({
                    'name': node.name,
                    'type': node.__class__.__name__,
                    'docstring': docstring,
                    'filepath': str(filepath)
                })
        return elements
    except Exception:
        return []

def parse_markdown_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        headings = re.findall(r'^# (.*)', content, re.MULTILINE)
        code_snippets = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
        return {
            'headings': headings,
            'code_snippets': code_snippets,
            'filepath': str(filepath)
        }
    except Exception:
        return {'headings': [], 'code_snippets': [], 'filepath': str(filepath)}
