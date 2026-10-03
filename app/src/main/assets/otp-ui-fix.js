(function(){
  function removeOtpUi(){
    var phone=document.getElementById('loginPhone');
    if(phone){ phone.style.setProperty('display','none','important'); }
    var otp=document.getElementById('otpbox');
    if(otp){ otp.style.setProperty('display','none','important'); otp.remove(); }
    var msg=document.getElementById('loginMsg');
    if(msg){ msg.style.setProperty('display','none','important'); }
    document.querySelectorAll('button').forEach(function(b){
      if((b.textContent||'').trim().toLowerCase()==='send otp'){
        b.style.setProperty('display','none','important');
        b.remove();
      }
    });
    document.querySelectorAll('.help').forEach(function(x){
      if((x.textContent||'').toLowerCase().indexOf('help center')>=0){
        x.remove();
      }
    });
    document.querySelectorAll('*').forEach(function(x){
      var t=(x.textContent||'').trim();
      if(t==='+91XXXXXXXXXX' || t==='Send OTP' || t==='☎ Help Center'){
        var p=x.closest('div');
        if(p && p!==document.body) p.style.setProperty('display','none','important');
      }
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',removeOtpUi); else removeOtpUi();
  new MutationObserver(removeOtpUi).observe(document.documentElement,{childList:true,subtree:true});
})();