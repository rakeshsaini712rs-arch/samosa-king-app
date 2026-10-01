from pathlib import Path

p = Path('app/src/main/assets/settings-fix.js')
s = p.read_text(encoding='utf-8')

info_marker = '/* __SK_FINAL_CUSTOMER_INFO_CLEANUP__ */'
if info_marker not in s:
    patch = r'''

/* __SK_FINAL_CUSTOMER_INFO_CLEANUP__ */
(function(){
  if(window.__skFinalCustomerInfoCleanup)return;
  window.__skFinalCustomerInfoCleanup=true;
  function remove(){
    document.querySelectorAll('.info,.serviceMeta').forEach(function(el){
      el.style.setProperty('display','none','important');
    });
    document.querySelectorAll('body *').forEach(function(el){
      if(el.children.length!==0)return;
      var t=(el.textContent||'').replace(/\s+/g,' ').trim();
      if(t.indexOf('📍 Nansa Gate, Nawalgarh')>=0 && t.indexOf('₹100 minimum')>=0 && t.indexOf('COD')>=0){
        el.style.setProperty('display','none','important');
      }
    });
  }
  function run(){remove();setTimeout(remove,300);setTimeout(remove,1000);setTimeout(remove,2500);setTimeout(remove,5000);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){
    if(window.__skFinalCustomerInfoCleanupRunning)return;
    window.__skFinalCustomerInfoCleanupRunning=true;
    setTimeout(function(){window.__skFinalCustomerInfoCleanupRunning=false;remove()},150);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
'''
    s += patch

banner_marker = '/* __SK_MENU_PHOTO_BANNER_RESTORE__ */'
if banner_marker not in s:
    banner_patch = r'''

/* __SK_MENU_PHOTO_BANNER_RESTORE__ */
(function(){
  if(window.__skMenuPhotoBannerRestore)return;
  window.__skMenuPhotoBannerRestore=true;
  function make(){
    if(document.getElementById('skBannerCarousel'))return true;
    var cats=document.getElementById('cats');
    if(!cats)return false;
    var imgs=window.SK_IMAGES||{};
    var data=function(key){return imgs[key] ? 'data:image/jpeg;base64,'+imgs[key] : ''};
    var slides=[
      {key:'pizza',title:'HOT & FRESH PIZZA',sub:'Freshly prepared • Order now'},
      {key:'burger',title:'JUICY BURGER',sub:'Hot • Fresh • Delicious'},
      {key:'kachori',title:'CRISPY SAMOSA',sub:'Hot • Fresh • Crispy'}
    ];
    var wrap=document.createElement('section');
    wrap.id='skBannerCarousel';
    wrap.setAttribute('aria-label','Samosa King menu photos');
    wrap.innerHTML='<div class="skBannerViewport"><div class="skBannerTrack">'+slides.map(function(x){
      var src=data(x.key);
      return '<div class="skPromo"><img src="'+src+'" alt="'+x.title+'"><div class="skPromoText"><span>👑 SAMOSA KING • NAWALGARH</span><b>'+x.title+'</b><small>'+x.sub+'</small></div></div>';
    }).join('')+'</div></div><div class="skPromoDots">'+slides.map(function(_,i){return '<i class="skPromoDot '+(i===0?'active':'')+'"></i>'}).join('')+'</div>';
    var style=document.createElement('style');
    style.id='skMenuPhotoBannerStyle';
    style.textContent='#skBannerCarousel{margin:10px 12px 8px;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px #0002;background:#160d08}#skBannerCarousel .skBannerViewport{overflow:hidden}#skBannerCarousel .skBannerTrack{display:flex;transition:transform .45s ease}#skBannerCarousel .skPromo{min-width:100%;height:190px;position:relative;overflow:hidden;background:#21140c}#skBannerCarousel .skPromo img{width:100%;height:100%;object-fit:cover;display:block}#skBannerCarousel .skPromo:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#0009 0%,#0002 55%,transparent 82%)}#skBannerCarousel .skPromoText{position:absolute;z-index:2;left:18px;top:50%;transform:translateY(-50%);color:#fff;max-width:70%;text-shadow:0 2px 8px #000}#skBannerCarousel .skPromoText span{display:block;font-size:10px;font-weight:900;letter-spacing:1px}#skBannerCarousel .skPromoText b{display:block;font-size:25px;line-height:1.05;margin:5px 0}#skBannerCarousel .skPromoText small{font-size:11px;font-weight:700}#skBannerCarousel .skPromoDots{display:flex;justify-content:center;gap:6px;padding:8px;background:#160d08}#skBannerCarousel .skPromoDot{display:block;width:7px;height:7px;border-radius:50%;background:#ffffff66}#skBannerCarousel .skPromoDot.active{background:#fff;width:18px;border-radius:5px}';
    document.head.appendChild(style);
    cats.parentNode.insertBefore(wrap,cats);
    var track=wrap.querySelector('.skBannerTrack');
    var dots=[].slice.call(wrap.querySelectorAll('.skPromoDot'));
    var index=0;
    function show(i){index=(i+slides.length)%slides.length;track.style.transform='translateX(-'+(index*100)+'%)';dots.forEach(function(d,n){d.classList.toggle('active',n===index)})}
    dots.forEach(function(d,n){d.onclick=function(){show(n)}});
    setInterval(function(){show(index+1)},3500);
    return true;
  }
  function start(){
    if(make())return;
    var tries=0;
    var timer=setInterval(function(){if(make()||++tries>30)clearInterval(timer)},200);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
'''
    s += banner_patch

p.write_text(s, encoding='utf-8')
print('Customer cleanup retained and missing menu photo banner carousel restored.')