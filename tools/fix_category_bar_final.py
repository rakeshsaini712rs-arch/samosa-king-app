from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text(encoding='utf-8')

# Remove old category-bar/photo patch blocks so this build has one cleanup layer only.
for style_id in ('categoryPhotoEmbeddedFinalCss', 'skRemoveCategoryBar', 'categoryPhotoRemovedFinalCss'):
    marker = f'<style id="{style_id}">'
    start = s.find(marker)
    if start >= 0:
        end = s.find('</style>', start)
        if end >= 0:
            s = s[:start] + s[end + len('</style>'):]

for script_id in ('categoryPhotoEmbeddedFinal', 'categoryDuplicateCleanupFinal'):
    marker = f'<script id="{script_id}">'
    start = s.find(marker)
    if start >= 0:
        end = s.find('</script>', start)
        if end >= 0:
            s = s[:start] + s[end + len('</script>'):]

# One stable category-bar cleanup: keep exactly one button per category and
# remove duplicated/generated "category" text from labels. Do not touch products,
# banners, cart, orders, payment, location, or other app UI.
css = '''<style id="categoryDuplicateCleanupFinalCss">
#cats{display:flex!important;overflow-x:auto!important;overflow-y:hidden!important;gap:8px!important;padding:10px 12px!important;visibility:visible!important;opacity:1!important;min-height:0!important}
#cats .cat{display:flex!important;flex:0 0 auto!important;width:auto!important;height:auto!important;min-height:44px!important;padding:9px 12px!important;box-sizing:border-box!important;flex-direction:row!important;align-items:center!important;justify-content:center!important;gap:0!important;overflow:hidden!important;visibility:visible!important;opacity:1!important}
#cats .skCategoryLabel{display:block!important;padding:0!important;text-align:center!important;font-size:11px!important;line-height:1.15!important;font-weight:900!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
</style>'''

js = '''<script id="categoryDuplicateCleanupFinal">
(function(){
  if(window.__SK_CATEGORY_DUPLICATE_CLEANUP_V1__) return;
  window.__SK_CATEGORY_DUPLICATE_CLEANUP_V1__=true;
  var names=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\\s+/g,' ')}
  function categoryKey(v){
    var t=norm(v).replace(/\\bcategory\\b/g,' ').replace(/\\s+/g,' ').trim();
    for(var i=0;i<names.length;i++){
      var n=norm(names[i]);
      if(t===n || t.indexOf(n)>=0 || n.indexOf(t)>=0) return n;
    }
    return t;
  }
  function clean(){
    var root=document.getElementById('cats')||document.querySelector('.cats');
    if(!root) return;
    var seen={};
    Array.prototype.slice.call(root.querySelectorAll('.cat')).forEach(function(c){
      var label=c.getAttribute('data-label')||c.textContent||'';
      var k=categoryKey(label);
      if(!k) return;
      if(seen[k]) { c.remove(); return; }
      seen[k]=true;
      c.setAttribute('data-label',names.find(function(n){return norm(n)===k})||label.replace(/\\bcategory\\b/ig,' ').replace(/\\s+/g,' ').trim());
    });
  }
  function run(){clean();[100,400,900,1800,3500,7000].forEach(function(t){setTimeout(clean,t)});}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  new MutationObserver(function(){clearTimeout(window.__skCategoryCleanTimer);window.__skCategoryCleanTimer=setTimeout(clean,80)}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''

head = s.lower().rfind('</head>')
if head < 0:
    raise RuntimeError('index.html has no </head> marker')
s = s[:head] + css + js + s[head:]
html.write_text(s, encoding='utf-8')
print('CATEGORY_DUPLICATES_REMOVED_FINAL_V1: one category button per category; duplicate/generated category text removed')
