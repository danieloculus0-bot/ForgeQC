import forgeqc_app


CONTEXT_CSS = """
:root{--bg:#071018;--panel:#101922;--panel2:#121f2b;--line:#26384a;--text:#eaf2fb;--muted:#98aabd;--accent:#4ea1d8;--good:#5fc48a;--warn:#d8aa4e;--bad:#d86b6b;--shadow:0 18px 55px rgba(0,0,0,.35)}
*{scrollbar-color:#33485c #0b131c;scrollbar-width:thin}body{background:radial-gradient(circle at 20% 0%,#12283a 0,#071018 34%,#060b10 100%);color:var(--text);font:14px/1.45 Segoe UI,Arial,sans-serif}aside{width:236px;background:linear-gradient(180deg,#071018,#080d12 70%);border-right:1px solid var(--line);padding:20px 16px;box-shadow:10px 0 35px rgba(0,0,0,.18)}.brand{font-size:24px;letter-spacing:.3px;font-weight:800;margin:0 0 18px;color:#fff}.brand:after{content:'Quality Command';display:block;margin-top:3px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:600}nav{display:grid;gap:4px}nav a{display:block;color:#a8b8c8;text-decoration:none;padding:9px 11px;border-radius:10px;border:1px solid transparent}nav a:hover{background:#132331;color:#fff;border-color:#24384c}main{margin-left:236px;padding:24px 26px 44px;max-width:1580px}h1{font-size:26px;letter-spacing:.2px;margin:0 0 18px}h2{font-size:16px;margin:0 0 12px;color:#f5f9ff}.cards{grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:14px}.card,section{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:var(--shadow)}.card span{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}.card b{font-size:28px;line-height:1.1;margin:7px 0 10px}.notice{border:1px solid #2c4a62;border-left:5px solid var(--accent);background:linear-gradient(90deg,#102335,#101923);padding:12px 14px;border-radius:12px;color:#d7e5f2;box-shadow:0 10px 30px rgba(0,0,0,.2)}table{border-collapse:separate;border-spacing:0;width:100%;overflow:hidden;border-radius:14px;border:1px solid var(--line);background:#101922}th,td{border-bottom:1px solid #223344;padding:9px 10px;text-align:left;vertical-align:top}tr:last-child td{border-bottom:0}th{position:sticky;top:0;background:#0d1721;color:#a9bbca;font-size:12px;letter-spacing:.06em;text-transform:uppercase}tr:hover td{background:#132130}input,select,textarea{background:#08131d;color:var(--text);border:1px solid #2c4054;border-radius:10px;padding:9px 10px;width:100%;outline:none;transition:border-color .12s ease,box-shadow .12s ease,background .12s ease}input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(78,161,216,.18);background:#0b1722}textarea{min-height:96px;resize:vertical}.form{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:13px}.wide{grid-column:1/-1}label{color:#bfd0df;font-size:13px;font-weight:600}label input,label select,label textarea{margin-top:5px}.btn,button{background:linear-gradient(180deg,#4ea1d8,#347da9);color:white;border:1px solid #5dade3;border-radius:10px;padding:9px 13px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;cursor:pointer;font-weight:700;box-shadow:0 8px 20px rgba(30,105,150,.24)}.btn:hover,button:hover{filter:brightness(1.08)}.toolbar{display:flex;gap:10px;margin-bottom:14px;align-items:center;flex-wrap:wrap}.muted{color:var(--muted)}a{color:#8ed2ff}.badge{display:inline-flex;align-items:center;border-radius:999px;padding:3px 8px;font-size:12px;font-weight:700;border:1px solid #35506a;background:#152638;color:#dceeff}.badge.open,.badge.draft,.badge.submitted{border-color:#6b5b31;background:#2a2415;color:#ffd98a}.badge.approved,.badge.closed,.badge.resolved{border-color:#2d6948;background:#14281d;color:#8df0b5}.badge.rejected,.badge.critical,.badge.high{border-color:#723a3a;background:#2a1717;color:#ffaaaa}.ctx-menu{position:fixed;z-index:9999;display:none;min-width:270px;background:#08131d;border:1px solid #32465a;border-radius:14px;box-shadow:0 18px 55px rgba(0,0,0,.5);padding:8px;color:#e8eef5}.ctx-menu.open{display:block}.ctx-menu .ctx-title{font-size:12px;color:#a8bacb;padding:8px 10px;border-bottom:1px solid #263647;margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em}.ctx-menu a{display:block;width:100%;box-sizing:border-box;text-align:left;background:transparent;border:0;color:#dce7f2;text-decoration:none;padding:8px 10px;border-radius:9px;font:14px Segoe UI,Arial;cursor:pointer;box-shadow:none}.ctx-menu a:hover{background:#172433;color:#fff}.ctx-sep{height:1px;background:#263647;margin:6px 4px}.ctx-muted{font-size:12px;color:#95a4b5;padding:6px 10px}
@media(max-width:900px){aside{position:relative;width:auto;inset:auto}main{margin-left:0;padding:18px}.cards{grid-template-columns:1fr}.form{grid-template-columns:1fr}}
"""


