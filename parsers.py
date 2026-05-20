import ast

def parse_code_file(filepath):
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        functions = []
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({'name': node.name, 'docstring': ast.get_docstring(node)})
            elif isinstance(node, ast.ClassDef):
                classes.append({'name': node.name, 'docstring': ast.get_docstring(node)})
        return functions, classes
    except Exception:
        return [], []

def parse_markdown_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    sections = {}
    for line in content.split('\n'):
        if line.startswith('## '):
            name = line[3:].strip()
            sections[name] = ""
    return sections
