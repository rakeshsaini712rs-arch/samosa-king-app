from pathlib import Path
import re

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')

# Keep the delivery ticker content to one copy. This also handles older ticker markup.
s = re.sub(
    r"function skProductTicker\(\)\{.*?\}",
    "function skProductTicker(){return '<div class=\"skProductTicker\"><div class=\"skTickerTrack\"><span class=\"skTickerItem\">⏱ 20–30 min</span><span class=\"skTickerDot\">•</span><span class=\"skTickerItem\">⚡ Near & Fast</span><span class=\"skTickerDot\">•</span><span class=\"skTickerItem\">🔥 Fresh & Hot</span><span class=\"skTickerDot\">•</span><span class=\"skTickerItem\">🚴 Fast Delivery</span></div></div>'}",
    s,
    count=1,
    flags=re.S,
)

# Remove obsolete customer OTP/login UI and old 5 km wording.
s = re.sub(r'<input id="loginPhone".*?</div>', '', s, count=1, flags=re.S)
s = s.replace('₹30 up to 5 km', '₹30').replace('Delivery ₹30 up to 5 km', 'Delivery ₹30')

# Remove duplicate Sold Out button; keep the availability label only.
s = re.sub(r'<button[^>]*class=["\']add["\'][^>]*disabled[^>]*>\s*Sold Out\s*</button>', '', s, flags=re.I)

# Remove duplicate service metadata/help blocks when present in source.
s = re.sub(r'<div[^>]*class=["\'][^"\']*serviceMeta[^"\']*["\'][^>]*>.*?</div>', '', s, count=1, flags=re.S|re.I)
s = re.sub(r'<div[^>]*class=["\']help["\'][^>]*>\s*<b>☎ Help Center</b>.*?</div>', '', s, count=1, flags=re.S|re.I)

# Runtime normalization is intentional: some customer UI blocks are rendered dynamically.
# It removes only exact repeated text/controls and does not touch products, prices, cart or Firebase data.
runtime = r'''<script id="skCustomerDuplicateCleanup">
(function(){
  if(window.__skCustomerDuplicateCleanup)return;
  window.__skCustomerDuplicateCleanup=true;
  function cleanRepeatedText(el){
    if(!el || el.children.length) return;
    var t=(el.textContent||'').replace(/\s+/g,' ').trim();
    if(!t || t.length%2) return;
    var h=t.length/2;
    if(t.slice(0,h)===t.slice(h)) el.textContent=t.slice(0,h);
  }
  function clean(){
    // Category buttons: collapse labels such as "AllAll" while preserving the button.
    document.querySelectorAll('.cat').forEach(function(e){cleanRepeatedText(e);});

    // Remove exact duplicate category buttons, if two separate buttons render with the same label/action.
    var seenCats={};
    document.querySelectorAll('.cat').forEach(function(e){
      var k=((e.getAttribute('onclick')||'')+'|'+(e.textContent||'')).replace(/\s+/g,' ').trim();
      if(k && seenCats[k]) e.remove(); else if(k) seenCats[k]=1;
    });

    // Product delivery strip: never show the same strip twice inside one card.
    document.querySelectorAll('.card').forEach(function(card){
      var tickers=card.querySelectorAll('.skProductTicker');
      for(var i=1;i<tickers.length;i++) tickers[i].remove();

      // Some older builds render the product name in two identical heading elements.
      var heads=card.querySelectorAll('h3');
      var seenHeads={};
      heads.forEach(function(h){
        var t=(h.textContent||'').replace(/\s+/g,' ').trim();
        if(t && seenHeads[t]) h.remove(); else if(t) seenHeads[t]=1;
      });

      // Keep only the availability label; remove a disabled Sold Out action button.
      card.querySelectorAll('button[disabled]').forEach(function(b){
        if((b.textContent||'').replace(/\s+/g,' ').trim().toLowerCase()==='sold out') b.remove();
      });
    });

    // The service summary already contains delivery/payment/help actions; remove duplicate blocks.
    document.querySelectorAll('.serviceMeta').forEach(function(e){e.remove();});
    document.querySelectorAll('.help').forEach(function(e){
      if(/Help Center|Order\/help:|7891851475/.test(e.textContent||'')) e.remove();
    });

    // Remove a second identical bottom help action group if dynamically rendered.
    var helpSeen={};
    document.querySelectorAll('.helpActions').forEach(function(e){
      var k=(e.textContent||'').replace(/\s+/g,' ').trim();
      if(helpSeen[k]) e.remove(); else helpSeen[k]=1;
    });
  }
  function run(){clean();setTimeout(clean,150);setTimeout(clean,500);setTimeout(clean,1200);setTimeout(clean,2500);}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  new MutationObserver(function(){setTimeout(clean,50);}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>'''

if 'id="skCustomerDuplicateCleanup"' not in s:
    s = s.replace('</body>', runtime + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Customer-only duplicate cleanup applied: delivery ticker, category labels/buttons, Sold Out action, duplicate product headings, service metadata and Help Center duplicates.')