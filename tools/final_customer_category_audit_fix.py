from pathlib import Path
import re

HTML = Path('app/src/main/assets/index.html')
s = HTML.read_text(encoding='utf-8')

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
    'skStableCategoryPhotoCss','skStableCategoryPhotoController',
    'FINAL_CATEGORY_IMAGES_CSS','FINAL_CATEGORY_IMAGES_CONTROLLER',
]
for ident in ids:
    pat = r'<(?:style|script)\b[^>]*\bid=["\']' + re.escape(ident) + r'["\'][^>]*>.*?</(?:style|script)>'
    s = re.sub(pat, '', s, flags=re.I | re.S)

# Remove old category-specific scripts so their click handlers cannot fight the final controller.
def strip_bad_script(m):
    b = m.group(0).lower()
    markers = ('skcatphoto','skcategoryphoto','categoryphotoembedded','categoryfinalclean','categoryduplicatecleanup','skembeddedlabel','final_category_images')
    return '' if any(x in b for x in markers) else m.group(0)
s = re.sub(r'<script\b[^>]*>.*?</script>', strip_bad_script, s, flags=re.I | re.S)

cats = '''<div id="cats" class="cats" aria-label="Food categories">
<button class="cat active" type="button" data-category="all"><img src="product-images/samosa.jpg" alt="All"><span>All</span></button>
<button class="cat" type="button" data-category="fast"><img src="product-images/pizza.jpg" alt="Fast Food"><span>Fast Food</span></button>
<button class="cat" type="button" data-category="snacks"><img src="product-images/mirchi-bada.jpg" alt="Snacks"><span>Snacks</span></button>
<button class="cat" type="button" data-category="chaat"><img src="product-images/dahi-bhalla-1.jpg" alt="Chaat &amp; Special"><span>Chaat &amp; Special</span></button>
<button class="cat" type="button" data-category="thali"><img src="product-images/manchurian.jpg" alt="Indian Thali"><span>Indian Thali</span></button>
<button class="cat" type="button" data-category="desirsoi"><img src="product-images/pasta.jpg" alt="Desi Rasoi"><span>Desi Rasoi</span></button>
<button class="cat" type="button" data-category="birthday"><img src="product-images/gulab-jamun.jpg" alt="Birthday Special"><span>Birthday Special</span></button>
<button class="cat" type="button" data-category="beverages"><img src="product-images/burger.jpg" alt="Beverages"><span>Beverages</span></button>
<button class="cat" type="button" data-category="sweets"><img src="product-images/kaju-katli.jpg" alt="Sweets"><span>Sweets</span></button>
<button class="cat" type="button" data-category="restaurants"><img src="product-images/wraps.jpg" alt="Restaurant / Hotel"><span>Restaurant / Hotel</span></button>
</div>'''

# Remove EVERY existing category container, then insert exactly one canonical container.
s = re.sub(r'<div\s+id=["\']cats["\'][^>]*>.*?</div>', '', s, flags=re.I | re.S)
pos = s.lower().find('</header>')
if pos < 0:
    pos = s.lower().find('<body')
    pos = s.find('>', pos) + 1 if pos >= 0 else 0
s = s[:pos] + cats + s[pos:]

css = '''<style id="skStableCategoryCss">
#cats{display:flex!important;align-items:center!important;gap:8px!important;overflow-x:auto!important;overflow-y:hidden!important;padding:10px 12px!important;position:relative!important;top:auto!important;z-index:15!important;scrollbar-width:none!important;background:#17120f!important;border-bottom:1px solid #3a3028!important;-webkit-overflow-scrolling:touch!important}
#cats::-webkit-scrollbar{display:none!important}
#cats .cat{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;gap:5px!important;flex:0 0 88px!important;width:88px!important;min-width:88px!important;height:88px!important;min-height:88px!important;padding:6px 4px 7px!important;box-sizing:border-box!important;border-radius:14px!important;border:1px solid #4a3b30!important;background:#241c17!important;color:#fff!important;font-size:10px!important;font-weight:900!important;line-height:1.1!important;white-space:normal!important;cursor:pointer!important;touch-action:manipulation!important;overflow:hidden!important}
#cats .cat img{display:block!important;width:58px!important;height:50px!important;flex:0 0 50px!important;object-fit:cover!important;border-radius:10px!important;background:#33251d!important;pointer-events:none!important;margin:0!important;padding:0!important;border:0!important}
#cats .cat span{display:block!important;width:100%!important;max-width:100%!important;text-align:center!important;white-space:normal!important;overflow:hidden!important;text-overflow:ellipsis!important;color:inherit!important}
#cats .cat.active{background:#f6c94a!important;border-color:#f6c94a!important;color:#17100b!important;box-shadow:0 3px 10px #d99d1844!important}
</style>'''

