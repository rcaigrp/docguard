import pytest
from unittest.mock import patch, mock_open
import sys
from pathlib import Path

from main import main, scan_directory
from parsers import parse_code_file, parse_markdown_file
from drift_detector import detect_drift

class TestCriterion1_ScanDirectory:
    def test_recursive_scan(self):
        with patch('pathlib.Path.rglob') as mock_rglob:
            mock_rglob.return_value = [
                (Path('a'), [], ['test.py']),
                (Path('b'), [], ['doc.md'])
            ]
            code_files, doc_files = scan_directory('./test')
            assert len(code_files) == 1
            assert len(doc_files) == 1

class TestCriterion2_ParseFiles:
    def test_parse_code_and_docs(self):
        with patch('builtins.open', mock_open(read_data='def foo(): pass')):
            elements = parse_code_file(Path('test.py'))
            assert len(elements) == 1
            assert elements[0]['name'] == 'foo'

        with patch('builtins.open', mock_open(read_data='# Bar\n\n```python\ndef bar(): pass\n```')):
            doc = parse_markdown_file(Path('doc.md'))
            assert 'Bar' in doc['headings']
            assert len(doc['code_snippets']) == 1

class TestCriterion3_DriftDetection:
    def test_identify_drift(self):
        code_elements = [{'name': 'foo', 'type': 'FunctionDef', 'docstring': None, 'filepath': 'test.py'}]
        doc_elements = {'headings': ['Bar'], 'code_snippets': [], 'filepath': 'combined'}
        findings = detect_drift(code_elements, doc_elements)
        assert len(findings) == 1
        assert 'foo' in findings[0]['element']

class TestCriterion4_RichTable:
    @patch('main.console')
    def test_rich_table_output(self, mock_console):
        with patch('main.scan_directory') as mock_scan:
            mock_scan.return_value = ([Path('test.py')], [Path('doc.md')])
            with patch('main.parse_code_file', return_value=[{'name': 'test', 'type': 'FunctionDef', 'docstring': None, 'filepath': 'test.py'}]):
                with patch('main.parse_markdown_file', return_value={'headings': [], 'code_snippets': [], 'filepath': 'doc.md'}):
                    with patch('main.detect_drift', return_value=[{'type': 'Code', 'element': 'test', 'issue': 'No doc'}]):
                        main()
                        mock_console.print.assert_called()

class TestCriterion5_DryRun:
    @patch('argparse.ArgumentParser.parse_args')
    def test_dry_run_mode(self, mock_parse):
        mock_parse.return_value = type('Args', (), {'directory': './test', 'dry_run': True, 'output': None})()
        with patch('main.scan_directory', return_value=([], [])):
            with patch('main.parse_code_file', return_value=[]):
                with patch('main.parse_markdown_file', return_value={'headings': [], 'code_snippets': [], 'filepath': 'doc.md'}):
                    with patch('main.detect_drift', return_value=[]):
                        with patch('main.console'):
                            main()
                            with patch('builtins.open') as mock_file:
                                main()
                                mock_file.assert_not_called()

class TestCriterion6_JSONExport:
    @patch('argparse.ArgumentParser.parse_args')
    def test_json_export(self, mock_parse):
        mock_parse.return_value = type('Args', (), {'directory': './test', 'dry_run': False, 'output': 'out.json'})()
        with patch('main.scan_directory', return_value=([], [])):
            with patch('main.parse_code_file', return_value=[]):
                with patch('main.parse_markdown_file', return_value={'headings': [], 'code_snippets': [], 'filepath': 'doc.md'}):
                    with patch('main.detect_drift', return_value=[]):
                        with patch('main.console'):
                            with patch('builtins.open', mock_open()) as mock_file:
                                main()
                                mock_file.assert_called_once_with('out.json', 'w')
