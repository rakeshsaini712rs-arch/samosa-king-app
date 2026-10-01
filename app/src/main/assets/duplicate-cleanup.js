(function(){
  'use strict';
  if(window.__SK_DUPLICATE_CLEANUP__) return;
  window.__SK_DUPLICATE_CLEANUP__=true;
  function norm(s){return String(s||'').replace(/\s+/g,' ').trim();}
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
  function removePhoneNumberBox(){
    document.querySelectorAll('input,textarea').forEach(function(el){
      var value=norm(el.value||el.getAttribute('value')||'').replace(/[\s()-]/g,'');
      var id=norm(el.id).toLowerCase();
      var name=norm(el.getAttribute('name')).toLowerCase();
      var ph=norm(el.getAttribute('placeholder')).toLowerCase();
      var looksLikePhone=/^\+?91\d{10}$/.test(value)||/^\d{10}$/.test(value);
      var phoneField=/(phone|mobile|contact|whatsapp|number)/.test(id+' '+name+' '+ph);
      if(looksLikePhone || (phoneField && (el.type==='tel'||el.type==='text'))){
        var box=el;
        for(var n=0;n<5 && box.parentElement;n++){
          if(box.parentElement.children.length===1) box=box.parentElement;
          else break;
        }
        box.remove();
      }
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
  function clean(){
    var seen={};
    document.querySelectorAll('.cats .cat').forEach(function(el){
      var raw=norm(el.textContent), known=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'], label='';
      for(var i=0;i<known.length;i++){if(raw.indexOf(known[i])>=0){label=known[i];break;}}
      if(label){if(seen[label]) el.remove(); else {seen[label]=1;el.textContent=label;}}
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
    removePhoneNumberBox();
    restorePromoBanners();
  }
  function run(){try{clean()}catch(e){}}
  run();
  var timer=0;
  var obs=new MutationObserver(function(){clearTimeout(timer);timer=setTimeout(run,120);});
  obs.observe(document.body,{childList:true,subtree:true});
  [300,800,1500,3000,6000].forEach(function(ms){setTimeout(run,ms);});
})();
