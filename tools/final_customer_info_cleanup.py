from pathlib import Path

p = Path('app/src/main/assets/settings-fix.js')
s = p.read_text(encoding='utf-8')
marker = '/* __SK_FINAL_CUSTOMER_INFO_CLEANUP__ */'
if marker in s:
    print('Final customer info cleanup already installed.')
    raise SystemExit(0)

patch = r'''

/* __SK_FINAL_CUSTOMER_INFO_CLEANUP__ */
(function(){
  if(window.__skFinalCustomerInfoCleanup)return;
  window.__skFinalCustomerInfoCleanup=true;
  function remove(){
    document.querySelectorAll('.info,.help,.helpActions,.serviceMeta').forEach(function(el){
      el.style.setProperty('display','none','important');
    });
    document.querySelectorAll('body *').forEach(function(el){
      if(el.children.length!==0)return;
      var t=(el.textContent||'').replace(/\s+/g,' ').trim();
      if(t==='☎ Help Center' || t.indexOf('Order/help: 7891851475')>=0){
        var p=el.closest('.help')||el.parentElement;
        if(p)p.style.setProperty('display','none','important');
        else el.style.setProperty('display','none','important');
      }
      if(t.indexOf('📍 Nansa Gate, Nawalgarh')>=0 && t.indexOf('₹100 minimum')>=0 && t.indexOf('COD')>=0){
        el.style.setProperty('display','none','important');
      }
    });
  }
  function run(){remove();setTimeout(remove,300);setTimeout(remove,1000);setTimeout(remove,2500);setTimeout(remove,5000);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){
    if(window.__skFinalCustomerInfoCleanupRunning)return;
    window.__skFinalCustomerInfoCleanupRunning=true;
    setTimeout(function(){window.__skFinalCustomerInfoCleanupRunning=false;remove()},150);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
'''
p.write_text(s + patch, encoding='utf-8')
print('Final customer info/help cleanup installed.')
