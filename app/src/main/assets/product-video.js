(function(){'use strict';
window.SKProductVideo={init:function(){
  if(document.getElementById('sk-real-product-video'))return;
  var css=document.createElement('style');
  css.textContent='.skpv{margin:14px 0 18px;border-radius:22px;overflow:hidden;background:#111;box-shadow:0 10px 30px rgba(0,0,0,.18);position:relative}.skpv-video{display:block;width:100%;height:260px;object-fit:cover;background:#111}.skpv-head{position:absolute;z-index:3;left:16px;top:14px;color:#fff;font-weight:900;font-size:15px;text-shadow:0 2px 8px #000}.skpv-badge{position:absolute;z-index:3;left:16px;bottom:16px;color:#fff;font-size:12px;font-weight:800;letter-spacing:1px;text-shadow:0 2px 8px #000}.skpv-sound{position:absolute;z-index:4;right:14px;top:14px;width:40px;height:40px;border:0;border-radius:50%;background:rgba(255,255,255,.9);font-size:17px}.skpv-shade{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.38),transparent 38%,rgba(0,0,0,.42))}';
  document.head.appendChild(css);
  var box=document.createElement('section');
  box.id='sk-real-product-video';
  box.className='skpv';
  box.innerHTML='<div class="skpv-head">Samosa King • Fresh & Hot</div><video class="skpv-video" autoplay muted loop playsinline preload="auto" poster="product-images/pizza.jpg"><source src="product-video.mp4" type="video/mp4"></video><div class="skpv-shade"></div><div class="skpv-badge">OUR SPECIAL MENU • ORDER NOW</div><button class="skpv-sound" aria-label="Turn sound on">🔇</button>';
  var anchor=document.querySelector('.search-bar')||document.querySelector('.hero')||document.querySelector('.container')||document.body;
  anchor.parentNode.insertBefore(box,anchor.nextSibling);
  var video=box.querySelector('video'),btn=box.querySelector('.skpv-sound');
  btn.onclick=function(){video.muted=!video.muted;btn.textContent=video.muted?'🔇':'🔊';btn.setAttribute('aria-label',video.muted?'Turn sound on':'Turn sound off');if(video.paused)video.play().catch(function(){})};
  video.addEventListener('error',function(){box.remove()});
  video.play().catch(function(){});
}};
setTimeout(function(){window.SKProductVideo.init()},900);
})();