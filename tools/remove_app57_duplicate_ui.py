from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')

static_cats = '''<div id="cats" class="cats"><button class="cat active" onclick="selectCategory('all')">🍽️ All</button><button class="cat" onclick="selectCategory('fast')">🍕 Fast Food</button><button class="cat" onclick="selectCategory('snacks')">🥟 Snacks</button><button class="cat" onclick="selectCategory('chaat')">🥣 Chaat &amp; Special</button><button class="cat" onclick="selectCategory('birthday')">🎂 Birthday Special</button><button class="cat" onclick="selectCategory('beverages')">🥤 Beverages</button><button class="cat" onclick="selectCategory('sweets')">🍬 Sweets</button><button class="cat restaurantBtn" onclick="openRestaurants()">🏨 Restaurant / Hotel</button></div>'''
if static_cats in s:
    s = s.replace(static_cats, '<div id="cats" class="cats"></div>', 1)

# Remove the second "Sold Out" label while preserving the availability state.
s = s.replace("`<button class=\"add\" disabled>Sold Out</button>`", "`<span class=\"soldOutSpacer\"></span>`", 1)

settings = Path('app/src/main/assets/settings-fix.js')
if settings.exists():
    ss = settings.read_text(encoding='utf-8')
    marker = '/* __SK_APP57_DUPLICATE_UI_FIX__ */'
    if marker not in ss:
        ss += r'''

/* __SK_APP57_DUPLICATE_UI_FIX__ */
(function(){
  if(window.__skApp57DuplicateUiFix)return;
  window.__skApp57DuplicateUiFix=true;
  function fix(){
    document.querySelectorAll('.profileMenuBtn').forEach(function(el){el.remove()});
    document.querySelectorAll('.helpActions,.serviceMeta').forEach(function(el){el.style.setProperty('display','none','important')});
    document.querySelectorAll('.help .small').forEach(function(el){el.style.setProperty('display','none','important')});
    var cats=document.getElementById('cats');
    if(cats && !cats.querySelector('[data-sk-category]') && !cats.querySelector('.catImg')){
      cats.innerHTML='';
      if(typeof renderCats==='function')renderCats();
    }
  }
  function run(){fix();setTimeout(fix,250);setTimeout(fix,800);setTimeout(fix,1800);setTimeout(fix,3500);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){
    if(window.__skApp57DuplicateUiFixRunning)return;
    window.__skApp57DuplicateUiFixRunning=true;
    setTimeout(function(){window.__skApp57DuplicateUiFixRunning=false;fix()},80);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
'''
        settings.write_text(ss, encoding='utf-8')

p.write_text(s, encoding='utf-8')
print('App 57 duplicate UI fix applied: single category renderer, single menu, single Help Center, and single Sold Out label.')
