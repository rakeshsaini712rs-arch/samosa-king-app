from pathlib import Path

p = Path('admin/src/main/assets/admin.html')
if not p.exists():
    raise SystemExit(f'Admin source not found: {p}')

s = p.read_text(encoding='utf-8')
original = s

# Make the existing Admin payment action explicit: Admin verifies the payment
# before the delivery captain is shown that no cash is required.
s = s.replace('Mark Payment Received', 'Verify Payment')
s = s.replace('Payment Received', 'Payment Verified')

# Keep the change idempotent so repeated builds do not modify the source again.
if s != original:
    p.write_text(s, encoding='utf-8')
    print('Admin payment verification UI patch applied.')
else:
    print('Admin payment verification UI patch already applied or source unchanged.')
