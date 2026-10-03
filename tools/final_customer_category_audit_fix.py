from pathlib import Path
import re

HTML = Path('app/src/main/assets/index.html')
s = HTML.read_text(encoding='utf-8')

# Remove the known category-cleanup patches that mutate the same DOM and can
# duplicate labels or fight the original click handlers.
for ident in (
    'categoryDuplicateCleanupFinalCss',
    'categoryDuplicateCleanupFinal',
    'categoryFinalCleanV2Css',
    'categoryFinalCleanV2Script',
):
    s = re.sub(
        rf'<(?:style|script)\s+id=["\']{re.escape(ident)}["\'][^>]*>.*?</(?:style|script)>',
        '', s, flags=re.I | re.S,
    )

# Remove the embedded category-image DOM observer patch. Category buttons must
# be controlled by one stable renderer instead of multiple observers.
s = re.sub(
    r'<script[^>]*>.*?skEmbeddedLabel.*?</script>',
    '', s, flags=re.I | re.S,
)

# Replace the category bar with exactly one authoritative set of buttons.
cats = '''<div id="cats" class="cats" aria-label="Food categories">
<button class="cat active" type="button" data-category="all">🍽️ All</button>
<button class="cat" type="button" data-category="fast">🍕 Fast Food</button>
<button class="cat" type="button" data-category="snacks">🥟 Snacks</button>
<button class="cat" type="button" data-category="chaat">🥣 Chaat &amp; Special</button>
<button class="cat" type="button" data-category="thali">🍛 Indian Thali</button>
<button class="cat" type="button" data-category="desirsoi">🥘 Desi Rasoi</button>
<button class="cat" type="button" data-category="birthday">🎂 Birthday Special</button>
<button class="cat" type="button" data-category="beverages">🥤 Beverages</button>
<button class="cat" type="button" data-category="sweets">🍬 Sweets</button>
<button class="cat restaurantBtn" type="button" data-category="restaurants">🏨 Restaurant / Hotel</button>
</div>'''
s, n = re.subn(r'<div\s+id=["\']cats["\'][^>]*>.*?</div>', cats, s, count=1, flags=re.I | re.S)
if n != 1:
    raise RuntimeError('Could not replace the customer category bar')

# One small, deterministic controller. It uses the existing product renderer
# when available and then scrolls to the actual rendered section. No observers,
# no repeated DOM rewrites, and no replacement of product/cart/order logic.
css = '''<style id="skStableCategoryCss">
#cats{display:flex!important;align-items:center!important;gap:8px!important;overflow-x:auto!important;overflow-y:hidden!important;padding:10px 12px!important;position:relative!important;top:auto!important;z-index:15!important;scrollbar-width:none!important;background:#fff!important}
#cats::-webkit-scrollbar{display:none!important}
#cats .cat{display:inline-flex!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;min-height:44px!important;width:auto!important;padding:9px 13px!important;border-radius:12px!important;border:1px solid #eadfce!important;background:#fffaf1!important;color:#21170f!important;font-size:11px!important;font-weight:900!important;white-space:nowrap!important;cursor:pointer!important}
#cats .cat.active{background:#f6c94a!important;border-color:#f6c94a!important;color:#17100b!important;box-shadow:0 3px 10px #d99d1844!important}
body.dark #cats,body.dark-theme #cats,body[data-theme="dark"] #cats,html.dark #cats,html[data-theme="dark"] #cats{background:#17120f!important;border-bottom-color:#3a3028!important}
body.dark #cats .cat,body.dark-theme #cats .cat,body[data-theme="dark"] #cats .cat,html.dark #cats .cat,html[data-theme="dark"] #cats .cat{background:#241c17!important;border-color:#4a3b30!important;color:#f7eee5!important}
body.dark #cats .cat.active,body.dark-theme #cats .cat.active,body[data-theme="dark"] #cats .cat.active,html.dark #cats .cat.active,html[data-theme="dark"] #cats .cat.active{background:#f6c94a!important;border-color:#f6c94a!important;color:#17100b!important}
</style>'''

js = '''<script id="skStableCategoryController">
(function(){
  'use strict';
  if(window.__SK_STABLE_CATEGORY_CONTROLLER__) return;
  window.__SK_STABLE_CATEGORY_CONTROLLER__=true;
  var map={all:'All',fast:'Fast Food',snacks:'Snacks',chaat:'Chaat & Special',thali:'Indian Thali',desirsoi:'Desi Rasoi',birthday:'Birthday Special',beverages:'Beverages',sweets:'Sweets'};
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').replace(/\\s+/g,' ').trim();}
  function sectionFor(key){
    var wanted=norm(map[key]||'');
    var sections=document.querySelectorAll('#sections .section,#sections [data-category]');
    for(var i=0;i<sections.length;i++){
      var el=sections[i];
      var dc=norm(el.getAttribute('data-category')||'');
      if(dc && (dc===wanted || dc===norm(key))) return el;
      var h=el.querySelector('h2,h3');
      if(h && norm(h.textContent).indexOf(wanted)>=0) return el;
    }
    return null;
  }
  function activate(btn){
    document.querySelectorAll('#cats .cat').forEach(function(b){b.classList.toggle('active',b===btn);});
  }
  function choose(key,btn){
    activate(btn);
    if(key==='restaurants'){
      if(typeof window.openRestaurants==='function') window.openRestaurants();
      return;
    }
    try{ if(typeof window.selectCategory==='function') window.selectCategory(key); }catch(e){}
    var tries=0;
    function jump(){
      var el=key==='all' ? document.querySelector('#sections .section') : sectionFor(key);
      if(el){el.scrollIntoView({behavior:'smooth',block:'start'});return;}
      if(tries++<12) setTimeout(jump,100);
    }
    setTimeout(jump,30);
  }
  function bind(){
    var root=document.getElementById('cats');
    if(!root || root.getAttribute('data-stable-bound')==='1') return;
    root.setAttribute('data-stable-bound','1');
    root.addEventListener('click',function(e){
      var btn=e.target.closest('.cat');
      if(!btn || !root.contains(btn)) return;
      e.preventDefault();e.stopPropagation();
      choose(btn.getAttribute('data-category')||'all',btn);
    },true);
  }
  function start(){bind();}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
  setTimeout(bind,500);setTimeout(bind,1500);
})();
</script>'''

# Insert immediately before body close so it is loaded after the original UI
# functions and becomes the final category event handler.
marker='</body>'
pos=s.lower().rfind(marker)
if pos < 0:
    raise RuntimeError('No </body> found')
s=s[:pos]+css+js+s[pos:]
HTML.write_text(s,encoding='utf-8')
print('FINAL_CUSTOMER_CATEGORY_AUDIT_FIX_APPLIED')