import unittest
import tempfile
from pathlib import Path
from parsers import parse_code, parse_docs
from drift_detector import find_drift

class TestParsers(unittest.TestCase):
    def test_parse_code(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test.py").write_text("def func():\n    '''doc'''\n")
            result = parse_code(tmpdir)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "func")

    def test_parse_docs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "doc.md").write_text("## Section\n")
            result = parse_docs(tmpdir)
            self.assertEqual(len(result), 1)

class TestDriftDetector(unittest.TestCase):
    def test_find_drift_undocumented(self):
        code = [{"name": "foo", "doc": None}]
        docs = [{"headers": []}]
        findings = find_drift(code, docs)
        self.assertEqual(findings[0]["type"], "UNDOCUMENTED")

    def test_find_drift_outdated(self):
        code = [{"name": "foo", "doc": "doc"}]
        docs = [{"headers": []}]
        findings = find_drift(code, docs)
        self.assertEqual(findings[0]["type"], "OUTDATED")

if __name__ == "__main__":
    unittest.main()
