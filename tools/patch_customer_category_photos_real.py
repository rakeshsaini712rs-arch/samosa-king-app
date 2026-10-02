from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
marker = 'SK_CATEGORY_PHOTOS_REAL_LOCAL_20261002'
if marker in s:
    print('Real local category-photo fix already present.')
    raise SystemExit(0)

css_js = r'''<style id="skRealCategoryPhotoStyle">
/* SK_CATEGORY_PHOTOS_REAL_LOCAL_20261002 */
#cats .cat{position:relative!important;overflow:hidden!important;min-height:78px!important;height:78px!important;padding:53px 8px 6px!important;display:flex!important;align-items:center!important;justify-content:center!important;text-align:center!important;background-image:none!important}
#cats .cat .skCatPhoto{position:absolute!important;top:5px!important;left:50%!important;transform:translateX(-50%)!important;width:46px!important;height:46px!important;border-radius:50%!important;overflow:hidden!important;border:2px solid #ffffff!important;box-shadow:0 2px 8px #00000022!important;background:#fff!important;display:block!important;z-index:1!important}
#cats .cat .skCatPhoto img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;visibility:visible!important;opacity:1!important}
#cats .cat.active .skCatPhoto{border-color:#17100b!important;box-shadow:0 2px 8px #00000033!important}
#cats .cat>span:not(.skCatPhoto){position:relative!important;z-index:2!important;display:block!important}
</style>
<script id="skRealCategoryPhotoScript">
(function(){
  if(window.__SK_CATEGORY_PHOTOS_REAL_LOCAL__) return;
  window.__SK_CATEGORY_PHOTOS_REAL_LOCAL__=true;
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
  function cleanText(el){return (el.textContent||'').replace(/\\s+/g,' ').trim();}
  function fix(){
    var root=document.getElementById('cats');
    if(!root) return;
    root.querySelectorAll('.cat').forEach(function(el){
      var key=cleanText(el);
      var src=MAP[key];
      if(!src) return;
      var holder=el.querySelector('.skCatPhoto');
      if(!holder){
        holder=document.createElement('span');
        holder.className='skCatPhoto';
        var img=document.createElement('img');
        img.alt=key+' category';
        img.loading='eager';
        img.decoding='sync';
        img.src=src;
        img.onerror=function(){this.style.display='none';};
        holder.appendChild(img);
        el.insertBefore(holder,el.firstChild);
      }else{
        var img=holder.querySelector('img');
        if(img && img.getAttribute('src')!==src) img.src=src;
        if(img) {img.style.setProperty('display','block','important');img.style.setProperty('visibility','visible','important');img.style.setProperty('opacity','1','important');}
      }
    });
  }
  function run(){fix();setTimeout(fix,50);setTimeout(fix,200);setTimeout(fix,500);setTimeout(fix,1000);setTimeout(fix,2000);}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat')) run();},true);
  new MutationObserver(function(){fix();}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''

if '</head>' not in s:
    raise SystemExit('Could not find </head> in customer index.html')
s=s.replace('</head>',css_js+'</head>',1)
p.write_text(s,encoding='utf-8')
print('Injected local, bundled category photos with persistent DOM restoration.')
