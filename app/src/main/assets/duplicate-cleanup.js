(function(){
  'use strict';
  if(window.__SK_DUPLICATE_CLEANUP__) return;
  window.__SK_DUPLICATE_CLEANUP__=true;
  function norm(s){return String(s||'').replace(/\s+/g,' ').trim();}
  var CATEGORY_IMAGES={
    'All':'product-images/samosa.jpg',
    'Fast Food':'product-images/pizza.jpg',
    'Snacks':'product-images/samosa.jpg',
    'Chaat & Special':'product-images/dahi-bhalla-1.jpg',
    'Indian Thali':'product-images/manchurian.jpg',
    'Desi Rasoi':'product-images/manchurian.jpg',
    'Birthday Special':'product-images/gulab-jamun.jpg',
    'Beverages':'product-images/burger.jpg',
    'Sweets':'product-images/gulab-jamun.jpg',
    'Restaurant / Hotel':'product-images/pizza.jpg'
  };
  var CATEGORY_KEYS=Object.keys(CATEGORY_IMAGES);
  function removeExactText(text){
    var nodes=[];
    document.querySelectorAll('body *').forEach(function(el){
      if(el.children.length===0 && norm(el.textContent)===text) nodes.push(el);
    });
    nodes.forEach(function(el){
      var p=el;
      for(var n=0;n<6 && p.parentElement;n++){
        if(p.classList && (p.classList.contains('help')||p.classList.contains('services')||p.classList.contains('info'))){el=p;break;}
        p=p.parentElement;
      }
      if(el && el!==document.body) el.remove();
    });
  }
  function restorePromoBanners(){
    if(document.getElementById('skBannerCarousel')) return;
    var anchor=document.querySelector('.cats') || document.querySelector('.hero');
    if(!anchor || !anchor.parentElement) return;
    var imgs=window.SK_IMAGES||{};
    var data=function(key){return imgs[key] ? 'data:image/jpeg;base64,'+imgs[key] : '';};
    var items=[
      {key:'pizza',title:'HOT & FRESH PIZZA',sub:'Freshly prepared • Order now'},
      {key:'burger',title:'JUICY BURGER',sub:'Hot • Fresh • Delicious'},
      {key:'samosa',title:'CRISPY SAMOSA',sub:'Hot • Fresh • Crispy'}
    ];
    var wrap=document.createElement('section');
    wrap.id='skBannerCarousel';
    wrap.style.cssText='margin:10px 12px 8px;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px #0003;background:#160d08;display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;';
    items.forEach(function(item){
      var card=document.createElement('div');
      card.style.cssText='min-width:88%;height:180px;position:relative;overflow:hidden;border-radius:18px;scroll-snap-align:start;background:linear-gradient(135deg,#5b1b0c,#17100b);';
      var src=data(item.key);
      if(src){
        var img=document.createElement('img');
        img.src=src; img.alt=item.title;
        img.style.cssText='width:100%;height:100%;object-fit:cover;display:block;';
        card.appendChild(img);
      }
      var shade=document.createElement('div');
      shade.style.cssText='position:absolute;inset:0;background:linear-gradient(90deg,#000b,#0002 60%,transparent);';
      card.appendChild(shade);
      var text=document.createElement('div');
      text.style.cssText='position:absolute;left:16px;top:50%;transform:translateY(-50%);color:#fff;max-width:72%;text-shadow:0 2px 8px #000;';
      text.innerHTML='<span style="display:block;font-size:11px;font-weight:900;letter-spacing:1px;color:#f6c94a">SAMOSA KING • NAWALGARH</span><b style="display:block;font-size:25px;line-height:1.05;margin:5px 0">'+item.title+'</b><small style="font-size:11px;font-weight:700">'+item.sub+'</small>';
      card.appendChild(text);
      wrap.appendChild(card);
    });
    anchor.parentElement.insertBefore(wrap,anchor);
  }
  function categoryLabel(raw){
    for(var i=0;i<CATEGORY_KEYS.length;i++) if(raw.indexOf(CATEGORY_KEYS[i])>=0) return CATEGORY_KEYS[i];
    return '';
  }
  function ensureCategoryPhoto(el,label){
    if(el.querySelector('.skCategoryFixed')) return;
    var src=CATEGORY_IMAGES[label];
    if(!src) return;
    el.innerHTML='';
    el.classList.add('skCategoryFixed');
    el.style.cssText+=';position:relative!important;overflow:hidden!important;min-height:102px!important;height:auto!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;text-align:center!important;background:#fff!important;';
    var photo=document.createElement('span');
    photo.className='skCategoryFixedPhoto';
    photo.style.cssText='display:block!important;width:100%!important;height:70px!important;min-height:70px!important;overflow:hidden!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important;flex:0 0 70px!important;';
    var img=document.createElement('img');
    img.src=src;img.alt=label+' category';img.loading='eager';img.decoding='sync';
    img.style.cssText='display:block!important;width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important;';
    img.onerror=function(){this.style.display='none';photo.style.background='#f4e4c5';};
    photo.appendChild(img);
    var text=document.createElement('span');
    text.className='skCategoryFixedLabel';
    text.textContent=label;
    text.style.cssText='display:block!important;padding:6px 3px 8px!important;text-align:center!important;line-height:1.15!important;font-weight:900!important;font-size:11px!important;color:inherit!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;';
    el.appendChild(photo);el.appendChild(text);
  }
  function clean(){
    var seen={};
    document.querySelectorAll('.cats .cat').forEach(function(el){
      var raw=norm(el.textContent), label=categoryLabel(raw);
      if(label){
        if(seen[label]) el.remove();
        else {seen[label]=1;ensureCategoryPhoto(el,label);}
      }
    });
    document.querySelectorAll('.card').forEach(function(card){
      var t=card.querySelectorAll('.skProductTicker');
      for(var i=1;i<t.length;i++) t[i].remove();
      var av=card.querySelector('.availability');
      if(av){
        var s=norm(av.textContent);
        if(s.indexOf('Sold Out')>=0){av.textContent='● Sold Out';av.classList.add('soldout');}
        else if(s.indexOf('Available')>=0){av.textContent='● Available';av.classList.add('available');}
      }
    });
    document.querySelectorAll('.info').forEach(function(el){el.remove();});
    removeExactText('☎ Help Center');
    removeExactText('Order/help: 7891851475');
    removeExactText('📞 Call💬 WhatsApp');
    removeExactText('Order/help');
    restorePromoBanners();
  }
  function run(){try{clean()}catch(e){}}
  run();
  var timer=0;
  var obs=new MutationObserver(function(){clearTimeout(timer);timer=setTimeout(run,120);});
  obs.observe(document.body,{childList:true,subtree:true});
  [300,800,1500,3000,6000].forEach(function(ms){setTimeout(run,ms);});
})();
