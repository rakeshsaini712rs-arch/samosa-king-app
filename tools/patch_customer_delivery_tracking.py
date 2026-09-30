from pathlib import Path

p=Path('app/src/main/java/com/samosaking/nawalgarh/MainActivity.java')
s=p.read_text(encoding='utf-8')
if 'trackingOrderListener' not in s:
    s=s.replace('ListenerRegistration sl,ml;', 'ListenerRegistration sl,ml,trackingOrderListener,trackingBoyListener;')
if 'startCustomerDeliveryTracking();' not in s:
    s=s.replace('images();premium();loadLast();loadMenu();settingsFix();', 'images();premium();loadLast();loadMenu();startCustomerDeliveryTracking();settingsFix();')
if 'tracking-ui.js' not in s:
    s=s.replace("var z=document.createElement('script');z.src='premium-v2.js?v=1';document.head.appendChild(z)", "var z=document.createElement('script');z.src='premium-v2.js?v=1';document.head.appendChild(z);var t=document.createElement('script');t.src='tracking-ui.js?v=1';document.head.appendChild(t)")
marker=' String itemName(String id){'
if 'void startCustomerDeliveryTracking()' not in s:
    method=''' void startCustomerDeliveryTracking(){String oid=getPreferences(0).getString("lastOrderId","");if(oid==null||oid.isEmpty())return;if(trackingOrderListener!=null)trackingOrderListener.remove();trackingOrderListener=db.collection("orders").document(oid).addSnapshotListener((d,e)->{if(e!=null||d==null||!d.exists())return;String st=d.getString("status");if("OUT_FOR_DELIVERY".equals(st)){String em=d.getString("deliveryBoyEmail");Double clat=d.getDouble("latitude"),clon=d.getDouble("longitude");js("window.deliveryTrackingStart&&window.deliveryTrackingStart("+JSONObject.quote(oid)+");");if(em!=null&&!em.trim().isEmpty())listenDeliveryBoyLocation(em.trim(),clat,clon);}else{if(trackingBoyListener!=null){trackingBoyListener.remove();trackingBoyListener=null;}js("window.deliveryTrackingStop&&window.deliveryTrackingStop("+JSONObject.quote(st==null?"":st)+");");}});} void listenDeliveryBoyLocation(String email,Double clat,Double clon){if(trackingBoyListener!=null)trackingBoyListener.remove();trackingBoyListener=db.collection("deliveryBoys").whereEqualTo("email",email).limit(1).addSnapshotListener((s,e)->{if(e!=null||s==null||s.isEmpty())return;DocumentSnapshot d=s.getDocuments().get(0);Double lat=d.getDouble("latitude"),lon=d.getDouble("longitude");if(lat==null||lon==null)return;double km=0;String eta="Calculating…";if(clat!=null&&clon!=null){float[] z={0};Location.distanceBetween(lat,lon,clat,clon,z);km=z[0]/1000.0;int mins=(int)Math.max(1,Math.ceil((km/25.0)*60.0));eta="~"+mins+" min";}Double accuracy=d.getDouble("accuracyMeters");String acc=accuracy==null?"":String.format(Locale.US,"%.0f",accuracy);js("window.deliveryTrackingUpdate&&window.deliveryTrackingUpdate("+lat+","+lon+","+JSONObject.quote(String.format(Locale.US,"%.2f",km))+","+JSONObject.quote(eta)+","+JSONObject.quote(acc)+");");});}
'''
    s=s.replace(marker,method+marker)
p.write_text(s,encoding='utf-8')

p=Path('delivery/src/main/java/com/samosaking/delivery/DeliveryActivity.java')
s=p.read_text(encoding='utf-8')
old='b.setOnClickListener(v->db.collection("orders").document(d.getId()).update("status",value).addOnSuccessListener(x->toast("Status updated.")).addOnFailureListener(x->toast("Update failed: "+x.getMessage())));'
new='b.setOnClickListener(v->{Map<String,Object> up=new HashMap<>();up.put("status",value);if("OUT_FOR_DELIVERY".equals(value)){up.put("trackingActive",true);up.put("deliveryStartedAt",FieldValue.serverTimestamp());up.put("deliveryBoyEmail",auth.getCurrentUser()==null?"":auth.getCurrentUser().getEmail());}else if("DELIVERED".equals(value)){up.put("trackingActive",false);up.put("deliveryCompletedAt",FieldValue.serverTimestamp());}db.collection("orders").document(d.getId()).update(up).addOnSuccessListener(x->toast("Status updated.")).addOnFailureListener(x->toast("Update failed: "+x.getMessage()));});'
if old not in s: raise SystemExit('Delivery action pattern not found')
s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
print('Customer live delivery tracking patch applied.')
