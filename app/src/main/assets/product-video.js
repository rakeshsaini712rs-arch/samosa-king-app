(function(){'use strict';
window.SKProductVideo={init:function(){
 if(document.getElementById('sk-real-product-video'))return;
 var css=document.createElement('style');
 css.textContent='.skpv{margin:10px 14px 16px;border-radius:18px;overflow:hidden;position:relative;height:190px;background:#fff;box-shadow:0 5px 18px rgba(0,0,0,.14);font-family:inherit}.skpv-grid{display:grid;grid-template-columns:repeat(3,1fr);height:100%;gap:3px}.skpv-grid img{width:100%;height:100%;object-fit:cover;display:block;image-rendering:auto}.skpv-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.72),rgba(0,0,0,.18) 55%,rgba(0,0,0,.28));z-index:2}.skpv-copy{position:absolute;left:17px;top:15px;z-index:3;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.5)}.skpv-brand{display:inline-block;background:#e23744;color:#fff;border-radius:7px;padding:5px 8px;font-size:9px;font-weight:900;letter-spacing:.4px}.skpv-copy b{display:block;font-size:25px;line-height:1.05;margin-top:9px}.skpv-copy small{display:block;font-size:11px;margin-top:6px;font-weight:800}.skpv-cta{margin-top:11px;background:#fff;color:#111;border:0;border-radius:9px;padding:8px 14px;font-size:11px;font-weight:900}.skpv-note{position:absolute;right:12px;bottom:10px;z-index:3;color:#fff;font-size:9px;font-weight:900;background:rgba(0,0,0,.48);padding:5px 8px;border-radius:999px}';
 document.head.appendChild(css);
 var box=document.createElement('section');box.id='sk-real-product-video';box.className='skpv';
 box.innerHTML='<div class="skpv-grid"><img src="product-images/samosa.jpg" alt="Samosa"><img src="product-images/pizza.jpg" alt="Pizza"><img src="product-images/burger.jpg" alt="Burger"></div><div class="skpv-shade"></div><div class="skpv-copy"><span class="skpv-brand">👑 SAMOSA KING • NAWALGARH</span><b>Fresh & Hot<br>Every Day</b><small>🥟 Samosa • Pizza • Burger & More</small><button class="skpv-cta" type="button">Order Now →</button></div><div class="skpv-note">3 FOOD PICKS • 1 BANNER</div>';
 var anchor=document.querySelector('.cats')||document.querySelector('.hero')||document.body;
 if(anchor.parentNode)anchor.parentNode.insertBefore(box,anchor.nextSibling);
 box.querySelector('.skpv-cta').onclick=function(){var c=document.getElementById('cats')||document.querySelector('.cats');if(c)c.scrollIntoView({behavior:'smooth',block:'start'});};
}};
setTimeout(function(){window.SKProductVideo.init()},900);
})();