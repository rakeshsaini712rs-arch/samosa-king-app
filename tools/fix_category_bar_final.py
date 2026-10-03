from pathlib import Path
import base64
import json

html = Path('app/src/main/assets/index.html')
s = html.read_text(encoding='utf-8')

# Keep the category bar visible; remove any older hide rule from previous experiments.
marker = 'FINAL_REMOVE_CATEGORY_BAR'
if marker in s:
    start = s.find('<style id="skRemoveCategoryBar">')
    end = s.find('</style>', start)
    if start >= 0 and end >= 0:
        s = s[:start] + s[end + len('</style>'):]

# The previous fixes relied on file:///android_asset image URLs. On some WebView/build
# combinations those URLs are not resolved by the injected renderer. Embed the existing
# local JPG bytes directly into the HTML so category photos have no runtime dependency.
photos = [
    ('All', 'samosa.jpg'),
    ('Fast Food', 'pizza.jpg'),
    ('Snacks', 'mirchi-bada.jpg'),
    ('Chaat & Special', 'dahi-bhalla-1.jpg'),
    ('Indian Thali', 'manchurian.jpg'),
    ('Desi Rasoi', 'pasta.jpg'),
    ('Birthday Special', 'gulab-jamun.jpg'),
    ('Beverages', 'burger.jpg'),
    ('Sweets', 'kaju-katli.jpg'),
    ('Restaurant / Hotel', 'wraps.jpg'),
]

payload = []
for label, filename in photos:
    p = html.parent / 'product-images' / filename
    if not p.exists():
        raise FileNotFoundError(f'Missing category photo asset: {p}')
    b64 = base64.b64encode(p.read_bytes()).decode('ascii')
    payload.append({'label': label, 'src': 'data:image/jpeg;base64,' + b64})

marker_js = 'CATEGORY_PHOTO_EMBEDDED_FINAL_V1'
if marker_js in s:
    a = s.find('<script id="categoryPhotoEmbeddedFinal">')
    b = s.find('</script>', a)
    if a >= 0 and b >= 0:
        s = s[:a] + s[b + len('</script>'):]

css = '''<style id="categoryPhotoEmbeddedFinalCss">
#cats{display:flex!important;overflow-x:auto!important;overflow-y:hidden!important;gap:8px!important;padding:10px 12px!important;visibility:visible!important;opacity:1!important;min-height:116px!important}
#cats .cat{display:flex!important;flex:0 0 96px!important;width:96px!important;height:100px!important;min-height:100px!important;padding:6px!important;box-sizing:border-box!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;gap:5px!important;overflow:hidden!important;visibility:visible!important;opacity:1!important}
#cats .skEmbeddedPhoto{display:block!important;width:100%!important;height:68px!important;min-height:68px!important;flex:0 0 68px!important;object-fit:cover!important;border-radius:10px!important;visibility:visible!important;opacity:1!important;background:#f4e4c5!important}
#cats .skEmbeddedLabel{display:block!important;width:100%!important;padding:2px 2px 0!important;text-align:center!important;font-size:11px!important;line-height:1.15!important;font-weight:900!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
</style>'''

js_data = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
script = '''<script id="categoryPhotoEmbeddedFinal">
/* CATEGORY_PHOTO_EMBEDDED_FINAL_V1 */
(function(){
  var DATA=%s;
  function apply(){
    var root=document.getElementById('cats')||document.querySelector('.cats');
    if(!root) return;
    var cards=root.querySelectorAll('.cat');
    if(!cards.length) return;
    cards.forEach(function(c,i){
      if(i>=DATA.length) return;
      var old=c.querySelector('.skEmbeddedPhoto');
      if(!old){
        var img=document.createElement('img');
        img.className='skEmbeddedPhoto';
        img.alt=DATA[i].label;
        img.src=DATA[i].src;
        img.draggable=false;
        var label=document.createElement('span');
        label.className='skEmbeddedLabel';
        label.textContent=DATA[i].label;
        c.innerHTML='';
        c.appendChild(img);
        c.appendChild(label);
      }else{
        old.src=DATA[i].src;
        var lab=c.querySelector('.skEmbeddedLabel');
        if(lab) lab.textContent=DATA[i].label;
      }
      c.style.setProperty('display','flex','important');
      c.style.setProperty('visibility','visible','important');
      c.style.setProperty('opacity','1','important');
    });
  }
  function run(){apply();setTimeout(apply,50);setTimeout(apply,250);setTimeout(apply,800);setTimeout(apply,1800);}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  new MutationObserver(function(){clearTimeout(window.__skEmbeddedCatTimer);window.__skEmbeddedCatTimer=setTimeout(apply,120);}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>''' % js_data

head = s.lower().rfind('</head>')
if head < 0:
    raise RuntimeError('index.html has no </head> marker')
s = s[:head] + css + script + s[head:]
html.write_text(s, encoding='utf-8')
print('CATEGORY_PHOTO_EMBEDDED_FINAL_V1: embedded all 10 category JPGs directly into index.html')
