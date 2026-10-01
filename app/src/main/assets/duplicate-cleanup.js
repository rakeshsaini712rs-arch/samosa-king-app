(function(){
  'use strict';
  if(window.__SK_DUPLICATE_CLEANUP__) return;
  window.__SK_DUPLICATE_CLEANUP__=true;
  function norm(s){return String(s||'').replace(/\s+/g,' ').trim();}
  function onceText(root,text){var target=norm(text),nodes=[];root.querySelectorAll('*').forEach(function(el){if(norm(el.textContent)===target)nodes.push(el);});for(var i=1;i<nodes.length;i++)nodes[i].remove();}
  function clean(){
    var seen={};
    document.querySelectorAll('.cats .cat').forEach(function(el){
      var raw=norm(el.textContent), known=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'], label='';
      for(var i=0;i<known.length;i++){if(raw.indexOf(known[i])>=0){label=known[i];break;}}
      if(label){if(seen[label])el.remove();else{seen[label]=1;el.textContent=label;}}
    });
    document.querySelectorAll('.card').forEach(function(card){
      var t=card.querySelectorAll('.skProductTicker');for(var i=1;i<t.length;i++)t[i].remove();
      var av=card.querySelector('.availability');if(av){var s=norm(av.textContent);if(s.indexOf('Sold Out')===0)av.textContent='● Sold Out';else if(s.indexOf('Available')===0)av.textContent='● Available';}
    });
    document.querySelectorAll('body *').forEach(function(el){
      var t=norm(el.textContent);
      if(t==='☎ Help Center'||t==='Order/help: 7891851475'||t==='📞 Call💬 WhatsApp'){
        var p=el;
        for(var n=0;n<5&&p.parentElement;n++){if(p.classList&&(p.classList.contains('help')||p.classList.contains('services')||p.classList.contains('info')))break;p=p.parentElement;}
        if(p&&p!==document.body)p.remove();else el.remove();
      }
    });
    onceText(document.body,'☎ Help Center');onceText(document.body,'Order/help: 7891851475');
  }
  clean();
  var timer=0,obs=new MutationObserver(function(){clearTimeout(timer);timer=setTimeout(clean,80);});
  obs.observe(document.body,{childList:true,subtree:true});
  setTimeout(clean,300);setTimeout(clean,1000);setTimeout(clean,2500);
})();
