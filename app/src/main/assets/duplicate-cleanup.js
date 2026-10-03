(function(){
  'use strict';
  if(window.__SK_DUPLICATE_CLEANUP__) return;
  window.__SK_DUPLICATE_CLEANUP__=true;
  var CATEGORY_IMAGES={
    'All':'samosa.jpg','Fast Food':'pizza.jpg','Snacks':'mirchi-bada.jpg','Chaat & Special':'dahi-bhalla-1.jpg','Indian Thali':'manchurian.jpg','Desi Rasoi':'pasta.jpg','Birthday Special':'gulab-jamun.jpg','Beverages':'burger.jpg','Sweets':'kaju-katli.jpg','Restaurant / Hotel':'wraps.jpg'
  };
  var CATEGORY_KEYS=Object.keys(CATEGORY_IMAGES);
  var BASE='file:///android_asset/product-images/';
  function norm(s){return String(s||'').replace(/\s+/g,' ').trim();}
  function categoryLabel(raw){raw=norm(raw);for(var i=0;i<CATEGORY_KEYS.length;i++)if(raw.indexOf(CATEGORY_KEYS[i])>=0)return CATEGORY_KEYS[i];return '';}
  function ensureCategoryBar(){
    var root=document.getElementById('cats')||document.querySelector('.cats');
    if(!root){
      root=document.createElement('div');root.id='cats';root.className='cats skGuaranteedCategories';
      var anchor=document.querySelector('#homePage .section')||document.querySelector('.section')||document.querySelector('.hero')||document.body.firstElementChild;
      if(anchor&&anchor.parentElement)anchor.parentElement.insertBefore(root,anchor);else document.body.insertBefore(root,document.body.firstChild);
    }
    root.classList.add('skGuaranteedCategories');
    root.style.cssText='display:flex!important;visibility:visible!important;opacity:1!important;overflow-x:auto!important;gap:9px!important;padding:10px 12px!important;background:#fff!important;position:relative!important;z-index:100!important;scrollbar-width:none!important;';
    var existing={};root.querySelectorAll('.cat').forEach(function(x){var l=categoryLabel(x.textContent);if(l)existing[l]=x;});
    CATEGORY_KEYS.forEach(function(label){
      var c=existing[label];
      if(!c){c=document.createElement('button');c.type='button';c.className='cat';c.setAttribute('data-label',label);root.appendChild(c);}
      c.style.cssText='position:relative!important;display:flex!important;flex:0 0 94px!important;width:94px!important;min-width:94px!important;height:98px!important;min-height:98px!important;padding:7px 5px 6px!important;margin:0!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;gap:5px!important;overflow:hidden!important;border:1px solid #eadfce!important;border-radius:15px!important;background:#fff!important;color:#21170f!important;font-weight:900!important;';
      var holder=c.querySelector('.skCategoryFixedPhoto');
      if(!holder){c.innerHTML='';holder=document.createElement('span');holder.className='skCategoryFixedPhoto';holder.style.cssText='display:flex!important;width:68px!important;height:68px!important;min-width:68px!important;min-height:68px!important;flex:0 0 68px!important;border-radius:50%!important;overflow:hidden!important;background:#f4e4c5!important;border:2px solid #f6c94a!important;align-items:center!important;justify-content:center!important;';var img=document.createElement('img');img.alt=label;img.src=BASE+CATEGORY_IMAGES[label];img.loading='eager';img.decoding='sync';img.style.cssText='display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;border-radius:50%!important;visibility:visible!important;opacity:1!important;';img.onerror=function(){this.onerror=null;this.src=BASE+'samosa.jpg';};holder.appendChild(img);c.appendChild(holder);var text=document.createElement('span');text.className='skCategoryFixedLabel';text.textContent=label;text.style.cssText='display:block!important;width:100%!important;height:14px!important;line-height:14px!important;text-align:center!important;color:inherit!important;font-size:10px!important;font-weight:900!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;';c.appendChild(text);}
      c.onclick=function(){var wanted=label.toLowerCase();var sections=document.querySelectorAll('.section');for(var i=0;i<sections.length;i++){var h=sections[i].querySelector('h2');if(h&&h.textContent.toLowerCase().indexOf(wanted.replace(' & special',''))>=0){sections[i].scrollIntoView({behavior:'smooth',block:'start'});break;}}};
    });
  }
  function removeExactText(text){document.querySelectorAll('body *').forEach(function(el){if(el.children.length===0&&norm(el.textContent)===text){var p=el;for(var n=0;n<6&&p.parentElement;n++){if(p.classList&&(p.classList.contains('help')||p.classList.contains('services')||p.classList.contains('info'))){el=p;break;}p=p.parentElement;}if(el&&el!==document.body)el.remove();}});}
  function restorePromoBanners(){
    if(document.getElementById('skBannerCarousel'))return;
    var anchor=document.querySelector('.cats')||document.querySelector('.hero');if(!anchor||!anchor.parentElement)return;
    var imgs=window.SK_IMAGES||{};var data=function(k){return imgs[k]?'data:image/jpeg;base64,'+imgs[k]:''};
    var items=[{key:'pizza',title:'HOT & FRESH PIZZA',sub:'Freshly prepared • Order now'},{key:'burger',title:'JUICY BURGER',sub:'Hot • Fresh • Delicious'},{key:'samosa',title:'CRISPY SAMOSA',sub:'Hot • Fresh • Crispy'}];
    var wrap=document.createElement('section');wrap.id='skBannerCarousel';wrap.style.cssText='margin:10px 12px 8px;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px #0003;background:#160d08;display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;';
    items.forEach(function(item){var card=document.createElement('div');card.style.cssText='min-width:88%;height:180px;position:relative;overflow:hidden;border-radius:18px;scroll-snap-align:start;background:linear-gradient(135deg,#5b1b0c,#17100b);';var src=data(item.key);if(src){var img=document.createElement('img');img.src=src;img.alt=item.title;img.style.cssText='width:100%;height:100%;object-fit:cover;display:block;';card.appendChild(img);}var shade=document.createElement('div');shade.style.cssText='position:absolute;inset:0;background:linear-gradient(90deg,#000b,#0002 60%,transparent);';card.appendChild(shade);var text=document.createElement('div');text.style.cssText='position:absolute;left:16px;top:50%;transform:translateY(-50%);color:#fff;max-width:72%;text-shadow:0 2px 8px #000;';text.innerHTML='<span style="display:block;font-size:11px;font-weight:900;letter-spacing:1px;color:#f6c94a">SAMOSA KING • NAWALGARH</span><b style="display:block;font-size:25px;line-height:1.05;margin:5px 0">'+item.title+'</b><small style="font-size:11px;font-weight:700">'+item.sub+'</small>';card.appendChild(text);wrap.appendChild(card);});anchor.parentElement.insertBefore(wrap,anchor);
  }
  function ensureCategoryPhoto(el,label){if(el.querySelector('.skCategoryFixed'))return;var src=BASE+CATEGORY_IMAGES[label];if(!src)return;el.innerHTML='';el.classList.add('skCategoryFixed');el.style.cssText+=';position:relative!important;overflow:hidden!important;min-height:102px!important;height:auto!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;text-align:center!important;background:#fff!important;';var photo=document.createElement('span');photo.className='skCategoryFixedPhoto';photo.style.cssText='display:block!important;width:100%!important;height:70px!important;min-height:70px!important;overflow:hidden!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important;flex:0 0 70px!important;';var img=document.createElement('img');img.src=src;img.alt=label+' category';img.loading='eager';img.decoding='sync';img.style.cssText='display:block!important;width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important;';img.onerror=function(){this.src=BASE+'samosa.jpg';};photo.appendChild(img);var text=document.createElement('span');text.className='skCategoryFixedLabel';text.textContent=label;text.style.cssText='display:block!important;padding:6px 3px 8px!important;text-align:center!important;line-height:1.15!important;font-weight:900!important;font-size:11px!important;color:inherit!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;';el.appendChild(photo);el.appendChild(text);}
  function clean(){
    ensureCategoryBar();
    var seen={};document.querySelectorAll('.cats .cat').forEach(function(el){var raw=norm(el.textContent),label=categoryLabel(raw);if(label){if(seen[label])el.remove();else{seen[label]=1;ensureCategoryPhoto(el,label);}}});
    document.querySelectorAll('.card').forEach(function(card){var t=card.querySelectorAll('.skProductTicker');for(var i=1;i<t.length;i++)t[i].remove();var av=card.querySelector('.availability');if(av){var s=norm(av.textContent);if(s.indexOf('Sold Out')>=0){av.textContent='● Sold Out';av.classList.add('soldout');}else if(s.indexOf('Available')>=0){av.textContent='● Available';av.classList.add('available');}}});
    document.querySelectorAll('.info').forEach(function(el){if(!el.closest('.cats'))el.remove();});
    removeExactText('☎ Help Center');removeExactText('Order/help: 7891851475');removeExactText('📞 Call💬 WhatsApp');removeExactText('Order/help');restorePromoBanners();
  }
  function run(){try{clean()}catch(e){}}
  run();var timer=0;var obs=new MutationObserver(function(){clearTimeout(timer);timer=setTimeout(run,120);});obs.observe(document.documentElement,{childList:true,subtree:true});[300,800,1500,3000,6000].forEach(function(ms){setTimeout(run,ms);});
})();
