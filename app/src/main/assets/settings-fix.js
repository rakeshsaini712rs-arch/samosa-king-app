/* Samosa King customer settings helpers. Category photos intentionally disabled for now. */
(function(){
  'use strict';
  /* Category photos are intentionally removed. Keep category names/click behavior unchanged. */
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
