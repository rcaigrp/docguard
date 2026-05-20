import ast
import re

def parse_code(path):
    try:
        with open(path) as f: tree = ast.parse(f.read())
        res = []
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                res.append({"name": n.name, "type": type(n).__name__, "file": path})
        return res
    except: return []

def parse_docs(path):
    try:
        with open(path) as f: content = f.read()
        headings = re.findall(r'^# (.+)', content, re.MULTILINE)
        return [{"name": h, "type": "Doc", "file": path} for h in headings]
    except: return []
