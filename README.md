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

The app creates `data/forgeqc.db` automatically on first run.

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


