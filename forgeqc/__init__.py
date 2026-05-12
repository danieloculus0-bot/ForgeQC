
from pathlib import Path
from datetime import datetime, date
from flask import Flask, request, redirect, send_file, render_template_string
from flask_sqlalchemy import SQLAlchemy
from openpyxl import load_workbook, Workbook

db = SQLAlchemy()

class Customer(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(180),unique=True,nullable=False); active=db.Column(db.Boolean,default=True); description=db.Column(db.Text)
class Department(Customer): __tablename__='department'
class ReasonCode(Customer): __tablename__='reason_code'
class RMA(db.Model):
    id=db.Column(db.Integer,primary_key=True); rma_number=db.Column(db.String(32),unique=True); date_opened=db.Column(db.Date,default=date.today); customer_id=db.Column(db.Integer,db.ForeignKey('customer.id')); order_number=db.Column(db.String(120)); part_number=db.Column(db.String(120)); quantity_affected=db.Column(db.Integer); department_id=db.Column(db.Integer,db.ForeignKey('department.id')); person=db.Column(db.String(180)); defect_description=db.Column(db.Text); reason_code_id=db.Column(db.Integer,db.ForeignKey('reason_code.id')); status=db.Column(db.String(80),default='Open'); disposition=db.Column(db.String(120)); due_date=db.Column(db.Date); closed_date=db.Column(db.Date); notes=db.Column(db.Text); attachment_path=db.Column(db.String(500))
    customer=db.relationship('Customer'); department=db.relationship('Department'); reason_code=db.relationship('ReasonCode')
class NCR(db.Model):
    id=db.Column(db.Integer,primary_key=True); ncr_number=db.Column(db.String(32),unique=True); date_opened=db.Column(db.Date,default=date.today); source=db.Column(db.String(120)); part_number=db.Column(db.String(120)); status=db.Column(db.String(80),default='Open'); description=db.Column(db.Text); notes=db.Column(db.Text)
class DMR(db.Model):
    id=db.Column(db.Integer,primary_key=True); dmr_number=db.Column(db.String(32),unique=True); date_opened=db.Column(db.Date,default=date.today); source_name=db.Column(db.String(120)); part_number=db.Column(db.String(120)); status=db.Column(db.String(80),default='Open'); defect_description=db.Column(db.Text); notes=db.Column(db.Text)
class Deviation(db.Model):
    id=db.Column(db.Integer,primary_key=True); deviation_number=db.Column(db.String(32),unique=True); request_date=db.Column(db.Date,default=date.today); requested_by=db.Column(db.String(180)); customer_id=db.Column(db.Integer,db.ForeignKey('customer.id')); part_number=db.Column(db.String(120)); requirement_deviated_from=db.Column(db.Text); reason_for_deviation=db.Column(db.Text); risk_level=db.Column(db.String(80)); internal_approval_status=db.Column(db.String(80),default='Draft'); effective_end_date=db.Column(db.Date); notes=db.Column(db.Text)
    customer=db.relationship('Customer')
class MoraleSignal(db.Model):
    id=db.Column(db.Integer,primary_key=True); date=db.Column(db.Date,default=date.today); department_id=db.Column(db.Integer,db.ForeignKey('department.id')); signal_type=db.Column(db.String(140)); count_value=db.Column(db.Integer,default=1); severity=db.Column(db.String(40),default='Low'); notes=db.Column(db.Text)
    department=db.relationship('Department')
class ActivityLog(db.Model):
    id=db.Column(db.Integer,primary_key=True); created_at=db.Column(db.DateTime,default=datetime.utcnow); area=db.Column(db.String(80)); action=db.Column(db.String(120)); detail=db.Column(db.Text)

