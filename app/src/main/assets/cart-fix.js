(function(){
'use strict';
function install(){
  if(window.__SK_CART_FIX)return;
  window.__SK_CART_FIX=true;
  function change(id,delta){
    try{
      if(typeof keepProductCategory==='function')keepProductCategory(id);
      var old=Number(cart[id])||0;
      var next=old+Number(delta||0);
      if(next>0)cart[id]=next;else delete cart[id];
      if(typeof saveCart==='function')saveCart();
      if(typeof render==='function')render();
      if(typeof updateCart==='function')updateCart();
      if(typeof renderCart==='function')renderCart();
    }catch(e){console.error('Cart quantity error',e);}
  }
  window.changeQty=function(id,delta){change(id,delta)};
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.qty button');
    if(!b)return;
    var card=b.closest('.card');
    if(!card)return;
    var m=b.getAttribute('onclick')||'';
    var hit=m.match(/changeQty\\(['"]([^'"]+)['"],\\s*([-+]?\\d+)\\)/);
    if(!hit)return;
    e.preventDefault();
    e.stopImmediatePropagation();
    change(hit[1],Number(hit[2]));
  },true);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
setTimeout(install,500);
})();