"""Traceable dimensional inspection of a CSV lot, using explicit drawing limits.

Input columns: serial,characteristic,measured,lower,upper. Values use Decimal.
Run: python inspection_lot.py observations.csv --output inspection_result.json
"""
import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


def number(value, field, row):
    try:
        result = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        raise ValueError(f"row {row}: invalid {field}") from None
    if not result.is_finite():
        raise ValueError(f"row {row}: non-finite {field}")
    return result


def inspect(rows):
    """Return a complete result; fail closed on malformed/duplicate measurements."""
    results = []
    seen = set()
    for index, record in enumerate(rows, 2):
        serial = str(record.get("serial") or "").strip()
        feature = str(record.get("characteristic") or "").strip()
        if not serial or not feature:
            raise ValueError(f"row {index}: serial and characteristic required")
        key = (serial, feature)
        if key in seen:
            raise ValueError(f"row {index}: duplicate serial/characteristic {key}")
        seen.add(key)
        actual = number(record.get("measured"), "measured", index)
        low = number(record.get("lower"), "lower", index)
        high = number(record.get("upper"), "upper", index)
        if low > high:
            raise ValueError(f"row {index}: lower limit exceeds upper limit")
        passed = low <= actual <= high
        results.append(dict(serial=serial, characteristic=feature, measured=str(actual),
                            lower=str(low), upper=str(high), pass_inspection=passed,
                            deviation=str(low - actual if actual < low else actual - high if actual > high else Decimal(0))))
    if not results:
        raise ValueError("inspection lot contains no measurements")
    by_feature = defaultdict(lambda: {"inspected": 0, "failed": 0})
    failed_serials = set()
    for record in results:
        bucket = by_feature[record["characteristic"]]
        bucket["inspected"] += 1
        if not record["pass_inspection"]:
            bucket["failed"] += 1
            failed_serials.add(record["serial"])
    return {"disposition": "REJECT" if failed_serials else "ACCEPT",
            "measurement_count": len(results), "part_count": len({r["serial"] for r in results}),
            "nonconforming_parts": len(failed_serials), "characteristics": dict(sorted(by_feature.items())),
            "measurements": results}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Evaluate measured dimensions against explicit print limits")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    with args.csv_file.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        required = {"serial", "characteristic", "measured", "lower", "upper"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            parser.error("CSV requires serial,characteristic,measured,lower,upper")
        try:
            report = inspect(reader)
        except ValueError as exc:
            parser.error(str(exc))
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