CSS = """body{margin:0;background:#0b1117;color:#e8eef5;font:14px Segoe UI,Arial}aside{position:fixed;inset:0 auto 0 0;width:210px;background:#080d12;border-right:1px solid #263647;padding:18px}.brand{font-size:22px;font-weight:700;margin-bottom:18px}nav a{display:block;color:#95a4b5;text-decoration:none;padding:9px;border-radius:8px}nav a:hover{background:#172433;color:white}main{margin-left:210px;padding:20px}h1{font-size:22px}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card,section{background:#121b24;border:1px solid #263647;border-radius:12px;padding:14px}.card b{display:block;font-size:26px;margin-top:6px}table{width:100%;border-collapse:collapse;background:#121b24;border:1px solid #263647}th,td{border-bottom:1px solid #263647;padding:8px;text-align:left}th{color:#95a4b5}input,select,textarea{background:#0b1117;color:#e8eef5;border:1px solid #263647;border-radius:8px;padding:8px;width:100%}textarea{min-height:90px}.form{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.wide{grid-column:1/-1}.btn,button{background:#3e78a8;color:white;border:0;border-radius:8px;padding:8px 12px;text-decoration:none;display:inline-block}.secondary{background:#4a5563}.toolbar{display:flex;gap:8px;margin-bottom:12px}"""
BASE = """<!doctype html><html><head><title>ForgeQC</title><style>{{css}}</style></head><body><aside><div class='brand'>ForgeQC</div><nav><a href='/'>Dashboard</a><a href='/rma'>RMA</a><a href='/ncr'>NCR</a><a href='/dmr'>DMR</a><a href='/deviation'>Deviations</a><a href='/metrics'>Metrics</a><a href='/morale'>Morale Signals</a><a href='/admin'>Admin</a></nav></aside><main><h1>{{title}}</h1>{{body|safe}}</main></body></html>"""

def page(title, body): return render_template_string(BASE, css=CSS, title=title, body=body)
def d(v):
    if isinstance(v, datetime): return v.date()
    if isinstance(v, date): return v
    try: return datetime.strptime(v,'%Y-%m-%d').date() if v else None
    except Exception: return None
def ref(model, name):
    if name is None or str(name).strip()=='': return None
    name=str(name).strip(); row=model.query.filter_by(name=name).first()
    if not row: row=model(name=name); db.session.add(row); db.session.flush()
    return row
def num(model, field, prefix): return f"{prefix}-{date.today().year}-{model.query.count()+1:04d}"
def log(a,b,c=''): db.session.add(ActivityLog(area=a,action=b,detail=c))

