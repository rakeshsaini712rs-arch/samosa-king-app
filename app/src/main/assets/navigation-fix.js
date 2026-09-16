(function(){'use strict';
const SHOP_LAT=27.8514056,SHOP_LON=75.2711528;
function openMaps(){
  var web='https://www.google.com/maps/dir/?api=1&destination='+SHOP_LAT+','+SHOP_LON+'&travelmode=driving';
  var intent='intent://maps.google.com/maps?daddr='+SHOP_LAT+','+SHOP_LON+'&directionsmode=driving#Intent;scheme=https;package=com.google.android.apps.maps;end';
  try{
    if(window.AndroidBridge&&typeof AndroidBridge.openShopNavigation==='function'){AndroidBridge.openShopNavigation();return;}
  }catch(e){}
  try{window.location.href=intent;}catch(e){}
  setTimeout(function(){try{window.location.href=web;}catch(e){window.open(web,'_blank');}},900);
}
window.SKNavigateToShop=openMaps;
function install(){document.querySelectorAll('button,a,[role="button"]').forEach(function(b){var t=(b.textContent||'').trim().toLowerCase();if(t.includes('navigate to shop')||t.includes('navigation to shop')){b.removeAttribute('onclick');b.onclick=function(e){if(e){e.preventDefault();e.stopImmediatePropagation();}openMaps();return false;};b.style.touchAction='manipulation';b.style.pointerEvents='auto';}})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
new MutationObserver(install).observe(document.documentElement,{childList:true,subtree:true});
})();
