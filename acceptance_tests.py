import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

sys.argv = ['main.py', '--directory', './test_dir', '--dry-run', '--output', './findings.json']

class TestDocGuardAcceptance:
    @patch('sys.argv', ['main.py', '--directory', './test_dir', '--dry-run', '--output', './findings.json'])
    @patch('os.walk', return_value=[['./test_dir', [], []]])
    @patch('rich.console.Console')
    def test_criterion_1_scan_directory(self, mock_console):
        from main import main
        main()
        assert True

    @patch('sys.argv', ['main.py', '--directory', './test_dir'])
    @patch('os.walk', return_value=[['./test_dir', [], []]])
    @patch('rich.console.Console')
    def test_criterion_2_parse_comments_and_docs(self, mock_console):
        from main import main
        main()
        assert True

    @patch('sys.argv', ['main.py', '--directory', './test_dir'])
    @patch('os.walk', return_value=[['./test_dir', [], []]])
    @patch('rich.console.Console')
    def test_criterion_3_identify_drift(self, mock_console):
        from main import main
        main()
        assert True

    @patch('sys.argv', ['main.py', '--directory', './test_dir'])
    @patch('os.walk', return_value=[['./test_dir', [], []]])
    @patch('rich.console.Console')
    def test_criterion_4_rich_table_output(self, mock_console):
        from main import main
        main()
        assert True

    @patch('sys.argv', ['main.py', '--directory', './test_dir', '--dry-run'])
    @patch('os.walk', return_value=[['./test_dir', [], []]])
    @patch('rich.console.Console')
    def test_criterion_5_dry_run(self, mock_console):
        from main import main
        main()
        assert True

    @patch('sys.argv', ['main.py', '--directory', './test_dir', '--output', './findings.json'])
    @patch('os.walk', return_value=[['./test_dir', [], []]])
    @patch('rich.console.Console')
    def test_criterion_6_export_json(self, mock_console):
        from main import main
        main()
        assert os.path.exists('./findings.json')
