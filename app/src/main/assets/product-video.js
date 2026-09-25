(function(){'use strict';
window.SKProductVideo={init:function(){
 if(document.getElementById('sk-real-product-video'))return;
 var css=document.createElement('style');
 css.textContent='.skpv{margin:10px 14px 16px;border-radius:18px;overflow:hidden;position:relative;height:205px;background:#111;box-shadow:0 7px 20px rgba(0,0,0,.16)}.skpv img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}.skpv-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.82) 0%,rgba(0,0,0,.43) 47%,rgba(0,0,0,.06) 100%);z-index:2}.skpv-copy{position:absolute;left:18px;top:17px;right:43%;color:#fff;z-index:3}.skpv-copy span{display:inline-block;background:#e23744;color:#fff;border-radius:999px;padding:5px 9px;font-size:9px;font-weight:900}.skpv-copy b{display:block;font-size:26px;line-height:1.05;margin-top:9px}.skpv-copy small{display:block;font-size:11px;margin-top:7px;font-weight:800}.skpv-order{position:absolute;left:18px;bottom:15px;z-index:4;border:0;border-radius:11px;background:#fff;color:#17100b;padding:9px 16px;font-weight:900;font-size:11px}.skpv-tag{position:absolute;right:14px;top:14px;z-index:4;background:rgba(0,0,0,.58);color:#fff;border-radius:999px;padding:6px 9px;font-size:9px;font-weight:900}';
 document.head.appendChild(css);
 var box=document.createElement('section');box.id='sk-real-product-video';box.className='skpv';
 box.innerHTML='<img src="https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6b/Samosa_with_chutney.jpg/1280px-Samosa_with_chutney.jpg" alt="Fresh Samosa King samosa with chutney" loading="eager"><div class="skpv-shade"></div><div class="skpv-copy"><span>👑 SAMOSA KING • NAWALGARH</span><b>Hot & Crispy Samosa</b><small>Freshly made • Perfect with chutney</small></div><button class="skpv-order" type="button">Order Now</button><div class="skpv-tag">TODAY'S SPECIAL</div>';
 var anchor=document.querySelector('.cats')||document.querySelector('.hero')||document.body;
 if(anchor.parentNode)anchor.parentNode.insertBefore(box,anchor.nextSibling);
 box.querySelector('.skpv-order').onclick=function(){var c=document.getElementById('cats')||document.querySelector('.cats');if(c)c.scrollIntoView({behavior:'smooth',block:'start'});};
}};
setTimeout(function(){window.SKProductVideo.init()},900);
})();