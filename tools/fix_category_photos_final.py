from pathlib import Path
import json
import re

P = Path('app/src/main/assets/index.html')
IMG = Path('app/src/main/assets/image-data.js')
s = P.read_text(encoding='utf-8')

# Remove every known/experimental category renderer. Old renderers installed
# MutationObservers that repeatedly rewrote #cats and caused duplicate labels,
# broken category clicks and WebView hangs.
style_ids = ['skRealCategoryPhotoStyle','skCategoryPhotoDedupV2','skCategoryPhotoMatchV3','skCategoryPhotoMatchV4','skCategoryPhotoFinalStyle','skCategoryPhotoGuaranteedStyle','customerCategoryPhotoDedupStyle','categoryPhotoEmbeddedFinalStyle','categoryFinalCleanV2Css']
script_ids = ['skRealCategoryPhotoScript','skCategoryPhotoDedupV2Script','skCategoryPhotoMatchV3Script','skCategoryPhotoMatchV4Script','skCategoryPhotoFinalScript','skCategoryPhotoGuaranteedScript','customerCategoryPhotoDedupScript','categoryPhotoEmbeddedFinal','categoryFinalCleanV2Script']
for ident in style_ids:
    s = re.sub(r'<style[^>]*id=["\']' + re.escape(ident) + r'["\'][^>]*>.*?</style>', '', s, flags=re.S|re.I)
for ident in script_ids:
    s = re.sub(r'<script[^>]*id=["\']' + re.escape(ident) + r'["\'][^>]*>.*?</script>', '', s, flags=re.S|re.I)

def keep_category_script(m):
    body = m.group(0).lower()
    markers = ('skcatphoto','skcategoryphoto','categoryphotoembedded','categoryfinalclean','sk_category_photos_final')
    return '' if any(x in body for x in markers) else m.group(0)
s = re.sub(r'<script\b[^>]*>.*?</script>', keep_category_script, s, flags=re.S|re.I)

def keep_category_style(m):
    body = m.group(0).lower()
    markers = ('skcatphoto','skcategoryphoto','categoryphotoembedded','categoryfinalclean','sk_category_photos_final')
    return '' if any(x in body for x in markers) else m.group(0)
s = re.sub(r'<style\b[^>]*>.*?</style>', keep_category_style, s, flags=re.S|re.I)

raw = IMG.read_text(encoding='utf-8')
m = re.search(r'window\.SK_IMAGES\s*=\s*(\{.*\})\s*;?\s*$', raw, flags=re.S)
if not m:
    raise RuntimeError('SK_IMAGES not found in image-data.js')
DATA = json.loads(m.group(1))
PHOTO_KEYS = {'All':'samosa','Fast Food':'pizza','Snacks':'samosa','Chaat & Special':'dahi-bhalla-1','Indian Thali':'manchurian','Desi Rasoi':'pasta','Birthday Special':'gulab-jamun','Beverages':'burger','Sweets':'kaju-katli','Restaurant / Hotel':'wraps'}
PHOTO_DATA = {k:'data:image/jpeg;base64,' + DATA[v] for k,v in PHOTO_KEYS.items()}
photo_json = json.dumps(PHOTO_DATA, ensure_ascii=False, separators=(',',':'))

