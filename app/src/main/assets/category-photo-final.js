/* CATEGORY PHOTO FINAL - GUARANTEED CATEGORY BAR */
(function(){
  if(window.__SK_CATEGORY_PHOTO_GUARANTEED__) return;
  window.__SK_CATEGORY_PHOTO_GUARANTEED__=true;

  var BASE='file:///android_asset/product-images/';
  var DATA=[
    ['all','samosa.jpg','All'],
    ['fast','pizza.jpg','Fast Food'],
    ['snacks','mirchi-bada.jpg','Snacks'],
    ['chaat','dahi-bhalla-1.jpg','Chaat & Special'],
    ['thali','manchurian.jpg','Indian Thali'],
    ['desi','pasta.jpg','Desi Rasoi'],
    ['birthday','gulab-jamun.jpg','Birthday Special'],
    ['beverages','burger.jpg','Beverages'],
    ['sweets','kaju-katli.jpg','Sweets'],
    ['restaurant','wraps.jpg','Restaurant / Hotel']
  ];

  function css(){
    if(document.getElementById('sk-category-guaranteed-css')) return;
    var s=document.createElement('style');
    s.id='sk-category-guaranteed-css';
    s.textContent=''+
      '#cats{display:flex!important;visibility:visible!important;opacity:1!important;overflow-x:auto!important;overflow-y:hidden!important;gap:10px!important;padding:10px 12px!important;background:#fff!important;border-bottom:1px solid #eadfce!important;min-height:116px!important;scrollbar-width:none!important;position:relative!important;z-index:9!important}'+
      '#cats::-webkit-scrollbar{display:none!important}'+
      '#cats .cat{display:flex!important;visibility:visible!important;opacity:1!important;flex:0 0 96px!important;width:96px!important;min-width:96px!important;height:100px!important;min-height:100px!important;margin:0!important;padding:6px!important;box-sizing:border-box!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;gap:5px!important;overflow:hidden!important;border:1px solid #e5d7c5!important;border-radius:15px!important;background:#fffaf1!important;color:#241a12!important;cursor:pointer!important}'+
      '#cats .cat.active{background:#f5b91f!important;color:#17110a!important;border-color:#d99d18!important}'+
      '#cats .skGuaranteedPhoto{display:block!important;visibility:visible!important;opacity:1!important;width:68px!important;height:68px!important;min-width:68px!important;min-height:68px!important;flex:0 0 68px!important;border-radius:50%!important;overflow:hidden!important;background:#eee!important;border:2px solid #f5b91f!important;box-sizing:border-box!important}'+
      '#cats .skGuaranteedPhoto img{display:block!important;visibility:visible!important;opacity:1!important;width:100%!important;height:100%!important;object-fit:cover!important;border-radius:50%!important}'+
      '#cats .skGuaranteedLabel{display:block!important;visibility:visible!important;opacity:1!important;width:100%!important;height:14px!important;line-height:14px!important;text-align:center!important;font-size:10px!important;font-weight:900!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}';
    (document.head||document.documentElement).appendChild(s);
  }

  function makeCard(item){
    var c=document.createElement('button');
    c.type='button';
    c.className='cat';
    c.setAttribute('data-sk-category',item[0]);
    c.setAttribute('aria-label',item[2]);
    var holder=document.createElement('span');
    holder.className='skGuaranteedPhoto';
    var img=document.createElement('img');
    img.src=BASE+item[1];
    img.alt=item[2];
    img.loading='eager';
    img.decoding='async';
    img.onerror=function(){
      if(img.getAttribute('data-fallback')==='1') return;
      img.setAttribute('data-fallback','1');
      img.src=BASE+'samosa.jpg';
    };
    holder.appendChild(img);
    var label=document.createElement('span');
    label.className='skGuaranteedLabel';
    label.textContent=item[2];
    c.appendChild(holder);
    c.appendChild(label);
    return c;
  }

  function ensure(){
    var root=document.getElementById('cats');
    if(!root) return;
    css();
    var cards=root.querySelectorAll('.cat');
    if(cards.length!==DATA.length){
      root.innerHTML='';
      DATA.forEach(function(item){root.appendChild(makeCard(item));});
    }else{
      cards.forEach(function(c,i){
        c.style.display='flex';
        c.style.visibility='visible';
        c.style.opacity='1';
        if(!c.querySelector('.skGuaranteedPhoto')){
          var fresh=makeCard(DATA[i]);
          c.innerHTML=fresh.innerHTML;
        }
        c.setAttribute('data-sk-category',DATA[i][0]);
      });
    }
    if(!root.querySelector('.cat.active')) root.querySelector('.cat').classList.add('active');
  }

  function scrollToCategory(key,label){
    if(key==='all'){
      window.scrollTo({top:0,behavior:'smooth'});
      return;
    }
    var sections=document.querySelectorAll('.section');
    var wanted=label.toLowerCase();
    var target=null;
    sections.forEach(function(sec){
      var h=sec.querySelector('h2');
      var t=(h?h.textContent:sec.textContent||'').toLowerCase();
      if(!target && (t.indexOf(wanted)>=0 || (key==='desi'&&t.indexOf('desi')>=0) || (key==='birthday'&&t.indexOf('birthday')>=0) || (key==='restaurant'&&(t.indexOf('restaurant')>=0||t.indexOf('hotel')>=0))) ) target=sec;
    });
    if(target) target.scrollIntoView({behavior:'smooth',block:'start'});
  }

  function bind(){
    var root=document.getElementById('cats');
    if(!root || root.__skBound) return;
    root.__skBound=true;
    root.addEventListener('click',function(e){
      var c=e.target.closest('.cat');
      if(!c) return;
      root.querySelectorAll('.cat').forEach(function(x){x.classList.remove('active');});
      c.classList.add('active');
      var key=c.getAttribute('data-sk-category')||'all';
      var item=DATA.find(function(x){return x[0]===key;})||DATA[0];
      scrollToCategory(key,item[2]);
    });
  }

  function run(){ensure();bind();}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  [100,300,700,1200,2000,3500,5000].forEach(function(t){setTimeout(run,t);});
  var timer=null;
  new MutationObserver(function(){
    clearTimeout(timer);
    timer=setTimeout(run,120);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
