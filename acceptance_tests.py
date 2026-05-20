import unittest
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Mock rich before importing main to avoid terminal dependencies
sys.modules['rich'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.table'] = MagicMock()

class TestDocGuard(unittest.TestCase):
    def test_criterion_1_scan_directory(self):
        """1. Scan specified directory recursively."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test.py").write_text("# test")
            from parsers import parse_code
            result = parse_code(tmpdir)
            self.assertIsInstance(result, list)

    def test_criterion_2_parse_comments_and_docs(self):
        """2. Parse code comments and markdown documentation files."""
        from parsers import parse_code, parse_docs
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "code.py").write_text("def foo():\n    '''doc'''\n")
            Path(tmpdir, "doc.md").write_text("## foo\n")
            code = parse_code(tmpdir)
            docs = parse_docs(tmpdir)
            self.assertEqual(len(code), 1)
            self.assertEqual(len(docs), 1)

    def test_criterion_3_identify_drift(self):
        """3. Identify potential drift (e.g., undocumented functions, outdated references)."""
        from drift_detector import find_drift
        code = [{"name": "foo", "doc": None}]
        docs = [{"headers": []}]
        findings = find_drift(code, docs)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["type"], "UNDOCUMENTED")

    def test_criterion_4_rich_output(self):
        """4. Output a formatted rich terminal table with findings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test.py").write_text("def bar():\n    pass\n")
            from main import main
            console = MagicMock()
            with patch("sys.argv", ["main.py", "--directory", tmpdir]):
                with patch("rich.console.Console", return_value=console):
                    with patch("rich.table.Table"):
                        main()
            self.assertTrue(console.print.called)

    def test_criterion_5_dry_run(self):
        """5. Support dry-run mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test.py").write_text("def baz():\n    pass\n")
            from main import main
            console = MagicMock()
            with patch("sys.argv", ["main.py", "--directory", tmpdir, "--dry-run"]):
                with patch("rich.console.Console", return_value=console):
                    main()
            self.assertTrue(console.print.called)

    def test_criterion_6_export_json(self):
        """6. Export findings to JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test.py").write_text("def export_me():\n    pass\n")
            from main import main
            output_path = Path(tmpdir, "output.json")
            console = MagicMock()
            with patch("sys.argv", ["main.py", "--directory", tmpdir, "--output", str(output_path)]):
                with patch("rich.console.Console", return_value=console):
                    main()
            self.assertTrue(output_path.exists())

if __name__ == "__main__":
    unittest.main()
