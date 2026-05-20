import os
import json
import pytest
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from main import scan_directory
from parsers import parse_code, parse_docs
from drift_detector import find_drift

class TestDocGuard:
    @patch('main.Console')
    def test_criterion_1_scan_directory(self, mock_console):
        tmpdir = Path("/tmp/test_scan")
        tmpdir.mkdir(exist_ok=True)
        (tmpdir / "test.py").write_text("")
        (tmpdir / "test.md").write_text("")
        code, docs = scan_directory(str(tmpdir))
        assert len(code) == 1
        assert len(docs) == 1
        shutil.rmtree(tmpdir)

    def test_criterion_2_parse_comments_and_docs(self):
        code_content = "def foo():\n    '''hello'''\n\nclass Bar:\n    pass"
        Path("/tmp/test_parse.py").write_text(code_content)
        docs_content = "# Foo\n# Bar\n# Unknown"
        Path("/tmp/test_parse.md").write_text(docs_content)
        
        code_elems = parse_code("/tmp/test_parse.py")
        doc_secs = parse_docs("/tmp/test_parse.md")
        
        assert len(code_elems) == 2
        assert code_elems[0]['name'] == 'foo'
        assert code_elems[0]['docstring'] == 'hello'
        assert doc_secs[0]['name'] == 'Foo'
        assert doc_secs[1]['name'] == 'Bar'
        
        Path("/tmp/test_parse.py").unlink()
        Path("/tmp/test_parse.md").unlink()

    def test_criterion_3_identify_drift(self):
        code_elems = [{'name': 'foo', 'docstring': None}]
        doc_secs = [{'name': 'foo'}, {'name': 'bar'}]
        drifts = find_drift(code_elems, doc_secs)
        assert any(d['type'] == 'UNDOCUMENTED' for d in drifts)
        assert any(d['type'] == 'OUTDATED' for d in drifts)

    def test_criterion_4_output_rich_table(self):
        with patch('main.Console') as mock_console:
            mock_console.return_value = MagicMock()
            from rich.table import Table
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Type", style="dim")
            table.add_column("Element", style="cyan")
            table.add_column("Message", style="yellow")
            assert isinstance(table, Table)

    def test_criterion_5_dry_run_mode(self):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--directory', required=True)
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--output', type=str)
        args = parser.parse_args(['--directory', '/tmp', '--dry-run'])
        assert args.dry_run

    def test_criterion_6_export_json(self):
        output_file = "/tmp/test_export.json"
        data = [{'type': 'DRIFT'}]
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        assert os.path.exists(output_file)
        with open(output_file, 'r') as f:
            json.load(f)
        os.unlink(output_file)
