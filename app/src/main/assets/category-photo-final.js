/* CATEGORY PHOTO FINAL - guaranteed local Android assets, no remote URLs */
(function(){
  if(window.__SK_CATEGORY_PHOTO_FINAL_LOCAL__) return;
  window.__SK_CATEGORY_PHOTO_FINAL_LOCAL__=true;

  var MAP={
    'all':'product-images/samosa.jpg',
    'fast':'product-images/pizza.jpg',
    'snacks':'product-images/mirchi-bada.jpg',
    'chaat':'product-images/dahi-bhalla-1.jpg',
    'thali':'product-images/manchurian.jpg',
    'desirsoi':'product-images/pasta.jpg',
    'birthday':'product-images/gulab-jamun.jpg',
    'beverages':'product-images/burger.jpg',
    'sweets':'product-images/kaju-katli.jpg',
    'restaurant':'product-images/wraps.jpg'
  };

  function keyFor(cat){
    var k=cat.getAttribute('data-sk-category');
    if(k) return String(k).toLowerCase().trim();
    var t=(cat.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
    if(t==='all') return 'all';
    if(t.indexOf('fast food')>=0) return 'fast';
    if(t==='snacks') return 'snacks';
    if(t.indexOf('chaat')>=0) return 'chaat';
    if(t.indexOf('indian thali')>=0) return 'thali';
    if(t.indexOf('desi rasoi')>=0) return 'desirsoi';
    if(t.indexOf('birthday')>=0) return 'birthday';
    if(t.indexOf('beverages')>=0) return 'beverages';
    if(t.indexOf('sweets')>=0) return 'sweets';
    if(t.indexOf('restaurant')>=0 || t.indexOf('hotel')>=0) return 'restaurant';
    return '';
  }

  function apply(){
    var root=document.getElementById('cats');
    if(!root) return;
    root.querySelectorAll('.cat').forEach(function(cat){
      var key=keyFor(cat), src=MAP[key];
      if(!src) return;
      var holder=cat.querySelector('.catImg');
      if(!holder){
        holder=document.createElement('span');
        holder.className='catImg';
        cat.insertBefore(holder,cat.firstChild);
      }
      var img=holder.querySelector('img');
      if(!img){
        img=document.createElement('img');
        holder.appendChild(img);
      }
      img.src=src;
      img.alt=(cat.querySelector('.catName')||cat).textContent.trim()+' category';
      img.loading='eager';
      img.decoding='sync';
      img.style.setProperty('display','block','important');
      img.style.setProperty('visibility','visible','important');
      img.style.setProperty('opacity','1','important');
      holder.classList.remove('fallback');
    });
  }

  function run(){
    apply();
    [100,300,700,1500,3000].forEach(function(t){setTimeout(apply,t);});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  document.addEventListener('click',function(e){
    if(e.target.closest && e.target.closest('#cats .cat')) setTimeout(apply,30);
  },true);
  new MutationObserver(function(){setTimeout(apply,30);}).observe(document.documentElement,{childList:true,subtree:true});
})();
