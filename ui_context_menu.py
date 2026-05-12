import forgeqc_app


CONTEXT_CSS = """
.ctx-menu{position:fixed;z-index:9999;display:none;min-width:260px;background:#0b1117;border:1px solid #32465a;border-radius:12px;box-shadow:0 16px 45px rgba(0,0,0,.45);padding:8px;color:#e8eef5}
.ctx-menu.open{display:block}.ctx-menu .ctx-title{font-size:12px;color:#95a4b5;padding:8px 10px;border-bottom:1px solid #263647;margin-bottom:6px}.ctx-menu button,.ctx-menu a{display:block;width:100%;box-sizing:border-box;text-align:left;background:transparent;border:0;color:#dce7f2;text-decoration:none;padding:8px 10px;border-radius:8px;font:14px Segoe UI,Arial;cursor:pointer}.ctx-menu button:hover,.ctx-menu a:hover{background:#172433;color:#fff}.ctx-sep{height:1px;background:#263647;margin:6px 4px}.ctx-muted{font-size:12px;color:#95a4b5;padding:6px 10px}
"""


CONTEXT_HTML = r"""
<div id="ctx-menu" class="ctx-menu" role="menu" aria-hidden="true">
  <div class="ctx-title" id="ctx-title">ForgeQC</div>
  <a data-ctx="module" href="/">Dashboard</a>
  <a data-ctx="module" href="/quoting">Quoting Resources</a>
  <a data-ctx="module" href="/materials">Approved Materials</a>
  <a data-ctx="module" href="/workorders">Work Orders</a>
  <a data-ctx="module" href="/planning">Planning / Purchasing</a>
  <a data-ctx="module" href="/metrics">Metrics</a>
  <div class="ctx-sep"></div>
  <button type="button" data-action="copy">Copy</button>
  <button type="button" data-action="cut">Cut</button>
  <button type="button" data-action="paste">Paste</button>
  <button type="button" data-action="selectAll">Select All</button>
  <div class="ctx-sep"></div>
  <div class="ctx-muted" id="ctx-breadcrumb">/</div>
</div>
<script>
(function(){
  const menu = document.getElementById('ctx-menu');
  const title = document.getElementById('ctx-title');
  const breadcrumb = document.getElementById('ctx-breadcrumb');
  let target = null;
  function labelForPath(path){
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
    if(path.startsWith('/quoting') || path.startsWith('/bom') || path.startsWith('/quote-materials')) ['/quoting','/materials','/planning'].forEach(x=>show.add(x));
    else if(path.startsWith('/workorders') || path.startsWith('/planning')) ['/workorders','/planning','/materials','/clocking'].forEach(x=>show.add(x));
    else if(path.startsWith('/rma')) ['/rma','/metrics','/workorders'].forEach(x=>show.add(x));
    else ['/quoting','/materials','/workorders','/planning'].forEach(x=>show.add(x));
    links.forEach(a => a.style.display = show.has(a.getAttribute('href')) ? 'block' : 'none');
  }
  function showMenu(e){
    target = e.target;
    title.textContent = labelForPath(location.pathname) + ' - Related Actions';
    breadcrumb.textContent = 'Breadcrumb: ' + (location.pathname || '/') + (target && target.tagName ? ' | ' + target.tagName.toLowerCase() : '');
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
  document.addEventListener('contextmenu', function(e){e.preventDefault();showMenu(e);});
  document.addEventListener('click', function(e){if(!menu.contains(e.target)) hideMenu();});
  document.addEventListener('keydown', function(e){if(e.key === 'Escape') hideMenu();});
  menu.addEventListener('click', async function(e){
    const action = e.target.getAttribute('data-action');
    if(!action) return;
    if(target && (target.matches('input, textarea') || target.isContentEditable)) target.focus();
    try{
      if(action === 'copy') document.execCommand('copy');
      if(action === 'cut') document.execCommand('cut');
      if(action === 'paste') document.execCommand('paste');
      if(action === 'selectAll') document.execCommand('selectAll');
    }catch(err){console.warn('Context action blocked by browser security:', err);}
    hideMenu();
  });
})();
</script>
"""


def install():
    if 'ctx-menu' not in forgeqc_app.CSS:
        forgeqc_app.CSS += CONTEXT_CSS
    if 'id="ctx-menu"' not in forgeqc_app.BASE:
        forgeqc_app.BASE = forgeqc_app.BASE.replace('</body>', CONTEXT_HTML + '</body>')
