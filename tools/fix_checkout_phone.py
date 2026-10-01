from pathlib import Path

INDEX = Path("app/src/main/assets/index.html")
MARKER = "</body>"

s = INDEX.read_text(encoding="utf-8")
if MARKER not in s:
    raise SystemExit("ERROR: index.html closing body tag not found")

script = """<script>
(function(){
  if(window.__skCheckoutPhoneFix)return;
  window.__skCheckoutPhoneFix=true;

  function cleanMainPhoneFields(){
    var main=document.getElementById('homePage')||document.body;
    main.querySelectorAll('#loginPhone').forEach(function(el){
      el.style.setProperty('display','none','important');
      el.setAttribute('aria-hidden','true');
      var next=el.nextElementSibling;
      if(next && next.tagName==='BUTTON') next.style.setProperty('display','none','important');
    });
    var otp=document.getElementById('otpbox');
    if(otp) otp.style.setProperty('display','none','important');
    var loginMsg=document.getElementById('loginMsg');
    if(loginMsg) loginMsg.style.setProperty('display','none','important');
    document.querySelectorAll('input#phone,input[name="phone"],input[data-field="phone"]').forEach(function(el){
      var modal=document.getElementById('modal');
      if(modal && modal.contains(el)) return;
      if(el.id==='profileMobile') return;
      var wrap=el.closest('label,.field,.inputGroup,.formGroup');
      if(wrap && wrap.querySelectorAll('input').length===1) wrap.style.setProperty('display','none','important');
      else el.style.setProperty('display','none','important');
    });
  }

  function ensureCheckoutPhone(){
    cleanMainPhoneFields();
    var modal=document.getElementById('modal');
    if(!modal || !modal.querySelector('.sheet')) return;
    var sheet=modal.querySelector('.sheet');
    var phone=sheet.querySelector('#phone');
    if(!phone){
      var name=sheet.querySelector('#name');
      phone=document.createElement('input');
      phone.id='phone';
      phone.type='tel';
      phone.inputMode='numeric';
      phone.autocomplete='tel';
      phone.maxLength=10;
      phone.className='input';
      phone.placeholder='Mobile number (10 digits)';
      phone.setAttribute('aria-label','Mobile number');
      if(name && name.parentNode) name.parentNode.insertBefore(phone,name.nextSibling);
      else sheet.insertBefore(phone,sheet.firstChild);
    }
    phone.oninput=function(){this.value=this.value.replace(/\D/g,'').slice(0,10);};
  }

  function enforceCheckoutPhoneValidation(){
    if(typeof window.placeOrder!=='function' || window.__skCheckoutPhoneWrapped)return;
    window.__skCheckoutPhoneWrapped=true;
    var original=window.placeOrder;
    window.placeOrder=function(){
      var phone=document.getElementById('phone');
      var value=phone ? phone.value.replace(/\D/g,'') : '';
      if(!/^\d{10}$/.test(value)){
        if(phone){phone.focus();phone.setCustomValidity('Please enter a valid 10-digit mobile number.');}
        alert('Please enter a valid 10-digit mobile number.');
        return;
      }
      if(phone) phone.setCustomValidity('');
      return original.apply(this,arguments);
    };
  }

  function run(){
    cleanMainPhoneFields();
    ensureCheckoutPhone();
    enforceCheckoutPhoneValidation();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  document.addEventListener('click',function(e){
    var t=e.target;
    if(t && (t.closest('#modal .order') || t.closest('.cartbtn') || t.closest('.buyNow'))){
      setTimeout(run,60);
    }
  },true);
  new MutationObserver(function(){
    if(window.__skCheckoutPhoneBusy)return;
    window.__skCheckoutPhoneBusy=true;
    setTimeout(function(){window.__skCheckoutPhoneBusy=false;run();},80);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>\n"""

while "window.__skCheckoutPhoneFix" in s:
    marker_pos=s.find("window.__skCheckoutPhoneFix")
    start=s.rfind("<script>",0,marker_pos)
    end=s.find("</script>",marker_pos)
    if start<0 or end<0: break
    s=s[:start]+s[end+len("</script>"):]

s=s.replace(MARKER,script+MARKER,1)
INDEX.write_text(s,encoding="utf-8")
print("Checkout-only mobile number fix injected; main-screen phone hidden and 10-digit checkout validation enforced.")
