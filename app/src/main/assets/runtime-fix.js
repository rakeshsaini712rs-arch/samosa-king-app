(function(){'use strict';
function bindOrder(){
 var b=document.querySelector('.order');
 if(!b||b.dataset.skRuntime==='1')return;
 b.dataset.skRuntime='1';b.removeAttribute('onclick');
 b.addEventListener('click',function(){if(typeof window.placeOrder==='function')window.placeOrder();});
}
function bind(){bindOrder();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind);else bind();
setTimeout(bind,500);setTimeout(bind,1500);
new MutationObserver(bind).observe(document.documentElement,{childList:true,subtree:true});
})();