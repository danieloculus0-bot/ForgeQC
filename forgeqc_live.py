from flask import redirect

from forgeqc_quote_bom import create_app as create_quote_app, BOMLine, QuoteResource
from material_quote_engine import register as register_material_routes, resolve_material_assignment, QuoteMaterialAssignment
from forgeqc_app import db, log


def sync_quote_material_assignments(upload_id):
    quote = QuoteResource.query.filter_by(bom_upload_id=upload_id).first()
    if not quote:
        return 0

    created = 0
    lines = BOMLine.query.filter_by(upload_id=upload_id).all()
    for line in lines:
        if not line.material and not line.description and not line.part_number:
            continue
        existing = QuoteMaterialAssignment.query.filter_by(quote_id=quote.id, bom_line_id=line.id).first()
        if existing:
            continue
        material_key = line.material or line.description or line.part_number
        resolve_material_assignment(
            quote_id=quote.id,
            bom_line_id=line.id,
            material_key=material_key,
            required_qty=line.quantity or 1,
            quote_length=0,
        )
        created += 1
    if created:
        log('Quote', 'Material assignments created', f'{quote.quote_number}: {created} BOM line(s) resolved against catalog/history')
    return created


def create_app():
    app = create_quote_app()
    register_material_routes(app)

    with app.app_context():
        db.create_all()

    original_view = app.view_functions.get('bom_review')

    if original_view:
        def bom_review_with_material_sync(upload_id):
            response = original_view(upload_id)
            if getattr(response, 'status_code', None) in (301, 302):
                sync_quote_material_assignments(upload_id)
                db.session.commit()
            return response
        app.view_functions['bom_review'] = bom_review_with_material_sync

    @app.route('/quoting/<int:quote_id>/materials')
    def quote_material_shortcut(quote_id):
        return redirect(f'/quote-materials/{quote_id}')

    return app
