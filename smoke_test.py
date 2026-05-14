import sys


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
            '/corrective-actions/<int:row_id>',
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

    print('ForgeQC smoke test passed: imports, tables, routes, pulse intelligence, CAPA assistant, and core pages are alive.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ForgeQC smoke test failed: {exc}', file=sys.stderr)
        raise
