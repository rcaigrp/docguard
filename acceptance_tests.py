import pytest
import unittest.mock as mock
import json
import os
import sys
from pathlib import Path
import tempfile

# Mock sys.argv for tests that call main()
@pytest.fixture
def mock_sys_argv_directory():
    original = sys.argv
    sys.argv = ['docguard', '--directory', '/tmp/test_dir']
    yield
    sys.argv = original

@pytest.fixture
def mock_sys_argv_full():
    original = sys.argv
    sys.argv = ['docguard', '--directory', '/tmp/test_dir', '--dry-run', '--output', '/tmp/test_output.json']
    yield
    sys.argv = original

def test_criterion_1_scan_directory(mock_sys_argv_directory):
    with mock.patch('os.walk') as mock_walk:
        mock_walk.return_value = [('/tmp/test_dir', [], ['test.py'])]
        from main import main
        main()
        assert mock_walk.called
        assert mock_walk.call_args[0][0] == '/tmp/test_dir'

def test_criterion_2_parse_comments_and_docs():
    from parsers import parse_python_code, parse_markdown_docs
    assert parse_python_code is not None
    assert parse_markdown_docs is not None
    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, 'test.py')
        with open(code_path, 'w') as f:
            f.write('def foo(): pass')
        doc_path = os.path.join(tmpdir, 'test.md')
        with open(doc_path, 'w') as f:
            f.write('# foo\n\nSome docs')
        result = parse_python_code(code_path)
        assert len(result) == 1
        assert result[0]['name'] == 'foo'
        docs = parse_markdown_docs(tmpdir)
        assert 'foo' in docs

def test_criterion_3_identify_drift():
    from drift_detector import detect_drift
    code = [{'name': 'foo', 'docstring': None}]
    docs = {}
    findings = detect_drift(code, docs, False)
    assert len(findings) > 0
    assert any(f['type'] == 'undocumented' for f in findings)

def test_criterion_4_output_rich_table():
    with mock.patch('rich.table.Table') as MockTable:
        with mock.patch('rich.console.Console') as MockConsole:
            with mock.patch('sys.argv', ['docguard', '--directory', '/tmp/test_dir']):
                with mock.patch('os.walk') as mock_walk:
                    mock_walk.return_value = []
                    with mock.patch('os.path.exists', return_value=False):
                        from main import main
                        main()
                        MockTable.assert_called()
                        MockConsole.assert_called()

def test_criterion_5_dry_run_mode(mock_sys_argv_full):
    with mock.patch('sys.argv', ['docguard', '--directory', '/tmp/test_dir', '--dry-run']):
        with mock.patch('os.walk') as mock_walk:
            mock_walk.return_value = []
            with mock.patch('os.path.exists', return_value=False):
                from main import main
                main()
                pass

def test_criterion_6_export_json(mock_sys_argv_full):
    with mock.patch('sys.argv', ['docguard', '--directory', '/tmp/test_dir', '--output', '/tmp/test_output.json']):
        with mock.patch('os.walk') as mock_walk:
            mock_walk.return_value = []
            with mock.patch('os.path.exists', return_value=False):
                with mock.patch('builtins.open', mock.mock_open()) as mock_file:
                    from main import main
                    main()
                    assert mock_file.called
                    assert mock_file().write.called
