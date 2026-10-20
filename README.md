# ForgeQC

Standalone manufacturing quality and quoting workflow web application. ForgeQC contributes ideas/source snapshots to Axiom, but that does not automatically synchronize deployed databases.

## Current build and CI

**Reviewed:** 2026-10-20 · **Main:** `71c21d9627f3` · **Status:** working standalone experimental/beta product.

- [ForgeQC Smoke Test](https://github.com/danieloculus0-bot/ForgeQC/actions/runs/39489831169) — **Passed** at inspected `main`.
- [ForgeQC Windows Server Build](https://github.com/danieloculus0-bot/ForgeQC/actions/runs/39489831263) — **Passed** at inspected `main`.

[Live Actions](https://github.com/danieloculus0-bot/ForgeQC/actions) supersede this dated snapshot.

## Working today

- Quality tracking for RMA/NCR/CAR and shop-floor records, with audit/event-oriented workflows and KPI support.
- Quoting support, drawing/BOM candidate review, supplier/material resources and Windows server build tooling.
- Standalone Flask-based experience with successful code smoke checks and Windows packaging.

## Run and verify

Windows launchers include `run.bat` and `run.ps1`; follow setup steps in [the archived full README](docs/archive/README_2026-10-20_before_refresh.md). The launchers run an application smoke check before starting the service.

## Known boundaries

- Source vendored into Axiom is not evidence of a live integrated ForgeQC instance or data migration.
- Quoting BOMs and shop-quality insights need human review and current source data; CI is not manufacturing acceptance.

## Next engineering work

Specify migration/contracts for shared quality records and preserve standalone functionality alongside Axiom.

## Related documentation

- [Axiom ERP consolidation](https://github.com/danieloculus0-bot/Axiom_Beta)
- [Original full README: earlier details and development history](docs/archive/README_2026-10-20_before_refresh.md)
