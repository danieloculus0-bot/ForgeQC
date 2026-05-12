# ForgeQC

ForgeQC is a lightweight manufacturing Quality Control web app intended to become the Quality module of the future Forge ERP suite.

Current working features:
- RMA tracking
- NCR tracking
- DMR tracking
- deviation request tracking
- morale signal tracking by department
- editable customers, departments, and reason codes
- dashboard metrics
- Excel RMA tracker import from `data/imports/RMA_Tracker.xlsx`
- Excel export to `data/exports/`

## Run locally

```bat
run.bat
```

Or manually:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Legacy RMA import

The importer expects:

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
