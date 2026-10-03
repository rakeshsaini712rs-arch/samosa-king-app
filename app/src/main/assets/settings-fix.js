/* FINAL CUSTOMER CATEGORY BAR REMOVAL — 2026-10-03 */
(function(){
  'use strict';
  if(window.__SK_CATEGORY_BAR_REMOVED_V1) return;
  window.__SK_CATEGORY_BAR_REMOVED_V1=true;
  function hide(){
    var wrap=document.getElementById('cats')||document.querySelector('.cats');
    if(wrap){
      wrap.style.setProperty('display','none','important');
      wrap.setAttribute('aria-hidden','true');
      wrap.querySelectorAll('.cat').forEach(function(el){el.style.setProperty('display','none','important');});
    }
  }
  hide();
  [0,50,150,300,700,1200,2000,3500,5000].forEach(function(ms){setTimeout(hide,ms);});
  new MutationObserver(function(){hide();}).observe(document.documentElement,{childList:true,subtree:true});
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
