from pathlib import Path
import re

P = Path('app/src/main/assets/index.html')
s = P.read_text(encoding='utf-8')
ids = ['skRealCategoryPhotoStyle','skRealCategoryPhotoScript','skCategoryPhotoDedupV2','skCategoryPhotoDedupV2Script','skCategoryPhotoMatchV3','skCategoryPhotoMatchV3Script','skCategoryPhotoMatchV4','skCategoryPhotoMatchV4Script','skCategoryPhotoFinalStyle','skCategoryPhotoFinalScript','customerCategoryPhotoDedupStyle','customerCategoryPhotoDedupScript']
for ident in ids:
    s = re.sub(r'<style id="'+re.escape(ident)+r'">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script id="'+re.escape(ident)+r'">.*?</script>', '', s, flags=re.S)

patch = r'''<style id="skCategoryPhotoFinalStyle">
/* SK_CATEGORY_PHOTOS_FINAL_DOM_V5 */
#cats .cat,.cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:0!important;min-height:94px!important}
.cat .skFinalCatPhoto{display:block!important;width:100%!important;height:68px!important;flex:0 0 68px!important;overflow:hidden!important;margin:0!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}
.cat .skFinalCatPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}
.cat .skFinalCatLabel{display:block!important;padding:6px 4px 7px!important;text-align:center!important;line-height:1.15!important;font-weight:800!important;color:inherit!important;font-size:11px!important;min-height:25px!important}
</style>
<script id="skCategoryPhotoFinalScript">
(function(){
  if(window.__SK_CATEGORY_PHOTOS_FINAL_DOM_V5__)return;
  window.__SK_CATEGORY_PHOTOS_FINAL_DOM_V5__=true;
  var KEY={'all':'samosa','fast food':'pizza','snacks':'samosa','chaat special':'dahi-bhalla-1','indian thali':'indian-thali','desi rasoi':'sabji','birthday special':'cake','beverages':'cold-drink','sweets':'gulab-jamun','restaurant hotel':'dosa'};
  var MATCH={'all':['samosa'],'fast food':['pizza','sandwich','burger','maggi','chili potato'],'snacks':['samosa','kachori','mirchi bada','pakoda'],'chaat special':['chole kulche','chole bhature','dahi','chaat'],'indian thali':['indian thali','thali'],'desi rasoi':['desi rasoi','sabji','dal','roti'],'birthday special':['cake','balloon','birthday'],'beverages':['cold drink','beverage','juice','lassi'],'sweets':['besan laddu','bundi ladoo','gulab','ladoo','sweet'],'restaurant hotel':['dosa','idli','vada pav','restaurant','hotel']};
  var ICON={'all':'🥟','fast food':'🍕','snacks':'🥟','chaat special':'🍲','indian thali':'🍛','desi rasoi':'🍲','birthday special':'🎂','beverages':'🥤','sweets':'🍬','restaurant hotel':'🍽️'};
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ')}
  function labelOf(cat){
    var saved=cat.getAttribute('data-sk-category-label');if(saved)return saved;
    var c=cat.cloneNode(true);c.querySelectorAll('img,picture,svg,.skFinalCatPhoto,.skFinalCatLabel').forEach(function(x){x.remove()});
    var t=(c.textContent||'').replace(/\s+/g,' ').trim();
    t=t.replace(/\bcategory\b/ig,'').trim();
    return t;
  }
  function productImage(label){
    var key=norm(label),terms=MATCH[key]||[],found='';
    document.querySelectorAll('.card').forEach(function(card){
      if(found)return;var txt=norm(card.textContent||'');
      if(terms.some(function(x){return txt.indexOf(norm(x))>=0})){var im=card.querySelector('.visual img,.visual picture img,img');if(im)found=im.currentSrc||im.src||im.getAttribute('src')||'';}
    });
    return found;
  }
  function fallback(label){
    var key=norm(label),icon=ICON[key]||'🍽️';
    var title=String(label).replace(/[<>&\"']/g,'');
    var svg='<svg xmlns="http://www.w3.org/2000/svg" width="640" height="300" viewBox="0 0 640 300"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#fff0b8"/><stop offset="1" stop-color="#f7d77a"/></linearGradient></defs><rect width="640" height="300" fill="url(#g)"/><circle cx="320" cy="112" r="78" fill="#ffffff99"/><text x="320" y="145" text-anchor="middle" font-size="105">'+icon+'</text><text x="320" y="258" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" font-weight="700" fill="#21170f">'+title+'</text></svg>';
    return 'data:image/svg+xml;charset=UTF-8,'+encodeURIComponent(svg);
  }
  function sourceFor(label){
    var p=productImage(label);if(p)return p;
    var key=KEY[norm(label)],data=window.SK_IMAGES&&key?window.SK_IMAGES[key]:'';
    if(data)return data.indexOf('data:')===0?data:'data:image/jpeg;base64,'+data.replace(/^data:image\/[^;]+;base64,/,'');
    return fallback(label);
  }
  function apply(){
    var cats=document.querySelectorAll('#cats .cat,.cats .cat,.cat');
    cats.forEach(function(cat){
      var label=labelOf(cat);if(!label)return;
      cat.setAttribute('data-sk-category-label',label);
      var holder=cat.querySelector('.skFinalCatPhoto');if(!holder){holder=document.createElement('span');holder.className='skFinalCatPhoto';cat.insertBefore(holder,cat.firstChild)}
      var img=holder.querySelector('img');if(!img){img=document.createElement('img');holder.appendChild(img)}
      var src=sourceFor(label);if(img.getAttribute('src')!==src)img.src=src;img.alt=label;img.loading='eager';img.style.display='block';img.style.visibility='visible';img.style.opacity='1';
      var lab=cat.querySelector('.skFinalCatLabel');if(!lab){lab=document.createElement('span');lab.className='skFinalCatLabel';cat.appendChild(lab)}lab.textContent=label;
    });
  }
  function run(){apply();[50,150,400,800,1500,3000,6000].forEach(function(ms){setTimeout(apply,ms)})}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.cat'))setTimeout(apply,80)},true);
  var observer=new MutationObserver(function(){clearTimeout(observer._t);observer._t=setTimeout(apply,50)});
  function watch(){var root=document.querySelector('#cats')||document.querySelector('.cats');if(root)observer.observe(root,{childList:true,subtree:true});else setTimeout(watch,100)}watch();
})();
</script>'''

s = s.replace('</head>', patch + '\n</head>', 1)
P.write_text(s, encoding='utf-8')
print('Definitive category DOM image implementation V5 written.')