(function(){'use strict';
window.SKProductVideo={init:function(){
 if(document.getElementById('sk-real-product-video'))return;
 var css=document.createElement('style');
 css.textContent='.skpv{margin:10px 14px 16px;border-radius:20px;overflow:hidden;background:#fff7e8;box-shadow:0 8px 24px rgba(0,0,0,.16);position:relative;min-height:205px}.skpv-img{display:block;width:100%;height:205px;object-fit:cover;background:#fff7e8}.skpv-copy{position:absolute;left:18px;top:18px;right:18px;color:#24150b;z-index:3}.skpv-copy span{display:inline-block;background:#17100b;color:#fff;border-radius:999px;padding:5px 9px;font-size:10px;font-weight:900}.skpv-order{position:absolute;left:18px;bottom:16px;z-index:4;border:0;border-radius:12px;background:#17100b;color:#fff;padding:10px 17px;font-weight:900;font-size:12px}.skpv-dots{position:absolute;right:16px;bottom:20px;z-index:4;color:#17100b;font-size:11px;font-weight:900}.skpv-img{image-rendering:auto}';
 document.head.appendChild(css);
 var box=document.createElement('section');box.id='sk-real-product-video';box.className='skpv';
 box.innerHTML='<img class="skpv-img" src="samosa-king-banner.svg" alt="Samosa King promotional banner"><button class="skpv-order" type="button">Order Now</button><div class="skpv-dots" id="skpvDots">●</div>';
 var anchor=document.querySelector('.cats')||document.querySelector('.hero')||document.body;
 if(anchor.parentNode)anchor.parentNode.insertBefore(box,anchor.nextSibling);
 box.querySelector('.skpv-order').onclick=function(){var c=document.getElementById('categories')||document.querySelector('.cats');if(c)c.scrollIntoView({behavior:'smooth',block:'start'});else window.scrollTo({top:0,behavior:'smooth'})};
}};
setTimeout(function(){window.SKProductVideo.init()},900);
})();