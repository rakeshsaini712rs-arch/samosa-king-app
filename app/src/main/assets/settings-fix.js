/* Customer category-photo stability fix — 2026-10-02
 * Keep exactly one category photo per button and restore it after renderCats()/category taps.
 * Do not change product/cart/order behaviour.
 */
(function(){
  if(window.__SK_CATEGORY_PHOTO_STABLE_FIX__) return;
  window.__SK_CATEGORY_PHOTO_STABLE_FIX__=true;

  var MAP={
    'All':'product-images/samosa.jpg',
    'Fast Food':'product-images/pizza.jpg',
    'Snacks':'product-images/samosa.jpg',
    'Chaat & Special':'product-images/dahi-bhalla-1.jpg',
    'Indian Thali':'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=1200&q=95',
    'Desi Rasoi':'https://chokhidhani.com/welcome-indore/wp-content/uploads/2025/06/5-1024x768-1.jpg',
    'Birthday Special':'https://images.pexels.com/photos/8015241/pexels-photo-8015241.jpeg?cs=srgb&dl=pexels-cup-of-couple-8015241.jpg&fm=jpg',
    'Beverages':'https://images.unsplash.com/photo-1617814192855-5bd13c3f0977?auto=format&fit=crop&w=900&q=90',
    'Sweets':'product-images/kaju-katli.jpg',
    'Restaurant / Hotel':'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=90'
  };

  function clean(s){return String(s||'').replace(/\s+/g,' ').trim();}

  function fix(){
    var root=document.getElementById('cats');
    if(!root) return;

    root.querySelectorAll('.cat').forEach(function(btn){
      /* Remove the older competing photo implementation. */
      btn.querySelectorAll('.skCatPhoto').forEach(function(x){x.remove();});

      var nameEl=btn.querySelector('.catName');
      var key=clean(nameEl ? nameEl.textContent : btn.textContent);
      var src=MAP[key];
      if(!src) return;

      /* Exactly one .catImg and exactly one img. */
      var holders=btn.querySelectorAll('.catImg');
      var holder=holders[0];
      for(var i=1;i<holders.length;i++) holders[i].remove();
      if(!holder){
        holder=document.createElement('span');
        holder.className='catImg';
        btn.insertBefore(holder,nameEl||btn.firstChild);
      }

      var imgs=holder.querySelectorAll('img');
      var img=imgs[0];
      for(var j=1;j<imgs.length;j++) imgs[j].remove();
      if(!img){
        img=document.createElement('img');
        holder.appendChild(img);
      }
      img.alt=key;
      img.loading='eager';
      img.decoding='sync';
      if(img.getAttribute('src')!==src) img.src=src;
      img.style.display='block';
      img.style.visibility='visible';
      img.style.opacity='1';
      img.onerror=function(){this.style.display='block';};
    });
  }

  function run(){fix();setTimeout(fix,50);setTimeout(fix,250);setTimeout(fix,700);setTimeout(fix,1500);}

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat')) setTimeout(fix,0);},true);
  document.addEventListener('touchend',function(e){if(e.target.closest&&e.target.closest('#cats .cat')) setTimeout(fix,0);},true);
  new MutationObserver(function(){fix();}).observe(document.documentElement,{childList:true,subtree:true});
})();
