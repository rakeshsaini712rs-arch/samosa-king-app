package com.samosaking.nawalgarh;

import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.*;
import org.json.*;
import java.util.*;

public class AdminBridge {
  private final MainActivity a; private final WebView w; private final FirebaseFirestore db; private final FirebaseAuth auth;
  AdminBridge(MainActivity a, WebView w){this.a=a;this.w=w;db=FirebaseFirestore.getInstance();auth=FirebaseAuth.getInstance();}
  private void js(String s){a.runOnUiThread(()->w.evaluateJavascript(s,null));}
  private boolean signed(){return auth.getCurrentUser()!=null;}
  private void admin(Runnable r){if(!signed()){js("window.adminError('Login required.');");return;} db.collection("admins").document(auth.getCurrentUser().getUid()).get().addOnSuccessListener(d->{if(!d.exists()){js("window.adminError('Admin access denied.');");return;}r.run();});}

  @JavascriptInterface public void loadDashboard(){admin(()->{
    db.collection("orders").get().addOnSuccessListener(s->{long sales=0;int placed=0;int delivered=0;long todaySales=0;Calendar c=Calendar.getInstance();c.set(Calendar.HOUR_OF_DAY,0);c.set(Calendar.MINUTE,0);c.set(Calendar.SECOND,0);c.set(Calendar.MILLISECOND,0);Date start=c.getTime();
      for(DocumentSnapshot d:s){Long t=d.getLong("total");String st=d.getString("status");Date dt=d.getDate("createdAt");if(t!=null&&"DELIVERED".equals(st)){sales+=t;delivered++;if(dt!=null&&dt.after(start))todaySales+=t;}if("PLACED".equals(st))placed++;}
      js("window.adminDashboard("+sales+","+todaySales+","+placed+","+delivered+","+s.size()+")");
    });
  });}

  @JavascriptInterface public void loadReviews(){admin(()->db.collection("reviews").get().addOnSuccessListener(s->{try{JSONArray out=new JSONArray();for(DocumentSnapshot d:s){JSONObject o=new JSONObject();o.put("id",d.getId());o.put("orderId",String.valueOf(d.get("orderId")));o.put("rating",d.getLong("rating")!=null?d.getLong("rating"):0);o.put("comment",String.valueOf(d.get("comment")));o.put("date",d.getDate("createdAt")!=null?d.getDate("createdAt").toString():"Recent");out.put(o);}js("window.adminReviewsResult("+JSONObject.quote(out.toString())+");");}catch(Exception e){js("window.adminError('Could not load reviews.');");}}));}

  @JavascriptInterface public void loadMenu(){admin(()->db.collection("menu").get().addOnSuccessListener(s->{try{JSONArray out=new JSONArray();for(DocumentSnapshot d:s){JSONObject o=new JSONObject();o.put("id",d.getId());o.put("name",String.valueOf(d.get("name")));o.put("price",d.getLong("price")!=null?d.getLong("price"):0);o.put("enabled",Boolean.TRUE.equals(d.getBoolean("enabled")));out.put(o);}js("window.adminMenuResult("+JSONObject.quote(out.toString())+");");}catch(Exception e){js("window.adminError('Could not load menu.');");}}));}

  @JavascriptInterface public void saveMenu(String id,String name,int price,boolean enabled){admin(()->{Map<String,Object>m=new HashMap<>();m.put("name",name);m.put("price",price);m.put("enabled",enabled);m.put("updatedAt",FieldValue.serverTimestamp());db.collection("menu").document(id).set(m,SetOptions.merge()).addOnSuccessListener(x->js("window.adminSaved('Menu updated.');"));});}
  @JavascriptInterface public void saveOffer(String id,String title,String type,int value,String code,boolean enabled){admin(()->{Map<String,Object>m=new HashMap<>();m.put("title",title);m.put("type",type);m.put("value",value);m.put("code",code.toUpperCase(Locale.US));m.put("enabled",enabled);m.put("updatedAt",FieldValue.serverTimestamp());db.collection("offers").document(id).set(m,SetOptions.merge()).addOnSuccessListener(x->js("window.adminSaved('Offer saved.');"));});}
  @JavascriptInterface public void saveCoupon(String code,String type,int value,int minOrder,boolean firstOnly,boolean enabled){admin(()->{String k=code.trim().toUpperCase(Locale.US);Map<String,Object>m=new HashMap<>();m.put("code",k);m.put("type",type);m.put("value",value);m.put("minOrder",minOrder);m.put("firstOnly",firstOnly);m.put("enabled",enabled);m.put("updatedAt",FieldValue.serverTimestamp());db.collection("coupons").document(k).set(m,SetOptions.merge()).addOnSuccessListener(x->js("window.adminSaved('Coupon saved.');"));});}

  @JavascriptInterface public void loadStoreData(){
    Map<String,Object> all=new HashMap<>();
    db.collection("menu").get().addOnSuccessListener(menu->{try{JSONArray m=new JSONArray();for(DocumentSnapshot d:menu){JSONObject o=new JSONObject();o.put("id",d.getId());o.put("name",String.valueOf(d.get("name")));o.put("price",d.getLong("price")!=null?d.getLong("price"):0);o.put("enabled",!Boolean.FALSE.equals(d.getBoolean("enabled")));m.put(o);}all.put("menu",m.toString());}catch(Exception e){all.put("menu","[]");}
      db.collection("offers").get().addOnSuccessListener(offers->{try{JSONArray o=new JSONArray();for(DocumentSnapshot d:offers)if(!Boolean.FALSE.equals(d.getBoolean("enabled"))){JSONObject x=new JSONObject();x.put("id",d.getId());x.put("title",String.valueOf(d.get("title")));x.put("type",String.valueOf(d.get("type")));x.put("value",d.getLong("value")!=null?d.getLong("value"):0);x.put("code",String.valueOf(d.get("code")));o.put(x);}all.put("offers",o.toString());}catch(Exception e){all.put("offers","[]");}js("window.storeDataResult("+JSONObject.quote("{\\"menu\\":"+JSONObject.quote(String.valueOf(all.get("menu")))+",\\"offers\\":"+JSONObject.quote(String.valueOf(all.get("offers")))+"}")+");");});
    });
  }
}
