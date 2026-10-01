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
    removeExactText('☎ Help Center');
    removeExactText('Order/help: 7891851475');
    removeExactText('📞 Call💬 WhatsApp');
    removeExactText('Order/help');
  }
  function run(){try{clean()}catch(e){}}
  run();
  var timer=0;
  var obs=new MutationObserver(function(){clearTimeout(timer);timer=setTimeout(run,120);});
  obs.observe(document.body,{childList:true,subtree:true});
  [300,800,1500,3000,6000].forEach(function(ms){setTimeout(run,ms);});
})();
