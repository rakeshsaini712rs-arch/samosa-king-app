/* CATEGORY PHOTO FINAL - SINGLE SOURCE OF TRUTH */
(function(){
  if(window.__SK_CATEGORY_PHOTO_SINGLE_SOURCE__) return;
  window.__SK_CATEGORY_PHOTO_SINGLE_SOURCE__=true;

  var BASE='file:///android_asset/product-images/';
  var MAP={
    all:['samosa.jpg','All'],
    fast:['pizza.jpg','Fast Food'],
    snacks:['mirchi-bada.jpg','Snacks'],
    chaat:['dahi-bhalla-1.jpg','Chaat & Special'],
    thali:['manchurian.jpg','Indian Thali'],
    desirsoi:['pasta.jpg','Desi Rasoi'],
    birthday:['gulab-jamun.jpg','Birthday Special'],
    beverages:['burger.jpg','Beverages'],
    sweets:['kaju-katli.jpg','Sweets'],
    restaurant:['wraps.jpg','Restaurant / Hotel']
  };

  function normal(v){
    return String(v||'').replace(/\s+/g,' ').trim().toLowerCase();
  }
  function keyFor(cat,index){
    var raw=normal(cat.getAttribute('data-sk-category')||cat.getAttribute('data-label')||cat.textContent);
    raw=raw.replace(/\s*category\s*/g,' ').replace(/\s+/g,' ').trim();
    if(raw==='all'||raw.indexOf('all')===0)return 'all';
    if(raw.indexOf('fast food')>=0)return 'fast';
    if(raw==='snacks'||raw.indexOf('snacks')>=0)return 'snacks';
    if(raw.indexOf('chaat')>=0)return 'chaat';
    if(raw.indexOf('indian thali')>=0)return 'thali';
    if(raw.indexOf('desi rasoi')>=0)return 'desirsoi';
    if(raw.indexOf('birthday')>=0)return 'birthday';
    if(raw.indexOf('beverages')>=0)return 'beverages';
    if(raw.indexOf('sweets')>=0)return 'sweets';
    if(raw.indexOf('restaurant')>=0||raw.indexOf('hotel')>=0)return 'restaurant';
    return Object.keys(MAP)[index]||'all';
  }

  function css(){
    if(document.getElementById('sk-category-single-source-css'))return;
    var s=document.createElement('style');
    s.id='sk-category-single-source-css';
    s.textContent=
      '#cats{display:flex!important;overflow-x:auto!important;gap:9px!important;padding:10px 12px!important;scrollbar-width:none!important;}' +
      '#cats::-webkit-scrollbar{display:none!important;}' +
      '#cats .cat{position:relative!important;display:flex!important;flex:0 0 94px!important;width:94px!important;min-width:94px!important;height:98px!important;min-height:98px!important;padding:7px 5px 6px!important;margin:0!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;gap:5px!important;overflow:hidden!important;border:1px solid #49392e!important;border-radius:15px!important;background:#211914!important;color:#fff!important;}' +
      '#cats .cat .skFinalCategoryImage{display:flex!important;width:68px!important;height:68px!important;min-width:68px!important;min-height:68px!important;flex:0 0 68px!important;border-radius:50%!important;overflow:hidden!important;background:#fff!important;border:2px solid #f6c94a!important;box-shadow:0 3px 10px #0008!important;align-items:center!important;justify-content:center!important;}' +
      '#cats .cat .skFinalCategoryImage img{display:block!important;width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;object-fit:cover!important;border-radius:50%!important;visibility:visible!important;opacity:1!important;}' +
      '#cats .cat .skFinalCategoryLabel{display:block!important;width:100%!important;height:14px!important;line-height:14px!important;text-align:center!important;color:#fff!important;font-size:10px!important;font-weight:900!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;}' +
      '#cats .cat.active{background:linear-gradient(145deg,#f6c94a,#d99d18)!important;border-color:#d99d18!important;color:#17100b!important;}' +
      '#cats .cat.active .skFinalCategoryImage{border-color:#17100b!important;}' +
      '#cats .cat.active .skFinalCategoryLabel{color:#17100b!important;}';
    (document.head||document.documentElement).appendChild(s);
  }

  function apply(){
    css();
    var root=document.getElementById('cats');
    if(!root)return;
    root.querySelectorAll('.cat').forEach(function(cat,index){
      var key=keyFor(cat,index),item=MAP[key]||MAP.all;
      var active=cat.classList.contains('active');
      /* Remove every previous category-image/label implementation. */
      cat.innerHTML='';
      cat.setAttribute('data-sk-category',key);
      var holder=document.createElement('span');
      holder.className='skFinalCategoryImage';
      var img=document.createElement('img');
      img.src=BASE+item[0];
      img.alt=item[1];
      img.loading='eager';
      img.decoding='sync';
      img.onerror=function(){
        if(img.dataset.fallback==='1')return;
        img.dataset.fallback='1';
        img.src=BASE+'samosa.jpg';
      };
      holder.appendChild(img);
      var label=document.createElement('span');
      label.className='skFinalCategoryLabel';
      label.textContent=item[1];
      cat.appendChild(holder);
      cat.appendChild(label);
      if(active)cat.classList.add('active');
    });
  }

  function schedule(){
    clearTimeout(window.__SK_CATEGORY_FINAL_TIMER__);
    window.__SK_CATEGORY_FINAL_TIMER__=setTimeout(apply,80);
  }
  function start(){
    apply();
    [100,300,700,1200,2000,3500,5000,8000].forEach(function(t){setTimeout(apply,t);});
    setInterval(apply,1500);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
  new MutationObserver(schedule).observe(document.documentElement,{childList:true,subtree:true});
})();
