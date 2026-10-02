from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
marker = 'SK_CATEGORY_PHOTOS_MATCH_BY_SECTION_V4_20261002'
if marker in s:
    print('V4 already present')
    raise SystemExit(0)

js = r'''<style id="skCategoryPhotoMatchV4">
/* SK_CATEGORY_PHOTOS_MATCH_BY_SECTION_V4_20261002 */
#cats .cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important}
#cats .cat .skCatPhotoV4{display:block!important;width:100%!important;height:74px!important;flex:0 0 74px!important;overflow:hidden!important;margin:0 0 5px!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}
#cats .cat .skCatPhotoV4 img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}
#cats .cat .skCatLabelV4{display:block!important;padding:4px 4px 8px!important;text-align:center!important;line-height:1.2!important}
#cats .cat>img,#cats .cat>picture,#cats .cat>svg{display:none!important}
</style>
<script id="skCategoryPhotoMatchV4Script">
(function(){
 if(window.__SK_CATEGORY_PHOTO_MATCH_V4__)return;window.__SK_CATEGORY_PHOTO_MATCH_V4__=true;
 function norm(v){return String(v||'').toLowerCase().replace(/[&+]/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ')}
 function label(cat){var x=cat.querySelector('.skCatLabelV4');return x?x.textContent:cat.textContent}
 function sections(){return Array.from(document.querySelectorAll('.section'))}
 function title(sec){var h=sec.querySelector('h2,h3,.sectionTitle');return h?norm(h.textContent):''}
 function image(sec){var i=sec.querySelector('.card .visual img,.card img');return i&&i.currentSrc||i&&i.src||''}
 var aliases={
  'all':'',
  'fast food':'fast food','fastfood':'fast food',
  'snacks':'snacks','snack':'snacks',
  'chaat special':'chaat special','chaat and special':'chaat special',
  'indian thali':'indian thali','desi rasoi':'desi rasoi',
  'birthday special':'birthday special','beverages':'beverages','sweets':'sweets',
  'restaurant hotel':'restaurant hotel','restaurant':'restaurant hotel','hotel':'restaurant hotel'
 };
 function findSection(name){
  var n=norm(name), key=aliases[n]||n;
  var list=sections();
  var exact=list.find(function(sec){return title(sec)===key});
  if(exact)return exact;
  return list.find(function(sec){var t=title(sec);return t===n||t.indexOf(key)>=0||key.indexOf(t)>=0});
 }
 function apply(){
  var root=document.getElementById('cats');if(!root)return;
  root.querySelectorAll('.cat').forEach(function(cat){
   var text=(cat.textContent||'').replace(/\s+/g,' ').trim();
   var sec=findSection(text), src=image(sec), old=cat.querySelector('.skCatPhotoV4');
   if(!old){old=document.createElement('span');old.className='skCatPhotoV4';old.innerHTML='<img loading="eager" decoding="async"><span class="skCatLabelV4"></span>';cat.insertBefore(old,cat.firstChild)}
   var img=old.querySelector('img'), lab=old.querySelector('.skCatLabelV4');
   if(lab)lab.textContent=text;
   if(img&&src){if(img.getAttribute('src')!==src)img.src=src;img.style.display='block'}
   Array.from(cat.children).forEach(function(ch){if(ch!==old)ch.style.setProperty('display','none','important')});
  });
 }
 function run(){apply();[100,300,700,1500,3000].forEach(function(t){setTimeout(apply,t)})}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
 new MutationObserver(function(){apply()}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''
if '</head>' not in s: raise SystemExit('No </head>')
s=s.replace('</head>',js+'</head>',1)
p.write_text(s,encoding='utf-8')
print('Added V4 section-aware category photo matching')
