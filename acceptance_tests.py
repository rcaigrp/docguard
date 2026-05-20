import unittest
import sys
import os
from pathlib import Path
import tempfile
import json
import responses
from unittest.mock import patch, MagicMock

# Mock rich before importing main
sys.modules['rich'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.table'] = MagicMock()

from parsers import parse_code, parse_docs
from drift_detector import detect_drift
from main import scan_directory, detect_drift_logic, main

class TestDocGuard(unittest.TestCase):
    def test_criterion_1_scan_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'test.py').write_text('def foo(): pass')
            Path(tmpdir, 'docs.md').write_text('# foo\n# bar')
            
            code, docs = scan_directory(tmpdir)
            self.assertEqual(len(code), 1)
            self.assertEqual(len(docs), 2)

    def test_criterion_2_parse_comments(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'test.py').write_text('def foo(): pass')
            code = parse_code(tmpdir)
            self.assertEqual(len(code), 1)

    def test_criterion_3_identify_drift(self):
        code = [{'name': 'foo', 'type': 'FunctionDef'}]
        docs = [{'name': 'bar'}]
        drifts = detect_drift(code, docs)
        self.assertEqual(len(drifts), 2)

    def test_criterion_4_rich_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'test.py').write_text('def foo(): pass')
            Path(tmpdir, 'docs.md').write_text('# foo')
            
            code, docs = scan_directory(tmpdir)
            drifts = detect_drift_logic(code, docs)
            self.assertEqual(len(drifts), 0)
            
            with patch('rich.console.Console') as mock_console:
                mock_console.return_value = MagicMock()
                with patch('sys.argv', ['main.py', '--directory', tmpdir]):
                    main()
                mock_console.assert_called_once()

    def test_criterion_5_dry_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'test.py').write_text('def foo(): pass')
            Path(tmpdir, 'docs.md').write_text('# foo')
            
            with patch('sys.argv', ['main.py', '--directory', tmpdir, '--dry-run']):
                main()

    def test_criterion_6_export_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'test.py').write_text('def foo(): pass')
            Path(tmpdir, 'docs.md').write_text('# foo')
            
            output_file = Path(tmpdir, 'out.json')
            with patch('sys.argv', ['main.py', '--directory', tmpdir, '--output', str(output_file)]):
                main()
            self.assertTrue(output_file.exists())
            with open(output_file) as f:
                json.load(f)

if __name__ == '__main__':
    unittest.main()
