# ForgeQC

ForgeQC is a lightweight manufacturing Quality Control and quoting intelligence web app intended to become the Quality module of the future Forge ERP suite.

Current working features:
- RMA tracking
- work order tracking
- FPY clocking summaries
- operator efficiency and quoting throughput baselines
- planning, lead time, and purchasing watchlists
- privacy-safe aggregate morale pulse tracking by department
- operating setup profile for JIT, hybrid, or inventory-buffered mode
- customer drawing intake for quoting resources
- automatic PDF BOM candidate extraction from customer drawings
- BOM review before use
- approved supplier/material catalog entry
- automatic quote material assignment drafts
- material cost, standard length, pieces required, and lead-time estimates
- dashboard metrics
- editable customers, departments, and reason codes
- local-only Excel RMA tracker import from `data/imports/RMA_Tracker.xlsx`

## Run locally on Windows

```bat
run.bat
```

Or PowerShell:

```powershell
.\run.ps1
```

Both launchers create the virtual environment, install dependencies, run `smoke_test.py`, then start the app only if the smoke test passes.

Open:

```text
http://127.0.0.1:5000
```

## Smoke test

```bash
python smoke_test.py
```

The smoke test verifies imports, database table creation, required routes, and core GET pages.

## Privacy and public repo rules

Do not commit real customer drawings, customer names, RMA events, defect logs, attendance data, quote PDFs, exported files, or local databases.

The attendance and morale side stores aggregate department metrics only. It must not store employee names, employee numbers, badge IDs, payroll IDs, schedules, or individual attendance records.

## Legacy RMA import

The importer expects a private local workbook here:

```text
data/imports/RMA_Tracker.xlsx
```

Expected workbook sheets:
- `RMA Log`
- `Customer List`
- `Reason Codes`
- `Department List`

Expected `RMA Log` columns:
- Date
- Order Number
- Customer
- Department
- Person
- Defect Description
- Reason Code

The app creates `data/forgeqc.db` automatically on first run.
