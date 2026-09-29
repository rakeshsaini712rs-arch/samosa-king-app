package com.samosaking.delivery;

import android.app.*;
import android.os.*;
import android.content.*;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.view.*;
import android.widget.*;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.*;
import java.util.*;

public class DeliveryActivity extends Activity {
    private FirebaseAuth auth; private FirebaseFirestore db;
    private LinearLayout root,list; private EditText email,password; private ListenerRegistration listener;
    private static final String PROJECT="samosa-king-3b90d";
    private static final String APP_ID="1:855148039257:android:535730f98ea24e77253548";
    private static final String API_KEY="AIzaSyCusjrBM2M59Obiwv-Dgy1m6PgiYDQtwQw";

    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        FirebaseOptions o=new FirebaseOptions.Builder().setProjectId(PROJECT).setApplicationId(APP_ID).setApiKey(API_KEY).build();
        if(FirebaseApp.getApps(this).isEmpty()) FirebaseApp.initializeApp(this,o);
        FirebaseApp app=FirebaseApp.getInstance(); auth=FirebaseAuth.getInstance(app); db=FirebaseFirestore.getInstance(app); showLogin();
    }
    private TextView tv(String s,int n){TextView v=new TextView(this);v.setText(s);v.setTextSize(n);v.setTextColor(Color.rgb(40,30,24));v.setPadding(20,12,20,12);return v;}
    private Button btn(String s){Button b=new Button(this);b.setText(s);b.setAllCaps(false);return b;}
    private void showLogin(){
        root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(28,60,28,28);root.setBackgroundColor(Color.rgb(250,247,243));
        TextView t=tv("👑 SAMOSA KING",28);t.setTextColor(Color.rgb(145,83,0));root.addView(t);root.addView(tv("Delivery Partner Login",20));
        email=new EditText(this);email.setHint("Delivery boy email");email.setInputType(33);root.addView(email,new LinearLayout.LayoutParams(-1,-2));
        password=new EditText(this);password.setHint("Password");password.setInputType(129);root.addView(password,new LinearLayout.LayoutParams(-1,-2));
        Button login=btn("LOGIN");root.addView(login,new LinearLayout.LayoutParams(-1,-2));root.addView(tv("Only authorized delivery accounts can access assigned orders.",14));login.setOnClickListener(v->login());setContentView(root);
    }
    private void login(){String e=email.getText().toString().trim(),p=password.getText().toString();if(e.isEmpty()||p.isEmpty()){toast("Email and password required.");return;}auth.signInWithEmailAndPassword(e,p).addOnSuccessListener(r->loadDashboard()).addOnFailureListener(x->toast("Login failed: "+x.getMessage()));}
    private void loadDashboard(){
        if(auth.getCurrentUser()==null){showLogin();return;} root.removeAllViews();
        LinearLayout head=new LinearLayout(this);head.setGravity(Gravity.CENTER_VERTICAL);TextView t=tv("🚚 Delivery Dashboard",22);head.addView(t,new LinearLayout.LayoutParams(0,-2,1));Button lo=btn("Logout");head.addView(lo);root.addView(head);lo.setOnClickListener(v->{if(listener!=null)listener.remove();auth.signOut();showLogin();});
        root.addView(tv("My Assigned Orders",18));list=new LinearLayout(this);list.setOrientation(LinearLayout.VERTICAL);root.addView(list,new LinearLayout.LayoutParams(-1,-1));listenAssignedOrders();
    }
    private void listenAssignedOrders(){
        if(listener!=null)listener.remove();String email=auth.getCurrentUser().getEmail(); if(email==null)email=""; email=email.trim().toLowerCase(Locale.US);
        listener=db.collection("orders").whereEqualTo("deliveryBoyEmail",email).addSnapshotListener((snap,e)->{list.removeAllViews();if(e!=null){list.addView(tv("Could not load orders: "+e.getMessage(),15));return;}if(snap==null||snap.isEmpty()){list.addView(tv("No assigned deliveries right now.",16));return;}for(DocumentSnapshot d:snap.getDocuments())addOrder(d);});
    }
    private void addOrder(DocumentSnapshot d){
        LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(14,14,14,14);GradientDrawable bg=new GradientDrawable();bg.setColor(Color.WHITE);bg.setCornerRadius(18);card.setBackground(bg);
        card.addView(tv("📦 "+safe(d.getString("customerName"))+"  •  ₹"+money(d.get("total")),18));
        card.addView(tv("📍 "+safe(d.getString("address")),15));card.addView(tv("📞 "+safe(d.getString("mobile"))+"\nStatus: "+safe(d.getString("status")),14));
        LinearLayout actions=new LinearLayout(this);String status=safe(d.getString("status"));
        if("PLACED".equals(status)||"ACCEPTED".equals(status)||"PREPARING".equals(status))addAction(actions,d,"PICKED UP","OUT_FOR_DELIVERY");
        if("OUT_FOR_DELIVERY".equals(status))addAction(actions,d,"DELIVERED","DELIVERED");
        Button call=btn("📞 Call");actions.addView(call);call.setOnClickListener(v->{try{startActivity(new Intent(Intent.ACTION_DIAL,Uri.parse("tel:"+d.getString("mobile"))));}catch(Exception ignored){}});card.addView(actions);
        LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(-1,-2);cp.setMargins(0,8,0,8);list.addView(card,cp);
    }
    private void addAction(LinearLayout row,DocumentSnapshot d,String label,String value){Button b=btn(label);row.addView(b);b.setOnClickListener(v->db.collection("orders").document(d.getId()).update("status",value).addOnSuccessListener(x->toast("Status updated.")).addOnFailureListener(x->toast("Update failed: "+x.getMessage())));}
    private String safe(String s){return s==null?"":s;} private String money(Object x){try{return String.valueOf(Math.round(Double.parseDouble(String.valueOf(x))));}catch(Exception e){return "0";}} private void toast(String s){Toast.makeText(this,s,Toast.LENGTH_SHORT).show();}
}