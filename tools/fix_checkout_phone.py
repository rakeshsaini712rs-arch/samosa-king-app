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
    document.querySelectorAll('input#phone,input[name=\"phone\"],input[data-field=\"phone\"]').forEach(function(el){
      var modal=document.getElementById('modal');
      if(modal && modal.contains(el)) return;
      var wrap=el.closest('label,.field,.inputGroup,.formGroup');
      if(wrap && wrap.querySelectorAll('input').length===1) wrap.remove();
      else el.remove();
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

  function run(){
    cleanMainPhoneFields();
    ensureCheckoutPhone();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();

  document.addEventListener('click',function(e){
    var t=e.target;
    if(t && (t.closest('#modal .order') || t.closest('.cartbtn') || t.closest('.buyNow'))){
      setTimeout(ensureCheckoutPhone,60);
    }
  },true);

  new MutationObserver(function(){
    if(window.__skCheckoutPhoneBusy)return;
    window.__skCheckoutPhoneBusy=true;
    setTimeout(function(){window.__skCheckoutPhoneBusy=false;run();},80);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>\n"""

# Remove any previous copy of this exact build-time fix before adding one.
while "window.__skCheckoutPhoneFix" in s:
    start = s.rfind("<script>", 0, s.find("window.__skCheckoutPhoneFix"))
    end = s.find("</script>", s.find("window.__skCheckoutPhoneFix"))
    if start < 0 or end < 0:
        break
    end += len("</script>")
    s = s[:start] + s[end:]

s = s.replace(MARKER, script + MARKER, 1)
INDEX.write_text(s, encoding="utf-8")
print("Checkout-only mobile number fix injected.")
