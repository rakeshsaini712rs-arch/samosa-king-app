from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
files = list(ROOT.rglob('*.html')) + list(ROOT.rglob('*.kt')) + list(ROOT.rglob('*.java'))
htmls = [p for p in files if p.suffix == '.html']
if not htmls:
    raise SystemExit('No HTML app source found')

p = htmls[0]
s = p.read_text(encoding='utf-8')

marker = 'skCategoryImagesReliableV1'
if marker in s:
    print('Reliable category image fix already present')
    raise SystemExit(0)

patch = r'''<style id="skCategoryImagesReliableV1">
#cats .cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;min-height:94px!important;background:var(--card,#fff)!important}
#cats .skReliableCatPhoto{display:block!important;width:100%!important;height:68px!important;flex:0 0 68px!important;overflow:hidden!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}
#cats .skReliableCatPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}
#cats .skReliableCatLabel{display:block!important;padding:5px 4px 7px!important;text-align:center!important;line-height:1.15!important;font-weight:800!important;color:inherit!important;font-size:11px!important}
</style>
<script id="skCategoryImagesReliableV1">
(function(){
 if(window.__SK_CATEGORY_IMAGES_RELIABLE_V1__)return; window.__SK_CATEGORY_IMAGES_RELIABLE_V1__=true;
 var MAP={
  'all':'samosa','fast food':'pizza','snacks':'samosa','chaat special':'dahi-bhalla-1',
  'indian thali':'indian-thali','desi rasoi':'sabji','birthday special':'cake',
  'beverages':'cold-drink','sweets':'gulab-jamun','restaurant hotel':'dosa'
 };
 var TERMS={
  'all':['samosa'],'fast food':['pizza','sandwich','burger','maggi','chili potato'],
  'snacks':['samosa','kachori','mirchi bada','pakoda'],'chaat special':['chole kulche','chole bhature','dahi','chaat'],
  'indian thali':['indian thali','thali'],'desi rasoi':['desi rasoi','sabji','dal','roti'],
  'birthday special':['cake','balloon','birthday'],'beverages':['cold drink','beverage','juice','lassi'],
  'sweets':['besan laddu','bundi ladoo','gulab','ladoo','sweet'],
  'restaurant hotel':['dosa','idli','vada pav','restaurant','hotel']
 };
 function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ')}
 function label(cat){var x=cat.getAttribute('data-sk-cat-label');if(x)return x;var c=cat.cloneNode(true);c.querySelectorAll('img,svg,picture,.skReliableCatPhoto').forEach(function(n){n.remove()});return (c.textContent||'').replace(/\s+/g,' ').trim()}
 function productSrc(key){
   var terms=TERMS[key]||[]; var found='';
   document.querySelectorAll('.card').forEach(function(card){if(found)return;var t=norm(card.textContent||'');if(terms.some(function(x){return t.indexOf(norm(x))>=0})){var im=card.querySelector('.visual img, img');if(im&&im.src)found=im.src;}});
   return found;
 }
 function apply(){var root=document.getElementById('cats');if(!root)return;root.querySelectorAll('.cat').forEach(function(cat){
   var text=label(cat), key=norm(text); if(!text)return; cat.setAttribute('data-sk-cat-label',text);
   var holder=cat.querySelector('.skReliableCatPhoto')||document.createElement('span');holder.className='skReliableCatPhoto';
   var img=holder.querySelector('img')||document.createElement('img');img.loading='eager';img.decoding='sync';img.alt=text;
   var src=productSrc(key); if(src){img.src=src;img.style.display='block';img.style.visibility='visible';img.style.opacity='1'}
   if(!img.parentNode)holder.appendChild(img); if(holder.parentNode!==cat)cat.insertBefore(holder,cat.firstChild);
   var lab=cat.querySelector('.skReliableCatLabel')||document.createElement('span');lab.className='skReliableCatLabel';lab.textContent=text;if(lab.parentNode!==cat)cat.appendChild(lab);
 });}
 function run(){apply();[100,300,700,1500,3000,6000].forEach(function(ms){setTimeout(apply,ms)})}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
 new MutationObserver(function(){clearTimeout(window.__skCatT);window.__skCatT=setTimeout(apply,100)}).observe(document.body,{childList:true,subtree:true});
})();
</script>'''

if '</head>' not in s:
    raise SystemExit('HTML head not found')
s=s.replace('</head>', patch+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Reliable category image fallback added')
