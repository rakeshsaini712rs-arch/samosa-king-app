from pathlib import Path

p = Path('delivery/src/main/java/com/samosaking/delivery/DeliveryActivity.java')
if not p.exists():
    raise SystemExit(f'Delivery source not found: {p}')
s = p.read_text(encoding='utf-8')
old = 'Payment Successfully Received — No Cash to Collect'
new = 'Payment Successfully Submitted — No Cash to Collect'
if old in s:
    s = s.replace(old, new)
# Make the delivery instruction explicit and tied to the verified Firestore state.
s = s.replace('Payment: Collect Cash from Customer', 'COD — Collect Cash from Customer')
s = s.replace('Online Payment: Awaiting Confirmation', 'UPI — Awaiting Admin Payment Verification')
if 'Payment Successfully Submitted — No Cash to Collect' not in s:
    raise SystemExit('Expected verified-UPI delivery instruction was not found after patch.')
p.write_text(s, encoding='utf-8')
print('Delivery COD/UPI payment instructions patched.')
