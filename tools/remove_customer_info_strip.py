from pathlib import Path

p = Path('app/src/main/assets/settings-fix.js')
if not p.exists():
    raise SystemExit('settings-fix.js not found')

fix = r'''

/* FINAL CUSTOMER REQUEST: remove the old Delivery/Payment/Open/Help information strip. */
(function(){
  if(window.__skFinalRemoveInfoStrip)return;
  window.__skFinalRemoveInfoStrip=true;
  function remove(){
    document.querySelectorAll('.info').forEach(function(el){
      var t=(el.textContent||'').replace(/\\s+/g,' ').trim().toLowerCase();
      if(t.indexOf('delivery')>=0 && t.indexOf('payment')>=0 && t.indexOf('open')>=0 && t.indexOf('help')>=0){
        el.style.setProperty('display','none','important');
        el.setAttribute('aria-hidden','true');
      }
    });
    document.querySelectorAll('body *').forEach(function(el){
      if(el.children.length)return;
      var t=(el.textContent||'').replace(/\\s+/g,' ').trim().toLowerCase();
      if(t==='delivery ₹30 up to 5 km' || t==='payment cash on delivery' || t==='open 8:30 am–6:00 pm' || t==='help 7891851475'){
        var p=el.closest('.info') || el.parentElement;
        if(p)p.style.setProperty('display','none','important');
      }
    });
  }
  function run(){remove();setTimeout(remove,250);setTimeout(remove,1000);setTimeout(remove,2500);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){
    if(window.__skFinalRemoveInfoStripBusy)return;
    window.__skFinalRemoveInfoStripBusy=true;
    setTimeout(function(){window.__skFinalRemoveInfoStripBusy=false;remove()},100);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
'''

text = p.read_text(encoding='utf-8')
if 'window.__skFinalRemoveInfoStrip' not in text:
    p.write_text(text + fix, encoding='utf-8')
print('Final customer info-strip removal patch installed.')
