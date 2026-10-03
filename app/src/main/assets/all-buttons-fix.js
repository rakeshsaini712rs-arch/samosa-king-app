(function(){'use strict';
function ready(){
 var B=window.AndroidBridge;
 function msg(t){var m=document.getElementById('msg');if(m)m.textContent=t;else alert(t)}
 window.callShop=function(){location.href='tel:7891851475'};
 window.waShop=function(){location.href='https://wa.me/917891851475'};
 window.authError=function(){var x=document.getElementById('loginMsg');if(x)x.textContent='Firebase account could not be created. Please try again.'};
 window.orderStarted=function(){msg('Checking delivery area and placing COD order…')};
 window.locationRequired=function(){msg('Please allow location permission to continue your order.')};
 window.locationResult=function(km){msg('Delivery distance: '+km+' km. Checking order…')};
 window.orderError=function(e){msg(String(e||'Order could not be placed. Please try again.'))};
 if(typeof window.orderCreated!=='function')window.orderCreated=function(id){try{cart={};localStorage.removeItem('samosaKingCart');if(typeof saveCart==='function')saveCart();if(typeof render==='function')render();if(typeof renderCart==='function')renderCart();if(typeof updateCart==='function')updateCart()}catch(e){}msg('Order placed successfully. Order ID: '+String(id||'').slice(0,8));if(typeof closeCart==='function')closeCart();if(B&&B.loadLastOrder)B.loadLastOrder()};
 window.profileResult=function(raw){try{var d=JSON.parse(raw);alert('Profile\nName: '+(d.name||'Not set')+'\nMobile: '+(d.mobile||'Not set'))}catch(e){alert('Profile could not be loaded.')}};
 window.profileSaved=function(){alert('Profile saved to your Firebase account.')};
 window.addressesResult=function(raw){try{var a=JSON.parse(raw||'[]');alert(a.length?'Saved addresses\n\n'+a.map(function(x){return(x.label||'Address')+': '+x.address}).join('\n\n'):'No saved addresses yet.')}catch(e){alert('Could not load addresses.')}};
 window.reviewSaved=function(){alert('Thank you. Your review was saved.')};window.reviewError=function(e){alert(String(e||'Review could not be submitted.'))};
 if(B){window.skOpenProfile=function(){if(B.getProfile)B.getProfile()};window.skSaveProfile=function(){var n=prompt('Name');if(n===null)return;var p=prompt('Mobile number','7891851475');if(p===null)return;if(B.saveProfile)B.saveProfile(n,p)};window.skAddressBook=function(){if(B.getAddresses)B.getAddresses()};window.skSaveAddress=function(){var a=prompt('Full delivery address');if(a&&B.saveAddress)B.saveAddress('Saved',a)}}
 var names=['All','Fast Food','Snacks','Chaat & Special','Indian Thali','Desi Rasoi','Birthday Special','Beverages','Sweets','Restaurant / Hotel'];
 function norm(s){return String(s||'').toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ')}
 function cleanLabel(s){var n=norm(s);for(var i=0;i<names.length;i++)if(n===norm(names[i])||n.indexOf(norm(names[i])+' category')===0||n.indexOf(norm(names[i])+' category '+norm(names[i]))===0)return names[i];return String(s||'').replace(/\s+category\s*/ig,' ').replace(/\s+/g,' ').trim()}
 function targetFor(label){var n=norm(label);if(n==='all')return null;var sections=[].slice.call(document.querySelectorAll('.section'));for(var i=0;i<sections.length;i++){var h=sections[i].querySelector('h2');if(h&&norm(h.textContent)===n)return sections[i]}return null}
 function bindCategories(){
  var cats=document.querySelectorAll('.cat');if(!cats.length)return;
  var css=document.getElementById('sk-category-final-style');
  if(!css){css=document.createElement('style');css.id='sk-category-final-style';css.textContent='.cats{position:relative!important;z-index:20!important;background:#111!important;color:#fff!important;display:flex!important;gap:8px!important;overflow-x:auto!important;padding:8px 10px!important;border-radius:12px!important;scrollbar-width:none!important}.cats::-webkit-scrollbar{display:none}.cats .cat{flex:0 0 auto!important;background:#1b1b1b!important;color:#fff!important;border:1px solid #3a3a3a!important;border-radius:10px!important;min-height:40px!important;padding:8px 12px!important;font-weight:800!important;white-space:nowrap!important}.cats .cat.active{background:#f6c94a!important;color:#111!important;border-color:#f6c94a!important}';document.head.appendChild(css)}
  cats.forEach(function(cat,index){
   var label=cleanLabel(cat.getAttribute('data-sk-cat-label')||cat.textContent);
   if(!label&&names[index])label=names[index];
   if(names.indexOf(label)<0&&names[index])label=names[index];
   cat.setAttribute('data-sk-cat-label',label);cat.setAttribute('aria-label',label);cat.title=label;
   if(cat.dataset.skFinalBound==='1')return;
   cat.textContent=label;
   cat.dataset.skFinalBound='1';
   cat.addEventListener('click',function(ev){
    ev.preventDefault();ev.stopPropagation();
    cats.forEach(function(c){c.classList.remove('active')});cat.classList.add('active');
    if(label==='All'){window.scrollTo({top:0,behavior:'smooth'});return}
    var sec=targetFor(label);
    if(sec)sec.scrollIntoView({behavior:'smooth',block:'start'});
   },true);
  });
  if(cats[1])cats[1].classList.add('active');
 }
 bindCategories();setTimeout(bindCategories,400);setTimeout(bindCategories,1200);
 function fixCategoryPhotos(){try{bindCategories();}catch(e){}}
 fixCategoryPhotos();
 var oldCancel=window.cancelOrder;window.cancelOrder=function(){if(typeof oldCancel==='function')oldCancel();else if(B&&B.cancelLastOrder)B.cancelLastOrder()};
 document.querySelectorAll('button').forEach(function(b){b.style.touchAction='manipulation'});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(ready,300)});else setTimeout(ready,100);setTimeout(ready,1200);
})();