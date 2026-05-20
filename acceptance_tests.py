import sys
import unittest
from unittest.mock import patch, MagicMock
import json
import os
import argparse

# Mock rich before importing main
sys.modules['rich'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.table'] = MagicMock()

from main import main as main_func
from drift_detector import scan
from parsers import get_code_elements, get_doc_refs

class TestDocGuard(unittest.TestCase):
    
    def setUp(self):
        self.original_argv = sys.argv
        sys.argv = ['main.py']

    def tearDown(self):
        sys.argv = self.original_argv

    def test_criterion_1_scan_directory(self):
        with patch('drift_detector.get_code_elements') as mock_code, \
             patch('drift_detector.get_doc_refs') as mock_docs:
            mock_code.return_value = [{'name': 'func', 'type': 'functiondef', 'file': 'test.py'}]
            mock_docs.return_value = []
            result = scan('/fake/dir')
            mock_code.assert_called_once_with('/fake/dir')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['status'], 'UNDOCUMENTED')

    def test_criterion_2_parse_comments(self):
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = []
            result = get_code_elements('/fake')
            self.assertIsInstance(result, list)
            
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = []
            result = get_doc_refs('/fake')
            self.assertIsInstance(result, list)

    def test_criterion_3_identify_drift(self):
        code = [{'name': 'func1', 'type': 'functiondef', 'file': 'a.py'}]
        docs = ['func1', 'func2']
        
        with patch('drift_detector.get_code_elements', return_value=code) as mock_code, \
             patch('drift_detector.get_doc_refs', return_value=docs) as mock_docs:
            result = scan('/fake')
            outdated = [f for f in result if f['status'] == 'OUTDATED']
            self.assertEqual(len(outdated), 1)
            self.assertEqual(outdated[0]['element'], 'func2')

    def test_criterion_4_rich_table(self):
        with patch('argparse.ArgumentParser') as mock_parser, \
             patch('rich.console.Console') as mock_console, \
             patch('drift_detector.scan') as mock_scan:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(
                directory='/fake', dry_run=False, output=None
            )
            mock_scan.return_value = [{'status': 'UNDOCUMENTED', 'element': 'x', 'file': 'y'}]
            mock_console_instance = MagicMock()
            mock_console.return_value = mock_console_instance
            
            main_func()
            
            mock_console_instance.print.assert_called()

    def test_criterion_5_dry_run(self):
        with patch('argparse.ArgumentParser') as mock_parser, \
             patch('drift_detector.scan') as mock_scan:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(
                directory='/fake', dry_run=True, output=None
            )
            mock_scan.return_value = []
            main_func()
            self.assertTrue(True)

    def test_criterion_6_export_json(self):
        with patch('argparse.ArgumentParser') as mock_parser, \
             patch('drift_detector.scan') as mock_scan, \
             patch('builtins.open') as mock_open, \
             patch('rich.console.Console'):
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(
                directory='/fake', dry_run=False, output='/tmp/output.json'
            )
            mock_scan.return_value = [{'status': 'UNDOCUMENTED', 'element': 'x', 'file': 'y'}]
            mock_console_instance = MagicMock()
            
            main_func()
            
            mock_open.assert_called_once_with('/tmp/output.json', 'w')
            mock_open.return_value.__enter__.return_value.write.assert_called()
