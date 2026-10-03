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
  function findSection(name){
    var wanted=(name||'').trim().toLowerCase();
    if(wanted==='all')return document.getElementById('homePage')||document.body;
    var sections=document.querySelectorAll('.section');
    for(var i=0;i<sections.length;i++){
      var h=sections[i].querySelector('h2');
      var text=(h?h.textContent:sections[i].textContent).replace(/[^a-z0-9 &/]/gi,' ').replace(/\s+/g,' ').trim().toLowerCase();
      if(text.indexOf(wanted)!==-1)return sections[i];
    }
    return null;
  }
  function wireCategories(){
    var root=document.getElementById('cats');
    if(!root||root.getAttribute('data-sk-wired')==='1')return;
    root.setAttribute('data-sk-wired','1');
    root.addEventListener('click',function(e){
      var cat=e.target.closest&&e.target.closest('.cat');
      if(!cat||!root.contains(cat))return;
      e.preventDefault();
      var name=(cat.getAttribute('aria-label')||cat.textContent||'').replace(/\s+/g,' ').trim();
      var section=findSection(name);
      root.querySelectorAll('.cat').forEach(function(x){x.classList.toggle('active',x===cat);});
      if(section){
        section.scrollIntoView({behavior:'smooth',block:'start'});
      }else if(name.toLowerCase()==='all'){
        window.scrollTo({top:0,behavior:'smooth'});
      }
    });
  }
  function themeMenu(){
    var root=document.getElementById('cats');
    if(!root||root.getAttribute('data-sk-theme')==='1')return;
    root.setAttribute('data-sk-theme','1');
    var style=document.createElement('style');
    style.textContent='#cats{background:#17110d!important;border-color:#3a2a20!important}#cats .cat{background:#241a14!important;color:#f7eee5!important;border-color:#4b392c!important;box-shadow:none!important}#cats .cat:hover,#cats .cat:focus{background:#302219!important;color:#fff!important;border-color:#d99d18!important}#cats .cat.active{background:#d99d18!important;color:#17100b!important;border-color:#f6c94a!important;box-shadow:0 3px 10px #0008!important}';
    document.head.appendChild(style);
  }
  function start(){
    removeOtp();
    cleanCategories();
    wireCategories();
    themeMenu();
    [300,1000,2500].forEach(function(ms){setTimeout(function(){removeOtp();cleanCategories();wireCategories();themeMenu();},ms);});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
  [300,1000,2500,4000].forEach(function(ms){setTimeout(loadCaptain,ms);});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',loadCaptain);else loadCaptain();
})();