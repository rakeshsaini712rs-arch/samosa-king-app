from pathlib import Path

p = Path('app/src/main/assets/settings-fix.js')
if not p.exists():
    raise SystemExit('settings-fix.js not found')

fix = r'''

/* FINAL: hide the obsolete customer Delivery / Payment / Open / Help card. */
(function(){
  if(window.__skFinalRemoveInfoStrip)return;
  window.__skFinalRemoveInfoStrip=true;
  function remove(){
    document.querySelectorAll('.info').forEach(function(el){
      var t=(el.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
      if(t.indexOf('delivery')>=0 && t.indexOf('payment')>=0 && t.indexOf('open')>=0 && t.indexOf('help')>=0){
        el.remove();
      }
    });
  }
  function run(){remove();setTimeout(remove,100);setTimeout(remove,500);setTimeout(remove,1500);setTimeout(remove,3000);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){
    if(window.__skFinalRemoveInfoStripBusy)return;
    window.__skFinalRemoveInfoStripBusy=true;
    setTimeout(function(){window.__skFinalRemoveInfoStripBusy=false;remove()},50);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
'''

text = p.read_text(encoding='utf-8')
if 'window.__skFinalRemoveInfoStrip' not in text:
    p.write_text(text + fix, encoding='utf-8')

# Also put a source-level CSS guard in index.html so the block cannot flash before JS runs.
idx = Path('app/src/main/assets/index.html')
if idx.exists():
    html = idx.read_text(encoding='utf-8')
    guard = '<style id="sk-final-hide-customer-info">.info{display:none!important}</style>'
    if 'id="sk-final-hide-customer-info"' not in html:
        html = html.replace('</head>', guard + '</head>', 1)
        idx.write_text(html, encoding='utf-8')
print('Final customer Delivery/Payment/Open/Help information card removal installed.')
