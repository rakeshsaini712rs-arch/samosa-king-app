(function(){
function installOrderFix(){
  var b=document.querySelector('.order');
  if(!b || b.dataset.skFixed==='1') return;
  b.dataset.skFixed='1'; b.removeAttribute('onclick');
  b.onclick=function(){
    var c=(typeof cart!=='undefined')?cart:{};
    var sub=typeof subtotal==='function'?Number(subtotal()):0;
    var n=(document.getElementById('name')?.value||'').trim();
    var p=(document.getElementById('phone')?.value||'').trim();
    var ad=(document.getElementById('address')?.value||'').trim();
    var code=(document.getElementById('skorderCoupon')?.value||'').trim().toUpperCase();
    var msg=document.getElementById('msg');
    if(!Object.keys(c).length){if(msg)msg.textContent='Cart is empty.';return;}
    if(sub<100){if(msg)msg.textContent='Minimum order is ₹100.';return;}
    if(!/^[\p{L} ]{2,50}$/u.test(n)){if(msg)msg.textContent='Please enter a valid name (letters and spaces only).';return;}if(!/^[6-9]\d{9}$/.test(p)){if(msg)msg.textContent='Please enter a valid 10-digit mobile number.';return;}if(!ad){if(msg)msg.textContent='Please enter name, phone and delivery address.';return;}if(!window.AndroidBridge||typeof AndroidBridge.isPhoneVerified!=='function'){if(msg)msg.textContent='Mobile verification service is not available.';return;}if(!AndroidBridge.isPhoneVerified(p)){if(msg)msg.textContent='Please verify this mobile number with OTP before placing the order.';return;}
    var items=Object.entries(c).map(function(e){return{id:e[0],qty:Number(e[1])}});
    if(!window.AndroidBridge||typeof AndroidBridge.placeOrderWithCoupon!=='function'){if(msg)msg.textContent='Order service is not available.';return;}
    if(msg)msg.textContent=code==='DIWALI'?'Applying DIWALI 10% discount and placing COD order…':'Checking delivery area and placing COD order…';
    try{AndroidBridge.placeOrderWithCoupon(n,p,ad,JSON.stringify(items),sub,code);}catch(e){if(msg)msg.textContent='Could not start order: '+e.message;}
  };
}
function addCoupon(){
  var sheet=document.querySelector('.sheet');
  if(!sheet||document.getElementById('skcouponOrder'))return;
  var box=document.createElement('div');box.id='skcouponOrder';box.className='sksection';
  box.innerHTML='<h3>🎁 Coupon</h3><div class="skrow"><input id="skorderCoupon" class="skinput" placeholder="Coupon code"><button type="button" class="skbtn gold">Apply</button></div><div id="skorderCouponMsg" class="sksmall"></div>';
  var h=sheet.querySelector('h3');if(h)h.after(box);else sheet.prepend(box);
  box.querySelector('button').onclick=function(){var v=document.getElementById('skorderCoupon').value.trim().toUpperCase();var m=document.getElementById('skorderCouponMsg');if(v==='DIWALI'){var s=Number(typeof subtotal==='function'?subtotal():0),d=Math.floor(s*.10);m.textContent=d?'✅ DIWALI applied: ₹'+d+' discount. Final amount will be verified securely.':'Minimum order is ₹100.';}else m.textContent=v?'Coupon will be validated securely when the order is submitted.':'Enter a coupon code.';};
}
function run(){addCoupon();installOrderFix();}
setInterval(run,800);document.addEventListener('DOMContentLoaded',run);
})();
