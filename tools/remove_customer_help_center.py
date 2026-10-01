from pathlib import Path

idx = Path('app/src/main/assets/index.html')
settings = Path('app/src/main/assets/settings-fix.js')

if not idx.exists():
    raise SystemExit('index.html not found')
if not settings.exists():
    raise SystemExit('settings-fix.js not found')

html = idx.read_text(encoding='utf-8')
css = '<style id="sk-final-hide-customer-help-center">.help{display:none!important}</style>'
if 'sk-final-hide-customer-help-center' not in html:
    html = html.replace('</head>', css + '</head>', 1)
    idx.write_text(html, encoding='utf-8')

js = r'''

/* FINAL: remove the obsolete customer Help Center block only. */
(function(){
  if(window.__skFinalRemoveHelpCenter)return;
  window.__skFinalRemoveHelpCenter=true;
  function remove(){
    document.querySelectorAll('.help').forEach(function(el){el.remove();});
  }
  function run(){remove();setTimeout(remove,100);setTimeout(remove,500);setTimeout(remove,1500);setTimeout(remove,3000);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){
    if(window.__skFinalRemoveHelpCenterBusy)return;
    window.__skFinalRemoveHelpCenterBusy=true;
    setTimeout(function(){window.__skFinalRemoveHelpCenterBusy=false;remove()},50);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
'''
text = settings.read_text(encoding='utf-8')
if 'window.__skFinalRemoveHelpCenter' not in text:
    settings.write_text(text + js, encoding='utf-8')

print('Customer Help Center / Order-help / Call / WhatsApp block removal installed.')
