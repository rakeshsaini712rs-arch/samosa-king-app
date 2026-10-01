from pathlib import Path

path = Path('MainActivity.java')
s = path.read_text(encoding='utf-8')

marker = '</head><body>'
if marker not in s:
    raise SystemExit('Customer HTML <head><body> marker not found')

js = r'''<script>
const MAP={All:'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=160&h=160&fit=crop','Fast Food':'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=160&h=160&fit=crop',Snacks:'https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?w=160&h=160&fit=crop','Chaat & Special':'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=160&h=160&fit=crop','Indian Thali':'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=160&h=160&fit=crop','Desi Rasoi':'https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?w=160&h=160&fit=crop','Birthday Special':'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=160&h=160&fit=crop',Beverages:'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=160&h=160&fit=crop',Sweets:'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=160&h=160&fit=crop','Restaurant / Hotel':'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=160&h=160&fit=crop'};
function fixCats(){document.querySelectorAll('#cats .cat').forEach(function(el){var t=(el.textContent||'').replace(/\s+/g,' ').trim();var u=MAP[t];if(u){el.style.backgroundImage="url('"+u+"')";el.style.backgroundSize='46px 46px';el.style.backgroundPosition='center 5px';el.style.backgroundRepeat='no-repeat';el.style.paddingTop='54px';el.style.minHeight='78px';el.style.backgroundColor='#fff';el.style.borderRadius='14px';}})}
document.addEventListener('DOMContentLoaded',function(){fixCats();var c=document.getElementById('cats');if(c)new MutationObserver(fixCats).observe(c,{childList:true,subtree:true});});
</script>'''

java_js = js.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '')

if 'const MAP={All:' in s and 'function fixCats()' in s:
    raise SystemExit('Category photo patch already present')

s = s.replace(marker, marker + java_js, 1)
path.write_text(s, encoding='utf-8')
print('Customer category photo patch applied')
