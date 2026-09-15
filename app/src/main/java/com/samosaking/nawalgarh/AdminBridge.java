package com.samosaking.nawalgarh;

import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.*;
import java.util.*;

public class AdminBridge {
  private final MainActivity a; private final WebView w; private final FirebaseFirestore db; private final FirebaseAuth auth;
  AdminBridge(MainActivity a, WebView w){this.a=a;this.w=w;db=FirebaseFirestore.getInstance();auth=FirebaseAuth.getInstance();}
  private void js(String s){a.runOnUiThread(()->w.evaluateJavascript(s,null));}
  private boolean signed(){return auth.getCurrentUser()!=null;}
  private void admin(Runnable r){if(!signed()){js("window.adminError('Login required.');");return;} db.collection("admins").document(auth.getCurrentUser().getUid()).get().addOnSuccessListener(d->{if(!d.exists()){js("window.adminError('Admin access denied.');");return;}r.run();});}
  @JavascriptInterface public void loadDashboard(){admin(()->{db.collection("orders").get().addOnSuccessListener(s->{long sales=0;int placed=0;for(DocumentSnapshot d:s){Long t=d.getLong("total");if(t!=null&&"DELIVERED".equals(d.getString("status")))sales+=t;if("PLACED".equals(d.getString("status")))placed++;}js("window.adminDashboard("+sales+","+placed+","+s.size()+")");});});}
  @JavascriptInterface public void saveMenu(String id,String name,int price,boolean enabled){admin(()->{Map<String,Object>m=new HashMap<>();m.put("name",name);m.put("price",price);m.put("enabled",enabled);m.put("updatedAt",FieldValue.serverTimestamp());db.collection("menu").document(id).set(m,SetOptions.merge()).addOnSuccessListener(x->js("window.adminSaved('Menu updated.')"));});}
  @JavascriptInterface public void saveOffer(String id,String title,String type,int value,String code,boolean enabled){admin(()->{Map<String,Object>m=new HashMap<>();m.put("title",title);m.put("type",type);m.put("value",value);m.put("code",code.toUpperCase(Locale.US));m.put("enabled",enabled);m.put("updatedAt",FieldValue.serverTimestamp());db.collection("offers").document(id).set(m,SetOptions.merge()).addOnSuccessListener(x->js("window.adminSaved('Offer saved.')"));});}
  @JavascriptInterface public void saveCoupon(String code,String type,int value,int minOrder,boolean firstOnly,boolean enabled){admin(()->{Map<String,Object>m=new HashMap<>();m.put("code",code.toUpperCase(Locale.US));m.put("type",type);m.put("value",value);m.put("minOrder",minOrder);m.put("firstOnly",firstOnly);m.put("enabled",enabled);m.put("updatedAt",FieldValue.serverTimestamp());db.collection("coupons").document(code.toUpperCase(Locale.US)).set(m,SetOptions.merge()).addOnSuccessListener(x->js("window.adminSaved('Coupon saved.')"));});}
}
