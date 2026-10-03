/* Samosa King customer settings helpers. */
(function(){
  'use strict';

  /* Keep the existing Captain Live module loading unchanged. */
  function loadCaptain(){
    if(window.__SK_CAPTAIN_LIVE_V2__||window.__SK_CAPTAIN_LIVE_LOADER__)return;
    window.__SK_CAPTAIN_LIVE_LOADER__=true;
    var s=document.createElement('script');
    s.src='captain-live.js?v=20261002-1';
    s.onload=function(){window.__SK_CAPTAIN_LIVE_LOADED__=true;};
    s.onerror=function(){window.__SK_CAPTAIN_LIVE_LOADER__=false;};
    document.head.appendChild(s);
  }

  /* OTP removal: remove only the OTP controls, never the checkout/customer form. */
  function removeOtp(){
    try{
      var selectors=[
        '.otpbox',
        '#otpBox',
        '#otpInput',
        'input[name="otp"]',
        'input[placeholder*="OTP" i]',
        'button[onclick*="otp" i]',
        'button[id*="otp" i]',
        '[class*="otp" i]'
      ];
      document.querySelectorAll(selectors.join(',')).forEach(function(el){
        if(el && el.id!=='checkout' && !el.closest('#checkout')) el.remove();
      });

      /* Remove a Send OTP button and its tiny OTP-only wrapper without touching
         the customer's name/mobile/address checkout fields. */
      document.querySelectorAll('button,input[type="button"],input[type="submit"],a').forEach(function(el){
        var t=(el.textContent||el.value||'').replace(/\s+/g,' ').trim().toLowerCase();
        if(t==='send otp'||t==='verify otp'||t==='resend otp'||t==='send otp again'){
          var p=el.parentElement;
          el.remove();
          if(p && !p.querySelector('input,button,textarea,select') && /otp/i.test(p.textContent||'')) p.remove();
        }
      });

      /* Remove standalone OTP/help text left by older UI patches. */
      document.querySelectorAll('body *').forEach(function(el){
        if(el.children.length) return;
        var t=(el.textContent||'').replace(/\s+/g,' ').trim();
        if(/^\+91X{4,}\d*$/i.test(t) || /^Send OTP$/i.test(t) || /^Verify OTP$/i.test(t)) el.remove();
      });
    }catch(e){}
  }

  function start(){
    removeOtp();
    [100,300,700,1500,3000].forEach(function(ms){setTimeout(removeOtp,ms);});
    if(!window.__SK_OTP_OBSERVER__){
      window.__SK_OTP_OBSERVER__=new MutationObserver(function(){removeOtp();});
      window.__SK_OTP_OBSERVER__.observe(document.documentElement,{childList:true,subtree:true});
    }
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
  [300,1000,2500,4000].forEach(function(ms){setTimeout(loadCaptain,ms);});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',loadCaptain);else loadCaptain();
})();