(function(){'use strict';
window.SKProductVideo={init:function(){
 if(document.getElementById('sk-real-product-video'))return;
 var css=document.createElement('style');
 css.textContent='.skpv{margin:10px 14px 16px;border-radius:20px;overflow:hidden;background:#17100b;box-shadow:0 8px 24px rgba(0,0,0,.16);position:relative;min-height:205px}.skpv-img{display:block;width:100%;height:205px;object-fit:cover;background:#2a1a0d}.skpv-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.78),rgba(0,0,0,.22) 70%,rgba(0,0,0,.12))}.skpv-copy{position:absolute;left:18px;top:18px;right:18px;color:#fff;z-index:3}.skpv-copy span{display:inline-block;background:#f6c94a;color:#17100b;border-radius:999px;padding:5px 9px;font-size:10px;font-weight:900}.skpv-copy b{display:block;font-size:25px;line-height:1.08;margin-top:9px}.skpv-copy small{display:block;font-size:12px;margin-top:7px;color:#fff}.skpv-order{position:absolute;left:18px;bottom:16px;z-index:4;border:0;border-radius:12px;background:#fff;color:#17100b;padding:10px 17px;font-weight:900;font-size:12px}.skpv-dots{position:absolute;right:16px;bottom:20px;z-index:4;color:#fff;font-size:11px;font-weight:900}';
 document.head.appendChild(css);
 var box=document.createElement('section');box.id='sk-real-product-video';box.className='skpv';
 box.innerHTML='<img class="skpv-img" src="product-images/pizza.jpg" alt="Samosa King food banner"><div class="skpv-shade"></div><div class="skpv-copy"><span id="skpvTag">🔥 FRESH & HOT</span><b id="skpvTitle">Fresh Food, Made for You</b><small id="skpvSub">Samosa • Pizza • Burger • Snacks</small></div><button class="skpv-order" type="button">Order Now</button><div class="skpv-dots" id="skpvDots">● ○ ○</div>';
 var anchor=document.querySelector('.cats')||document.querySelector('.hero')||document.body;
 if(anchor.parentNode)anchor.parentNode.insertBefore(box,anchor.nextSibling);
 var slides=[['🔥 FRESH & HOT','Fresh Food, Made for You','Samosa • Pizza • Burger • Snacks'],['👑 SAMOSA KING','Hot & Delicious Every Day','Freshly prepared in Nawalgarh'],['🛒 ORDER NOW','Your Favourite Food, One Tap Away','Minimum order ₹100 • COD available']];
 var i=0,tag=box.querySelector('#skpvTag'),title=box.querySelector('#skpvTitle'),sub=box.querySelector('#skpvSub'),dots=box.querySelector('#skpvDots');
 function show(){var x=slides[i];tag.textContent=x[0];title.textContent=x[1];sub.textContent=x[2];dots.textContent=i===0?'● ○ ○':i===1?'○ ● ○':'○ ○ ●'}
 box.querySelector('.skpv-order').onclick=function(){var c=document.getElementById('categories')||document.querySelector('.cats');if(c)c.scrollIntoView({behavior:'smooth',block:'start'});else window.scrollTo({top:0,behavior:'smooth'})};
 show();setInterval(function(){i=(i+1)%slides.length;show()},4500);
}};
setTimeout(function(){window.SKProductVideo.init()},900);
})();