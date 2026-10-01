from pathlib import Path

path = Path('MainActivity.java')
s = path.read_text(encoding='utf-8')

marker = '</head><body>'
if marker not in s:
    raise SystemExit('Customer HTML <head><body> marker not found')

js = r'''<script>
const MAP={All:'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=160&h=160&fit=crop','Fast Food':'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=160&h=160&fit=crop',Snacks:'https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?w=160&h=160&fit=crop','Chaat & Special':'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=160&h=160&fit=crop','Indian Thali':'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=160&h=160&fit=crop','Desi Rasoi':'https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?w=160&h=160&fit=crop','Birthday Special':'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=160&h=160&fit=crop',Beverages:'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=160&h=160&fit=crop',Sweets:'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=160&h=160&fit=crop','Restaurant / Hotel':'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=160&h=160&fit=crop'};
function fixCats(){document.querySelectorAll('#cats .cat').forEach(function(el){var t=(el.textContent||'').replace(/\s+/g,' ').trim();var u=MAP[t];if(u){el.setAttribute('data-category-photo',u);el.style.setProperty('background-image',"url('"+u+"')",'important');el.style.setProperty('background-size','46px 46px','important');el.style.setProperty('background-position','center 5px','important');el.style.setProperty('background-repeat','no-repeat','important');el.style.setProperty('padding-top','54px','important');el.style.setProperty('min-height','78px','important');el.style.setProperty('background-color','#fff','important');el.style.setProperty('border-radius','14px','important');}})}
function bootCategoryPhotos(){fixCats();var c=document.getElementById('cats');if(!c)return;if(window.__SK_CAT_PHOTO_OBSERVER__)return;window.__SK_CAT_PHOTO_OBSERVER__=new MutationObserver(function(){fixCats();});window.__SK_CAT_PHOTO_OBSERVER__.observe(c,{childList:true,subtree:true,attributes:true,attributeFilter:['style','class','data-category-photo']});}
document.addEventListener('DOMContentLoaded',function(){bootCategoryPhotos();[50,150,300,700,1200].forEach(function(ms){setTimeout(fixCats,ms);});});
document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat')){fixCats();setTimeout(fixCats,0);setTimeout(fixCats,100);setTimeout(fixCats,300);setTimeout(fixCats,800);}},true);
</script>'''

java_js = js.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '')

if 'const MAP={All:' in s and 'function fixCats()' in s:
    # Replace the old patch instead of refusing, so every new APK gets the permanent version.
    start = s.find('<script>const MAP={All:')
    end = s.find('</script>', start)
    if start >= 0 and end >= 0:
        end += len('</script>')
        old = s[start:end]
        old_java = old.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '')
        # MainActivity contains the script as a Java string, so replace the exact escaped payload.
        if old_java in s:
            s = s.replace(old_java, java_js, 1)
        else:
            raise SystemExit('Existing category photo patch payload not found')
    else:
        raise SystemExit('Existing category photo script bounds not found')
else:
    s = s.replace(marker, marker + java_js, 1)

path.write_text(s, encoding='utf-8')
print('Customer category photo persistence patch applied')
