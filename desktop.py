from __future__ import annotations

import os
import socket
import threading
import time
import webbrowser

from waitress import serve

from app import app
from audit_journal import record_event, verify_journal
from erp_integration import process_inbox
from runtime_paths import data_root, erp_inbox_dir


def _erp_worker():
    time.sleep(5)
    while True:
        try:
            with app.app_context():
                process_inbox()
        except Exception as exc:
            try:
                record_event("ERP_WORKER", "Scan failed", entity_type="SERVER", detail=str(exc)[:1000])
            except Exception:
                pass
        time.sleep(max(10, int(os.environ.get("FORGEQC_ERP_SCAN_SECONDS", "30"))))


def _lan_hint(port):
    try:
        hostname = socket.gethostname()
        address = socket.gethostbyname(hostname)
        if address and not address.startswith("127."):
            return f"http://{address}:{port}/report/ncr"
    except Exception:
        pass
    return f"http://<server-ip>:{port}/report/ncr"


def main():
    host = os.environ.get("FORGEQC_HOST", "0.0.0.0")
    try:
        port = int(os.environ.get("FORGEQC_PORT", "5080"))
    except ValueError:
        port = 5080

    verification = verify_journal()
    record_event(
        "SERVER",
        "Started",
        entity_type="FORGEQC_SERVER",
        entity_id=socket.gethostname(),
        detail=f"Host {host}:{port}",
        data={"data_root": str(data_root()), "audit_ok_before_start": verification.get("ok")},
    )

    threading.Thread(target=_erp_worker, daemon=True).start()

    local_url = f"http://127.0.0.1:{port}"
    if os.environ.get("FORGEQC_NO_BROWSER", "0") != "1":
        threading.Timer(1.25, lambda: webbrowser.open(local_url)).start()

    print("ForgeQC Server is running.")
    print(f"Desktop/admin UI: {local_url}")
    print(f"Shop-floor NCR reporter: {_lan_hint(port)}")
    print(f"ERP inbox: {erp_inbox_dir()}")
    print(f"Persistent data: {data_root()}")
    print("Remote network clients are restricted to the NCR reporter and health endpoint.")
    print("Close this window to stop ForgeQC Server.")

    serve(app, host=host, port=port, threads=16)


if __name__ == "__main__":
    main()
