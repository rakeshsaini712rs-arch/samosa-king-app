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
    'skStableCategoryPhotoCss','skStableCategoryPhotoController',
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
#cats{display:flex!important;align-items:stretch!important;gap:8px!important;overflow-x:auto!important;overflow-y:hidden!important;padding:10px 12px!important;position:relative!important;top:auto!important;z-index:15!important;scrollbar-width:none!important;background:#17120f!important;border-bottom:1px solid #3a3028!important;-webkit-overflow-scrolling:touch!important}
#cats::-webkit-scrollbar{display:none!important}
#cats .cat{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;flex:0 0 82px!important;width:82px!important;min-width:82px!important;height:88px!important;min-height:88px!important;box-sizing:border-box!important;padding:6px 4px 5px!important;border-radius:13px!important;border:1px solid #4a3b30!important;background:#241c17!important;color:#f7eee5!important;font-size:10px!important;font-weight:900!important;white-space:normal!important;cursor:pointer!important;touch-action:manipulation!important;overflow:hidden!important;position:relative!important}
#cats .cat.active{background:#f6c94a!important;border-color:#f6c94a!important;color:#17100b!important;box-shadow:0 3px 10px #d99d1844!important}
#cats .skCategoryPhoto{display:block!important;flex:0 0 54px!important;width:62px!important;height:54px!important;margin:0 0 5px!important;border-radius:10px!important;overflow:hidden!important;background:#33251d!important;pointer-events:none!important}
#cats .skCategoryPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;border:0!important;margin:0!important;padding:0!important;pointer-events:none!important;user-select:none!important;visibility:visible!important;opacity:1!important}
#cats .skCategoryLabel{display:block!important;width:100%!important;min-height:18px!important;padding:0 2px!important;text-align:center!important;line-height:1.1!important;font-size:10px!important;font-weight:900!important;white-space:normal!important;overflow:hidden!important;text-overflow:ellipsis!important;color:inherit!important}
#cats .ico{display:none!important}
</style>'''

js = '''<script id="skStableCategoryController">
(function(){
'use strict';
if(window.__SK_STABLE_CATEGORY_CONTROLLER__)return;
window.__SK_STABLE_CATEGORY_CONTROLLER__=true;
var map={
  all:['samosa.jpg','All'],
  fast:['pizza.jpg','Fast Food'],
  snacks:['mirchi-bada.jpg','Snacks'],
  chaat:['dahi-bhalla-1.jpg','Chaat & Special'],
  thali:['manchurian.jpg','Indian Thali'],
  desirsoi:['pasta.jpg','Desi Rasoi'],
  birthday:['gulab-jamun.jpg','Birthday Special'],
  beverages:['burger.jpg','Beverages'],
  sweets:['kaju-katli.jpg','Sweets'],
  restaurants:['wraps.jpg','Restaurant / Hotel']
};
var base='file:///android_asset/product-images/';
function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').replace(/\\s+/g,' ').trim();}
function keyFor(v){
 var n=norm(v);
 if(n==='all'||n.indexOf('all')===0)return 'all';
 if(n.indexOf('fast food')>=0||n==='fast')return 'fast';
 if(n.indexOf('snacks')>=0)return 'snacks';
 if(n.indexOf('chaat')>=0)return 'chaat';
 if(n.indexOf('indian thali')>=0||n==='thali')return 'thali';
 if(n.indexOf('desi rasoi')>=0||n.indexOf('desirsoi')>=0)return 'desirsoi';
 if(n.indexOf('birthday')>=0)return 'birthday';
 if(n.indexOf('beverages')>=0)return 'beverages';
 if(n.indexOf('sweets')>=0)return 'sweets';
 if(n.indexOf('restaurant')>=0||n.indexOf('hotel')>=0)return 'restaurants';
 return 'all';
}
function sectionFor(k){
 if(k==='all')return null;
 var wanted=norm(map[k]&&map[k][1]||'');
 var all=document.querySelectorAll('#sections .section,#sections [data-category]');
 for(var i=0;i<all.length;i++){
  var el=all[i],dc=norm(el.getAttribute('data-category')||'');
  if(dc&&(dc===wanted||dc===norm(k)))return el;
  var h=el.querySelector('h2,h3');
  if(h&&norm(h.textContent).indexOf(wanted)>=0)return el;
 }
 return null;
}
function activate(btn){document.querySelectorAll('#cats .cat').forEach(function(b){b.classList.toggle('active',b===btn);});}
function choose(k,btn){
 activate(btn);
 if(k==='restaurants'&&typeof window.openRestaurants==='function'){window.openRestaurants();return;}
 try{if(typeof window.selectCategory==='function')window.selectCategory(k);}catch(e){}
 var tries=0;
 function jump(){
  var el=sectionFor(k);
  if(k==='all'){window.scrollTo({top:0,behavior:'smooth'});return;}
  if(el){var top=document.querySelector('.top');var off=(top?top.getBoundingClientRect().height:0)+8;var y=el.getBoundingClientRect().top+window.pageYOffset-off;window.scrollTo({top:Math.max(0,y),behavior:'smooth'});return;}
  if(tries++<12)setTimeout(jump,100);
 }
 setTimeout(jump,30);
}
function render(){
 var root=document.getElementById('cats');
 if(!root)return;
 var buttons=Array.prototype.slice.call(root.querySelectorAll('.cat'));
 buttons.forEach(function(c){
  var k=c.getAttribute('data-category')||keyFor(c.textContent);
  var m=map[k]||map.all;
  c.setAttribute('data-category',k);
  // Critical: remove the old emoji/image/text nodes first. This prevents old + new photos from stacking.
  while(c.firstChild)c.removeChild(c.firstChild);
  var holder=document.createElement('span');holder.className='skCategoryPhoto';
  var img=document.createElement('img');img.src=base+m[0];img.alt=m[1];img.loading='eager';img.decoding='sync';
  img.onerror=function(){if(img.dataset.fallback==='1')return;img.dataset.fallback='1';img.src=base+'samosa.jpg';};
  holder.appendChild(img);
  var label=document.createElement('span');label.className='skCategoryLabel';label.textContent=m[1];
  c.appendChild(holder);c.appendChild(label);
  c.onclick=function(e){e.preventDefault();e.stopPropagation();choose(k,c);return false;};
 });
}
function bind(){
 var root=document.getElementById('cats');
 if(!root)return;
 render();
 if(root.getAttribute('data-stable-bound')!=='1'){
  root.setAttribute('data-stable-bound','1');
  root.addEventListener('click',function(e){var b=e.target.closest('.cat');if(!b||!root.contains(b))return;e.preventDefault();e.stopPropagation();choose(b.getAttribute('data-category')||'all',b);},true);
 }
}
function run(){bind();[100,400,900,1800,3500].forEach(function(t){setTimeout(bind,t);});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
new MutationObserver(function(){clearTimeout(window.__skStableTimer);window.__skStableTimer=setTimeout(bind,120);}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''

pos = s.lower().rfind('</body>')
if pos < 0:
    raise RuntimeError('No </body> found')
s = s[:pos] + css + js + s[pos:]
HTML.write_text(s, encoding='utf-8')
print('FINAL_CUSTOMER_CATEGORY_AUDIT_FIX_APPLIED')
