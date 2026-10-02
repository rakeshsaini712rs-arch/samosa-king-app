from pathlib import Path
import re
P=Path('app/src/main/assets/index.html')
s=P.read_text(encoding='utf-8')
ids=['skRealCategoryPhotoStyle','skRealCategoryPhotoScript','skCategoryPhotoDedupV2','skCategoryPhotoDedupV2Script','skCategoryPhotoMatchV3','skCategoryPhotoMatchV3Script','skCategoryPhotoMatchV4','skCategoryPhotoMatchV4Script','skCategoryPhotoFinalStyle','skCategoryPhotoFinalScript','customerCategoryPhotoDedupStyle','customerCategoryPhotoDedupScript']
for ident in ids:
    s=re.sub(r'<style id="'+re.escape(ident)+r'">.*?</style>','',s,flags=re.S)
    s=re.sub(r'<script id="'+re.escape(ident)+r'">.*?</script>','',s,flags=re.S)
patch=r'''<style id="skCategoryPhotoFinalStyle">
/* CLEAN CATEGORY CARDS: one image + one label */
#cats .cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:0!important;min-height:94px!important}
#cats .cat .skFinalCatPhoto{display:block!important;width:100%!important;height:68px!important;flex:0 0 68px!important;overflow:hidden!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}
#cats .cat .skFinalCatPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}
#cats .cat .skFinalCatLabel{display:block!important;padding:6px 4px 7px!important;text-align:center!important;font-weight:800!important;font-size:11px!important;line-height:1.15!important}
</style>
<script id="skCategoryPhotoFinalScript">
(function(){if(window.__SK_CATEGORY_CLEAN_V6__)return;window.__SK_CATEGORY_CLEAN_V6__=true;
var ORDER=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];
var TERMS={'All':['samosa'],'Fast Food':['pizza'],'Snacks':['samosa'],'Chaat & Special':['dahi bhalla','chole bhature'],'Indian Thali':['indian thali'],'Desi Rasoi':['sabji'],'Birthday Special':['cake'],'Beverages':['cold drink'],'Sweets':['gulab jamun','laddu'],'Restaurant / Hotel':['dosa']};
function imgFor(label){var terms=TERMS[label]||[];for(var i=0;i<terms.length;i++){var n=terms[i].toLowerCase();var cards=document.querySelectorAll('.card');for(var j=0;j<cards.length;j++){if((cards[j].textContent||'').toLowerCase().indexOf(n)>=0){var im=cards[j].querySelector('.visual img,img');if(im)return im.currentSrc||im.src||im.getAttribute('src')||'';}}}return '';}
function fallback(label){var svg='<svg xmlns="http://www.w3.org/2000/svg" width="640" height="300"><rect width="100%" height="100%" fill="#f7d77a"/><text x="50%" y="52%" text-anchor="middle" font-family="Arial" font-size="34" font-weight="700" fill="#21170f">'+label.replace(/&/g,'&amp;')+'</text></svg>';return 'data:image/svg+xml;charset=UTF-8,'+encodeURIComponent(svg)}
function apply(){var root=document.getElementById('cats');if(!root)return;var cats=root.querySelectorAll('.cat');for(var i=0;i<cats.length&&i<ORDER.length;i++){var c=cats[i],label=ORDER[i];c.setAttribute('data-sk-category-label',label);c.querySelectorAll('.skFinalCatPhoto,.skFinalCatLabel').forEach(function(x){x.remove()});var h=document.createElement('span');h.className='skFinalCatPhoto';var im=document.createElement('img');im.alt=label;im.loading='eager';im.src=imgFor(label)||fallback(label);h.appendChild(im);var l=document.createElement('span');l.className='skFinalCatLabel';l.textContent=label;c.innerHTML='';c.appendChild(h);c.appendChild(l)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply);else apply();setTimeout(apply,300);setTimeout(apply,1000);setTimeout(apply,2500);
})();
</script>'''
s=s.replace('</head>',patch+'\n</head>',1)
P.write_text(s,encoding='utf-8')
print('CLEAN CATEGORY V6')
