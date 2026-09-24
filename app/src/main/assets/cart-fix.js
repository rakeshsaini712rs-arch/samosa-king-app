(function(){'use strict';
function install(){
 if(window.__SK_CART_FIX)return;
 window.__SK_CART_FIX=true;
 function change(id,delta){
  try{
   if(typeof keepProductCategory==='function')keepProductCategory(id);
   var next=(Number(cart[id])||0)+Number(delta||0);
   if(next<=0) delete cart[id]; else cart[id]=next;
   if(typeof saveCart==='function')saveCart();
   if(typeof render==='function')render();
   if(typeof renderCart==='function')renderCart();
   if(typeof updateCart==='function')updateCart();
  }catch(e){console.error('Cart quantity error',e);}
 }
 window.changeQty=change;
 document.addEventListener('click',function(e){
  var b=e.target&&e.target.closest?e.target.closest('.qty button,.cartcontrols button'):null;
  if(!b)return;
  var onclick=b.getAttribute('onclick')||'';
  var m=onclick.match(/changeQty\(['"]([^'"]+)['"],\s*([-+]?\d+)\)/);
  if(!m)return;
  e.preventDefault();
  e.stopPropagation();
  e.stopImmediatePropagation();
  change(m[1],Number(m[2]));
 },true);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();