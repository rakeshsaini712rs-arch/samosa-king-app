from pathlib import Path
import re

P = Path('app/src/main/assets/index.html')
s = P.read_text(encoding='utf-8')

# Remove every experimental category-photo patch so only one final renderer remains.
ids = [
    'skRealCategoryPhotoStyle','skRealCategoryPhotoScript',
    'skCategoryPhotoDedupV2','skCategoryPhotoDedupV2Script',
    'skCategoryPhotoMatchV3','skCategoryPhotoMatchV3Script',
    'skCategoryPhotoMatchV4','skCategoryPhotoMatchV4Script',
    'skCategoryPhotoFinalStyle','skCategoryPhotoFinalScript',
    'customerCategoryPhotoDedupStyle','customerCategoryPhotoDedupScript'
]
for ident in ids:
    s = re.sub(r'<style id="' + re.escape(ident) + r'">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script id="' + re.escape(ident) + r'">.*?</script>', '', s, flags=re.S)

# Remove duplicate marker blocks left by older category experiments.
s = re.sub(r'<style id="skCategoryPhotoFinalStyle">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<script id="skCategoryPhotoFinalScript">.*?</script>', '', s, flags=re.S)

final_style = r'''<style id="skCategoryPhotoFinalStyle">
/* SK_CATEGORY_PHOTOS_FINAL_SINGLE_SOURCE_20261003_V4 */
#cats{background:#17110d!important;border-bottom:1px solid #3d3027!important;}
#cats .cat{position:relative!important;overflow:hidden!important;min-width:92px!important;width:92px!important;height:78px!important;min-height:78px!important;padding:53px 6px 6px!important;display:flex!important;align-items:center!important;justify-content:center!important;text-align:center!important;border:1px solid #49392e!important;border-radius:15px!important;background:#211914!important;color:#f5eee5!important;box-shadow:0 3px 10px #00000030!important;}
#cats .cat.active{background:linear-gradient(145deg,#f6c94a,#d99d18)!important;border-color:#d99d18!important;color:#17100b!important;}
#cats .cat .skCatPhoto,#cats .cat .skFinalCatPhoto{position:absolute!important;top:5px!important;left:50%!important;transform:translateX(-50%)!important;width:46px!important;height:46px!important;border-radius:50%!important;overflow:hidden!important;border:2px solid #fff!important;background:#fff!important;display:block!important;z-index:3!important;box-shadow:0 2px 8px #00000035!important;}
#cats .cat .skCatPhoto img,#cats .cat .skFinalCatPhoto img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;visibility:visible!important;opacity:1!important;}
#cats .cat.active .skCatPhoto,#cats .cat.active .skFinalCatPhoto{border-color:#17100b!important;}
#cats .cat>span:not(.skCatPhoto):not(.skFinalCatPhoto){position:relative!important;z-index:4!important;color:inherit!important;font-weight:900!important;}
body:not(.skDark) #cats{background:#fffaf1!important;border-bottom-color:#eadfce!important;}
body:not(.skDark) #cats .cat{background:linear-gradient(145deg,#fff,#fff8ed)!important;color:#3a2819!important;border-color:#eadcc9!important;}
body:not(.skDark) #cats .cat.active{color:#17100b!important;}
@media(max-width:500px){#cats .cat{min-width:92px!important;width:92px!important;height:78px!important;}}
</style>'''

final_script = r'''<script id="skCategoryPhotoFinalScript">
(function(){
  if(window.__SK_CATEGORY_PHOTOS_FINAL_V4__) return;
  window.__SK_CATEGORY_PHOTOS_FINAL_V4__=true;
  var MAP={
    'All':'product-images/samosa.jpg',
    'Fast Food':'product-images/pizza.jpg',
    'Snacks':'product-images/samosa.jpg',
    'Chaat & Special':'product-images/dahi-bhalla-1.jpg',
    'Indian Thali':'product-images/manchurian.jpg',
    'Desi Rasoi':'product-images/manchurian.jpg',
    'Birthday Special':'product-images/gulab-jamun.jpg',
    'Beverages':'product-images/burger.jpg',
    'Sweets':'product-images/gulab-jamun.jpg',
    'Restaurant / Hotel':'product-images/pizza.jpg'
  };
  function norm(v){return (v||'').replace(/\s+/g,' ').trim().replace(/\s*\/\s*/g,' / ');}
  function apply(){
    var root=document.getElementById('cats');
    if(!root)return;
    root.querySelectorAll('.cat').forEach(function(cat){
      var key=norm(cat.textContent);
      var src=MAP[key];
      if(!src)return;
      var holder=cat.querySelector('.skCatPhoto,.skFinalCatPhoto');
      if(!holder){
        holder=document.createElement('span');
        holder.className='skFinalCatPhoto';
        var img=document.createElement('img');
        img.alt=key+' category';
        img.loading='eager';
        img.decoding='sync';
        holder.appendChild(img);
        cat.insertBefore(holder,cat.firstChild);
      }else{
        holder.classList.add('skFinalCatPhoto');
      }
      var img=holder.querySelector('img');
      if(img && img.getAttribute('src')!==src) img.src=src;
      if(img){img.style.setProperty('display','block','important');img.style.setProperty('visibility','visible','important');img.style.setProperty('opacity','1','important');}
    });
  }
  function run(){apply();setTimeout(apply,100);setTimeout(apply,500);setTimeout(apply,1500);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat'))setTimeout(apply,20);},true);
})();
</script>'''

# Insert the final single source immediately before </head> so it wins over earlier CSS.
marker = final_style + final_script
s = s.replace('</head>', marker + '\n</head>', 1)
P.write_text(s, encoding='utf-8')
print('Final category photo renderer + dark-mode contrast fix applied.')
