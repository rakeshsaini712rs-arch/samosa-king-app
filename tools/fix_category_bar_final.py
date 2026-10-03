from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text(encoding='utf-8')

# Remove previous category cleanup layers created by this tool.
for tag, ident in [('style','categoryDuplicateCleanupFinalCss'),('script','categoryDuplicateCleanupFinal'),('style','categoryFinalCleanCss'),('script','categoryFinalCleanScript')]:
    marker = f'<{tag} id="{ident}">'
    while True:
        start = s.find(marker)
        if start < 0:
            break
        end = s.find(f'</{tag}>', start)
        if end < 0:
            break
        s = s[:start] + s[end + len(f'</{tag}>'):]

css = '''<style id="categoryDuplicateCleanupFinalCss">
#cats{display:flex!important;overflow-x:auto!important;overflow-y:hidden!important;gap:8px!important;padding:10px 12px!important;visibility:visible!important;opacity:1!important}
#cats .cat{display:flex!important;flex:0 0 auto!important;width:auto!important;min-height:44px!important;padding:8px 12px!important;box-sizing:border-box!important;align-items:center!important;justify-content:center!important;gap:7px!important;white-space:nowrap!important;overflow:hidden!important}
#cats .cat img{width:34px!important;height:34px!important;object-fit:cover!important;border-radius:9px!important;display:block!important;flex:0 0 auto!important}
#cats .cat .skCategoryLabel{display:block!important;padding:0!important;text-align:center!important;font-size:11px!important;line-height:1.15!important;font-weight:900!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
</style>'''

js = '''<script id="categoryDuplicateCleanupFinal">
(function(){
  if(window.__SK_CATEGORY_SOURCE_FIX_V2__) return;
  window.__SK_CATEGORY_SOURCE_FIX_V2__=true;
  var names=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\\s+/g,' ')}
  function getIndex(v){
    var t=norm(v).replace(/\\bcategory\\b/g,' ').replace(/\\s+/g,' ').trim();
    for(var i=0;i<names.length;i++){
      var n=norm(names[i]);
      if(t===n || t.indexOf(n)>=0 || n.indexOf(t)>=0) return i;
    }
    return -1;
  }
  function rebuildButton(c,i){
    var label=names[i];
    var img=c.querySelector('img');
    // Remove every text/label source that can produce "categoryAll" etc.
    Array.prototype.slice.call(c.childNodes).forEach(function(node){
      if(node!==img) c.removeChild(node);
    });
    var span=document.createElement('span');
    span.className='skCategoryLabel';
    span.textContent=label;
    c.appendChild(span);
    c.setAttribute('data-label',label);
    c.setAttribute('aria-label',label);
    c.title=label;
  }
  function clean(){
    var root=document.getElementById('cats')||document.querySelector('.cats');
    if(!root) return;
    var buttons=Array.prototype.slice.call(root.querySelectorAll('.cat'));
    var chosen=new Array(names.length);
    buttons.forEach(function(c){
      var raw=c.getAttribute('data-label')||c.textContent||c.getAttribute('aria-label')||'';
      var i=getIndex(raw);
      if(i<0){c.remove();return;}
      if(chosen[i]){c.remove();return;}
      chosen[i]=c;
      rebuildButton(c,i);
    });
    // Exact requested order, without creating extra buttons.
    names.forEach(function(_,i){if(chosen[i])root.appendChild(chosen[i]);});
  }
  function run(){clean();[100,400,900,1800,3500,7000].forEach(function(t){setTimeout(clean,t)});}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  new MutationObserver(function(){clearTimeout(window.__skCategoryCleanTimer);window.__skCategoryCleanTimer=setTimeout(clean,80)}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''

head=s.lower().rfind('</head>')
if head<0: raise RuntimeError('index.html has no </head> marker')
s=s[:head]+css+js+s[head:]
html.write_text(s,encoding='utf-8')
print('CATEGORY_SOURCE_FIX_V2: rebuild each button to exactly one clean label; preserve image and click handler; exact order; remove duplicates')
