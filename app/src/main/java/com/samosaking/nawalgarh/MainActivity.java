package com.samosaking.nawalgarh;

import android.Manifest;
import android.app.Activity;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.PhoneAuthCredential;
import com.google.firebase.auth.PhoneAuthOptions;
import com.google.firebase.auth.PhoneAuthProvider;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.ListenerRegistration;
import com.google.firebase.firestore.Query;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {
    private static final int LOCATION_REQ = 4101;
    private static final double SHOP_LAT = 27.8514056;
    private static final double SHOP_LON = 75.2711528;
    private static final double DELIVERY_KM = 5.0;
    private static final String CHANNEL_ID = "order_status";
    private WebView web;
    private FirebaseAuth auth;
    private FirebaseFirestore db;
    private ListenerRegistration statusListener;
    private String pendingName, pendingPhone, pendingAddress, pendingItems;
    private int pendingSubtotal;
    private boolean authInProgress = false;
    private boolean orderInProgress = false;
    private String verificationId;
    private String lastNotifiedStatus = "";

    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        createNotificationChannel();
        web = new WebView(this);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        web.setWebViewClient(new WebViewClient() {
            @Override public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                injectProductImages();
                web.postDelayed(() -> injectProductImages(), 300);
                web.postDelayed(() -> injectProductImages(), 1000);
                injectPremiumDashboard();
                web.postDelayed(() -> injectPremiumDashboard(), 500);
                loadLastOrder();
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, String url) {
                try { if (url.startsWith("tel:") || url.startsWith("https://wa.me/") || url.startsWith("whatsapp:")) { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); return true; } } catch (Exception ignored) {}
                return false;
            }
        });
        web.addJavascriptInterface(new AndroidBridge(), "AndroidBridge");
        setContentView(web);
        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();
        auth.addAuthStateListener(firebaseAuth -> {
            if (firebaseAuth.getCurrentUser() != null) { authInProgress = false; runJs("window.authReady&&window.authReady();"); if (pendingName != null && !orderInProgress) createOrder(); }
        });
        if (auth.getCurrentUser() == null) signIn();
        web.loadUrl("file:///android_asset/index.html");
    }

    private void injectProductImages() {
        String js = "(function(){var m={'Samosa':'samosa.jpg','Kachori':'samosa.jpg','Mirchi Bada':'mirchi-bada.jpg','Dahi Bhalla Plate 1':'dahi-bhalla-1.jpg','Dahi Bhalla Plate 2':'dahi-bhalla-2.jpg','Pizza':'pizza.jpg','Wraps':'wraps.jpg','Momos':'momos.jpg','Burger':'burger.jpg','Pasta':'pasta.jpg','Manchurian':'manchurian.jpg','Kaju Katli':'kaju-katli.jpg','Rasgulla':'rasgulla.jpg','Rajbhog':'rasgulla.jpg','Gulab Jamun':'gulab-jamun.jpg','Sohan Papdi':'sohan-papdi.jpg','Milk Cake':'milk-cake.jpg','Kalakand':'kalakand.jpg','Dilkushal':'dilkushal.jpg','Peda':'milk-cake.jpg','Petha':'kalakand.jpg','Namkin':'sohan-papdi.jpg','Rasmalai':'dahi-bhalla-1.jpg','Dahi (Curd)':'dahi-bhalla-2.jpg'};document.querySelectorAll('.card').forEach(function(c){var h=c.querySelector('h3');if(!h)return;var f=m[h.textContent.trim()];if(!f)return;var v=c.querySelector('.visual');if(!v)return;var img=v.querySelector('img');if(!img){img=document.createElement('img');img.style.cssText='width:100%;height:100%;object-fit:cover;border-radius:13px;display:block';img.loading='eager';v.innerHTML='';v.appendChild(img);}var src='product-images/'+f;if(img.getAttribute('src')!==src)img.src=src;});})();";
        runJs(js);
    }

    private void injectPremiumDashboard() {
        String js = "(function(){if(document.getElementById('premiumDash'))return;var s=document.createElement('style');s.textContent='.pd{margin:12px 14px;padding:15px;background:#17100b;color:#fff;border-radius:18px;box-shadow:0 5px 18px #0002}.pd h2{margin:0 0 10px;font-size:19px}.pdgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.pd button{border:1px solid #ffffff30;background:#2d1c0f;color:#fff;border-radius:11px;padding:11px 8px;font-weight:800}.progress{height:8px;background:#eee1ce;border-radius:99px;overflow:hidden;margin:8px 0}.progress i{display:block;height:100%;background:#f6c94a;width:0}.pdsmall{font-size:11px;color:#e9dfd5}.mini{margin:12px 14px;background:#fff;border:1px solid #eadfce;border-radius:17px;padding:15px}.mini h3{margin:0 0 9px}.historyRow{padding:10px 0;border-bottom:1px solid #eee6dc;font-size:12px}.historyRow:last-child{border-bottom:0}.reorder{float:right;border:0;background:#f6c94a;border-radius:9px;padding:7px 9px;font-weight:900}.saved{font-size:12px;color:#786a5d;line-height:1.5}';document.head.appendChild(s);var d=document.createElement('div');d.id='premiumDash';d.className='pd';d.innerHTML='<h2>👑 Royal Customer Dashboard</h2><div class=\"pdsmall\">Real account tools — no demo data</div><div class=\"pdgrid\" style=\"margin-top:10px\"><button onclick=\"showHistory()\">📦 Order History</button><button onclick=\"saveAddress()\">📍 Save Address</button><button onclick=\"reorderLast()\">🔁 Reorder Last</button><button onclick=\"scrollToCart()\">🛒 View Cart</button></div><div style=\"margin-top:12px\"><b>Minimum order progress</b><div class=\"progress\"><i id=\"minProg\"></i></div><div id=\"minText\" class=\"pdsmall\">Add items worth ₹100 to place your COD order.</div></div><div id=\"savedBox\" class=\"pdsmall\" style=\"margin-top:8px\"></div></div>';var hero=document.querySelector('.hero');hero&&hero.parentNode.insertBefore(d,hero.nextSibling);var h=document.createElement('div');h.id='historyBox';h.className='mini';h.style.display='none';h.innerHTML='<h3>📦 My Orders</h3><div id=\"historyList\" class=\"saved\">Loading real orders…</div>';d.parentNode.insertBefore(h,d.nextSibling);window.showHistory=function(){h.style.display=h.style.display==='none'?'block':'none';if(h.style.display==='block')AndroidBridge.getOrderHistory()};window.renderHistory=function(raw){try{var a=JSON.parse(raw),out='';a.forEach(function(o){out+='<div class=\"historyRow\"><button class=\"reorder\" onclick=\'reorderItems(\\''+o.itemsJson.replace(/'/g,"\\\\'")+"\\')\'>Reorder</button><b>₹"+o.total+"</b> • "+o.status+"<br>"+o.date+"</div>"});$('historyList').innerHTML=out||'No orders found yet.'}catch(e){$('historyList').textContent='Could not load order history.'}};window.reorderItems=function(raw){try{var a=JSON.parse(raw);a.forEach(function(x){for(var i=0;i<x.qty;i++)add(x.id)});scrollToCart()}catch(e){}};window.reorderLast=function(){var id=localStorage.getItem('lastOrderItems');if(!id){alert('No previous order found.');return}reorderItems(id)};window.scrollToCart=function(){openCart()};window.saveAddress=function(){var a=prompt('Enter your delivery address');if(a&&a.trim()){localStorage.setItem('savedAddress',a.trim());$('address').value=a.trim();$('savedBox').textContent='📍 Saved address: '+a.trim()}};var oldRender=window.updateCart;window.updateCart=function(){oldRender();var v=subtotal();$('minProg').style.width=Math.min(100,v)+'%';$('minText').textContent=v>=100?'✅ Minimum order reached. Delivery ₹30 • COD':'Add ₹'+(100-v)+' more to reach the ₹100 minimum.'};var saved=localStorage.getItem('savedAddress');if(saved){$('address').value=saved;$('savedBox').textContent='📍 Saved address: '+saved}window.updateCart()})();";
        runJs(js);
    }

    private void signIn() { if (authInProgress) return; authInProgress = true; auth.signInAnonymously().addOnSuccessListener(r -> {authInProgress=false;runJs("window.authReady&&window.authReady();");if(pendingName!=null&&!orderInProgress)createOrder();}).addOnFailureListener(e->{authInProgress=false;runJs("window.orderError("+JSONObject.quote("Firebase sign-in failed: "+e.getMessage())+");");}); }
    private void sendOtp(String phone) { PhoneAuthOptions options=PhoneAuthOptions.newBuilder(auth).setPhoneNumber(phone).setTimeout(60L,java.util.concurrent.TimeUnit.SECONDS).setActivity(this).setCallbacks(new PhoneAuthProvider.OnVerificationStateChangedCallbacks(){@Override public void onVerificationCompleted(PhoneAuthCredential credential){auth.signInWithCredential(credential).addOnSuccessListener(r->runJs("window.otpVerified("+JSONObject.quote(phone)+");")).addOnFailureListener(e->runJs("window.otpError("+JSONObject.quote(e.getMessage())+");"));}@Override public void onVerificationFailed(com.google.firebase.FirebaseException e){runJs("window.otpError("+JSONObject.quote(e.getMessage())+");");}@Override public void onCodeSent(String id,PhoneAuthProvider.ForceResendingToken token){verificationId=id;runJs("window.otpSent();");}}).build();PhoneAuthProvider.verifyPhoneNumber(options); }
    private void verifyOtp(String code){if(verificationId==null){runJs("window.otpError('Please request OTP first.');");return;}PhoneAuthCredential credential=PhoneAuthProvider.getCredential(verificationId,code);auth.signInWithCredential(credential).addOnSuccessListener(r->{String phone=r.getUser()!=null?r.getUser().getPhoneNumber():"";runJs("window.otpVerified("+JSONObject.quote(phone==null?"":phone)+");");}).addOnFailureListener(e->runJs("window.otpError("+JSONObject.quote(e.getMessage())+");"));}
    private void runJs(String js){runOnUiThread(()->{if(web!=null)web.evaluateJavascript(js,null);});}

    private void beginOrder(String n,String p,String a,String items,int sub){
        if(orderInProgress)return;
        pendingName=n;pendingPhone=p;pendingAddress=a;pendingItems=items;pendingSubtotal=sub;
        if(sub<100){runJs("window.orderError('Minimum order is ₹100.');");return;}
        if(auth.getCurrentUser()==null){signIn();return;}
        checkDeliveryLocation();
    }

    private void checkDeliveryLocation(){
        if(Build.VERSION.SDK_INT>=23 && ActivityCompat.checkSelfPermission(this,Manifest.permission.ACCESS_FINE_LOCATION)!=PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this,Manifest.permission.ACCESS_COARSE_LOCATION)!=PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.ACCESS_FINE_LOCATION,Manifest.permission.ACCESS_COARSE_LOCATION},LOCATION_REQ);
            runJs("window.locationRequired&&window.locationRequired();");
            return;
        }
        LocationManager lm=(LocationManager)getSystemService(LOCATION_SERVICE);
        Location last=null;
        try{last=lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);if(last==null)last=lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);}catch(Exception ignored){}
        if(last!=null){handleLocation(last);return;}
        try{lm.requestSingleUpdate(LocationManager.NETWORK_PROVIDER,new LocationListener(){@Override public void onLocationChanged(Location l){handleLocation(l);}},null);}catch(Exception e){runJs("window.orderError('Location could not be read. Please enable GPS and try again.');");}
    }

    private void handleLocation(Location loc){
        float[] d=new float[1];Location.distanceBetween(loc.getLatitude(),loc.getLongitude(),SHOP_LAT,SHOP_LON,d);double km=d[0]/1000.0;
        runJs("window.locationResult&&window.locationResult("+JSONObject.quote(String.format(java.util.Locale.US,"%.2f",km))+");");
        if(km>DELIVERY_KM){pendingName=null;runJs("window.orderError('Delivery is available only within 5 km of Nansa Gate, Nawalgarh. Your location is "+String.format(java.util.Locale.US,"%.2f",km)+" km away.');");return;}
        createOrder();
    }

    private void createOrder(){if(orderInProgress)return;if(auth.getCurrentUser()==null){signIn();return;}orderInProgress=true;int delivery=30;writeOrder(pendingSubtotal+delivery,delivery);}
    private void writeOrder(int total,int delivery){try{Map<String,Object> order=new HashMap<>();order.put("userId",auth.getCurrentUser().getUid());order.put("customerName",pendingName);order.put("mobile",pendingPhone);order.put("address",pendingAddress);order.put("paymentMethod","COD");order.put("subtotal",pendingSubtotal);order.put("deliveryFee",delivery);order.put("total",total);order.put("status","PLACED");order.put("createdAt",FieldValue.serverTimestamp());JSONArray arr=new JSONArray(pendingItems);Map<String,Object> items=new HashMap<>();for(int i=0;i<arr.length();i++){JSONObject item=arr.getJSONObject(i);items.put(item.getString("id"),item.getInt("qty"));}order.put("items",items);db.collection("orders").add(order).addOnSuccessListener(ref->{getPreferences(Context.MODE_PRIVATE).edit().putString("lastOrderId",ref.getId()).apply();getPreferences(Context.MODE_PRIVATE).edit().putString("lastOrderItems",pendingItems).apply();listenStatus(ref.getId());orderInProgress=false;pendingName=null;runJs("window.orderCreated("+JSONObject.quote(ref.getId())+");");}).addOnFailureListener(e->{orderInProgress=false;runJs("window.orderError("+JSONObject.quote("Order save failed: "+e.getMessage())+");");});}catch(Exception e){orderInProgress=false;runJs("window.orderError("+JSONObject.quote("Order error: "+e.getMessage())+");");}}

    private void getOrderHistory(){
        if(auth.getCurrentUser()==null){runJs("window.renderHistory('[]')");return;}
        db.collection("orders").whereEqualTo("userId",auth.getCurrentUser().getUid()).orderBy("createdAt",Query.Direction.DESCENDING).limit(20).get().addOnSuccessListener(snap->{try{JSONArray out=new JSONArray();for(com.google.firebase.firestore.DocumentSnapshot d:snap.getDocuments()){JSONObject o=new JSONObject();o.put("total",d.getLong("total")!=null?d.getLong("total"):0);o.put("status",d.getString("status")!=null?d.getString("status"):"PLACED");o.put("date",d.getDate("createdAt")!=null?d.getDate("createdAt").toString():"Recent order");Map<String,Object> im=d.get("items",Map.class);JSONArray ia=new JSONArray();if(im!=null)for(Map.Entry<String,Object> e:im.entrySet()){JSONObject x=new JSONObject();x.put("id",e.getKey());x.put("qty",((Number)e.getValue()).intValue());ia.put(x);}o.put("itemsJson",ia.toString());out.put(o);}runJs("window.renderHistory("+JSONObject.quote(out.toString())+");");}catch(Exception e){runJs("window.renderHistory('[]')");}}).addOnFailureListener(e->runJs("window.renderHistory('[]')"));
    }

    private void listenStatus(String id){if(statusListener!=null)statusListener.remove();statusListener=db.collection("orders").document(id).addSnapshotListener((snapshot,error)->{if(error!=null||snapshot==null||!snapshot.exists())return;String status=snapshot.getString("status");if(status==null)status="PLACED";runJs("window.statusUpdate("+JSONObject.quote(status)+");");if(!status.equals(lastNotifiedStatus)){lastNotifiedStatus=status;if(!status.equals("PLACED"))showStatusNotification(status);}});}
    private void createNotificationChannel(){if(Build.VERSION.SDK_INT>=26){NotificationManager nm=getSystemService(NotificationManager.class);nm.createNotificationChannel(new NotificationChannel(CHANNEL_ID,"Order status",NotificationManager.IMPORTANCE_DEFAULT));}}
    private void showStatusNotification(String status){if(Build.VERSION.SDK_INT>=33&&ActivityCompat.checkSelfPermission(this,Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED)return;NotificationCompat.Builder b=new NotificationCompat.Builder(this,CHANNEL_ID).setSmallIcon(android.R.drawable.ic_dialog_info).setContentTitle("Samosa King – Order Update").setContentText("Order status: "+status).setPriority(NotificationCompat.PRIORITY_DEFAULT).setAutoCancel(true);((NotificationManager)getSystemService(NOTIFICATION_SERVICE)).notify(8127,b.build());}
    private void loadLastOrder(){String id=getPreferences(Context.MODE_PRIVATE).getString("lastOrderId",null);if(id!=null)listenStatus(id);}

    @Override public void onRequestPermissionsResult(int requestCode,String[] permissions,int[] results){super.onRequestPermissionsResult(requestCode,permissions,results);if(requestCode==LOCATION_REQ){if(results.length>0&&(results[0]==PackageManager.PERMISSION_GRANTED||(results.length>1&&results[1]==PackageManager.PERMISSION_GRANTED)))checkDeliveryLocation();else runJs("window.orderError('Location permission is required to verify the 5 km delivery area.');");}}

    public class AndroidBridge{
        @JavascriptInterface public void sendOtp(String phone){runOnUiThread(()->sendOtp(phone));}
        @JavascriptInterface public void verifyOtp(String code){runOnUiThread(()->verifyOtp(code));}
        @JavascriptInterface public void placeOrder(String n,String p,String a,String items,int subtotal){runOnUiThread(()->beginOrder(n,p,a,items,subtotal));}
        @JavascriptInterface public void loadLastOrder(){runOnUiThread(()->loadLastOrder());}
        @JavascriptInterface public void cancelLastOrder(){runOnUiThread(()->{String id=getPreferences(Context.MODE_PRIVATE).getString("lastOrderId",null);if(id!=null)db.collection("orders").document(id).update("status","CANCELLED");});}
        @JavascriptInterface public void getLocation(){runOnUiThread(()->checkDeliveryLocation());}
        @JavascriptInterface public void getOrderHistory(){runOnUiThread(()->getOrderHistory());}
    }
}
