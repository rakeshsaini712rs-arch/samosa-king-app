from pathlib import Path
import re

P = Path('app/src/main/assets/index.html')
s = P.read_text(encoding='utf-8')

# Remove every previous category-photo implementation. Only this one must remain.
ids = [
    'skRealCategoryPhotoStyle','skRealCategoryPhotoScript',
    'skCategoryPhotoDedupV2','skCategoryPhotoDedupV2Script',
    'skCategoryPhotoMatchV3','skCategoryPhotoMatchV3Script',
    'skCategoryPhotoMatchV4','skCategoryPhotoMatchV4Script',
    'skCategoryPhotoFinalStyle','skCategoryPhotoFinalScript',
    'customerCategoryPhotoDedupStyle','customerCategoryPhotoDedupScript',
]
for ident in ids:
    s = re.sub(r'<style id="'+re.escape(ident)+r'">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script id="'+re.escape(ident)+r'">.*?</script>', '', s, flags=re.S)

patch = r'''<style id="skCategoryPhotoFinalStyle">
/* SK_CATEGORY_PHOTOS_FINAL_SINGLE_SOURCE_20261002_V2 */
#cats .cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:0!important;min-height:88px!important}
#cats .cat .skFinalCatPhoto{display:block!important;width:100%!important;height:66px!important;flex:0 0 66px!important;overflow:hidden!important;margin:0 0 4px!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}
#cats .cat .skFinalCatPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}
#cats .cat .skFinalCatLabel{display:block!important;padding:3px 4px 7px!important;text-align:center!important;line-height:1.2!important;font-weight:800!important;color:inherit!important}
#cats .cat>img,#cats .cat>picture,#cats .cat>svg,#cats .cat>.catPhoto,#cats .cat>.categoryImage,#cats .cat>.category-img,#cats .cat>.cat-image{display:none!important}
</style>
<script id="skCategoryPhotoFinalScript">
(function(){
  if(window.__SK_CATEGORY_PHOTOS_FINAL_SINGLE_SOURCE_V2__)return;
  window.__SK_CATEGORY_PHOTOS_FINAL_SINGLE_SOURCE_V2__=true;
  var FALLBACK={
    'all':'product-images/samosa.jpg',
    'fast food':'product-images/pizza.jpg',
    'snacks':'product-images/samosa.jpg',
    'chaat special':'product-images/dahi-bhalla-1.jpg',
    'indian thali':'product-images/paneer-tikka.jpg',
    'desi rasoi':'product-images/manchurian.jpg',
    'birthday special':'product-images/milk-cake.jpg',
    'beverages':'product-images/burger.jpg',
    'sweets':'product-images/gulab-jamun.jpg',
    'restaurant hotel':'product-images/pizza.jpg'
  };
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ')}
  function sectionImage(label){
    var key=norm(label), sec=null;
    if(key==='all') return document.querySelector('.section .card .visual img,.section .card img');
    var aliases={'chaat special':'chaat and special','restaurant':'restaurant hotel','hotel':'restaurant hotel'};
    key=aliases[key]||key;
    document.querySelectorAll('.section').forEach(function(x){
      var h=x.querySelector('h2,h3,.sectionTitle');
      var t=norm(h?h.textContent:'');
      if(!sec && (t===key || t.indexOf(key)>=0 || key.indexOf(t)>=0)) sec=x;
    });
    return sec&&sec.querySelector('.card .visual img,.card img');
  }
  function labelOf(cat){
    var saved=cat.getAttribute('data-sk-category-label');
    if(saved)return saved;
    var clone=cat.cloneNode(true);
    clone.querySelectorAll('.skFinalCatPhoto,.skCatPhoto,.skCatPhotoV4,img,picture,svg').forEach(function(x){x.remove()});
    return (clone.textContent||'').replace(/\s+/g,' ').trim();
  }
  function apply(){
    var root=document.getElementById('cats'); if(!root)return;
    root.querySelectorAll('.cat').forEach(function(cat){
      var label=labelOf(cat); if(!label)return;
      cat.setAttribute('data-sk-category-label',label);
      var key=norm(label);
      var source=sectionImage(label);
      var src=source?(source.getAttribute('src')||source.currentSrc||source.src||''):'';
      if(!src)src=FALLBACK[key]||'';
      var holder=cat.querySelector('.skFinalCatPhoto');
      if(!holder){
        holder=document.createElement('span');
        holder.className='skFinalCatPhoto';
        holder.innerHTML='<img loading="eager" decoding="sync"><span class="skFinalCatLabel"></span>';
        cat.insertBefore(holder,cat.firstChild);
      }
      var img=holder.querySelector('img'), lab=holder.querySelector('.skFinalCatLabel');
      if(lab)lab.textContent=label;
      if(img&&src){img.src=src;img.style.display='block';img.style.visibility='visible';img.style.opacity='1'}
      Array.from(cat.children).forEach(function(ch){
        if(ch!==holder && (ch.tagName==='IMG'||ch.tagName==='PICTURE'||ch.tagName==='SVG'||(ch.querySelector&&ch.querySelector('img'))))ch.remove();
      });
    });
  }
  function run(){apply();[100,300,700,1500,3000].forEach(function(ms){setTimeout(apply,ms)})}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat'))setTimeout(apply,30)},true);
  var observer=new MutationObserver(function(){setTimeout(apply,30)});
  function watch(){var root=document.getElementById('cats');if(root)observer.observe(root,{childList:true,subtree:true});else setTimeout(watch,100)}
  watch();
})();
</script>'''

s = s.replace('</head>', patch + '\n</head>', 1)
P.write_text(s, encoding='utf-8')
print('Final category photo implementation written.')
