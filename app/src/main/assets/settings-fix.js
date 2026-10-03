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
      var selectors=['.otpbox','#otpBox','#otpInput','input[name="otp"]','input[placeholder*="OTP" i]','button[onclick*="otp" i]','button[id*="otp" i]','[class*="otp" i]'];
      document.querySelectorAll(selectors.join(',')).forEach(function(el){
        if(el&&el.id!=='checkout'&&!el.closest('#checkout'))el.remove();
      });
      document.querySelectorAll('button,input[type="button"],input[type="submit"],a').forEach(function(el){
        var t=(el.textContent||el.value||'').replace(/\s+/g,' ').trim().toLowerCase();
        if(t==='send otp'||t==='verify otp'||t==='resend otp'||t==='send otp again'){
          var p=el.parentElement;el.remove();
          if(p&&!p.querySelector('input,button,textarea,select')&&/otp/i.test(p.textContent||''))p.remove();
        }
      });
      document.querySelectorAll('body *').forEach(function(el){
        if(el.children.length)return;
        var t=(el.textContent||'').replace(/\s+/g,' ').trim();
        if(/^\+91X{4,}\d*$/i.test(t)||/^Send OTP$/i.test(t)||/^Verify OTP$/i.test(t))el.remove();
      });
    }catch(e){}
  }

  /* Category buttons were rendered with duplicate visible labels such as
     "All category" + "All". Normalize each button by position so the
     existing click handlers/listeners remain attached to the same element. */
  function cleanCategories(){
    try{
      var names=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];
      var cats=document.querySelectorAll('.cat');
      for(var i=0;i<cats.length&&i<names.length;i++){
        var el=cats[i];
        if(el.textContent.replace(/\s+/g,' ').trim()!==names[i]){
          el.textContent=names[i];
        }
        el.setAttribute('aria-label',names[i]);
        el.setAttribute('title',names[i]);
      }
    }catch(e){}
  }

  function start(){
    removeOtp();
    cleanCategories();
    [50,150,300,700,1500,3000,5000].forEach(function(ms){
      setTimeout(function(){removeOtp();cleanCategories();},ms);
    });
    if(!window.__SK_UI_FIX_OBSERVER__){
      window.__SK_UI_FIX_OBSERVER__=new MutationObserver(function(){
        removeOtp();
        cleanCategories();
      });
      window.__SK_UI_FIX_OBSERVER__.observe(document.documentElement,{childList:true,subtree:true});
    }
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
  [300,1000,2500,4000].forEach(function(ms){setTimeout(loadCaptain,ms);});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',loadCaptain);else loadCaptain();
})();