js = '''<script id="skStableCategoryController">
(function(){
'use strict';
if(window.__SK_STABLE_CATEGORY_CONTROLLER__)return;
window.__SK_STABLE_CATEGORY_CONTROLLER__=true;
var names={all:'All',fast:'Fast Food',snacks:'Snacks',chaat:'Chaat & Special',thali:'Indian Thali',desirsoi:'Desi Rasoi',birthday:'Birthday Special',beverages:'Beverages',sweets:'Sweets',restaurants:'Restaurant / Hotel'};
function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').replace(/\\s+/g,' ').trim();}
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
 try{if(typeof window.selectCategory==='function')window.selectCategory(key);}catch(e){}
 if(key==='restaurants'&&typeof window.openRestaurants==='function'){window.openRestaurants();return;}
 var tries=0;
 function jump(){
  var el=key==='all'?document.querySelector('#sections .section'):sectionFor(key);
  if(el){
   var top=document.querySelector('.top');
   var offset=(top?top.getBoundingClientRect().height:0)+8;
   var y=el.getBoundingClientRect().top+window.pageYOffset-offset;
   window.scrollTo({top:Math.max(0,y),behavior:'smooth'}); return;
  }
  if(tries++<15)setTimeout(jump,100);
 }
 setTimeout(jump,30);
}
function sanitizeAndBind(){
 var roots=document.querySelectorAll('.cats');
 var root=document.getElementById('cats')||roots[0];
 if(!root)return;
 // If another renderer creates a second category bar, remove it.
 for(var i=0;i<roots.length;i++) if(roots[i]!==root) roots[i].remove();
 // Remove duplicate images/labels inside every category and detach old handlers by cloning buttons.
 var buttons=Array.prototype.slice.call(root.querySelectorAll('.cat'));
 buttons.forEach(function(old){
  var b=old.cloneNode(true);
  var imgs=b.querySelectorAll('img');
  for(var i=1;i<imgs.length;i++)imgs[i].remove();
  var spans=b.querySelectorAll('span');
  for(var j=1;j<spans.length;j++)spans[j].remove();
  b.type='button';
  b.onclick=null;
  old.replaceWith(b);
 });
 root.setAttribute('data-stable-bound','1');
 root.onclick=function(e){
  var b=e.target.closest('.cat');
  if(!b||!root.contains(b))return;
  e.preventDefault();e.stopImmediatePropagation();
  choose(b.getAttribute('data-category')||'all',b);
 };
}
function bind(){sanitizeAndBind();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind);else bind();
setTimeout(bind,250);setTimeout(bind,800);setTimeout(bind,1600);
var mo=new MutationObserver(function(){
 if(window.__SK_CATEGORY_GUARD__)return;
 window.__SK_CATEGORY_GUARD__=true;
 setTimeout(function(){window.__SK_CATEGORY_GUARD__=false;sanitizeAndBind();},0);
});
if(document.body)mo.observe(document.body,{childList:true,subtree:true});
})();
</script>'''

pos=s.lower().rfind('</body>')
if pos<0: raise RuntimeError('No </body> found')
s=s[:pos]+css+js+s[pos:]
HTML.write_text(s,encoding='utf-8')
print('FINAL_CUSTOMER_CATEGORY_AUDIT_FIX_APPLIED_V2')