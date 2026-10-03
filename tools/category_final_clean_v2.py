from pathlib import Path
html=Path('app/src/main/assets/index.html')
s=html.read_text(encoding='utf-8')
css='''<style id="categoryFinalCleanV2Css">#cats{display:flex!important;overflow-x:auto!important;gap:8px!important;padding:10px 12px!important;scrollbar-width:none!important;white-space:nowrap!important}#cats::-webkit-scrollbar{display:none!important}#cats .cat{display:flex!important;flex:0 0 auto!important;align-items:center!important;justify-content:center!important;min-height:44px!important;padding:9px 12px!important;white-space:nowrap!important;overflow:hidden!important;font-size:0!important}#cats .cat *{display:none!important}#cats .cat::after{content:attr(data-clean-label)!important;font-size:11px!important;line-height:1.15!important;font-weight:900!important;white-space:nowrap!important}</style>'''
js='''<script id="categoryFinalCleanV2Script">(function(){if(window.__SK_CATEGORY_FINAL_V2__)return;window.__SK_CATEGORY_FINAL_V2__=true;var names=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\\s+/g,' ')}function key(v){var t=norm(v).replace(/\\bcategory\\b/g,' ').replace(/\\s+/g,' ').trim();for(var i=0;i<names.length;i++){var n=norm(names[i]);if(t===n||t.indexOf(n)>=0||n.indexOf(t)>=0)return i}return -1}function clean(){var root=document.getElementById('cats')||document.querySelector('.cats');if(!root)return;var chosen=new Array(names.length);Array.prototype.slice.call(root.querySelectorAll('.cat')).forEach(function(c){var i=key(c.getAttribute('data-label')||c.textContent||'');if(i<0){c.remove();return}if(chosen[i]){c.remove();return}chosen[i]=c;c.setAttribute('data-clean-label',names[i]);c.setAttribute('aria-label',names[i])});names.forEach(function(_,i){if(chosen[i])root.appendChild(chosen[i])})}function run(){clean();[100,300,800,1500,3000,6000].forEach(function(t){setTimeout(clean,t)})}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();new MutationObserver(function(){clearTimeout(window.__skCatTimerV2);window.__skCatTimerV2=setTimeout(clean,60)}).observe(document.documentElement,{childList:true,subtree:true})})();</script>'''
for tag,ident in [('style','categoryFinalCleanV2Css'),('script','categoryFinalCleanV2Script')]:
 marker=f'<{tag} id="{ident}">'; start=s.find(marker)
 if start>=0:
  end=s.find(f'</{tag}>',start)
  if end>=0:s=s[:start]+s[end+len(f'</{tag}>'):]
head=s.lower().rfind('</head>')
if head<0:raise RuntimeError('no head')
s=s[:head]+css+js+s[head:]
html.write_text(s,encoding='utf-8')
print('CATEGORY_FINAL_CLEAN_V2_APPLIED')