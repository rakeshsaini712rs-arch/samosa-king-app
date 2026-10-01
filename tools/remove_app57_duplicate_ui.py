from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')

# Remove the old hard-coded category row; categories are rendered by the single runtime renderer.
static_cats = '''<div id="cats" class="cats"><button class="cat active" onclick="selectCategory('all')">🍽️ All</button><button class="cat" onclick="selectCategory('fast')">🍕 Fast Food</button><button class="cat" onclick="selectCategory('snacks')">🥟 Snacks</button><button class="cat" onclick="selectCategory('chaat')">🥣 Chaat &amp; Special</button><button class="cat" onclick="selectCategory('birthday')">🎂 Birthday Special</button><button class="cat" onclick="selectCategory('beverages')">🥤 Beverages</button><button class="cat" onclick="selectCategory('sweets')">🍬 Sweets</button><button class="cat restaurantBtn" onclick="openRestaurants()">🏨 Restaurant / Hotel</button></div>'''
if static_cats in s:
    s = s.replace(static_cats, '<div id="cats" class="cats"></div>', 1)

# Keep only one Sold Out control; the availability label remains visible.
s = s.replace('`<button class="add" disabled>Sold Out</button>`', '`<span class="soldOutSpacer"></span>`', 1)

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

  function text(el){ return (el.textContent||'').replace(/\s+/g,' ').trim(); }

  function fixCategories(){
    var cats=document.getElementById('cats');
    if(!cats)return;
    var seen={};
    Array.prototype.slice.call(cats.querySelectorAll('.cat')).forEach(function(el){
      var key=el.getAttribute('onclick') || text(el);
      if(seen[key]) el.remove(); else seen[key]=true;
    });
    if(!cats.querySelector('.cat') && typeof renderCats==='function')renderCats();
  }

  function fixTickers(){
    document.querySelectorAll('.skTickerTrack').forEach(function(track){
      var children=Array.prototype.slice.call(track.children);
      // One ticker is 7 children: item, dot, item, dot, item, dot, item.
      if(children.length>7) children.slice(7).forEach(function(el){el.remove()});
    });
  }

  function fixSoldOut(){
    document.querySelectorAll('.card .add[disabled]').forEach(function(el){
      if(text(el)==='Sold Out')el.remove();
    });
  }

  function fixOldServiceHelp(){
    // Keep the dedicated Help Center, but remove the older service-card Call/WhatsApp row.
    document.querySelectorAll('.services .helpActions').forEach(function(el){el.remove()});
    document.querySelectorAll('.serviceMeta').forEach(function(el){el.remove()});
    // Remove any obsolete OTP/login block if it is injected again.
    document.querySelectorAll('.login').forEach(function(el){el.remove()});
  }

  function fixOldDeliverySummary(){
    document.querySelectorAll('body *').forEach(function(el){
      if(el.children.length!==0)return;
      var t=text(el);
      if((t.indexOf('📍 Nansa Gate, Nawalgarh')>=0 && t.indexOf('₹100 minimum')>=0) ||
         t.indexOf('🚚 Delivery ₹30 up to 5 km')>=0 ||
         t==='Delivery ₹30 up to 5 km' ||
         t==='Cash on Delivery' ||
         t==='8:30 AM–6:00 PM' ||
         t==='7891851475'){
        // Only remove the old standalone info blocks, not the header hours/location.
        if(el.closest('.info,.serviceMeta'))el.remove();
      }
    });
  }

  function fixDuplicateMenu(){
    var menus=Array.prototype.slice.call(document.querySelectorAll('button,a,[role="button"]')).filter(function(el){return text(el)==='☰'});
    menus.slice(1).forEach(function(el){el.remove()});
  }

  function fixDuplicateCardTitles(){
    document.querySelectorAll('.card').forEach(function(card){
      var heads=Array.prototype.slice.call(card.querySelectorAll('h3'));
      var seen={};
      heads.forEach(function(h){
        var t=text(h);
        if(t && seen[t])h.remove(); else if(t)seen[t]=true;
      });
    });
  }

  function fix(){
    fixCategories();
    fixTickers();
    fixSoldOut();
    fixOldServiceHelp();
    fixOldDeliverySummary();
    fixDuplicateMenu();
    fixDuplicateCardTitles();
  }

  function run(){fix();setTimeout(fix,250);setTimeout(fix,800);setTimeout(fix,1800);setTimeout(fix,3500);setTimeout(fix,6000);}
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
print('App 57 duplicate UI cleanup strengthened: one menu, one category set, one ticker, one Sold Out state, one card title, and one Help Center.')