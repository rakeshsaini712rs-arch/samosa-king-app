from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
marker = 'SK_CATEGORY_PHOTOS_MATCH_BY_SECTION_V3_20261002'
if marker in s:
    print('Category photo section matching V3 already present.')
    raise SystemExit(0)

js = r'''<style id="skCategoryPhotoMatchV3">
/* SK_CATEGORY_PHOTOS_MATCH_BY_SECTION_V3_20261002 */
#cats .cat{background-image:none!important}
#cats .cat::before,#cats .cat::after{content:none!important;display:none!important;background:none!important}
#cats .cat .skCatPhoto{display:flex!important;position:relative!important;z-index:3!important;align-items:center!important;justify-content:center!important;overflow:hidden!important}
#cats .cat .skCatPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}
</style>
<script id="skCategoryPhotoMatchV3Script">
(function(){
  if(window.__SK_CATEGORY_PHOTO_MATCH_V3__) return;
  window.__SK_CATEGORY_PHOTO_MATCH_V3__=true;
  function norm(v){return (v||'').replace(/\s+/g,' ').trim().replace(/\s*\/\s*/g,' / ').toLowerCase();}
  function titleOf(el){
    var h=el.querySelector&&el.querySelector('h2,h3,.sectionTitle');
    return norm(h?h.textContent:el.textContent);
  }
  function findSection(key){
    var wanted=norm(key), best=null;
    document.querySelectorAll('.section').forEach(function(sec){
      var h=sec.querySelector('h2,h3,.sectionTitle');
      if(h && norm(h.textContent)===wanted){best=sec;}
    });
    return best;
  }
  function firstProductImage(sec){
    if(!sec)return '';
    var img=sec.querySelector('.card .visual img, .card img');
    return img && img.getAttribute('src') ? img.getAttribute('src') : '';
  }
  function apply(){
    var root=document.getElementById('cats');
    if(!root)return;
    root.querySelectorAll('.cat').forEach(function(cat){
      var key=(cat.textContent||'').replace(/\s+/g,' ').trim();
      var sec=findSection(key);
      var src=firstProductImage(sec);
      var old=cat.querySelectorAll('.skCatPhoto');
      old.forEach(function(x,i){if(i>0)x.remove();});
      var holder=old[0];
      if(!holder){
        holder=document.createElement('span');
        holder.className='skCatPhoto';
        holder.style.width='100%';
        holder.style.height='74px';
        holder.style.marginBottom='4px';
        holder.innerHTML='<img alt="'+key+' category">';
        cat.insertBefore(holder,cat.firstChild);
      }
      var img=holder.querySelector('img');
      if(src && img){
        img.src=src;
        img.style.display='block';
      }
      Array.from(cat.children).forEach(function(ch){
        if(ch!==holder && (ch.tagName==='IMG'||ch.tagName==='PICTURE'||(ch.querySelector&&ch.querySelector('img')))) ch.style.setProperty('display','none','important');
      });
    });
  }
  function run(){apply();setTimeout(apply,100);setTimeout(apply,400);setTimeout(apply,1000);setTimeout(apply,2000);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat'))run();},true);
  new MutationObserver(function(){apply();}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''

if '</head>' not in s:
    raise SystemExit('Could not find </head> in customer index.html')
s=s.replace('</head>',js+'</head>',1)
p.write_text(s,encoding='utf-8')
print('Added category-to-first-product image matching V3.')
