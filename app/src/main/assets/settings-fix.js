/* CUSTOMER CATEGORY IMAGE FIX — 2026-10-03 */
(function(){
  'use strict';
  if(window.__SK_CATEGORY_IMAGES_FIXED_V2__) return;
  window.__SK_CATEGORY_IMAGES_FIXED_V2__=true;

  var map=[
    ['all','samosa.jpg','All'],
    ['fast food','pizza.jpg','Fast Food'],
    ['snacks','mirchi-bada.jpg','Snacks'],
    ['chaat special','dahi-bhalla-1.jpg','Chaat & Special'],
    ['indian thali','manchurian.jpg','Indian Thali'],
    ['desi rasoi','pasta.jpg','Desi Rasoi'],
    ['birthday special','gulab-jamun.jpg','Birthday Special'],
    ['beverages','burger.jpg','Beverages'],
    ['sweets','kaju-katli.jpg','Sweets'],
    ['restaurant hotel','wraps.jpg','Restaurant / Hotel']
  ];
  var base='product-images/';
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ');}
  function getMap(text){
    var n=norm(text);
    for(var i=0;i<map.length;i++){
      if(n===map[i][0] || n.indexOf(map[i][0])>=0) return map[i];
    }
    return null;
  }
  function apply(){
    var root=document.getElementById('cats')||document.querySelector('.cats');
    if(!root) return;
    root.style.setProperty('display','flex','important');
    root.style.setProperty('overflow-x','auto','important');
    root.style.setProperty('gap','8px','important');
    root.style.setProperty('padding','10px 12px','important');
    root.querySelectorAll('.cat').forEach(function(c){
      var m=getMap(c.getAttribute('data-label')||c.textContent||'');
      if(!m) return;
      c.style.setProperty('display','flex','important');
      c.style.setProperty('flex-direction','column','important');
      c.style.setProperty('padding','0','important');
      c.style.setProperty('min-width','108px','important');
      c.style.setProperty('min-height','96px','important');
      c.style.setProperty('overflow','hidden','important');
      c.style.setProperty('border-radius','14px','important');
      var old=c.querySelector('.skCategoryPhoto');
      if(!old){
        old=document.createElement('span');
        old.className='skCategoryPhoto';
        var im=document.createElement('img');
        im.alt=m[2];
        im.loading='eager';
        im.decoding='sync';
        im.src=base+m[1];
        im.onerror=function(){
          if(im.dataset.fallback==='1') return;
          im.dataset.fallback='1';
          im.src=base+'samosa.jpg';
        };
        old.appendChild(im);
        c.innerHTML='';
        c.appendChild(old);
      }
      var label=c.querySelector('.skCategoryLabel');
      if(!label){
        label=document.createElement('span');
        label.className='skCategoryLabel';
        c.appendChild(label);
      }
      label.textContent=m[2];
      c.setAttribute('data-sk-category',m[0]);
    });
  }
  var style=document.createElement('style');
  style.textContent=''+
    '#cats,.cats{display:flex!important;overflow-x:auto!important;gap:8px!important;padding:10px 12px!important;scrollbar-width:none!important;}'+
    '#cats::-webkit-scrollbar,.cats::-webkit-scrollbar{display:none!important;}'+
    '#cats .cat,.cats .cat{display:flex!important;flex:0 0 108px!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;padding:0!important;min-width:108px!important;min-height:96px!important;overflow:hidden!important;border-radius:14px!important;}'+
    '#cats .skCategoryPhoto,.cats .skCategoryPhoto{display:block!important;width:100%!important;height:66px!important;min-height:66px!important;overflow:hidden!important;background:#f4e4c5!important;}'+
    '#cats .skCategoryPhoto img,.cats .skCategoryPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important;}'+
    '#cats .skCategoryLabel,.cats .skCategoryLabel{display:block!important;padding:7px 4px!important;text-align:center!important;line-height:1.15!important;font-weight:900!important;font-size:11px!important;white-space:normal!important;color:inherit!important;}';
  (document.head||document.documentElement).appendChild(style);
  function run(){apply();[100,400,900,1800,3500,7000].forEach(function(ms){setTimeout(apply,ms);});}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  new MutationObserver(function(){clearTimeout(window.__skCatFixTimer);window.__skCatFixTimer=setTimeout(apply,120);}).observe(document.documentElement,{childList:true,subtree:true});
})();

/* Load the already-built real Captain Live module into the customer page. */
(function(){
  'use strict';
  function loadCaptain(){
    if(window.__SK_CAPTAIN_LIVE_V2__||window.__SK_CAPTAIN_LIVE_LOADER__)return;
    window.__SK_CAPTAIN_LIVE_LOADER__=true;
    var s=document.createElement('script');
    s.src='captain-live.js?v=20261002-1';
    s.onload=function(){window.__SK_CAPTAIN_LIVE_LOADED__=true;};
    s.onerror=function(){window.__SK_CAPTAIN_LIVE_LOADER__=false;};
    document.head.appendChild(s);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',loadCaptain);else loadCaptain();
  [300,1000,2500,4000].forEach(function(ms){setTimeout(loadCaptain,ms);});
})();
