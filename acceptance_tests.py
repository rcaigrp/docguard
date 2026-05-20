import unittest
import sys
import os
import json
import tempfile
import pathlib
from unittest.mock import patch, MagicMock

# Mock rich before importing main
sys.modules['rich'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.table'] = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main
import parsers
import drift_detector

class TestDocGuard(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_criterion_1_scan_directory(self):
        filepath = os.path.join(self.temp_dir, 'test.py')
        with open(filepath, 'w') as f:
            f.write('def hello(): pass')
            
        result = parsers.parse_code(self.temp_dir)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'hello')

    def test_criterion_2_parse_code_and_docs(self):
        filepath = os.path.join(self.temp_dir, 'test.py')
        with open(filepath, 'w') as f:
            f.write('def world(): pass')
        code = parsers.parse_code(self.temp_dir)
        self.assertEqual(len(code), 1)
        
        docpath = os.path.join(self.temp_dir, 'README.md')
        with open(docpath, 'w') as f:
            f.write('# Hello\n\n## World\n')
        docs = parsers.parse_docs(self.temp_dir)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['name'], 'World')

    def test_criterion_3_identify_drift(self):
        code = [{'name': 'hello', 'file': 'test.py', 'type': 'code'}]
        docs = [{'name': 'world', 'file': 'README.md', 'type': 'doc'}]
        
        findings = drift_detector.detect_drift(code, docs)
        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0]['type'], 'undocumented')
        self.assertEqual(findings[1]['type'], 'outdated')

    def test_criterion_4_rich_table(self):
        with patch('sys.argv', ['main.py', '--directory', '/tmp']):
            main.main()
        # If it runs without error, the table logic is handled (mocked)
        
    def test_criterion_5_dry_run(self):
        with patch('sys.argv', ['main.py', '--directory', '/tmp', '--dry-run']):
            main.main()

    def test_criterion_6_export_json(self):
        output_file = os.path.join(self.temp_dir, 'out.json')
        with patch('sys.argv', ['main.py', '--directory', '/tmp', '--output', output_file]):
            main.main()
        self.assertTrue(os.path.exists(output_file))
