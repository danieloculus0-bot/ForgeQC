import os
import sys
import tempfile

_SMOKE_DATA_DIR = tempfile.mkdtemp(prefix="forgeqc-smoke-")
os.environ["FORGEQC_DATA_DIR"] = _SMOKE_DATA_DIR


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    from app import app
    from forgeqc_app import db

    with app.app_context():
        db.create_all()
        table_names = set(db.metadata.tables.keys())
        required_tables = {
            'customer',
            'department',
            'reason_code',
            'rma',
            'work_order',
            'operation_clock_summary',
            'operator_throughput',
            'purchase_requirement',
            'attendance_morale_metric',
            'quote_resource',
            'bom_upload',
            'bom_line',
            'approved_supplier',
            'material_catalog_item',
            'material_purchase_history',
            'quote_material_assignment',
            'deviation_request',
            'nonconformance_record',
            'corrective_action',
            'metric_snapshot',
            'quality_signal',
            'five_why_analysis',
            'quality_workflow_item',
            'quality_workflow_activity',
            'erp_import_batch',
            'erp_shipment',
        }
        missing = required_tables - table_names
        check(not missing, f'Missing tables: {sorted(missing)}')

        rules = {str(rule.rule) for rule in app.url_map.iter_rules()}
        required_routes = {
            '/',
            '/pulse',
            '/pulse/snapshot',
            '/pulse/export.csv',
            '/capa-assistant',
            '/five-whys',
            '/five-whys/<int:row_id>',
            '/quoting',
            '/quoting/<int:quote_id>',
            '/bom/<int:upload_id>',
            '/materials',
            '/quote-materials/<int:quote_id>',
            '/workorders',
            '/clocking',
            '/efficiency',
            '/planning',
            '/rma',
            '/metrics',
            '/morale',
            '/admin',
            '/quality-forms',
            '/deviations',
            '/deviations/<int:row_id>',
            '/ncr-dmr',
            '/ncr-dmr/<int:row_id>',
            '/corrective-actions',
        '/report/ncr',
        '/api/live/quality-summary',
        '/health',
        '/audit-journal',
        '/erp-import',
        '/api/erp/status',
            '/corrective-actions/<int:row_id>',
            '/expedite',
            '/expedite/<source_type>/<int:source_id>',
            '/expedite/<source_type>/<int:source_id>/note',
            '/expedite/ncr/<int:ncr_id>/create-car',
            '/expedite/snapshot',
            '/report/ncr',
            '/api/live/quality-summary',
            '/health',
            '/audit-journal',
            '/erp-import',
            '/erp-import/run',
            '/api/erp/status',
        }
        missing_routes = required_routes - rules
        check(not missing_routes, f'Missing routes: {sorted(missing_routes)}')

    client = app.test_client()
    for path in [
        '/',
        '/pulse',
        '/pulse/export.csv',
        '/capa-assistant',
        '/five-whys',
        '/quoting',
        '/materials',
        '/workorders',
        '/planning',
        '/metrics',
        '/morale',
        '/admin',
        '/quality-forms',
        '/deviations',
        '/ncr-dmr',
        '/corrective-actions',
    ]:
        response = client.get(path)
        check(response.status_code == 200, f'{path} returned {response.status_code}')

    response = client.post('/pulse/snapshot')
    check(response.status_code in (302, 303), f'/pulse/snapshot returned {response.status_code}')

    response = client.post('/five-whys', data={
        'analysis_number': 'WHY-SMOKE-0001',
        'status': 'Draft',
        'source_type': 'Internal',
        'problem_statement': 'Sample smoke-test problem statement for missing hardware on a controlled part.',
        'why_1': 'The hardware was missing at final inspection.',
        'why_2': 'The install step was not verified before moving to the next operation.',
        'why_3': 'The traveler did not include a defined verification point.',
        'why_4': 'The process relied on memory instead of a control point.',
        'why_5': 'The system did not identify the hardware as a critical verification item.',
        'final_root_cause': 'The process lacked a controlled verification point for required hardware installation.',
    })
    check(response.status_code in (302, 303), f'/five-whys POST returned {response.status_code}')


    response = client.post('/ncr-dmr', data={
        'record_number': 'NCR-SMOKE-0001',
        'record_type': 'NCR',
        'date_opened': '2026-09-24',
        'status': 'Open',
        'part_number': 'SMOKE-PART',
        'quantity_affected': '6',
        'defect_description': 'Smoke-test dimensional nonconformance used to verify workflow, KPI, PPM, and CAR integration.',
        'containment_action': 'Hold affected product for verification.',
        'disposition': 'Review Needed',
        'disposition_owner': 'Quality',
        'due_date': '2026-09-30',
    })
    check(response.status_code in (302, 303), f'/ncr-dmr POST returned {response.status_code}')

    response = client.post('/report/ncr', data={
        'reported_by': 'Smoke Reporter',
        'work_order_number': '',
        'department': 'Quality',
        'reason': 'Dimensional',
        'part_number': 'WEB-SMOKE-PART',
        'revision': 'A',
        'quantity_affected': '2',
        'source_location': 'Final Inspection',
        'defect_description': 'Web reporter smoke-test nonconformance.',
        'containment_action': 'Segregated affected quantity.',
        'notes': 'Smoke test only.',
    })
    check(response.status_code == 200, f'/report/ncr POST returned {response.status_code}')

    remote_dashboard = client.get('/', environ_overrides={'REMOTE_ADDR': '10.20.30.40'})
    check(remote_dashboard.status_code == 403, 'Remote network client was not blocked from the full ForgeQC UI')
    remote_reporter = client.get('/report/ncr', environ_overrides={'REMOTE_ADDR': '10.20.30.40'})
    check(remote_reporter.status_code == 200, 'Remote network client could not reach the NCR reporter')

    with app.app_context():
        from quality_forms import CorrectiveAction, NonconformanceRecord
        from quality_workflow import QualityWorkflowItem, create_car_from_ncr, ppm_metrics

        ncr = NonconformanceRecord.query.filter_by(record_number='NCR-SMOKE-0001').first()
        check(ncr is not None, 'Smoke NCR was not created')
        workflow = QualityWorkflowItem.query.filter_by(source_type='NCR', source_id=ncr.id).first()
        check(workflow is not None, 'NCR did not create an expedite workflow item')
        car, _created = create_car_from_ncr(ncr, 'Smoke Test')
        db.session.commit()
        check(car is not None and car.ncr_dmr_id == ncr.id, 'NCR did not create/link a CAR')
        check(CorrectiveAction.query.filter_by(ncr_dmr_id=ncr.id).count() == 1, 'CAR link is not unique for smoke NCR')
        ppm = ppm_metrics(30)
        check('ncr_ppm' in ppm and 'rma_ppm' in ppm, 'PPM metrics are unavailable')

        from audit_journal import verify_journal
        audit = verify_journal()
        check(audit.get('ok') is True and audit.get('entries', 0) > 0, f'Audit journal did not verify: {audit}')

        from erp_integration import ERPShipment, process_inbox
        from runtime_paths import erp_inbox_dir
        shipment_report = erp_inbox_dir() / 'shipment_smoke.csv'
        shipment_report.write_text(
            'Ship Date,Customer,Part Number,Work Order,Qty Shipped\n'
            '2026-09-24,Smoke Customer,SMOKE-PART,WO-SMOKE,1000\n',
            encoding='utf-8',
        )
        process_inbox()
        db.session.commit()
        check(ERPShipment.query.count() == 1, 'ERP shipment report did not import')
        ppm = ppm_metrics(30)
        check(ppm.get('denominator_source') == 'ERP shipped quantity', f'ERP shipped quantity did not become PPM denominator: {ppm}')
        check(float(ppm.get('units') or 0) == 1000.0, f'Unexpected ERP PPM denominator: {ppm}')

    print('ForgeQC smoke test passed: web NCR reporting, persistent audit journal, ERP ingest, live quality feed, expedite workflow, KPI/PPM integration, CAPA assistant, and core pages are alive.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ForgeQC smoke test failed: {exc}', file=sys.stderr)
        raise
