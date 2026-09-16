(function(){'use strict';
const SHOP_LAT=27.8514056, SHOP_LON=75.2711528;
window.SKNavigateToShop=function(){
  try{
    if(window.AndroidBridge&&typeof AndroidBridge.openShopNavigation==='function'){AndroidBridge.openShopNavigation();return;}
    var intent='google.navigation:q='+SHOP_LAT+','+SHOP_LON;
    window.location.href=intent;
    setTimeout(function(){window.location.href='https://www.google.com/maps/dir/?api=1&destination='+SHOP_LAT+','+SHOP_LON+'&travelmode=driving';},700);
  }catch(e){window.location.href='https://www.google.com/maps/dir/?api=1&destination='+SHOP_LAT+','+SHOP_LON+'&travelmode=driving'}
};
function install(){document.querySelectorAll('button,a').forEach(function(b){var t=(b.textContent||'').trim().toLowerCase();if(t.includes('navigate to shop')||t.includes('navigation to shop')){b.removeAttribute('onclick');b.onclick=function(e){e.preventDefault();e.stopImmediatePropagation();window.SKNavigateToShop();return false};b.style.touchAction='manipulation';}})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
new MutationObserver(install).observe(document.documentElement,{childList:true,subtree:true});
})();
