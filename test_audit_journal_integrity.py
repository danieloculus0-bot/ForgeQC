"""Regression tests for append-only audit journal integrity (synthetic records only)."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_journal


class JournalIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "audit.jsonl"
        self.path_patch = patch.object(audit_journal, "audit_journal_path", return_value=self.path)
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)

    def test_valid_append_and_verify(self):
        first = audit_journal.record_event("TEST", "create", entity_id="synthetic-1")
        second = audit_journal.record_event("TEST", "update", entity_id="synthetic-1")
        self.assertEqual((first["sequence"], second["sequence"]), (1, 2))
        self.assertEqual(second["previous_hash"], first["entry_hash"])
        self.assertEqual(audit_journal.verify_journal(self.path)["entries"], 2)

    def test_corrupt_tail_rejected_without_new_entry(self):
        audit_journal.record_event("TEST", "create")
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write('{"broken":\n')
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "integrity failure"):
            audit_journal.record_event("TEST", "update")
        self.assertEqual(self.path.read_bytes(), before)

    def test_earlier_tamper_rejected_even_with_valid_last_line(self):
        audit_journal.record_event("TEST", "create")
        audit_journal.record_event("TEST", "update")
        lines = self.path.read_text(encoding="utf-8").splitlines()
        first = json.loads(lines[0])
        first["action"] = "tampered"
        lines[0] = json.dumps(first)
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "integrity failure"):
            audit_journal.record_event("TEST", "later")
        self.assertEqual(self.path.read_bytes(), before)

    def test_sequence_gap_detected_even_if_hashes_recomputed(self):
        first = audit_journal.record_event("TEST", "create")
        second = audit_journal.record_event("TEST", "update")
        second["sequence"] = 3
        second["entry_hash"] = audit_journal._hash_record(
            {k: v for k, v in second.items() if k != "entry_hash"}
        )
        self.path.write_text(json.dumps(first) + "\n" + json.dumps(second) + "\n", encoding="utf-8")
        self.assertEqual(audit_journal.verify_journal(self.path)["error"], "Sequence mismatch")
        with self.assertRaises(ValueError):
            audit_journal.record_event("TEST", "later")


if __name__ == "__main__":
    unittest.main()
