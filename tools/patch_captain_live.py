from pathlib import Path

ROOT=Path('.')
main=ROOT/'app/src/main/java/com/samosaking/nawalgarh/MainActivity.java'
s=main.read_text()
marker='CAPTAIN_LIVE_NATIVE_V1'
if marker not in s:
    fields='/* CAPTAIN_LIVE_NATIVE_V1 */ ListenerRegistration captainOrderListener,captainBoyListener; String captainEmail=""; '
    s=s.replace('FirebaseAuth a;FirebaseFirestore db;', 'FirebaseAuth a;FirebaseFirestore db;'+fields, 1)
    method=r'''public void getCaptainLive(String orderId){
  try{
    if(captainOrderListener!=null)captainOrderListener.remove();
    if(captainBoyListener!=null)captainBoyListener.remove();
    captainEmail="";
    if(orderId==null||orderId.trim().isEmpty())return;
    final String oid=orderId.trim();
    captainOrderListener=db.collection("orders").document(oid).addSnapshotListener((snap,err)->{
      try{
        if(err!=null||snap==null||!snap.exists())return;
        String status=snap.getString("status"); if(status==null)status="";
        Double clat=snap.getDouble("latitude"), clon=snap.getDouble("longitude");
        String email=snap.getString("deliveryBoyEmail"); if(email==null)email=""; email=email.trim();
        JSONObject out=new JSONObject();out.put("orderId",oid);out.put("status",status);if(clat!=null)out.put("customerLat",clat);if(clon!=null)out.put("customerLon",clon);out.put("online",false);
        js("window.captainLiveData("+JSONObject.quote(out.toString())+");");
        boolean active="OUT_FOR_DELIVERY".equals(status)&&!email.isEmpty();
        if(!active){if(captainBoyListener!=null){captainBoyListener.remove();captainBoyListener=null;}captainEmail="";return;}
        if(email.equals(captainEmail)&&captainBoyListener!=null)return;
        if(captainBoyListener!=null)captainBoyListener.remove();
        captainEmail=email;
        captainBoyListener=db.collection("deliveryBoys").whereEqualTo("email",email).limit(1).addSnapshotListener((boys,be)->{
          try{
            JSONObject live=new JSONObject();live.put("orderId",oid);live.put("status",status);if(clat!=null)live.put("customerLat",clat);if(clon!=null)live.put("customerLon",clon);live.put("online",false);
            if(be==null&&boys!=null&&!boys.isEmpty()){
              DocumentSnapshot b=boys.getDocuments().get(0);Double lat=b.getDouble("latitude"),lon=b.getDouble("longitude");Boolean on=b.getBoolean("online");
              if(lat!=null)live.put("lat",lat);if(lon!=null)live.put("lon",lon);live.put("online",Boolean.TRUE.equals(on));
            }
            js("window.captainLiveData("+JSONObject.quote(live.toString())+");");
          }catch(Exception ignored){}
        });
      }catch(Exception ignored){}
    });
  }catch(Exception ignored){}
}
'''
    idx=s.find('class Bridge{')
    if idx<0: raise SystemExit('Bridge class not found')
    pos=idx+len('class Bridge{')
    s=s[:pos]+method+s[pos:]
    main.write_text(s)
html=ROOT/'app/src/main/assets/index.html'
h=html.read_text()
script='<script src="captain-live.js?v=1"></script>'
if 'captain-live.js' not in h:
    if '</body>' in h: h=h.replace('</body>',script+'</body>',1)
    else: h+=script
    html.write_text(h)
print('Captain Live patch applied')
