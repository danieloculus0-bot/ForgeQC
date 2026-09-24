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

The smoke test verifies imports, database table creation, required routes, and core GET pages. Pull requests are used as the audit path for visible smoke-test checks.

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

Source-development launchers keep local runtime data under `data/`. The packaged Windows server stores persistent runtime data under `%PROGRAMDATA%\\ForgeQC`.

## Quality Expedite integration

ForgeQC now includes an EZ Expedite-style workflow layer for controlled quality records.

The shared workflow covers:

- NCR / DMR records
- RMAs
- deviation requests
- corrective actions

Each source record can carry:

- accountable owner and email
- priority
- workflow status
- next action
- due date
- CAR-required flag
- timestamped progress history
- overdue, unassigned, and stale tracking

Use the `Quality Expedite` page at `/expedite` as the cross-functional action queue. Source records remain the controlled records. The expedite layer adds accountability and progress tracking without duplicating the source data.

### NCR to CAR linkage

NCR / DMR workflow records can create a linked corrective action directly. ForgeQC also flags repeat part/reason-code history and higher affected quantities as reasons to consider a CAR. The human quality owner still decides whether the condition is systemic and whether the CAR is appropriate.

### KPI and PPM flow

Saving or updating an NCR, RMA, deviation, or CAR updates its workflow record and refreshes the Quality Pulse.

Quality Pulse now includes:

- NCR PPM
- RMA PPM
- open NCR / DMR count
- overdue CARs
- overdue quality actions
- unassigned quality actions
- repeat-part risk
- FPY and existing delivery / quality indicators

Current PPM denominator:

```text
tracked operation output = first-pass-good + rework + scrap
```

This denominator comes from ForgeQC FPY clocking data. It is intentionally identified as tracked production output, not customer shipped quantity. When shipped quantity or ERP shipment data is connected, customer-facing PPM should use that shipment denominator instead.

## ChatGPT Assistant sidebar

ForgeQC includes a no-API ChatGPT handoff sidebar.

The sidebar can:

- collect the current ForgeQC page context and entered form values
- build a prompt for quality review, NCR disposition, CAR / 5-Why support, KPI / PPM interpretation, or audit readiness
- copy the prompt to the clipboard
- open the user's existing ChatGPT session in a new browser tab

No OpenAI API key is stored or required by ForgeQC.

ForgeQC does not scrape a signed-in ChatGPT session or automatically read ChatGPT replies. Approved conclusions must be entered back into the controlled ForgeQC record by the user. This keeps the quality record authoritative and avoids pretending a browser session is an application API.

## Central server + web NCR reporting

ForgeQC supports a central Windows server deployment. The packaged host listens on port `5080` by default.

The host machine opens the full ForgeQC desktop/admin UI locally:

```text
http://127.0.0.1:5080
```

Shop-floor devices use the lightweight NCR reporter:

```text
http://<forgeqc-server>:5080/report/ncr
```

A web submission creates the same controlled `NonconformanceRecord` used by the desktop/admin UI. It immediately creates/updates the Quality Expedite workflow and refreshes quality metrics. There is no shadow NCR database.

Remote network clients are intentionally limited to the NCR reporter and health endpoint. The full ForgeQC quality/admin surface remains local to the host unless a future authenticated remote-access layer is added.

### Live desktop quality state

The full ForgeQC UI polls `/api/live/quality-summary` every five seconds. New NCRs submitted from phones, tablets, or other workstations therefore appear in the host quality state without restarting the application.

The live endpoint includes:

- open NCR count
- open, overdue, and unassigned quality actions
- NCR and RMA PPM
- current PPM denominator source
- audit journal sequence
- recent NCR records

## ERP custom-report integration

ForgeQC has a persistent ERP inbox under:

```text
%PROGRAMDATA%\ForgeQC\imports\erp_inbox
```

Custom CSV, XLSX, or XLSM reports can be copied into that folder or uploaded through `/erp-import`.

The server:

1. SHA-256 hashes the source file.
2. Refuses duplicate imports by source hash.
3. Detects recognized Shipment or Work Order reports from normalized column names.
4. Imports recognized rows.
5. Moves the original source report into the persistent ERP archive.
6. Journals the import result, source hash, row counts, and archive path.

Recognized shipment reports provide the preferred customer-PPM denominator. If shipment data is unavailable, ForgeQC falls back to tracked production output and labels that denominator accordingly.

The mapping layer intentionally accepts common header variants such as `Work Order`, `WO`, `Part Number`, `Qty Shipped`, and `Ship Date`. Additional JobBoss²/custom-export aliases can be added once the exact report headers are known.

## Persistent audit journal

ForgeQC maintains a separate append-only JSONL journal:

```text
%PROGRAMDATA%\ForgeQC\audit\audit_journal.jsonl
```

The journal covers:

- web and desktop mutations
- NCR/RMA/deviation/CAR record saves
- Quality Expedite workflow changes and progress notes
- CAR creation and linkage
- ERP report upload/import activity
- server start events
- existing application actions routed through the ForgeQC activity logger

Each entry contains a sequence number, UTC timestamp, event/action, entity reference, actor/request context, previous-entry hash, and its own SHA-256 hash. This creates a tamper-evident hash chain. ForgeQC exposes journal verification in the local `/audit-journal` page and `/health` status.

The journal is not claimed to be physically undeletable by a Windows administrator. Instead, the installer deliberately places it outside the application directory and marks the entire persistent ForgeQC data tree `uninsneveruninstall`. Normal ForgeQC uninstall does not delete the database, ERP archive, uploaded evidence, or audit journal.

The Windows CI install test explicitly verifies this behavior by creating journal/database state, uninstalling ForgeQC, and failing if either file is removed.

## Windows server installer

Build locally on Windows:

```powershell
.\build_installer.ps1
```

The build:

- creates an isolated build environment
- installs dependencies
- runs the ForgeQC smoke test
- packages `ForgeQC_Server.exe` with PyInstaller
- creates an Inno Setup installer
- opens Windows Firewall TCP 5080 on Domain/Private profiles for the NCR reporter
- optionally starts ForgeQC at Windows user sign-in

The packaged application contains Python and application dependencies. End users do not need a separate Python installation.

