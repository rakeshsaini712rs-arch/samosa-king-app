from pathlib import Path
import re

HTML = Path('app/src/main/assets/index.html')
s = HTML.read_text(encoding='utf-8')

# Remove every known category patch/observer before installing one controller.
ids = [
    'categoryDuplicateCleanupFinalCss','categoryDuplicateCleanupFinal',
    'categoryFinalCleanV2Css','categoryFinalCleanV2Script',
    'skRealCategoryPhotoStyle','skRealCategoryPhotoScript',
    'skCategoryPhotoDedupV2','skCategoryPhotoDedupV2Script',
    'skCategoryPhotoMatchV3','skCategoryPhotoMatchV3Script',
    'skCategoryPhotoMatchV4','skCategoryPhotoMatchV4Script',
    'skCategoryPhotoFinalStyle','skCategoryPhotoFinalScript',
    'skCategoryPhotoGuaranteedStyle','skCategoryPhotoGuaranteedScript',
    'customerCategoryPhotoDedupStyle','customerCategoryPhotoDedupScript',
    'categoryPhotoEmbeddedFinal','categoryPhotoEmbeddedFinalStyle',
    'skStableCategoryCss','skStableCategoryController',
]
for ident in ids:
    pat = r'<(?:style|script)\b[^>]*\bid=["\']' + re.escape(ident) + r'["\'][^>]*>.*?</(?:style|script)>'
    s = re.sub(pat, '', s, flags=re.I | re.S)

def strip_bad_script(m):
    b = m.group(0).lower()
    markers = ('skcatphoto','skcategoryphoto','categoryphotoembedded','categoryfinalclean','categoryduplicatecleanup','skembeddedlabel')
    if any(x in b for x in markers):
        return ''
    if 'mutationobserver' in b and ('#cats' in b or 'category' in b):
        return ''
    return m.group(0)
s = re.sub(r'<script\b[^>]*>.*?</script>', strip_bad_script, s, flags=re.I | re.S)

cats = '''<div id="cats" class="cats" aria-label="Food categories">
<button class="cat active" type="button" data-category="all">All</button>
<button class="cat" type="button" data-category="fast">Fast Food</button>
<button class="cat" type="button" data-category="snacks">Snacks</button>
<button class="cat" type="button" data-category="chaat">Chaat &amp; Special</button>
<button class="cat" type="button" data-category="thali">Indian Thali</button>
<button class="cat" type="button" data-category="desirsoi">Desi Rasoi</button>
<button class="cat" type="button" data-category="birthday">Birthday Special</button>
<button class="cat" type="button" data-category="beverages">Beverages</button>
<button class="cat" type="button" data-category="sweets">Sweets</button>
<button class="cat" type="button" data-category="restaurants">Restaurant / Hotel</button>
</div>'''
s, n = re.subn(r'<div\s+id=["\']cats["\'][^>]*>.*?</div>', cats, s, count=1, flags=re.I | re.S)
if n != 1:
    raise RuntimeError('Could not replace customer category bar')

css = '''<style id="skStableCategoryCss">
#cats{display:flex!important;align-items:center!important;gap:8px!important;overflow-x:auto!important;overflow-y:hidden!important;padding:10px 12px!important;position:relative!important;top:auto!important;z-index:15!important;scrollbar-width:none!important;background:#17120f!important;border-bottom:1px solid #3a3028!important}
#cats::-webkit-scrollbar{display:none!important}
#cats .cat{display:inline-flex!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;min-height:44px!important;padding:9px 13px!important;border-radius:12px!important;border:1px solid #4a3b30!important;background:#241c17!important;color:#f7eee5!important;font-size:11px!important;font-weight:900!important;white-space:nowrap!important;cursor:pointer!important}
#cats .cat.active{background:#f6c94a!important;border-color:#f6c94a!important;color:#17100b!important;box-shadow:0 3px 10px #d99d1844!important}
</style>'''

js = '''<script id="skStableCategoryController">
(function(){
'use strict';
if(window.__SK_STABLE_CATEGORY_CONTROLLER__)return;
window.__SK_STABLE_CATEGORY_CONTROLLER__=true;
var names={all:'All',fast:'Fast Food',snacks:'Snacks',chaat:'Chaat & Special',thali:'Indian Thali',desirsoi:'Desi Rasoi',birthday:'Birthday Special',beverages:'Beverages',sweets:'Sweets'};
function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').replace(/\s+/g,' ').trim();}
function sectionFor(key){
 var wanted=norm(names[key]||'');
 var all=document.querySelectorAll('#sections .section,#sections [data-category]');
 for(var i=0;i<all.length;i++){
  var el=all[i],dc=norm(el.getAttribute('data-category')||'');
  if(dc&&(dc===wanted||dc===norm(key)))return el;
  var h=el.querySelector('h2,h3');
  if(h&&norm(h.textContent).indexOf(wanted)>=0)return el;
 }
 return null;
}
function activate(btn){document.querySelectorAll('#cats .cat').forEach(function(b){b.classList.toggle('active',b===btn);});}
function choose(key,btn){
 activate(btn);
 if(key==='restaurants'){if(typeof window.openRestaurants==='function')window.openRestaurants();return;}
 try{if(typeof window.selectCategory==='function')window.selectCategory(key);}catch(e){}
 var tries=0;
 function jump(){var el=key==='all'?document.querySelector('#sections .section'):sectionFor(key);if(el){el.scrollIntoView({behavior:'smooth',block:'start'});return;}if(tries++<10)setTimeout(jump,100);}
 setTimeout(jump,30);
}
function bind(){
 var root=document.getElementById('cats');
 if(!root||root.getAttribute('data-stable-bound')==='1')return;
 root.setAttribute('data-stable-bound','1');
 root.addEventListener('click',function(e){var b=e.target.closest('.cat');if(!b||!root.contains(b))return;e.preventDefault();e.stopPropagation();choose(b.getAttribute('data-category')||'all',b);},true);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind);else bind();
setTimeout(bind,500);setTimeout(bind,1500);
})();
</script>'''

pos = s.lower().rfind('</body>')
if pos < 0:
    raise RuntimeError('No </body> found')
s = s[:pos] + css + js + s[pos:]
HTML.write_text(s, encoding='utf-8')
print('FINAL_CUSTOMER_CATEGORY_AUDIT_FIX_APPLIED')
