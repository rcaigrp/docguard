import pytest
import os
import tempfile
from parsers import parse_python_code, parse_markdown_docs
from drift_detector import detect_drift

def test_parse_python_code():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('def foo(): pass\nclass Bar: pass')
        path = f.name
    result = parse_python_code(path)
    assert len(result) == 2
    assert result[0]['name'] == 'foo'
    assert result[1]['name'] == 'Bar'
    os.unlink(path)

def test_parse_markdown_docs():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write('# Hello\n\nWorld\n\n# Goodbye\n\nFarewell')
        path = f.name
    docs = parse_markdown_docs(os.path.dirname(path))
    assert 'hello' in docs
    assert 'goodbye' in docs
    os.unlink(path)

def test_detect_drift_undocumented():
    code = [{'name': 'foo', 'docstring': None}]
    docs = {}
    findings = detect_drift(code, docs, False)
    assert len(findings) == 1
    assert findings[0]['type'] == 'undocumented'

def test_detect_drift_outdated():
    code = [{'name': 'foo', 'docstring': None}]
    docs = {'foo': 'docs'}
    findings = detect_drift(code, docs, False)
    assert len(findings) == 1
    assert findings[0]['type'] == 'outdated'