CONTEXT_HTML = r"""
<div id="ctx-menu" class="ctx-menu" role="menu" aria-hidden="true">
  <div class="ctx-title" id="ctx-title">ForgeQC</div>
  <a data-ctx="module" href="/">Dashboard</a>
  <a data-ctx="module" href="/quality-forms">Quality Forms</a>
  <a data-ctx="module" href="/deviations">Deviation Requests</a>
  <a data-ctx="module" href="/ncr-dmr">NCR / DMR</a>
  <a data-ctx="module" href="/corrective-actions">Corrective Actions</a>
  <a data-ctx="module" href="/quoting">Quoting Resources</a>
  <a data-ctx="module" href="/materials">Approved Materials</a>
  <a data-ctx="module" href="/workorders">Work Orders</a>
  <a data-ctx="module" href="/planning">Planning / Purchasing</a>
  <a data-ctx="module" href="/metrics">Metrics</a>
  <div class="ctx-sep"></div>
  <div class="ctx-muted" id="ctx-breadcrumb">/</div>
</div>
<script>
(function(){
  const menu = document.getElementById('ctx-menu');
  const title = document.getElementById('ctx-title');
  const breadcrumb = document.getElementById('ctx-breadcrumb');
  function labelForPath(path){
    if(path.startsWith('/deviations')) return 'Deviation Requests';
    if(path.startsWith('/ncr-dmr')) return 'NCR / DMR';
    if(path.startsWith('/corrective-actions')) return 'Corrective Actions';
    if(path === '/quality-forms') return 'Quality Forms';
    if(path.startsWith('/quoting/')) return 'Quote Detail';
    if(path === '/quoting') return 'Quoting Resources';
    if(path.startsWith('/bom/')) return 'BOM Review';
    if(path.startsWith('/quote-materials/')) return 'Quote Material Assignments';
    if(path === '/materials') return 'Approved Material Catalog';
    if(path === '/workorders') return 'Work Orders';
    if(path === '/planning') return 'Planning / Purchasing';
    if(path === '/clocking') return 'FPY Clocking';
    if(path === '/efficiency') return 'Operator Efficiency';
    if(path === '/rma') return 'RMA';
    return 'ForgeQC';
  }
  function setRelated(path){
    const links = Array.from(menu.querySelectorAll('[data-ctx="module"]'));
    const show = new Set(['/', '/metrics']);
    if(path.startsWith('/deviations') || path.startsWith('/ncr-dmr') || path.startsWith('/corrective-actions') || path === '/quality-forms') ['/quality-forms','/deviations','/ncr-dmr','/corrective-actions','/rma'].forEach(x=>show.add(x));
    else if(path.startsWith('/quoting') || path.startsWith('/bom') || path.startsWith('/quote-materials')) ['/quoting','/materials','/planning'].forEach(x=>show.add(x));
    else if(path.startsWith('/workorders') || path.startsWith('/planning')) ['/workorders','/planning','/materials','/clocking'].forEach(x=>show.add(x));
    else if(path.startsWith('/rma')) ['/rma','/quality-forms','/metrics','/workorders'].forEach(x=>show.add(x));
    else ['/quality-forms','/quoting','/materials','/workorders','/planning'].forEach(x=>show.add(x));
    links.forEach(a => a.style.display = show.has(a.getAttribute('href')) ? 'block' : 'none');
  }
  function decorate(){
    document.querySelectorAll('td').forEach(td=>{
      const txt = td.textContent.trim().toLowerCase();
      if(['open','draft','submitted','approved','rejected','closed','resolved','critical','high'].includes(txt) && !td.querySelector('.badge')){
        const span = document.createElement('span');
        span.className = 'badge ' + txt.replaceAll(' ','-').replaceAll('/','-');
        span.textContent = td.textContent.trim();
        td.textContent = '';
        td.appendChild(span);
      }
    });
    document.querySelectorAll('input,select,textarea').forEach(el=>{
      if(!el.closest('label') && !el.getAttribute('aria-label')) el.setAttribute('aria-label', el.name || 'Field');
    });
  }
  function showMenu(e){
    title.textContent = labelForPath(location.pathname) + ' - Related';
    breadcrumb.textContent = 'Path: ' + (location.pathname || '/');
    setRelated(location.pathname);
    menu.classList.add('open');
    menu.setAttribute('aria-hidden','false');
    const pad = 12;
    const x = Math.min(e.clientX, window.innerWidth - menu.offsetWidth - pad);
    const y = Math.min(e.clientY, window.innerHeight - menu.offsetHeight - pad);
    menu.style.left = Math.max(pad, x) + 'px';
    menu.style.top = Math.max(pad, y) + 'px';
  }
  function hideMenu(){menu.classList.remove('open');menu.setAttribute('aria-hidden','true');}
  document.addEventListener('DOMContentLoaded', decorate);
  document.addEventListener('contextmenu', function(e){e.preventDefault();showMenu(e);});
  document.addEventListener('click', function(e){if(!menu.contains(e.target)) hideMenu();});
  document.addEventListener('keydown', function(e){if(e.key === 'Escape') hideMenu();});
})();
</script>
"""


def install():
    if 'Quality Command' not in forgeqc_app.CSS:
        forgeqc_app.CSS += CONTEXT_CSS
    if 'id="ctx-menu"' not in forgeqc_app.BASE:
        forgeqc_app.BASE = forgeqc_app.BASE.replace('</body>', CONTEXT_HTML + '</body>')
