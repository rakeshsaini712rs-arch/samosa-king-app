/* CATEGORY PHOTO FINAL - GUARANTEED CATEGORY BAR V5 */
(function(){
  if(window.__SK_CATEGORY_PHOTO_GUARANTEED_V5__) return;
  window.__SK_CATEGORY_PHOTO_GUARANTEED_V5__=true;

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
    var old=document.getElementById('sk-category-guaranteed-css');
    if(old) old.remove();
    var s=document.createElement('style');
    s.id='sk-category-guaranteed-css';
    s.textContent=
      '#cats{display:flex!important;visibility:visible!important;opacity:1!important;overflow-x:auto!important;overflow-y:hidden!important;gap:10px!important;padding:10px 12px!important;background:#fff!important;border-bottom:1px solid #eadfce!important;min-height:116px!important;scrollbar-width:none!important;position:relative!important;z-index:100!important}'+
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
    img.decoding='sync';
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
    var current=root.querySelectorAll('.cat');
    var needsRebuild=current.length!==DATA.length;
    if(!needsRebuild){
      current.forEach(function(c,i){
        var img=c.querySelector('.skGuaranteedPhoto img');
        var expected=BASE+DATA[i][1];
        if(!img || img.getAttribute('src')!==expected || !c.querySelector('.skGuaranteedLabel')) needsRebuild=true;
      });
    }
    if(needsRebuild){
      var frag=document.createDocumentFragment();
      DATA.forEach(function(item){frag.appendChild(makeCard(item));});
      root.innerHTML='';
      root.appendChild(frag);
    }else{
      current.forEach(function(c,i){
        c.style.setProperty('display','flex','important');
        c.style.setProperty('visibility','visible','important');
        c.style.setProperty('opacity','1','important');
        var img=c.querySelector('.skGuaranteedPhoto img');
        if(img){
          img.src=BASE+DATA[i][1];
          img.style.setProperty('display','block','important');
          img.style.setProperty('visibility','visible','important');
          img.style.setProperty('opacity','1','important');
        }
        c.setAttribute('data-sk-category',DATA[i][0]);
      });
    }
    if(!root.querySelector('.cat.active')){
      var first=root.querySelector('.cat');
      if(first) first.classList.add('active');
    }
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
    if(!root || root.__skBoundV5) return;
    root.__skBoundV5=true;
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
  [50,150,300,700,1200,2000,3500,5000].forEach(function(t){setTimeout(run,t);});
  var timer=null;
  new MutationObserver(function(){
    clearTimeout(timer);
    timer=setTimeout(run,100);
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
