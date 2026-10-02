from pathlib import Path

p = Path('delivery/src/main/java/com/samosaking/delivery/DeliveryActivity.java')
s = p.read_text(encoding='utf-8')
old = 'db.collection("orders").document(d.getId()).update("status",value)'
new = 'db.collection("orders").document(d.getId()).update("status",value,"deliveryBoyEmail",auth.getCurrentUser().getEmail(),"trackingActive","OUT_FOR_DELIVERY".equals(value),"deliveryStartedAt","OUT_FOR_DELIVERY".equals(value)?FieldValue.serverTimestamp():null)'
if old in s:
    s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Delivery Captain tracking patch applied')
