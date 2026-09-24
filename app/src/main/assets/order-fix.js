(function(){
function validateAndOpenPayment(){
  var c=(typeof cart!=='undefined')?cart:{};
  var sub=typeof subtotal==='function'?Number(subtotal()):0;
  var n=(document.getElementById('name')?.value||'').trim();
  var p=(document.getElementById('phone')?.value||'').trim();
  var ad=(document.getElementById('address')?.value||'').trim();
  var msg=document.getElementById('msg');
  function error(t){if(msg){msg.textContent=t;msg.style.color='#c62828';msg.style.fontWeight='800';}return false;}
  if(!Object.keys(c).length)return error('Cart is empty.');
  if(sub<100)return error('Minimum order is ₹100.');
  if(!/^[\p{L} ]{2,50}$/u.test(n))return error('Please enter a valid name (letters and spaces only).');
  if(!/^[6-9]\d{9}$/.test(p))return error('Please enter a valid 10-digit mobile number.');
  if(!ad)return error('Please enter the delivery address.');
  if(msg){msg.textContent='';msg.style.color='';}
  if(typeof closeCart==='function')closeCart();
  var pm=document.getElementById('paymentChoiceModal');
  var op=document.getElementById('onlinePaymentBox');
  if(pm)pm.style.display='block';
  if(op)op.style.display='none';
  return true;
}
window.SKOrderFix={submit:validateAndOpenPayment};
document.addEventListener('click',function(e){var b=e.target&&e.target.closest?e.target.closest('#modal .order'):null;if(!b)return;e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();validateAndOpenPayment();},true);
function installOrderFix(){
  var b=document.querySelector('#modal .order');
  if(!b || b.dataset.skFixed==='1') return;
  b.dataset.skFixed='1'; b.removeAttribute('onclick');
  b.onclick=validateAndOpenPayment;
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
