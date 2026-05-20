import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

sys.argv = ['main.py', '--directory', './test_dir', '--dry-run']

from main import scan_directory, parse_files, generate_table, main
from parsers import parse_code, parse_markdown, extract_references
from drift_detector import detect_drift


class TestDocGuard(unittest.TestCase):
    def test_criterion_1_scan_directory(self):
        with patch('pathlib.Path.rglob') as mock_rglob:
            mock_rglob.return_value = [
                Path('/test_dir/a.py'),
                Path('/test_dir/b.md'),
            ]
            files = scan_directory('./test_dir')
            self.assertEqual(len(files), 2)
            mock_rglob.assert_called_once()

    def test_criterion_2_parse_code_comments_and_markdown(self):
        code_content = 'def foo():\n    """Doc."""\n    pass'
        md_content = '# Doc\n\n`foo` is great.'
        
        code_elements = parse_code(code_content)
        doc_sections = parse_markdown(md_content)
        
        self.assertIn('foo', code_elements)
        self.assertEqual(code_elements['foo']['docstring'], 'Doc.')
        self.assertIn('Doc', doc_sections)

    def test_criterion_3_identify_drift(self):
        code_elements = {'test.py': {'foo': {'type': 'FunctionDef', 'docstring': None}}}
        doc_sections = {'doc.md': {'Doc': '`bar` is used'}}
        
        findings = detect_drift(code_elements, doc_sections)
        self.assertTrue(any(f['type'] == 'undocumented' for f in findings))
        self.assertTrue(any(f['type'] == 'outdated_reference' for f in findings))

    def test_criterion_4_rich_table_output(self):
        with patch('main.Console') as MockConsole:
            console_instance = MockConsole.return_value
            findings = [
                {'type': 'undocumented', 'element': 'foo', 'file': 'a.py', 'message': 'No docstring'}
            ]
            generate_table(findings)
            MockConsole.return_value.print.assert_called_once()

    def test_criterion_5_dry_run_mode(self):
        with patch('main.Console') as MockConsole:
            with patch('main.Path') as MockPath:
                MockPath.return_value.rglob.return_value = []
                with patch('main.json') as mock_json:
                    main()
                    mock_json.dump.assert_not_called()

    def test_criterion_6_export_json(self):
        with patch('main.Console') as MockConsole:
            with patch('main.Path') as MockPath:
                MockPath.return_value.rglob.return_value = []
                with patch('builtins.open', MagicMock()) as mock_open:
                    with patch('sys.argv', ['main.py', '--directory', '.', '--export', 'output.json']):
                        main()
                        mock_open.assert_called_once()


if __name__ == '__main__':
    unittest.main()
