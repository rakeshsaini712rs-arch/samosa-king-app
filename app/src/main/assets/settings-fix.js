if(window.__skSettingsFixInstalled){/* already installed */}else{window.__skSettingsFixInstalled=true;
(function(){
function q(s){return document.querySelector(s)} function id(s){return document.getElementById(s)}
function show(s){var x=id(s);if(x){x.style.setProperty('display','block','important');x.style.setProperty('visibility','visible','important');x.style.setProperty('opacity','1','important');x.style.setProperty('pointer-events','auto','important');x.style.setProperty('z-index','999999','important')}}
function hide(s){var x=id(s);if(x){x.style.setProperty('display','none','important');x.style.setProperty('pointer-events','none','important')}}
function act(t){
 t=(t||'').toLowerCase();
 if(t.indexOf('payment')>=0){hide('settingsModal');show('paymentSettingsModal');return}
 if(t.indexOf('about')>=0){hide('settingsModal');show('aboutModal');return}
 if(t.indexOf('log out')>=0){hide('settingsModal');if(window.AndroidBridge&&AndroidBridge.logout)AndroidBridge.logout();else{localStorage.clear();alert('Logged out successfully.')}return}
 if(t.indexOf('profile')>=0&&typeof openProfile==='function'){hide('settingsModal');openProfile();return}
 if(t.indexOf('order')>=0&&typeof openHistoryFromSettings==='function'){hide('settingsModal');openHistoryFromSettings();return}
 if(t.indexOf('address')>=0&&typeof openAddressBook==='function'){hide('settingsModal');openAddressBook();return}
 if(t.indexOf('collection')>=0&&typeof openCollection==='function'){hide('settingsModal');openCollection();return}
 if(t.indexOf('feedback')>=0&&typeof openFeedback==='function'){hide('settingsModal');openFeedback();return}
}
function dedupeText(el){
 if(!el||el.children.length!==0)return;
 var raw=(el.textContent||'').replace(/\s+/g,' ').trim();
 if(!raw)return;
 var half=raw.length%2===0?raw.slice(0,raw.length/2):'';
 if(half&&half+half===raw)el.textContent=half;
}
function cleanRepeatedDelivery(card){
 var seq='20–30 min';
 var nodes=[].slice.call(card.querySelectorAll('*'));
 nodes.forEach(function(el){
   if(el===card)return;
   var t=(el.textContent||'').replace(/\s+/g,' ').trim();
   if(t.indexOf(seq)>=0&&t.indexOf('Near & Fast')>=0&&t.indexOf('Fresh & Hot')>=0&&t.indexOf('Fast Delivery')>=0){
     var half=t.length%2===0?t.slice(0,t.length/2):'';
     if(half&&half+half===t){
       el.textContent=half;
       el.style.fontSize='11px';
       el.style.color='#786a5d';
       el.style.lineHeight='1.45';
       el.style.margin='4px 0';
     }
   }
 });
}
function hideLeafText(text){
 var wanted=(text||'').replace(/\s+/g,' ').trim();
 document.querySelectorAll('body *').forEach(function(el){
   if(el.children.length===0 && (el.textContent||'').replace(/\s+/g,' ').trim()===wanted){
     el.style.setProperty('display','none','important');
     el.setAttribute('aria-hidden','true');
   }
 });
}
function removeObsoleteCustomerInfo(){
 /* These old footer/service/help rows were explicitly removed from the customer UI. Keep them hidden even if production.js recreates them. */
 [
  '📍 Nansa Gate, Nawalgarh • 🚚 Delivery ₹30 • ₹100 minimum • 💵 COD',
  '📍 Nansa Gate, Nawalgarh • 🚚 Delivery ₹30  • ₹100 minimum  • 💵 COD',
  'Delivery ₹30 up to 5 km',
  '₹30 up to 5 km',
  'Delivery ₹30',
  'Cash on Delivery',
  '8:30 AM–6:00 PM',
  '7891851475'
 ].forEach(hideLeafText);
 /* Hide the small service cards only when their heading is exactly Delivery/Payment/Open/Help. */
 ['Delivery','Payment','Open','Help'].forEach(function(label){
   document.querySelectorAll('body *').forEach(function(el){
     if(el.children.length===0 && (el.textContent||'').trim()===label){
       var p=el.parentElement;
       if(p && /Delivery|Payment|Open|Help/.test((p.textContent||'').trim()))p.style.setProperty('display','none','important');
     }
   });
 });
 /* Remove the obsolete Help Center block without affecting Order History or the cart. */
 document.querySelectorAll('body *').forEach(function(el){
   if(el.children.length===0 && (el.textContent||'').trim()==='☎ Help Center'){
     var p=el.parentElement;
     for(var i=0;i<3&&p;i++,p=p.parentElement){
       var tx=(p.textContent||'').replace(/\s+/g,' ').trim();
       if(tx.indexOf('Help Center')>=0 && tx.indexOf('Order/help:')>=0){p.style.setProperty('display','none','important');break;}
     }
   }
 });
 /* Remove the old marketing footer sentence as requested; keep the main ordering controls intact. */
 document.querySelectorAll('body *').forEach(function(el){
   if(el.children.length===0){
     var tx=(el.textContent||'').replace(/\s+/g,' ').trim();
     if(tx==='Minimum order ₹100 • Delivery ₹30 • Cash on Delivery' || tx==='Minimum order ₹100 • Delivery ₹30 • Cash on Delivery')el.style.setProperty('display','none','important');
   }
 });
}
function clean(){
 /* Keep the first visible hamburger/profile menu button and hide later duplicate buttons. */
 var menus=[].slice.call(document.querySelectorAll('button')).filter(function(b){return (b.textContent||'').trim()==='☰' && getComputedStyle(b).display!=='none';});
 menus.slice(1).forEach(function(b){b.style.setProperty('display','none','important');b.setAttribute('aria-hidden','true');});
 document.querySelectorAll('.cat').forEach(dedupeText);
 /* Remove obsolete 5 km wording everywhere in visible leaf text. */
 document.querySelectorAll('body *').forEach(function(el){
   if(el.children.length===0 && el.textContent){
     var t=el.textContent;
     var n=t.replace(/Delivery\s*₹30\s*up to 5 km/gi,'Delivery ₹30').replace(/₹30\s*up to 5 km/gi,'₹30');
     if(n!==t)el.textContent=n;
   }
 });
 /* Remove the old OTP/login block from the customer home screen. */
 document.querySelectorAll('body *').forEach(function(el){
   if(el.children.length===0 && (el.textContent||'').trim()==='Send OTP'){
     var p=el.closest('.login')||el.parentElement;
     if(p)p.style.setProperty('display','none','important');
   }
 });
 document.querySelectorAll('.card').forEach(function(card){
   cleanRepeatedDelivery(card);
   var strips=[];
   card.querySelectorAll('*').forEach(function(el){
     if(el.children.length===0)return;
     var t=(el.textContent||'').replace(/\s+/g,' ');
     if(t.indexOf('20–30 min')>=0 && t.indexOf('Near & Fast')>=0 && t.indexOf('Fresh & Hot')>=0 && t.indexOf('Fast Delivery')>=0)strips.push(el);
   });
   strips.forEach(function(el,i){if(i>0)el.style.setProperty('display','none','important');});
 });
 document.querySelectorAll('.card,.cats,.services,.info,.help,.cartbar').forEach(function(root){root.querySelectorAll('*').forEach(dedupeText);});
 var names=['Dahi Bhalla Plate 1','Dahi Bhalla Plate 2','Chole Bhature'];
 names.forEach(function(name){
   var hits=[].slice.call(document.querySelectorAll('body *')).filter(function(el){return el.children.length===0 && (el.textContent||'').trim()===name;});
   var cardHit=hits.find(function(el){return el.closest('.card');});
   hits.forEach(function(el){if(el!==cardHit && !el.closest('.card'))el.style.setProperty('display','none','important');});
 });
 removeObsoleteCustomerInfo();
}
function install(){
 document.querySelectorAll('.settingsMainBtn').forEach(function(b){b.style.setProperty('position','relative','important');b.style.setProperty('z-index','1000001','important');b.style.setProperty('pointer-events','auto','important')});
 document.querySelectorAll('.settingsPanel,.settingsList,.settingsList button,.payOptions,.payOptions button').forEach(function(b){b.style.setProperty('pointer-events','auto','important')});
 document.addEventListener('click',function(e){
  var t=e.target;
  var main=t.closest&&t.closest('.settingsMainBtn'); if(main){e.preventDefault();e.stopImmediatePropagation();show('settingsModal');return}
  var b=t.closest&&t.closest('#settingsModal .settingsList button');if(b){e.preventDefault();e.stopImmediatePropagation();act(b.textContent);return}
  var p=t.closest&&t.closest('#paymentSettingsModal .payOptions button');if(p){e.preventDefault();e.stopImmediatePropagation();var z=(p.textContent||'').toLowerCase();var bridge=window.AndroidBridge;if(z.indexOf('phonepe')>=0&&bridge&&typeof bridge.openUpi==='function')bridge.openUpi('phonepe');else if(z.indexOf('cred')>=0&&bridge&&typeof bridge.openUpi==='function')bridge.openUpi('cred');else if(z.indexOf('whatsapp')>=0&&bridge&&typeof bridge.openUpi==='function')bridge.openUpi('whatsapp');else if(z.indexOf('qr')>=0&&typeof showPaymentQr==='function')showPaymentQr();else if(z.indexOf('cash')>=0){localStorage.setItem('skPaymentMethod','COD');alert('Cash on Delivery selected.')}return}
  var c=t.closest&&t.closest('.modal .close');if(c){e.preventDefault();e.stopImmediatePropagation();var mm=c.closest('.modal');if(mm)hide(mm.id)}
 },true);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
}
(function(){
  function installPromoFix(){
    var v=document.getElementById('promoVideoEl'),s=document.getElementById('promoSource'),t=document.getElementById('promoText');
    if(!v||!s||!t||window.__skPromoFixInstalled)return;
    window.__skPromoFixInstalled=true;
    var slides=[{url:'https://videos.pexels.com/video-files/6603837/6603837-hd_1920_1080_25fps.mp4',tag:'🔥 FRESH & HOT',title:'Pizza Made Fresh',sub:'Chef-made pizza at Samosa King'},{url:'https://videos.pexels.com/video-files/6603839/6603839-hd_1920_1080_25fps.mp4',tag:'👨‍🍳 MADE FRESH',title:'Pizza Special',sub:'Hot • Fresh • Delicious'},{url:'https://videos.pexels.com/video-files/6603825/6603825-hd_1920_1080_25fps.mp4',tag:'👑 SAMOSA KING',title:'Fresh Food',sub:'Order your favourite food now'}];
    var i=0,loading=false,retries=0;function setText(x){t.innerHTML='<span>'+x.tag+'</span><b>'+x.title+'</b><small>'+x.sub+'</small>'}function play(){var p=v.play();if(p&&p.catch)p.catch(function(){})}function show(n){if(loading)return;loading=true;var x=slides[n%slides.length];i=n%slides.length;setText(x);s.src=x.url;v.load();retries=0;setTimeout(function(){loading=false;play()},80)}function next(){show((i+1)%slides.length)}v.addEventListener('ended',next);v.addEventListener('error',function(){if(retries<1){retries++;setTimeout(function(){v.load();play()},1000)}else{retries=0;next()}});document.addEventListener('visibilitychange',function(){if(!document.hidden)play()});setInterval(function(){if(!document.hidden&&!v.ended&&v.readyState>=2&&v.paused)play()},5000);show(0);
  }if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',installPromoFix);else installPromoFix();
})();
(function(){
  if(window.__skCustomerUiCleanup)return; window.__skCustomerUiCleanup=true;
  function clean(){var menus=[].slice.call(document.querySelectorAll('button')).filter(function(b){return (b.textContent||'').trim()==='☰'&&getComputedStyle(b).display!=='none';});menus.slice(1).forEach(function(b){b.style.setProperty('display','none','important');b.setAttribute('aria-hidden','true');});document.querySelectorAll('body *').forEach(function(el){if(el.children.length===0&&el.textContent){var t=el.textContent,n=t.replace(/Delivery\s*₹30\s*up to 5 km/gi,'Delivery ₹30').replace(/₹30\s*up to 5 km/gi,'₹30');if(n!==t)el.textContent=n;}});document.querySelectorAll('body *').forEach(function(el){if(el.children.length===0&&(el.textContent||'').trim()==='Send OTP'){var p=el.closest('.login')||el.parentElement;if(p)p.style.setProperty('display','none','important');}});document.querySelectorAll('.card').forEach(function(card){var strips=[];card.querySelectorAll('*').forEach(function(el){if(el.children.length===0)return;var t=(el.textContent||'').replace(/\s+/g,' ');if(t.indexOf('20–30 min')>=0&&t.indexOf('Near & Fast')>=0&&t.indexOf('Fresh & Hot')>=0&&t.indexOf('Fast Delivery')>=0)strips.push(el);});strips.forEach(function(el,i){if(i>0)el.style.setProperty('display','none','important');});});document.querySelectorAll('.cat').forEach(dedupeText);removeObsoleteCustomerInfo();}
  function dedupeText(el){if(!el||el.children.length!==0)return;var raw=(el.textContent||'').replace(/\s+/g,' ').trim();if(!raw||raw.length%2!==0)return;var half=raw.slice(0,raw.length/2);if(half&&half+half===raw)el.textContent=half;}
  function run(){clean();setTimeout(clean,500);setTimeout(clean,1500);setTimeout(clean,3000);setTimeout(clean,6000)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(function(){if(!window.__skCustomerUiCleanupRunning){window.__skCustomerUiCleanupRunning=true;setTimeout(function(){window.__skCustomerUiCleanupRunning=false;clean()},150)}}).observe(document.documentElement,{childList:true,subtree:true});
})();