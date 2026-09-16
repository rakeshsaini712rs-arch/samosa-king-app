(function(){'use strict';
const SHOP_LAT=27.8514056, SHOP_LON=75.2711528;
window.SKNavigateToShop=function(){
  try{
    const u='google.navigation:q='+SHOP_LAT+','+SHOP_LON;
    if(window.AndroidBridge&&typeof AndroidBridge.openShopNavigation==='function'){AndroidBridge.openShopNavigation();return;}
    window.location.href='https://www.google.com/maps/dir/?api=1&destination='+SHOP_LAT+','+SHOP_LON;
  }catch(e){alert('Navigation could not be opened. Please try again.');}
};
function install(){
  document.querySelectorAll('button,a').forEach(function(b){
    const t=(b.textContent||'').trim().toLowerCase();
    if(t.includes('navigate to shop')||t.includes('navigation to shop')){
      b.removeAttribute('onclick');
      b.onclick=function(e){e.preventDefault();e.stopPropagation();window.SKNavigateToShop();};
      b.style.touchAction='manipulation';
    }
  });
}
install();
new MutationObserver(install).observe(document.documentElement,{childList:true,subtree:true});
})();
