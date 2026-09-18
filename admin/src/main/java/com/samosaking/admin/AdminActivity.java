package com.samosaking.admin;

import android.app.*;import android.content.*;import android.net.Uri;import android.os.*;import android.webkit.*;import android.graphics.Color;import android.widget.TextView;import com.google.firebase.FirebaseApp;import com.google.firebase.FirebaseOptions;import com.google.firebase.auth.FirebaseAuth;import com.google.firebase.firestore.*;import org.json.*;import java.util.*;

public class AdminActivity extends Activity{
 private WebView w; private FirebaseAuth auth; private FirebaseFirestore db; private ListenerRegistration ordersListener;
 private static final String PROJECT="samosa-king-3b90d"; private static final String APP_ID="1:855148039257:android:535730f98ea24e77253548"; private static final String API_KEY="AIzaSyCusjrBM2M59Obiwv-Dgy1m6PgiYDQtwQw";
 private static final String ADMIN_UID="vJCq3yQDe0QcCg5EoEPnjVKwUgJ2";
 @Override public void onCreate(Bundle b){super.onCreate(b);try{
   FirebaseOptions o=new FirebaseOptions.Builder().setProjectId(PROJECT).setApplicationId(APP_ID).setApiKey(API_KEY).build();
   if(FirebaseApp.getApps(this).isEmpty()){FirebaseApp.initializeApp(this,o);} FirebaseApp app=FirebaseApp.getInstance(); auth=FirebaseAuth.getInstance(app); db=FirebaseFirestore.getInstance(app);
   w=new WebView(this);w.setBackgroundColor(Color.WHITE);WebSettings s=w.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setAllowFileAccess(true);s.setAllowContentAccess(true);
   w.setWebViewClient(new WebViewClient(){@Override public void onPageFinished(WebView v,String u){if(auth.getCurrentUser()!=null)checkAdmin();else v.evaluateJavascript("window.showLogin()",null);} @Override public boolean shouldOverrideUrlLoading(WebView v,String u){try{if(u.startsWith("tel:")||u.startsWith("https://wa.me/")){startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(u)));return true;}}catch(Exception ignored){}return false;}});
   w.addJavascriptInterface(new Bridge(),"AdminNative");setContentView(w);w.loadUrl("file:///android_asset/admin.html");
 }catch(Throwable e){fatal(e);}}
 private void fatal(Throwable e){TextView t=new TextView(this);t.setText("Samosa King ADMIN\n\nStartup error: "+e.getClass().getSimpleName()+"\n"+String.valueOf(e.getMessage()));t.setTextSize(17);t.setTextColor(Color.DKGRAY);t.setPadding(40,80,40,40);setContentView(t);}
 private void js(String code){runOnUiThread(()->{if(w!=null)w.evaluateJavascript(code,null);});}
 private void message(String x){js("window.adminError("+JSONObject.quote(x)+")");}
 private boolean isConfiguredAdmin(){return auth!=null&&auth.getCurrentUser()!=null&&ADMIN_UID.equals(auth.getCurrentUser().getUid());}
 private void deny(String uid){auth.signOut();js("window.showLogin();window.loginError("+JSONObject.quote("This account is not authorized as admin. UID: "+uid)+")");}
 private void checkAdmin(){if(auth==null||auth.getCurrentUser()==null){js("window.showLogin()");return;}String uid=auth.getCurrentUser().getUid();if(isConfiguredAdmin()){js("window.showDashboard("+JSONObject.quote("Admin")+")");listenOrders();}else{deny(uid);}}
 private void listenOrders(){if(ordersListener!=null)ordersListener.remove();ordersListener=db.collection("orders").addSnapshotListener((snap,e)->{if(e!=null){message("Could not load live orders: "+e.getClass().getSimpleName()+" — "+e.getMessage());return;}sendOrders(snap);});}
 private void refresh(){if(auth.getCurrentUser()==null){js("window.showLogin()");return;}checkAdmin();}
 private void sendOrders(QuerySnapshot snap){try{JSONArray out=new JSONArray();for(DocumentSnapshot d:snap.getDocuments()){JSONObject o=new JSONObject();o.put("id",d.getId());o.put("name",d.getString("customerName"));o.put("mobile",d.getString("mobile"));o.put("address",d.getString("address"));o.put("payment",d.getString("paymentMethod"));o.put("subtotal",num(d.get("subtotal")));o.put("delivery",num(d.get("deliveryFee")));o.put("discount",num(d.get("discount")));o.put("total",num(d.get("total")));o.put("status",d.getString("status"));o.put("date",dateText(d.get("createdAt")));JSONArray items=new JSONArray();Object im=d.get("items");if(im instanceof Map){for(Object v:((Map<?,?>)im).values()){if(v instanceof Map){Map<?,?> m=(Map<?,?>)v;JSONObject it=new JSONObject();it.put("name",String.valueOf(m.get("name")));it.put("qty",num(m.get("qty")));items.put(it);}}}o.put("items",items);out.put(o);}js("window.ordersResult("+JSONObject.quote(out.toString())+")");}catch(Exception e){message("Order data error: "+e.getMessage());}}
 private String dateText(Object x){if(x instanceof com.google.firebase.Timestamp)return ((com.google.firebase.Timestamp)x).toDate().toString();return x==null?"":String.valueOf(x);}
 private long num(Object x){if(x instanceof Number)return ((Number)x).longValue();try{return Long.parseLong(String.valueOf(x));}catch(Exception e){return 0;}}
 private boolean isAdmin(Runnable yes){if(auth==null||auth.getCurrentUser()==null){message("Admin login required.");return false;}if(!isConfiguredAdmin()){deny(auth.getCurrentUser().getUid());return false;}yes.run();return true;}
 private void updateStatus(String id,String st){isAdmin(()->db.collection("orders").document(id).update("status",st).addOnSuccessListener(v->message("Order "+id+" → "+st)).addOnFailureListener(e->message("Status update failed: "+e.getMessage())));}
 private void reject(String id){updateStatus(id,"REJECTED");}
 private void call(String n){try{startActivity(new Intent(Intent.ACTION_DIAL,Uri.parse("tel:"+n)));}catch(Exception e){message("Could not open phone dialer.");}}
 private void whatsapp(String n){try{String x=n.replaceAll("[^0-9]","");if(x.length()==10)x="91"+x;startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://wa.me/"+x)));}catch(Exception e){message("Could not open WhatsApp.");}}
 private void nav(String a){try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://www.google.com/maps/dir/?api=1&destination="+Uri.encode(a)+"&travelmode=driving")));}catch(Exception e){message("Could not open Maps.");}}
 public class Bridge{@JavascriptInterface public void login(String e,String p){auth.signInWithEmailAndPassword(e,p).addOnSuccessListener(x->checkAdmin()).addOnFailureListener(x->js("window.loginError("+JSONObject.quote("Login failed: "+x.getMessage())+")"));}@JavascriptInterface public void refresh(){runOnUiThread(()->refresh());}@JavascriptInterface public void updateStatus(String id,String st){runOnUiThread(()->updateStatus(id,st));}@JavascriptInterface public void reject(String id){runOnUiThread(()->reject(id));}@JavascriptInterface public void logout(){runOnUiThread(()->{if(ordersListener!=null)ordersListener.remove();auth.signOut();js("window.showLogin()");});}@JavascriptInterface public void navigate(String ad){runOnUiThread(()->nav(ad));}@JavascriptInterface public void call(String n){runOnUiThread(()->call(n));}@JavascriptInterface public void whatsapp(String n){runOnUiThread(()->whatsapp(n));}}
 @Override public void onBackPressed(){if(w!=null&&w.canGoBack())w.goBack();else super.onBackPressed();}
 @Override protected void onDestroy(){if(ordersListener!=null)ordersListener.remove();super.onDestroy();}
}
