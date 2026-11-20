import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from inspection_lot import inspect


class InspectionLotTests(unittest.TestCase):
    def test_boundary_values_are_accepted(self):
        result = inspect([{"serial": "A", "characteristic": "hole", "measured": "0.4985", "lower": "0.4985", "upper": "0.5015"},
                          {"serial": "B", "characteristic": "hole", "measured": "0.5015", "lower": "0.4985", "upper": "0.5015"}])
        self.assertEqual(result["disposition"], "ACCEPT")
        self.assertEqual(result["part_count"], 2)

    def test_nonconforming_part_count_is_distinct(self):
        rows = [{"serial": "A", "characteristic": f, "measured": "1.1", "lower": "0.9", "upper": "1"} for f in ("width", "height")]
        report = inspect(rows)
        self.assertEqual((report["nonconforming_parts"], report["measurement_count"]), (1, 2))
        self.assertEqual(report["disposition"], "REJECT")

    def test_invalid_data_fails_closed(self):
        base = {"serial": "A", "characteristic": "width", "measured": "1", "lower": "0", "upper": "2"}
        for field, value in (("measured", "NaN"), ("lower", "3"), ("serial", "")):
            row = dict(base, **{field: value})
            with self.subTest(field=field), self.assertRaises(ValueError):
                inspect([row])
        with self.assertRaises(ValueError):
            inspect([base, base])
        with self.assertRaises(ValueError):
            inspect([])

    def test_cli_csv_to_json(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "lot.csv"
            output = Path(directory) / "report.json"
            with source.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["serial", "characteristic", "measured", "lower", "upper"])
                writer.writeheader()
                writer.writerow(dict(serial="P1", characteristic="diameter", measured="2.01", lower="1.99", upper="2.01"))
            proc = subprocess.run([sys.executable, "inspection_lot.py", str(source), "--output", str(output)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(output.read_text())["disposition"], "ACCEPT")


if __name__ == "__main__":
    unittest.main()
