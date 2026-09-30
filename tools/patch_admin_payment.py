from pathlib import Path

p = Path('admin/src/main/assets/admin.html')
if not p.exists():
    raise SystemExit(f'Admin source not found: {p}')

s = p.read_text(encoding='utf-8')
original = s

# Keep the payment action explicit when the existing UI contains these labels.
s = s.replace('Mark Payment Received', 'Verify Payment')
s = s.replace('Payment Received', 'Payment Verified')

# Add a reliable visible payment-control panel to every live order card.
# The native AdminActivity already handles samosa://admin/payment and writes
# paymentStatus to Firestore, so the delivery app can receive the result.
if 'id="skPaymentVerificationPatch"' not in s:
    inject = r'''<script id="skPaymentVerificationPatch">
(function(){
  function orderId(card){
    var el=card.querySelector('[data-order-id],[data-id],[id^="order-"]');
    if(el){var v=el.getAttribute('data-order-id')||el.getAttribute('data-id')||el.id.replace(/^order-/,'');if(v)return v;}
    var t=card.innerText||'';
    var m=t.match(/Order\s*#\s*([A-Za-z0-9_-]{6,})/i);
    return m?m[1]:'';
  }
  function paymentKind(t){
    t=(t||'').toUpperCase();
    if(/\bCOD\b|CASH ON DELIVERY|CASH/.test(t)) return 'COD';
    if(/\bUPI\b|ONLINE PAYMENT|PHONEPE|PHONE PAY|ONLINE/.test(t)) return 'UPI';
    return '';
  }
  function enhance(card){
    if(!card||card.dataset.skPayEnhanced==='1')return;
    var text=card.innerText||'';
    var kind=paymentKind(text);
    if(!kind)return;
    var id=orderId(card);
    if(!id)return;
    card.dataset.skPayEnhanced='1';
    var box=document.createElement('div');
    box.className='paymentBox skPaymentVerificationBox';
    box.style.cssText='margin-top:10px;padding:12px;border-radius:14px;border:1px solid #eadfd3;background:#fffaf1;';
    if(kind==='COD'){
      box.innerHTML='<div style="font-weight:900;font-size:16px">💵 COD</div><div style="margin-top:5px;color:#6b5b50">Delivery Boy instruction: <b>Collect Cash from Customer</b></div>';
    }else{
      var paid=/PAYMENT\s*(VERIFIED|RECEIVED)|PAYMENT SUCCESSFULLY|PAID|SUCCESSFUL|SUCCESS/.test(text.toUpperCase());
      if(paid){
        box.innerHTML='<div style="font-weight:900;font-size:16px;color:#16803c">✅ UPI — Payment Successfully Submitted</div><div style="margin-top:5px;color:#16803c;font-weight:800">Delivery Boy: No Cash to Collect</div>';
      }else{
        box.innerHTML='<div style="font-weight:900;font-size:16px">💳 UPI / Online Payment</div><div style="margin-top:5px;color:#b36b00;font-weight:800">Admin verification required before delivery</div><button type="button" class="btn goldbtn skVerifyPayment" style="width:100%;margin:10px 0 0">✓ Verify Payment</button>';
        box.querySelector('.skVerifyPayment').onclick=function(){
          this.disabled=true;this.textContent='Verifying…';
          location.href='samosa://admin/payment?id='+encodeURIComponent(id)+'&value=PAID';
        };
      }
    }
    card.appendChild(box);
  }
  function scan(){document.querySelectorAll('.order').forEach(enhance);}
  new MutationObserver(scan).observe(document.documentElement,{childList:true,subtree:true});
  setTimeout(scan,300);setTimeout(scan,1000);setTimeout(scan,2500);
})();
</script>'''
    if '</body>' not in s:
        raise SystemExit('admin.html body marker not found')
    s=s.replace('</body>',inject+'\n</body>',1)

if s != original:
    p.write_text(s,encoding='utf-8')
    print('Admin COD/UPI payment verification patch applied.')
else:
    print('Admin payment verification patch already applied or source unchanged.')
