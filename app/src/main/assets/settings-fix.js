/* Samosa King customer settings helpers. */
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
  function removeOtp(){
    try{
      document.querySelectorAll('.otpbox,#otpBox,#otpInput,input[name="otp"],input[placeholder*="OTP" i],[class*="otp" i]').forEach(function(el){
        if(el&&el.id!=='checkout'&&!el.closest('#checkout'))el.remove();
      });
      document.querySelectorAll('button,input[type="button"],input[type="submit"],a').forEach(function(el){
        var t=(el.textContent||el.value||'').replace(/\s+/g,' ').trim().toLowerCase();
        if(t==='send otp'||t==='verify otp'||t==='resend otp'||t==='send otp again')el.remove();
      });
    }catch(e){}
  }
  function cleanCategories(){
    try{
      var names=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];
      var cats=document.querySelectorAll('.cat');
      for(var i=0;i<cats.length&&i<names.length;i++){
        var el=cats[i], wanted=names[i];
        if(el.getAttribute('data-sk-cleaned')==='1')continue;
        if(el.textContent.replace(/\s+/g,' ').trim()!==wanted)el.textContent=wanted;
        el.setAttribute('aria-label',wanted);
        el.setAttribute('title',wanted);
        el.setAttribute('data-sk-cleaned','1');
      }
    }catch(e){}
  }
  function start(){
    removeOtp();
    cleanCategories();
    [300,1000,2500].forEach(function(ms){setTimeout(function(){removeOtp();cleanCategories();},ms);});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
  [300,1000,2500,4000].forEach(function(ms){setTimeout(loadCaptain,ms);});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',loadCaptain);else loadCaptain();
})();