"""Offline acceptance tests for the real audit-journal summary workflow."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_journal
from audit_summary import summarize, main


class AuditSummaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "audit.jsonl"

    def write_events(self):
        with patch.object(audit_journal, "audit_journal_path", return_value=self.path):
            audit_journal.record_event("RMA", "opened", actor="Fictional User", detail="Private sample")
            audit_journal.record_event("RMA", "closed")
            audit_journal.record_event("CAPA", "opened")

    def test_real_chained_events_aggregate_without_leaking_payload(self):
        self.write_events()
        report = summarize(self.path)
        self.assertEqual(report["entries"], 3)
        self.assertEqual(report["event_counts"], {"CAPA": 1, "RMA": 2})
        self.assertEqual(report["integrity"], "verified")
        self.assertNotIn("Fictional User", json.dumps(report))
        self.assertNotIn("Private sample", json.dumps(report))

    def test_empty_journal(self):
        report = summarize(self.path)
        self.assertEqual(report["entries"], 0)
        self.assertEqual(report["event_counts"], {})
        self.assertEqual(report["last_hash"], "GENESIS")

    def test_tampered_journal_refused(self):
        self.write_events()
        data = self.path.read_text(encoding="utf-8").replace('"opened"', '"altered"', 1)
        self.path.write_text(data, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "integrity failure"):
            summarize(self.path)

    def test_truncated_invalid_line_refused(self):
        self.write_events()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write('{"sequence":4')
        with self.assertRaisesRegex(ValueError, "integrity failure"):
            summarize(self.path)

    def test_cli_failure_is_nonzero(self):
        self.path.write_text('invalid json\n', encoding="utf-8")
        with self.assertRaises(SystemExit) as caught:
            main(["--journal", str(self.path)])
        self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