def create_app():
    app=Flask(__name__); root=Path(__file__).resolve().parent.parent
    (root/'data'/'imports').mkdir(parents=True,exist_ok=True); (root/'data'/'exports').mkdir(parents=True,exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{root/'data'/'forgeqc.db'}"; app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        for m,vals in [(Department,['Laser','Tube Laser','Machining','Welding','Forming','Powder','Quality','Shipping']),(ReasonCode,['Wrong revision','Wrong material','Wrong color / finish','Dimensional out of tolerance','Missing feature','Weld defect','Powder coat defect','Damaged']),(Customer,['Internal'])]:
            for v in vals: ref(m,v)
        db.session.commit()

    def activity_table():
        rows=''.join(f"<tr><td>{x.created_at:%m/%d}</td><td>{x.area}</td><td>{x.action}</td><td>{x.detail or ''}</td></tr>" for x in ActivityLog.query.order_by(ActivityLog.id.desc()).limit(20))
        return f"<table><tr><th>Date</th><th>Area</th><th>Action</th><th>Detail</th></tr>{rows}</table>"

    @app.route('/')
    def dashboard():
        cards=''.join(f"<div class='card'><span>{k}</span><b>{v}</b></div>" for k,v in {'Open RMAs':RMA.query.filter(RMA.status!='Closed').count(),'Open NCRs':NCR.query.filter(NCR.status!='Closed').count(),'Open DMRs':DMR.query.filter(DMR.status!='Closed').count(),'Open Deviations':Deviation.query.filter(Deviation.internal_approval_status!='Closed').count()}.items())
        return page('Dashboard',f"<div class='cards'>{cards}</div><br><section><h2>Recent Activity</h2>{activity_table()}</section>")

    def list_page(model,path,title,cols):
        rows=''
        for r in model.query.order_by(model.id.desc()).limit(500):
            rows += '<tr>' + ''.join(f"<td>{getattr(r,c,'') or ''}</td>" for c in cols) + f"<td><a href='/{path}/{r.id}/edit'>Edit</a></td></tr>"
        extra = "<form method='post' action='/rma/import'><button>Import RMA_Tracker.xlsx</button></form><a class='btn secondary' href='/rma/export'>Export</a>" if path=='rma' else ''
        if path=='deviation': extra="<a class='btn secondary' href='/deviation/export'>Export</a>"
        heads=''.join(f"<th>{c.replace('_',' ').title()}</th>" for c in cols)
        return page(title,f"<div class='toolbar'><a class='btn' href='/{path}/new'>New</a>{extra}</div><table><tr>{heads}<th></th></tr>{rows}</table>")
    app.add_url_rule('/rma','rma_list',lambda:list_page(RMA,'rma','RMA',['rma_number','date_opened','order_number','part_number','person','status']))
    app.add_url_rule('/ncr','ncr_list',lambda:list_page(NCR,'ncr','NCR',['ncr_number','date_opened','source','part_number','status']))
    app.add_url_rule('/dmr','dmr_list',lambda:list_page(DMR,'dmr','DMR',['dmr_number','date_opened','source_name','part_number','status']))
    app.add_url_rule('/deviation','dev_list',lambda:list_page(Deviation,'deviation','Deviation Requests',['deviation_number','request_date','requested_by','part_number','risk_level','internal_approval_status']))

    def form(kind,row):
        cust=''.join(f"<option value='{x.id}'>{x.name}</option>" for x in Customer.query.filter_by(active=True))
        dept=''.join(f"<option value='{x.id}'>{x.name}</option>" for x in Department.query.filter_by(active=True))
        reason=''.join(f"<option value='{x.id}'>{x.name}</option>" for x in ReasonCode.query.filter_by(active=True))
        title=getattr(row, kind+'_number', getattr(row,'deviation_number',''))
        body=f"<form method='post' class='form'><h2 class='wide'>{title}</h2><label>Date<input type='date' name='date'></label><label>Customer<select name='customer_id'><option></option>{cust}</select></label><label>Department<select name='department_id'><option></option>{dept}</select></label><label>Reason<select name='reason_code_id'><option></option>{reason}</select></label><label>Order/Job<input name='order'></label><label>Part<input name='part_number'></label><label>Person/Requested By<input name='person'></label><label>Status<input name='status' value='Open'></label><label class='wide'>Description / Requirement<textarea name='description'></textarea></label><label class='wide'>Notes<textarea name='notes'></textarea></label><button>Save</button></form>"
        return page(kind.upper()+' Form',body)

    def save(kind,row):
        f=request.form
        if hasattr(row,'date_opened'): row.date_opened=d(f.get('date')) or row.date_opened
        if hasattr(row,'request_date'): row.request_date=d(f.get('date')) or row.request_date
        if hasattr(row,'customer_id'): row.customer_id=int(f['customer_id']) if f.get('customer_id') else None
        if hasattr(row,'department_id'): row.department_id=int(f['department_id']) if f.get('department_id') else None
        if hasattr(row,'reason_code_id'): row.reason_code_id=int(f['reason_code_id']) if f.get('reason_code_id') else None
        if hasattr(row,'part_number'): row.part_number=f.get('part_number')
        if hasattr(row,'status'): row.status=f.get('status') or 'Open'
        if hasattr(row,'internal_approval_status'): row.internal_approval_status=f.get('status') or 'Draft'
        if kind=='rma': row.order_number=f.get('order'); row.person=f.get('person'); row.defect_description=f.get('description')
        if kind=='ncr': row.source=f.get('order'); row.description=f.get('description')
        if kind=='dmr': row.source_name=f.get('order'); row.defect_description=f.get('description')
        if kind=='deviation': row.requested_by=f.get('person'); row.requirement_deviated_from=f.get('description')
        row.notes=f.get('notes')

    def edit(model,kind,field,prefix,path,row_id=None):
        row=model.query.get(row_id) if row_id else model(**{field:num(model,field,prefix)})
        if request.method=='POST':
            save(kind,row); db.session.add(row); log(kind.upper(),'Save',getattr(row,field)); db.session.commit(); return redirect('/'+path)
        return form(kind,row)
    for url,model,kind,field,prefix in [('/rma',RMA,'rma','rma_number','RMA'),('/ncr',NCR,'ncr','ncr_number','NCR'),('/dmr',DMR,'dmr','dmr_number','DMR'),('/deviation',Deviation,'deviation','deviation_number','DEV')]:
        app.add_url_rule(url+'/new',kind+'_new',lambda model=model,kind=kind,field=field,prefix=prefix,url=url: edit(model,kind,field,prefix,url.strip('/')),methods=['GET','POST'])
        app.add_url_rule(url+'/<int:row_id>/edit',kind+'_edit',lambda row_id,model=model,kind=kind,field=field,prefix=prefix,url=url: edit(model,kind,field,prefix,url.strip('/'),row_id),methods=['GET','POST'])

    @app.route('/rma/import',methods=['POST'])
    def import_rma():
        path=root/'data'/'imports'/'RMA_Tracker.xlsx'; wb=load_workbook(path,data_only=True); imported=skipped=0
        for sheet,model in [('Customer List',Customer),('Department List',Department),('Reason Codes',ReasonCode)]:
            if sheet in wb.sheetnames:
                for (v,) in wb[sheet].iter_rows(min_row=2,max_col=1,values_only=True): ref(model,v)
        for row in wb['RMA Log'].iter_rows(min_row=2,values_only=True):
            dte,order,cust,dept,person,desc,reason=(list(row)+[None]*7)[:7]
            if not any([dte,order,cust,dept,person,desc,reason]): skipped+=1; continue
            c=ref(Customer,cust); dep=ref(Department,dept); rc=ref(ReasonCode,reason)
            if RMA.query.filter_by(date_opened=d(dte),order_number=str(order) if order else None,person=str(person) if person else None).first(): skipped+=1; continue
            db.session.add(RMA(rma_number=num(RMA,'rma_number','RMA'),date_opened=d(dte),customer_id=c.id if c else None,order_number=str(order) if order else None,department_id=dep.id if dep else None,person=str(person) if person else None,defect_description=str(desc) if desc else None,reason_code_id=rc.id if rc else None,status='Open')); imported+=1
        log('RMA','Import',f'Imported {imported}; skipped {skipped}'); db.session.commit(); return redirect('/rma')

    def export_xlsx(filename,headers,rows):
        wb=Workbook(); ws=wb.active; ws.append(headers)
        for row in rows: ws.append(row)
        path=root/'data'/'exports'/filename; wb.save(path); return send_file(path,as_attachment=True)
    @app.route('/rma/export')
    def export_rma(): return export_xlsx('rma_export.xlsx',['RMA','Date','Order','Part','Person','Status'],[[r.rma_number,r.date_opened,r.order_number,r.part_number,r.person,r.status] for r in RMA.query.all()])
    @app.route('/deviation/export')
    def export_dev(): return export_xlsx('deviation_export.xlsx',['Deviation','Date','Part','Risk','Status'],[[r.deviation_number,r.request_date,r.part_number,r.risk_level,r.internal_approval_status] for r in Deviation.query.all()])

    @app.route('/admin',methods=['GET','POST'])
    def admin():
        models={'customers':Customer,'departments':Department,'reason_codes':ReasonCode}
        if request.method=='POST':
            db.session.add(models[request.form['table']](name=request.form['name'],description=request.form.get('description'),active=True)); db.session.commit(); return redirect('/admin')
        body=''
        for name,m in models.items():
            rows=''.join(f'<tr><td>{r.name}</td><td>{r.description or ""}</td><td>{r.active}</td></tr>' for r in m.query.order_by(m.name))
            body+=f"<section><h2>{name}</h2><form method='post'><input type='hidden' name='table' value='{name}'><input name='name' placeholder='Name'><input name='description' placeholder='Description'><button>Add</button></form><table>{rows}</table></section><br>"
        return page('Admin Reference Data',body)

    @app.route('/morale',methods=['GET','POST'])
    def morale():
        if request.method=='POST':
            db.session.add(MoraleSignal(date=d(request.form.get('date')),signal_type=request.form.get('signal_type'),count_value=int(request.form.get('count_value') or 1),severity=request.form.get('severity') or 'Low',notes=request.form.get('notes'))); db.session.commit(); return redirect('/morale')
        rows=''.join(f'<tr><td>{r.date}</td><td>{r.signal_type}</td><td>{r.count_value}</td><td>{r.severity}</td></tr>' for r in MoraleSignal.query.order_by(MoraleSignal.id.desc()))
        return page('Morale Signals',f"<form method='post' class='form'><label>Date<input type='date' name='date'></label><label>Signal<input name='signal_type'></label><label>Count<input name='count_value' value='1'></label><label>Severity<select name='severity'><option>Low</option><option>Medium</option><option>High</option></select></label><label class='wide'>Notes<textarea name='notes'></textarea></label><button>Save</button></form><table>{rows}</table>")

    @app.route('/metrics')
    def metrics():
        rows=''.join(f'<tr><td>{c.name if c else "Unassigned"}</td><td>{n}</td></tr>' for c,n in db.session.query(Customer,db.func.count(RMA.id)).join(RMA,isouter=True).group_by(Customer.id).all())
        return page('Metrics',f'<section><h2>RMA by Customer</h2><table>{rows}</table></section>')
    return app
