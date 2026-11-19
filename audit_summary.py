"""Read-only integrity-gated summary of a ForgeQC audit journal.

No raw record fields or actor identifiers are emitted. The original journal is
never changed. Useful for offline quality reviews without copying sensitive data.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from audit_journal import verify_journal
from runtime_paths import audit_journal_path


def summarize(path: Path) -> dict:
    """Validate the entire hash chain before aggregating event categories."""
    path = Path(path)
    verification = verify_journal(path)
    if not verification["ok"]:
        raise ValueError(
            f"Audit integrity failure at line {verification.get('line', 'unknown')}: "
            f"{verification['error']}"
        )
    counts = Counter()
    if path.exists():
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                if line.strip():
                    record = json.loads(line)
                    counts[str(record["event_type"])] += 1
    return {
        "schema": "forgeqc.audit_summary.v1",
        "integrity": "verified",
        "entries": verification["entries"],
        "last_hash": verification["last_hash"],
        "event_counts": dict(sorted(counts.items())),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify and summarize ForgeQC audit events")
    parser.add_argument("--journal", type=Path, default=None, help="Journal JSONL path")
    args = parser.parse_args(argv)
    try:
        summary = summarize(args.journal or audit_journal_path())
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"Audit summary refused: {exc}\n")
    print(json.dumps(summary, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
