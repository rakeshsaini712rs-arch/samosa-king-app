(function(){'use strict';
window.SKProductVideo={init:function(){
 if(document.getElementById('sk-real-product-video'))return;
 var css=document.createElement('style');
 css.textContent='.skpv{margin:10px 14px 16px;border-radius:20px;overflow:hidden;background:linear-gradient(135deg,#fff7e8,#ffd66b);box-shadow:0 8px 24px rgba(0,0,0,.16);position:relative;min-height:205px}.skpv-art{position:absolute;right:12px;bottom:5px;width:48%;height:100%;display:flex;align-items:center;justify-content:center;font-size:105px}.skpv-copy{position:absolute;left:18px;top:18px;right:45%;color:#24150b;z-index:3}.skpv-copy span{display:inline-block;background:#17100b;color:#fff;border-radius:999px;padding:5px 9px;font-size:10px;font-weight:900}.skpv-copy b{display:block;font-size:25px;line-height:1.08;margin-top:9px}.skpv-copy small{display:block;font-size:12px;margin-top:7px;font-weight:700}.skpv-order{position:absolute;left:18px;bottom:16px;z-index:4;border:0;border-radius:12px;background:#17100b;color:#fff;padding:10px 17px;font-weight:900;font-size:12px}.skpv-dots{position:absolute;right:18px;bottom:20px;z-index:4;color:#17100b;font-size:11px;font-weight:900}';
 document.head.appendChild(css);
 var box=document.createElement('section');box.id='sk-real-product-video';box.className='skpv';
 box.innerHTML='<div class="skpv-copy"><span>👑 SAMOSA KING • NAWALGARH</span><b>Fresh & Hot Every Day</b><small>Samosa • Kachori • Snacks • More</small></div><div class="skpv-art" aria-hidden="true">🥟</div><button class="skpv-order" type="button">Order Now</button><div class="skpv-dots">●</div>';
 var anchor=document.querySelector('.cats')||document.querySelector('.hero')||document.body;
 if(anchor.parentNode)anchor.parentNode.insertBefore(box,anchor.nextSibling);
 box.querySelector('.skpv-order').onclick=function(){var c=document.getElementById('cats')||document.querySelector('.cats');if(c)c.scrollIntoView({behavior:'smooth',block:'start'});};
}};
setTimeout(function(){window.SKProductVideo.init()},900);
})();