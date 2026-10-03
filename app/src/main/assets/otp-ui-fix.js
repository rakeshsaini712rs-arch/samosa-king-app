(function(){
  function removeOtpUi(){
    /* Permanently remove the customer OTP/login UI. */
    document.querySelectorAll('.login,#loginPhone,#otpbox,#loginMsg').forEach(function(x){
      if(x && x.parentNode) x.parentNode.removeChild(x);
    });
    document.querySelectorAll('input,button,a,label,span,div,p,section').forEach(function(el){
      var t=(el.textContent||'').trim().toLowerCase();
      var ph=((el.getAttribute&&el.getAttribute('placeholder'))||'').toLowerCase();
      var val=((el.getAttribute&&el.getAttribute('value'))||'').toLowerCase();
      if(t==='send otp'||t==='verify otp'||t==='☎ help center'||t==='help center'){
        var p=el.closest('.login,.help');
        if(p && p.parentNode) p.parentNode.removeChild(p); else if(el.parentNode) el.parentNode.removeChild(el);
        return;
      }
      if(ph.indexOf('+91')>=0||ph.indexOf('otp')>=0||val.indexOf('+91')>=0||val.indexOf('send otp')>=0){
        var p2=el.closest('.login,.otpbox,.help');
        if(p2&&p2.parentNode)p2.parentNode.removeChild(p2);else if(el.parentNode)el.parentNode.removeChild(el);
      }
    });
    document.querySelectorAll('.otpbox,#otpbox,[id*=otp],[class*=otp]').forEach(function(el){
      if(el&&el.parentNode)el.parentNode.removeChild(el);
    });
  }
  function start(){
    removeOtpUi();
    new MutationObserver(removeOtpUi).observe(document.documentElement,{childList:true,subtree:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