final_style = r'''<style id="skCategoryPhotoFinalStyle">
/* SK_CATEGORY_AUDIT_SINGLE_SOURCE_20261003_V6 */
#cats{display:flex!important;overflow-x:auto!important;overflow-y:hidden!important;gap:8px!important;padding:10px 12px!important;scrollbar-width:none!important;background:#17110d!important;border-bottom:1px solid #3d3027!important;position:relative!important;top:auto!important;z-index:15!important}
#cats::-webkit-scrollbar{display:none!important}
#cats .cat{position:relative!important;overflow:hidden!important;flex:0 0 96px!important;width:96px!important;height:92px!important;min-height:92px!important;padding:53px 5px 5px!important;display:flex!important;align-items:center!important;justify-content:center!important;text-align:center!important;border:1px solid #49392e!important;border-radius:15px!important;background:#211914!important;color:#f5eee5!important;box-shadow:0 3px 10px #00000030!important;font-size:11px!important;font-weight:900!important;white-space:normal!important}
#cats .cat.active{background:linear-gradient(145deg,#f6c94a,#d99d18)!important;border-color:#d99d18!important;color:#17100b!important}
#cats .cat .skFinalCatPhoto{position:absolute!important;top:5px!important;left:50%!important;transform:translateX(-50%)!important;width:44px!important;height:44px!important;border-radius:50%!important;overflow:hidden!important;border:2px solid #fff!important;background:#fff!important;display:block!important;z-index:3!important;box-shadow:0 2px 8px #00000035!important}
#cats .cat .skFinalCatPhoto img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;visibility:visible!important;opacity:1!important}
#cats .cat .skFinalCatLabel{position:relative!important;z-index:4!important;color:inherit!important;font-weight:900!important;font-size:11px!important;line-height:1.15!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;max-width:100%!important}
</style>'''

final_script = '''<script id="skCategoryPhotoFinalScript">
(function(){
'use strict';
if(window.__SK_CATEGORY_AUDIT_V6__)return;
window.__SK_CATEGORY_AUDIT_V6__=true;
var MAP=%s;
var NAMES=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];
var KEYS={'Fast Food':'fast','Snacks':'snacks','Chaat & Special':'chaat','Indian Thali':'thali','Desi Rasoi':'desirsoi','Birthday Special':'birthday','Beverages':'beverages','Sweets':'sweets'};
function clean(v){return String(v||'').replace(/\\s+/g,' ').trim();}
function keyFor(cat,index){
 var raw=clean(cat.getAttribute('data-sk-category')||cat.getAttribute('data-label')||cat.textContent);
 var t=raw.toLowerCase().replace(/\\bcategory\\b/g,' ').replace(/\\s+/g,' ').trim();
 for(var i=0;i<NAMES.length;i++){var n=NAMES[i].toLowerCase();if(t===n||t.indexOf(n)>=0||n.indexOf(t)>=0)return NAMES[i];}
 return NAMES[index]||'All';
}
function decorate(){
 var root=document.getElementById('cats');if(!root)return;
 root.querySelectorAll('.cat').forEach(function(cat,index){
  var key=keyFor(cat,index);cat.setAttribute('data-sk-category',key);cat.setAttribute('aria-label',key);
  cat.innerHTML='';
  var holder=document.createElement('span');holder.className='skFinalCatPhoto';
  var img=document.createElement('img');img.src=MAP[key]||'';img.alt=key+' category';img.loading='eager';img.decoding='sync';holder.appendChild(img);
  var label=document.createElement('span');label.className='skFinalCatLabel';label.textContent=key;
  cat.appendChild(holder);cat.appendChild(label);
  cat.onclick=function(ev){
   ev.preventDefault();ev.stopPropagation();
   if(key==='Restaurant / Hotel'){if(typeof openRestaurants==='function')openRestaurants();return;}
   var fn=typeof selectCategory==='function'?selectCategory:null;
   if(fn)fn(key==='All'?'all':(KEYS[key]||key.toLowerCase()));
  };
 });
}
function stableRun(){try{if(typeof renderCats==='function')renderCats();}catch(e){}decorate();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(stableRun,0)});else setTimeout(stableRun,0);
setTimeout(stableRun,300);setTimeout(stableRun,1000);setTimeout(stableRun,2500);
})();
</script>''' % photo_json

pos=s.lower().rfind('</body>')
if pos<0:pos=s.lower().rfind('</html>')
if pos<0:raise RuntimeError('no body/html close tag')
s=s[:pos]+final_style+'\n'+final_script+'\n'+s[pos:]
P.write_text(s,encoding='utf-8')
print('CATEGORY_AUDIT_V6_APPLIED')
