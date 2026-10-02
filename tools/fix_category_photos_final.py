from pathlib import Path
import re

P = Path('app/src/main/assets/index.html')
s = P.read_text(encoding='utf-8')
ids = ['skRealCategoryPhotoStyle','skRealCategoryPhotoScript','skCategoryPhotoDedupV2','skCategoryPhotoDedupV2Script','skCategoryPhotoMatchV3','skCategoryPhotoMatchV3Script','skCategoryPhotoMatchV4','skCategoryPhotoMatchV4Script','skCategoryPhotoFinalStyle','skCategoryPhotoFinalScript','customerCategoryPhotoDedupStyle','customerCategoryPhotoDedupScript']
for ident in ids:
    s = re.sub(r'<style id="'+re.escape(ident)+r'">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script id="'+re.escape(ident)+r'">.*?</script>', '', s, flags=re.S)

patch = r'''<style id="skCategoryPhotoFinalStyle">
/* SK_CATEGORY_PHOTOS_FINAL_SINGLE_SOURCE_20261002_V4 */
#cats .cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:0!important;min-height:92px!important}
#cats .cat .skFinalCatPhoto{display:block!important;width:100%!important;height:68px!important;flex:0 0 68px!important;overflow:hidden!important;margin:0!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}
#cats .cat .skFinalCatPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}
#cats .cat .skFinalCatLabel{display:block!important;padding:5px 4px 7px!important;text-align:center!important;line-height:1.15!important;font-weight:800!important;color:inherit!important;font-size:11px!important}
</style>
<script id="skCategoryPhotoFinalScript">
(function(){
  if(window.__SK_CATEGORY_PHOTOS_FINAL_SINGLE_SOURCE_V4__)return;
  window.__SK_CATEGORY_PHOTOS_FINAL_SINGLE_SOURCE_V4__=true;
  var KEY={'all':'samosa','fast food':'pizza','snacks':'samosa','chaat special':'dahi-bhalla-1','indian thali':'indian-thali','desi rasoi':'sabji','birthday special':'cake','beverages':'cold-drink','sweets':'gulab-jamun','restaurant hotel':'dosa'};
  var MATCH={
    'all':['samosa'],
    'fast food':['pizza','sandwich','burger','maggi','chili potato'],
    'snacks':['samosa','kachori','mirchi bada','pakoda'],
    'chaat special':['chole kulche','chole bhature','dahi','chaat'],
    'indian thali':['indian thali','thali'],
    'desi rasoi':['desi rasoi','sabji','dal','roti'],
    'birthday special':['cake','balloon','birthday'],
    'beverages':['cold drink','beverage','juice','lassi'],
    'sweets':['besan laddu','bundi ladoo','gulab','ladoo','sweet'],
    'restaurant hotel':['dosa','idli','vada pav','restaurant','hotel']
  };
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ')}
  function cleanLabel(cat){
    var saved=cat.getAttribute('data-sk-category-label'); if(saved)return saved;
    var text=''; cat.childNodes.forEach(function(n){if(n.nodeType===3)text+=' '+n.textContent});
    if(!text.trim()){var c=cat.cloneNode(true);c.querySelectorAll('img,picture,svg,.skFinalCatPhoto,.skCatPhoto,.skCatPhotoV4').forEach(function(x){x.remove()});text=c.textContent||'';}
    return text.replace(/\s+/g,' ').trim();
  }
  function imageFromCard(card){return card&&(card.querySelector('.visual img')||card.querySelector('img'));}
  function findProductImage(label){
    var key=norm(label),found=null;
    document.querySelectorAll('.section').forEach(function(sec){
      if(found)return;
      var h=sec.querySelector('h2,h3,.sectionTitle'),t=norm(h?h.textContent:'');
      if(t===key||(t&&t.indexOf(key)>=0)||(key&&t.indexOf(key)>=0))found=imageFromCard(sec.querySelector('.card'));
    });
    if(found)return found;
    var terms=MATCH[key]||[];
    document.querySelectorAll('.card').forEach(function(card){
      if(found)return;
      var text=norm(card.textContent||'');
      if(terms.some(function(term){return text.indexOf(norm(term))>=0}))found=imageFromCard(card);
    });
    return found;
  }
  function srcFor(label){
    var p=findProductImage(label),src=p&&(p.currentSrc||p.getAttribute('src')||p.src); if(src)return src;
    var key=KEY[norm(label)],data=window.SK_IMAGES&&key?window.SK_IMAGES[key]:'';
    if(data)return data.indexOf('data:')===0?data:'data:image/jpeg;base64,'+data.replace(/^data:image\/[^;]+;base64,/,'');
    return '';
  }
  function apply(){
    var root=document.getElementById('cats');if(!root)return;
    root.querySelectorAll('.cat').forEach(function(cat){
      var label=cleanLabel(cat);if(!label)return;
      cat.setAttribute('data-sk-category-label',label);
      var src=srcFor(label);
      var old=cat.querySelector('.skFinalCatPhoto');
      var holder=old||document.createElement('span'); holder.className='skFinalCatPhoto';
      var img=holder.querySelector('img')||document.createElement('img');
      img.loading='eager';img.decoding='sync';img.alt=label;
      if(src){img.src=src;img.style.display='block';img.style.visibility='visible';img.style.opacity='1'}
      if(!img.parentNode)holder.appendChild(img);
      var lab=cat.querySelector('.skFinalCatLabel')||document.createElement('span');lab.className='skFinalCatLabel';lab.textContent=label;
      if(holder.parentNode!==cat)cat.insertBefore(holder,cat.firstChild);
      if(lab.parentNode!==cat)cat.appendChild(lab);
    });
  }
  function run(){apply();[100,300,700,1500,3000,6000].forEach(function(ms){setTimeout(apply,ms)})}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat'))setTimeout(apply,80)},true);
  var observer=new MutationObserver(function(){clearTimeout(observer._t);observer._t=setTimeout(apply,80)});
  function watch(){var root=document.getElementById('cats');if(root)observer.observe(root,{childList:true,subtree:true});else setTimeout(watch,100)} watch();
})();
</script>'''

s = s.replace('</head>', patch + '\n</head>', 1)
P.write_text(s, encoding='utf-8')
print('Final category photo implementation V4 written.')
