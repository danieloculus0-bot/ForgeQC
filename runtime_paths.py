from __future__ import annotations

import os
from pathlib import Path


APP_NAME = "ForgeQC"


def data_root() -> Path:
    override = os.environ.get("FORGEQC_DATA_DIR")
    if override:
        root = Path(override).expanduser().resolve()
    elif os.name == "nt":
        base = Path(os.environ.get("PROGRAMDATA") or r"C:\ProgramData")
        root = base / APP_NAME
    else:
        root = Path(__file__).resolve().parent / "data"
    root.mkdir(parents=True, exist_ok=True)
    return root


def database_path() -> Path:
    return data_root() / "forgeqc.db"


def imports_dir() -> Path:
    path = data_root() / "imports"
    path.mkdir(parents=True, exist_ok=True)
    return path


def erp_inbox_dir() -> Path:
    path = imports_dir() / "erp_inbox"
    path.mkdir(parents=True, exist_ok=True)
    return path


def erp_archive_dir() -> Path:
    path = imports_dir() / "erp_archive"
    path.mkdir(parents=True, exist_ok=True)
    return path


def uploads_dir() -> Path:
    path = data_root() / "uploads"
    path.mkdir(parents=True, exist_ok=True)
    return path


def audit_dir() -> Path:
    path = data_root() / "audit"
    path.mkdir(parents=True, exist_ok=True)
    return path


def audit_journal_path() -> Path:
    return audit_dir() / "audit_journal.jsonl"
