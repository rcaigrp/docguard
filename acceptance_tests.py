import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Mock rich module before any imports to prevent rendering errors in tests
sys.modules['rich'] = MagicMock()

class TestDocGuard:
    @patch('sys.argv', ['DocGuard', '--directory', '/tmp/test_dir', '--dry-run'])
    def test_criterion_1_scan_directory(self):
        with patch('pathlib.Path.rglob') as mock_rglob:
            mock_rglob.return_value = [Path('/tmp/test_dir/test.py')]
            from DocGuard.main import scan_directory
            scan_directory('/tmp/test_dir')
            assert mock_rglob.called

    @patch('sys.argv', ['DocGuard', '--directory', '/tmp/test_dir'])
    def test_criterion_2_parse_comments(self):
        from DocGuard.parsers import parse_code, parse_docs
        with patch('pathlib.Path.read_text') as mock_read:
            mock_read.return_value = 'def test(): pass'
            code_result = parse_code(Path('/tmp/test_dir/test.py'))
            assert isinstance(code_result, list)
            mock_read.return_value = '# Doc'
            doc_result = parse_docs(Path('/tmp/test_dir/test.py'))
            assert isinstance(doc_result, list)

    @patch('sys.argv', ['DocGuard', '--directory', '/tmp/test_dir'])
    def test_criterion_3_identify_drift(self):
        from DocGuard.drift_detector import detect_drift
        code = [{'name': 'missing_func', 'path': 'test.py'}]
        docs = []
        findings = detect_drift(code, docs)
        assert any(f['type'] == 'undocumented' for f in findings)

    @patch('sys.argv', ['DocGuard', '--directory', '/tmp/test_dir'])
    def test_criterion_4_rich_table(self):
        from DocGuard.main import display_findings
        console = MagicMock()
        with patch('rich.console.Console') as MockConsole:
            MockConsole.return_value = console
            display_findings([{'type': 'test', 'element': 'x'}])
            assert console.print_table.called

    @patch('sys.argv', ['DocGuard', '--directory', '/tmp/test_dir', '--dry-run'])
    def test_criterion_5_dry_run(self):
        from DocGuard.main import run
        with patch('DocGuard.main.export_findings') as mock_export:
            run()
            assert not mock_export.called

    @patch('sys.argv', ['DocGuard', '--directory', '/tmp/test_dir', '--output', '/tmp/findings.json'])
    def test_criterion_6_export_json(self):
        from DocGuard.main import run
        with patch('DocGuard.main.display_findings'):
            with patch('json.dump') as mock_dump:
                run()
                assert mock_dump.called
