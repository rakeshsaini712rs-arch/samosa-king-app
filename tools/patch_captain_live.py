from pathlib import Path

ROOT=Path('.')
main=ROOT/'app/src/main/java/com/samosaking/nawalgarh/MainActivity.java'
s=main.read_text()
marker='CAPTAIN_LIVE_NATIVE_V2'
if marker not in s:
    fields='/* CAPTAIN_LIVE_NATIVE_V2 */ '
    s=s.replace('FirebaseAuth a;FirebaseFirestore db;', 'FirebaseAuth a;FirebaseFirestore db;'+fields, 1)
    method=r'''public String getCaptainLastOrderId(){try{return getPreferences(0).getString("lastOrderId","");}catch(Exception e){return "";}}
 public void getCaptainLive(String orderId){
  try{
    if(orderId==null||orderId.trim().isEmpty())return;
    final String oid=orderId.trim();
    db.collection("orders").document(oid).addSnapshotListener((snap,err)->{
      try{
        if(err!=null||snap==null||!snap.exists())return;
        if(a.getCurrentUser()==null||!a.getCurrentUser().getUid().equals(snap.getString("userId")))return;
        String status0=snap.getString("status");String status=status0==null?"":status0;
        JSONObject out=new JSONObject();out.put("orderId",oid);out.put("status",status);
        Double clat=snap.getDouble("latitude"),clon=snap.getDouble("longitude");
        if(clat!=null)out.put("customerLat",clat);if(clon!=null)out.put("customerLon",clon);
        Double lat=snap.getDouble("captainLatitude"),lon=snap.getDouble("captainLongitude");
        if(lat!=null)out.put("lat",lat);if(lon!=null)out.put("lon",lon);
        out.put("online",Boolean.TRUE.equals(snap.getBoolean("trackingActive")));
        js("window.captainLiveData("+JSONObject.quote(out.toString())+");");
      }catch(Exception ignored){}
    });
  }catch(Exception ignored){}
}
'''
    idx=s.find('class Bridge{')
    if idx<0: raise SystemExit('Bridge class not found')
    pos=idx+len('class Bridge{')
    s=s[:pos]+method+s[pos:]
    bridge='@JavascriptInterface public String getCaptainLastOrderId(){return MainActivity.this.getCaptainLastOrderId();}@JavascriptInterface public void getCaptainLive(String id){runOnUiThread(()->MainActivity.this.getCaptainLive(id));}'
    s=s.replace('public class Bridge{@JavascriptInterface', 'public class Bridge{'+bridge+'@JavascriptInterface', 1)
    main.write_text(s)
html=ROOT/'app/src/main/assets/index.html'
h=html.read_text()
script='<script src="captain-live.js?v=3"></script>'
if 'captain-live.js' not in h:
    if '</body>' in h:h=h.replace('</body>',script+'</body>',1)
    else:h+=script
html.write_text(h)
print('Captain Live secure native patch applied')
