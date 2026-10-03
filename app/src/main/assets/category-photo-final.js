/* CATEGORY PHOTO FINAL V2 - guaranteed local Android assets */
(function(){
  if(window.__SK_CATEGORY_PHOTO_FINAL_V2__) return;
  window.__SK_CATEGORY_PHOTO_FINAL_V2__=true;

  var BASE='file:///android_asset/product-images/';
  var MAP={
    all:'samosa.jpg',
    fast:'pizza.jpg',
    snacks:'mirchi-bada.jpg',
    chaat:'dahi-bhalla-1.jpg',
    thali:'manchurian.jpg',
    desirsoi:'pasta.jpg',
    birthday:'gulab-jamun.jpg',
    beverages:'burger.jpg',
    sweets:'kaju-katli.jpg',
    restaurant:'wraps.jpg'
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

  function installCss(){
    if(document.getElementById('sk-category-photo-v2-css')) return;
    var s=document.createElement('style');
    s.id='sk-category-photo-v2-css';
    s.textContent='#cats .cat{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;gap:5px!important;min-width:86px!important;min-height:96px!important;padding:7px 5px 8px!important;overflow:hidden!important;background:#211914!important;border:1px solid #49392e!important;border-radius:14px!important;color:#fff!important}#cats .catImg{display:flex!important;width:62px!important;height:62px!important;min-width:62px!important;min-height:62px!important;flex:0 0 62px!important;padding:2px!important;border-radius:50%!important;background:#fff!important;border:2px solid #e0a72b!important;box-shadow:0 3px 10px #0008!important;overflow:hidden!important;align-items:center!important;justify-content:center!important}#cats .catImg img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;border-radius:50%!important;visibility:visible!important;opacity:1!important}#cats .catName{display:block!important;width:100%!important;text-align:center!important;color:#fff!important;font-size:11px!important;font-weight:900!important;line-height:1.15!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}#cats .cat.active{background:#2b1b0d!important;border-color:#f6c94a!important;box-shadow:0 0 0 2px #f6c94a55!important}';
    (document.head||document.documentElement).appendChild(s);
  }

  function apply(){
    installCss();
    var root=document.getElementById('cats');
    if(!root) return;
    root.querySelectorAll('.cat').forEach(function(cat){
      var key=keyFor(cat), file=MAP[key];
      if(!file) return;
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
      var wanted=BASE+file;
      if(img.src!==wanted) img.src=wanted;
      img.alt='';
      img.loading='eager';
      img.decoding='sync';
      img.style.setProperty('display','block','important');
      img.style.setProperty('visibility','visible','important');
      img.style.setProperty('opacity','1','important');
      img.onerror=function(){
        if(img.dataset.skFallback==='1') return;
        img.dataset.skFallback='1';
        img.src=BASE+'samosa.jpg';
      };
    });
  }

  function run(){
    apply();
    [100,300,700,1500,3000,6000,10000].forEach(function(t){setTimeout(apply,t);});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  document.addEventListener('click',function(e){
    if(e.target.closest && e.target.closest('#cats .cat')) setTimeout(apply,30);
  },true);
  new MutationObserver(function(){setTimeout(apply,30);}).observe(document.documentElement,{childList:true,subtree:true});
  setInterval(apply,2000);
})();
