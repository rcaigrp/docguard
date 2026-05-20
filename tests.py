"""Unit tests for DocGuard CLI parsers and detector."""
import pytest
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_parse_code_file_with_docstring():
    """Test parsing Python file with docstrings."""
    sys.path.insert(0, '/workspace/projects/DocGuard')
    from parsers import parse_code_file
    
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
        f.write(b'def foo(): "Doc for foo"\\n\n# comment\n\nclass Bar:\n    "Doc for Bar"\\n    pass')
        f.flush()
        
        funcs, classes = parse_code_file(f.name)
        assert len(funcs) == 1
        assert funcs[0]['name'] == 'foo'
        assert funcs[0]['docstring'] == 'Doc for foo'
        assert len(classes) == 1
        assert classes[0]['name'] == 'Bar'
        assert classes[0]['docstring'] == 'Doc for Bar'


def test_parse_code_file_without_docstring():
    """Test parsing Python file without docstrings."""
    sys.path.insert(0, '/workspace/projects/DocGuard')
    from parsers import parse_code_file
    
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
        f.write(b'def foo(): pass\n\nclass Bar:\n    pass')
        f.flush()
        
        funcs, classes = parse_code_file(f.name)
        assert len(funcs) == 1
        assert funcs[0]['docstring'] is None
        assert len(classes) == 1
        assert classes[0]['docstring'] is None


def test_parse_markdown_file():
    """Test parsing markdown file."""
    sys.path.insert(0, '/workspace/projects/DocGuard')
    from parsers import parse_markdown_file
    
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as f:
        f.write('# Main Title\\n## Section 1\\nContent 1\\n## Section 2\\nContent 2')
        f.flush()
        
        sections = parse_markdown_file(f.name)
        assert 'Section 1' in sections
        assert 'Section 2' in sections
        assert 'Content 1' in sections['Section 1']
        assert 'Content 2' in sections['Section 2']


def test_detect_drift_missing_docstring():
    """Test drift detection for missing docstrings."""
    sys.path.insert(0, '/workspace/projects/DocGuard')
    from drift_detector import detect_drift
    
    functions = [
        {'name': 'foo', 'lineno': 1, 'docstring': None, 'path': 'test.py'}
    ]
    classes = []
    sections = {}
    
    findings = detect_drift(functions, classes, sections)
    assert len(findings) == 1
    assert findings[0]['type'] == 'missing_docstring'
    assert findings[0]['element'] == 'foo'


def test_detect_drift_undocumented():
    """Test drift detection for undocumented elements."""
    sys.path.insert(0, '/workspace/projects/DocGuard')
    from drift_detector import detect_drift
    
    functions = [
        {'name': 'foo', 'lineno': 1, 'docstring': 'Doc', 'path': 'test.py'}
    ]
    classes = []
    sections = {
        'API': '## API\\n\\nContent here'
    }
    
    findings = detect_drift(functions, classes, sections)
    assert any(f['type'] == 'undocumented' and f['element'] == 'foo' for f in findings)


def test_scan_directory():
    """Test directory scanning."""
    sys.path.insert(0, '/workspace/projects/DocGuard')
    from parsers import scan_directory
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / 'test'
        test_dir.mkdir()
        
        (test_dir / 'test.py').write_text('pass')
        (test_dir / 'README.md').write_text('# README')
        
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [(str(test_dir), [], ['test.py', 'README.md'])]
            result = scan_directory(str(test_dir))
            assert len(result) == 2
