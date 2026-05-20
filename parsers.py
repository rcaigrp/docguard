import ast
import re


def parse_code(content):
    """Parse Python code to extract function/class definitions and docstrings."""
    tree = ast.parse(content)
    elements = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            elements[node.name] = {
                'type': node.__class__.__name__,
                'docstring': docstring
            }
    return elements


def parse_markdown(content):
    """Parse markdown content to extract documentation sections."""
    sections = {}
    pattern = r'^# (.+)$'
    current_section = None
    lines = content.split('\n')
    for line in lines:
        match = re.match(pattern, line)
        if match:
            current_section = match.group(1)
            sections[current_section] = ''
        elif current_section:
            sections[current_section] += line + '\n'
    return sections


def extract_references(text):
    """Extract references from documentation text (words in backticks)."""
    refs = re.findall(r'`([^`]+)`', text)
    return refs
