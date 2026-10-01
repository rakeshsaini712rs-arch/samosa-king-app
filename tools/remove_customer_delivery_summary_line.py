from pathlib import Path

p = Path('app/src/main/assets/settings-fix.js')
if not p.exists():
    raise SystemExit('settings-fix.js not found')

js = r'''

/* FINAL: remove the standalone customer delivery summary line. */
(function(){
  if(window.__skFinalRemoveDeliverySummary)return;
  window.__skFinalRemoveDeliverySummary=true;
  function remove(){
    var nodes=document.querySelectorAll('body *');
    nodes.forEach(function(el){
      if(el.children.length) return;
      var t=(el.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
      if(t.indexOf('nansa gate, nawalgarh')>=0 && t.indexOf('delivery ₹30')>=0 && t.indexOf('₹100 minimum')>=0 && t.indexOf('cod')>=0){
        var target=el;
        if(target.parentElement && target.parentElement.children.length===1) target=target.parentElement;
        target.remove();
      }
    });
  }
  function run(){remove();setTimeout(remove,100);setTimeout(remove,500);setTimeout(remove,1500);setTimeout(remove,3000);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){
    if(window.__skFinalRemoveDeliverySummaryBusy)return;
    window.__skFinalRemoveDeliverySummaryBusy=true;
    setTimeout(function(){window.__skFinalRemoveDeliverySummaryBusy=false;remove()},50);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
'''
text=p.read_text(encoding='utf-8')
if 'window.__skFinalRemoveDeliverySummary' not in text:
    p.write_text(text+js,encoding='utf-8')
print('Standalone customer delivery summary line removal installed.')
