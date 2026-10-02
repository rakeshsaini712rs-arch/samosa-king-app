from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
marker = 'SK_CATEGORY_PHOTOS_DEDUP_20261002_V2'
if marker in s:
    print('Category photo deduplication already present.')
    raise SystemExit(0)

css_js = r'''<style id="skCategoryPhotoDedupV2">
/* SK_CATEGORY_PHOTOS_DEDUP_20261002_V2 */
#cats .cat::before,#cats .cat::after{content:none!important;display:none!important;background:none!important}
#cats .cat{background-image:none!important}
#cats .cat>img,#cats .cat>picture,#cats .cat>.catPhoto,#cats .cat>.categoryImage,#cats .cat>.category-img,#cats .cat>.cat-image{display:none!important}
#cats .cat .skCatPhoto{z-index:3!important}
</style>
<script id="skCategoryPhotoDedupV2Script">
(function(){
  if(window.__SK_CATEGORY_PHOTO_DEDUP_V2__) return;
  window.__SK_CATEGORY_PHOTO_DEDUP_V2__=true;
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
  function text(el){return (el.textContent||'').replace(/\s+/g,' ').trim();}
  function fix(){
    var root=document.getElementById('cats');
    if(!root)return;
    root.querySelectorAll('.cat').forEach(function(cat){
      cat.style.setProperty('background-image','none','important');
      Array.from(cat.children).forEach(function(ch){
        if(ch.tagName==='IMG'||ch.tagName==='PICTURE'||(ch.querySelector&&ch.querySelector('img')&&!ch.classList.contains('skCatPhoto'))){
          ch.style.setProperty('display','none','important');
        }
      });
      var holders=Array.from(cat.querySelectorAll('.skCatPhoto'));
      holders.slice(1).forEach(function(h){h.remove();});
      var key=text(cat),src=MAP[key];
      if(!src)return;
      var holder=holders[0];
      if(!holder){
        holder=document.createElement('span');
        holder.className='skCatPhoto';
        holder.innerHTML='<img alt="'+key+' category" loading="eager" decoding="sync">';
        cat.insertBefore(holder,cat.firstChild);
      }
      var img=holder.querySelector('img');
      if(img){
        img.src=src;
        img.style.setProperty('display','block','important');
        img.style.setProperty('visibility','visible','important');
        img.style.setProperty('opacity','1','important');
      }
    });
  }
  function run(){fix();setTimeout(fix,50);setTimeout(fix,200);setTimeout(fix,500);setTimeout(fix,1000);setTimeout(fix,2000);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat'))run();},true);
  new MutationObserver(function(){fix();}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''

if '</head>' not in s:
    raise SystemExit('Could not find </head> in customer index.html')
s=s.replace('</head>',css_js+'</head>',1)
p.write_text(s,encoding='utf-8')
print('Injected category-photo deduplication and persistent single-photo restoration.')
