package com.samosaking.admin;

import android.app.*;import android.content.*;import android.net.Uri;import android.os.*;import android.webkit.*;import android.print.PrintAttributes;import android.print.PrintManager;import android.graphics.Color;import android.widget.TextView;import com.google.firebase.FirebaseApp;import com.google.firebase.FirebaseOptions;import com.google.firebase.auth.FirebaseAuth;import com.google.firebase.firestore.*;import org.json.*;import java.util.*;

public class AdminActivity extends Activity{
 private WebView w; private WebView printView; private FirebaseAuth auth; private FirebaseFirestore db; private ListenerRegistration ordersListener;
 private static final String PROJECT="samosa-king-3b90d"; private static final String APP_ID="1:855148039257:android:535730f98ea24e77253548"; private static final String API_KEY="AIzaSyCusjrBM2M59Obiwv-Dgy1m6PgiYDQtwQw";
 private static final String ADMIN_UID="vJCq3yQDe0QcCg5EoEPnjVKwUgJ2";
 @Override public void onCreate(Bundle b){super.onCreate(b);try{
   FirebaseOptions o=new FirebaseOptions.Builder().setProjectId(PROJECT).setApplicationId(APP_ID).setApiKey(API_KEY).build();
   if(FirebaseApp.getApps(this).isEmpty()){FirebaseApp.initializeApp(this,o);} FirebaseApp app=FirebaseApp.getInstance(); auth=FirebaseAuth.getInstance(app); db=FirebaseFirestore.getInstance(app);
   w=new WebView(this);w.setBackgroundColor(Color.WHITE);WebSettings s=w.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setAllowFileAccess(true);s.setAllowContentAccess(true);
   w.setWebChromeClient(new WebChromeClient(){@Override public boolean onConsoleMessage(ConsoleMessage m){android.util.Log.e("SAMOSA_ADMIN_JS",""+m.message()+" @ line "+m.lineNumber());return true;}});w.setWebViewClient(new WebViewClient(){@Override public void onPageFinished(WebView v,String u){if(auth.getCurrentUser()!=null)checkAdmin();else v.evaluateJavascript("window.showLogin()",null);}@Override public void onReceivedError(WebView v,int code,String desc,String url){showRuntimeError("WebView error "+code+": "+desc+"\n"+url);} @Override public boolean shouldOverrideUrlLoading(WebView v,String u){try{if(u.startsWith("samosa://admin/")){handleAdminUrl(u);return true;}if(u.startsWith("tel:")||u.startsWith("https://wa.me/")){startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(u)));return true;}}catch(Exception e){message("Action failed: "+e.getMessage());}return false;}});
   w.addJavascriptInterface(new Bridge(),"AdminNative");setContentView(w);w.loadUrl("file:///android_asset/admin.html");
 }catch(Throwable e){fatal(e);}}
 private void handleAdminUrl(String u){
  try{
    Uri x=Uri.parse(u);
    String action=x.getPath();
    if(action!=null&&action.startsWith("/"))action=action.substring(1);
    String id=x.getQueryParameter("id");
    String value=x.getQueryParameter("value");
    if(action==null||action.isEmpty()){message("Invalid admin action.");return;}
    if("refresh".equals(action)){refresh();return;}
    if("logout".equals(action)){if(ordersListener!=null)ordersListener.remove();auth.signOut();js("window.showLogin()");return;}
    if("payment".equals(action)){ if(id==null||id.trim().isEmpty()){message("Invalid payment action data.");return;} updatePaymentStatus(id,value);return;}
    if("status".equals(action)){
      if(id==null||id.trim().isEmpty()||value==null||value.trim().isEmpty()){message("Invalid status action data.");return;}
      updateStatus(id,value);return;
    }
    if("reject".equals(action)){reject(id);return;}
    if("call".equals(action)){call(value);return;}
    if("whatsapp".equals(action)){whatsapp(value);return;}
    if("navigate".equals(action)){nav(value);return;}
    if("print".equals(action)){printBill(id);return;}
    message("Unknown admin action: "+action);
  }catch(Exception e){message("Action error: "+e.getClass().getSimpleName()+" — "+e.getMessage());}
 }
 private void showRuntimeError(String x){js("window.nativeError&&window.nativeError("+JSONObject.quote(x)+")");}
 private void fatal(Throwable e){TextView t=new TextView(this);t.setText("Samosa King ADMIN\n\nStartup error: "+e.getClass().getSimpleName()+"\n"+String.valueOf(e.getMessage()));t.setTextSize(17);t.setTextColor(Color.DKGRAY);t.setPadding(40,80,40,40);setContentView(t);}
 private void js(String code){runOnUiThread(()->{if(w!=null)w.evaluateJavascript("(function(){try{"+code+"}catch(e){}})()",null);});}
 private void message(String x){js("window.adminError("+JSONObject.quote(x)+")");}
 private boolean isConfiguredAdmin(){return auth!=null&&auth.getCurrentUser()!=null&&ADMIN_UID.equals(auth.getCurrentUser().getUid());}
 private void deny(String uid){auth.signOut();js("window.showLogin();window.loginError("+JSONObject.quote("This account is not authorized as admin. UID: "+uid)+")");}
 private void checkAdmin(){if(auth==null||auth.getCurrentUser()==null){js("window.showLogin()");return;}String uid=auth.getCurrentUser().getUid();if(isConfiguredAdmin()){js("window.showDashboard("+JSONObject.quote("Admin")+")");listenOrders();}else{deny(uid);}}
 private void listenOrders(){if(db==null){message("Firestore is not initialized.");return;}if(ordersListener!=null)ordersListener.remove();ordersListener=db.collection("orders").addSnapshotListener((snap,e)->{if(e!=null){message("Could not load live orders: "+e.getClass().getSimpleName()+" — "+e.getMessage());return;}sendOrders(snap);});}
 private void refresh(){if(auth==null){message("Firebase is not initialized.");return;}if(auth.getCurrentUser()==null){js("window.showLogin()");return;}checkAdmin();}
 private String itemName(String id){
  if(id==null)return "Item";
  String x=id.trim().toLowerCase(Locale.US);
  if(x.equals("samosa"))return "Samosa";
  if(x.equals("kachori"))return "Kachori";
  if(x.equals("mirchi")||x.equals("mirchibada")||x.equals("mirchi-bada"))return "Mirchi Bada";
  if(x.equals("dahi1")||x.equals("dahibhalla1"))return "Dahi Bhalla Plate 1";
  if(x.equals("dahi2")||x.equals("dahibhalla2"))return "Dahi Bhalla Plate 2";
  if(x.equals("cholebhature"))return "Chole Bhature";
  if(x.equals("indianthali"))return "Indian Thali";
  if(x.equals("pizza")||x.equals("margherita"))return "Margherita Pizza";
  if(x.equals("cheesepizza"))return "Cheese Pizza";
  if(x.equals("corncheesepizza")||x.equals("cornpizza"))return "Corn Cheese Pizza";
  if(x.equals("paneerpizza"))return "Paneer Pizza";
  if(x.equals("farmhousepizza"))return "Farmhouse Pizza";
  if(x.equals("vegloadedpizza"))return "Veg Loaded Pizza";
  if(x.equals("doublecheesepizza"))return "Double Cheese Pizza";
  if(x.equals("peppypaneerpizza"))return "Peppy Paneer Pizza";
  if(x.equals("wraps")||x.equals("wrap"))return "Wraps";
  if(x.equals("momos"))return "Momos";
  if(x.equals("burger"))return "Burger";
  if(x.equals("pasta"))return "Pasta";
  if(x.equals("manchurian"))return "Manchurian";
  if(x.equals("maggi"))return "Maggi";
  if(x.equals("cholekulcha"))return "Chole Kulcha";
  if(x.equals("sandwich"))return "Sandwich";
  if(x.equals("popcorn"))return "Popcorn";
  if(x.equals("dhokla"))return "Dhokla";
  if(x.equals("idly"))return "Idly";
  if(x.equals("vadapav"))return "Vada Pav";
  if(x.equals("dosa"))return "Dosa";
  if(x.equals("birthdaycake")||x.equals("bdaycake"))return "Birthday Cake";
  if(x.equals("balloons"))return "Balloons";
  if(x.equals("birthdaycandles")||x.equals("bdaycandles"))return "Birthday Candles";
  if(x.equals("happybirthdaybanner")||x.equals("bdaybanner"))return "Happy Birthday Banner";
  if(x.equals("partyhats"))return "Party Hats";
  if(x.equals("returngifts"))return "Return Gifts";
  if(x.equals("birthdaydecoration")||x.equals("birthdaydecor"))return "Birthday Decoration";
  if(x.equals("birthdayribbons"))return "Birthday Ribbons";
  if(x.equals("cakecuttingknife")||x.equals("cakeknife"))return "Cake cutting knife";
  if(x.equals("cupcakes"))return "Cupcakes";
  if(x.equals("caketopper"))return "Cake Topper";
  if(x.equals("birthdaygiftpack"))return "Birthday Gift Pack";
  if(x.equals("colddrink200")||x.equals("cold200"))return "Cold Drink 200 ml";
  if(x.equals("colddrink500")||x.equals("cold500"))return "Cold Drink 500 ml";
  if(x.equals("colddrink1l")||x.equals("cold1l"))return "Cold Drink 1 Litre";
  if(x.equals("colddrink2l")||x.equals("cold2l"))return "Cold Drink 2 Litre";
  if(x.equals("waterbottle")||x.equals("water"))return "Water Bottle";
  if(x.equals("mangojuice"))return "Mango Juice";
  if(x.equals("orangejuice"))return "Orange Juice";
  if(x.equals("lemonsoda"))return "Lemon Soda";
  if(x.equals("freshlemonwater")||x.equals("lemonwater"))return "Fresh Lemon Water";
  if(x.equals("mangoshake"))return "Mango Shake";
  if(x.equals("bananashake"))return "Banana Shake";
  if(x.equals("papayashake"))return "Papaya Shake";
  if(x.equals("aloopyaz"))return "Aloo Pyaz Sabzi";
  if(x.equals("aloogobi"))return "Aloo Gobi";
  if(x.equals("aloomatar"))return "Aloo Matar";
  if(x.equals("aloomethi"))return "Aloo Methi";
  if(x.equals("palakpaneer"))return "Palak Paneer";
  if(x.equals("matarpaneer"))return "Matar Paneer";
  if(x.equals("shahipaneer"))return "Shahi Paneer";
  if(x.equals("kadaipaneer"))return "Kadai Paneer";
  if(x.equals("paneerbutter"))return "Paneer Butter Masala";
  if(x.equals("gatte"))return "Gatte Ki Sabzi";
  if(x.equals("sevtamatar"))return "Sev Tamatar";
  if(x.equals("bhindi"))return "Bhindi Masala";
  if(x.equals("baingan"))return "Baingan Masala";
  if(x.equals("chanamasala"))return "Chana Masala";
  if(x.equals("rajma"))return "Rajma Masala";
  if(x.equals("dumalo"))return "Dum Aloo";
  if(x.equals("mixveg"))return "Mix Veg";
  if(x.equals("daltadka"))return "Dal Tadka";
  if(x.equals("dalfry"))return "Dal Fry";
  if(x.equals("rajasthanikadhi"))return "Rajasthani Kadhi";
  if(x.equals("kersangri"))return "Ker Sangri";
  if(x.equals("papadsabzi"))return "Papad Ki Sabzi";
  if(x.equals("kajukatli")||x.equals("kaju-katli"))return "Kaju Katli";
  if(x.equals("rasgulla"))return "Rasgulla";
  if(x.equals("rajbhog"))return "Rajbhog";
  if(x.equals("gulabjamun")||x.equals("gulab-jamun"))return "Gulab Jamun";
  if(x.equals("sohanpapdi")||x.equals("sohan-papdi"))return "Sohan Papdi";
  if(x.equals("milkcake")||x.equals("milk-cake"))return "Milk Cake";
  if(x.equals("kalakand"))return "Kalakand";
  if(x.equals("dilkushal"))return "Dilkushal";
  if(x.equals("peda"))return "Peda";
  if(x.equals("petha"))return "Petha";
  if(x.equals("namkin"))return "Namkin";
  if(x.equals("rasmalai"))return "Rasmalai";
  if(x.equals("curd")||x.equals("dahi"))return "Dahi (Curd)";
  return id;
 }
 private void sendOrders(QuerySnapshot snap){
  try{
   JSONArray out=new JSONArray();
   for(DocumentSnapshot d:snap.getDocuments()){
    JSONObject o=new JSONObject();
    o.put("id",d.getId());o.put("name",d.getString("customerName"));o.put("mobile",d.getString("mobile"));
    o.put("address",d.getString("address"));o.put("payment",d.getString("paymentMethod"));o.put("paymentStatus",d.getString("paymentStatus"));
    o.put("subtotal",num(d.get("subtotal")));o.put("delivery",num(d.get("deliveryFee")));o.put("discount",num(d.get("discount")));
    o.put("total",num(d.get("total")));o.put("status",d.getString("status"));o.put("date",dateText(d.get("createdAt")));
    if(d.get("createdAt") instanceof com.google.firebase.Timestamp)o.put("createdAtMs",((com.google.firebase.Timestamp)d.get("createdAt")).toDate().getTime());
    JSONArray items=new JSONArray();
    Object im=d.get("items");
    if(im instanceof Map){
     for(Map.Entry<?,?> entry:((Map<?,?>)im).entrySet()){
      String key=String.valueOf(entry.getKey());
      Object v=entry.getValue();
      JSONObject it=new JSONObject();
      if(v instanceof Map){
       Map<?,?> m=(Map<?,?>)v;
       Object n=m.get("name");
       String name=n==null||"null".equals(String.valueOf(n))?itemName(key):String.valueOf(n);
       it.put("name",name);it.put("qty",num(m.get("qty")));
      }else{
       it.put("name",itemName(key));it.put("qty",num(v));
      }
      items.put(it);
     }
    }
    o.put("items",items);out.put(o);
   }
   js("window.ordersResult("+JSONObject.quote(out.toString())+")");
  }catch(Exception e){message("Order data error: "+e.getMessage());}
 }
 private String dateText(Object x){if(x instanceof com.google.firebase.Timestamp)return ((com.google.firebase.Timestamp)x).toDate().toString();return x==null?"":String.valueOf(x);}
 private long num(Object x){if(x instanceof Number)return ((Number)x).longValue();try{return Long.parseLong(String.valueOf(x));}catch(Exception e){return 0;}}
 private boolean isAdmin(Runnable yes){if(auth==null||auth.getCurrentUser()==null){message("Admin login required.");return false;}if(!isConfiguredAdmin()){deny(auth.getCurrentUser().getUid());return false;}yes.run();return true;}
 private void updateStatus(String id,String st){if(id==null||id.trim().isEmpty()){message("Invalid order ID.");return;}if(st==null||st.trim().isEmpty()){message("Invalid status.");return;}message("Updating order "+id+" → "+st+" …");isAdmin(()->db.collection("orders").document(id).update("status",st).addOnSuccessListener(v->{js("window.statusDone("+JSONObject.quote(id)+","+JSONObject.quote(st)+")");message("✓ Order "+id+" → "+st);}).addOnFailureListener(e->message("✗ Status update failed: "+e.getClass().getSimpleName()+" — "+e.getMessage())));}
 private void updatePaymentStatus(String id,String st){if(id==null||id.trim().isEmpty()){message("Invalid order ID.");return;}if(!"PAID".equals(st)){message("Invalid payment status.");return;}message("Payment status update ho raha hai…");isAdmin(()->db.collection("orders").document(id).update("paymentStatus","PAID","paymentVerifiedAt",FieldValue.serverTimestamp()).addOnSuccessListener(v->{message("✓ Payment received marked for order "+id);}).addOnFailureListener(e->message("✗ Payment status update failed: "+e.getClass().getSimpleName()+" — "+e.getMessage())));}
 private void reject(String id){updateStatus(id,"REJECTED");}
 private void call(String n){try{startActivity(new Intent(Intent.ACTION_DIAL,Uri.parse("tel:"+n)));}catch(Exception e){message("Could not open phone dialer.");}}
 private void whatsapp(String n){try{String x=n.replaceAll("[^0-9]","");if(x.length()==10)x="91"+x;startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://wa.me/"+x)));}catch(Exception e){message("Could not open WhatsApp.");}}
 private void nav(String a){try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://www.google.com/maps/dir/?api=1&destination="+Uri.encode(a)+"&travelmode=driving")));}catch(Exception e){message("Could not open Maps.");}}
 private void loadMenuPrices(){if(!isAdmin(()->{}))return;final String[] ids={"samosa","kachori","mirchi","dahi1","dahi2","cholebhature","margherita","cheesepizza","cornpizza","paneerpizza","farmhousepizza","vegloadedpizza","doublecheesepizza","peppypaneerpizza","wraps","momos","burger","pasta","manchurian","maggi","cholekulcha","sandwich","popcorn","dhokla","idly","vadapav","dosa","bdaycake","balloons","bdaycandles","bdaybanner","partyhats","returngifts","birthdaydecor","birthdayribbons","cakeknife","cupcakes","caketopper","birthdaygiftpack","cold200","cold500","cold1l","cold2l","water","mangojuice","orangejuice","lemonsoda","lemonwater","mangoshake","bananashake","papayashake","kajukatli","rasgulla","rajbhog","gulabjamun","sohanpapdi","milkcake","kalakand","dilkushal","peda","petha","namkin","rasmalai","curd","besanladdu","boondiladoo","indianthali","aloopyaz","aloogobi","aloomatar","aloomethi","palakpaneer","matarpaneer","shahipaneer","kadaipaneer","paneerbutter","gatte","sevtamatar","bhindi","baingan","chanamasala","rajma","dumalo","mixveg","daltadka","dalfry","rajasthanikadhi","kersangri","papadsabzi"};final long[] prices={20,30,30,40,80,80,100,120,120,140,150,160,150,160,100,60,50,60,100,50,60,60,40,50,50,40,80,350,80,10,100,50,300,400,20,0,30,50,300,20,40,60,90,20,40,40,40,30,80,70,80,600,12,20,15,150,500,500,500,500,250,300,80,80,200,400,150,120,120,110,110,150,150,170,170,170,150,130,120,120,130,140,150,140,100,100,120,160,120};db.collection("menu").get().addOnSuccessListener(s->{try{Map<String,DocumentSnapshot> saved=new HashMap<>();for(DocumentSnapshot d:s)saved.put(d.getId(),d);JSONArray a=new JSONArray();for(int i=0;i<ids.length;i++){DocumentSnapshot d=saved.get(ids[i]);JSONObject o=new JSONObject();o.put("id",ids[i]);o.put("name",d!=null&&d.getString("name")!=null?d.getString("name"):itemName(ids[i]));o.put("price",d!=null&&d.get("price")!=null?num(d.get("price")):prices[i]);boolean enabled=true; if(d!=null){ try{ Boolean ev=d.getBoolean("enabled"); enabled=ev==null||ev.booleanValue(); }catch(Exception ignored){ enabled=true; } } o.put("enabled",enabled);a.put(o);}js("window.menuResult("+JSONObject.quote(a.toString())+")");}catch(Exception e){message("Menu data error: "+e.getMessage());}}).addOnFailureListener(e->message("Could not load menu: "+e.getMessage()));}
 private void saveMenuPrice(String id,String price){if(id==null||id.trim().isEmpty()){message("Invalid item.");return;}long p;try{p=Long.parseLong(price.trim());}catch(Exception e){message("Invalid price.");return;}if(p<0){message("Price cannot be negative.");return;}if(!isAdmin(()->{}))return;Map<String,Object> m=new HashMap<>();m.put("price",p);db.collection("menu").document(id).set(m,SetOptions.merge()).addOnSuccessListener(v->{message("✓ Price updated for "+itemName(id)+" → ₹"+p);loadMenuPrices();}).addOnFailureListener(e->message("✗ Price update failed: "+e.getMessage()));}
 private void saveMenuAvailability(String id,boolean enabled){if(id==null||id.trim().isEmpty()){message("Invalid item.");return;}if(!isAdmin(()->{}))return;db.collection("menu").document(id).set(Collections.<String,Object>singletonMap("enabled",enabled),SetOptions.merge()).addOnSuccessListener(v->{message("✓ "+itemName(id)+(enabled?" available":"sold out"));loadMenuPrices();}).addOnFailureListener(e->message("✗ Availability update failed: "+e.getMessage()));}
 private String htmlEsc(String x){if(x==null)return "";return x.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\"","&quot;").replace("'","&#39;");}
 private void printBill(String id){
  if(id==null||id.trim().isEmpty()){message("Invalid order ID.");return;}
  isAdmin(()->db.collection("orders").document(id).get().addOnSuccessListener(d->{
   if(!d.exists()){message("Order not found: "+id);return;}
   try{
    StringBuilder h=new StringBuilder();
    h.append("<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>");
    h.append("body{font-family:Arial,sans-serif;color:#111;margin:0;padding:24px;font-size:14px}.bill{max-width:700px;margin:auto}");
    h.append("h1{text-align:center;margin:0 0 4px;font-size:26px}.sub{text-align:center;color:#555;margin-bottom:18px}");
    h.append(".line{border-top:1px solid #222;margin:12px 0}.row{display:flex;justify-content:space-between;padding:5px 0}");
    h.append(".items{margin:10px 0}.total{font-size:20px;font-weight:800;border-top:2px solid #111;margin-top:10px;padding-top:10px}");
    h.append(".small{font-size:12px;color:#555}@media print{body{padding:0}.bill{max-width:none}}</style></head><body><div class='bill'>");
    h.append("<h1>SAMOSA KING</h1><div class='sub'>Nawalgarh • Nansa Gate<br>Bill / Order Receipt</div>");
    h.append("<div><b>Order #").append(htmlEsc(d.getId())).append("</b><br>");
    h.append("Customer: ").append(htmlEsc(d.getString("customerName"))).append("<br>");
    h.append("Mobile: ").append(htmlEsc(d.getString("mobile"))).append("<br>");
    h.append("Address: ").append(htmlEsc(d.getString("address"))).append("<br>");
    h.append("Payment: ").append(htmlEsc(d.getString("paymentMethod"))).append("<br>");
    h.append("Date: ").append(htmlEsc(dateText(d.get("createdAt")))).append("</div><div class='line'></div>");
    h.append("<div class='items'><b>ITEMS</b>");
    Object im=d.get("items");
    if(im instanceof Map){
      for(Map.Entry<?,?> entry:((Map<?,?>)im).entrySet()){
        String key=String.valueOf(entry.getKey()); Object v=entry.getValue(); String name=itemName(key); long qty=0;
        if(v instanceof Map){Map<?,?> m=(Map<?,?>)v;Object n=m.get("name");if(n!=null&&!String.valueOf(n).equals("null"))name=String.valueOf(n);qty=num(m.get("qty"));}else qty=num(v);
        h.append("<div class='row'><span>").append(htmlEsc(name)).append(" × ").append(qty).append("</span></div>");
      }
    }
    h.append("</div><div class='line'>");
    h.append("</div><div class='row'><span>Subtotal</span><span>₹").append(num(d.get("subtotal"))).append("</span></div>");
    h.append("<div class='row'><span>Delivery</span><span>₹").append(num(d.get("deliveryFee"))).append("</span></div>");
    h.append("<div class='row'><span>Discount</span><span>− ₹").append(num(d.get("discount"))).append("</span></div>");
    h.append("<div class='row total'><span>TOTAL</span><span>₹").append(num(d.get("total"))).append("</span></div>");
    h.append("<div class='line'></div><div class='small'>Thank you for ordering from Samosa King – Nawalgarh.</div></div></body></html>");
    String title="Samosa King Bill "+d.getId();
    runOnUiThread(()->{
      try{
        if(printView!=null){printView.destroy();printView=null;}
        printView=new WebView(this);
        printView.getSettings().setJavaScriptEnabled(false);
        printView.setWebViewClient(new WebViewClient(){
          @Override public void onPageFinished(WebView v,String url){
            try{
              PrintManager pm=(PrintManager)getSystemService(PRINT_SERVICE);
              PrintAttributes attrs=new PrintAttributes.Builder().setMediaSize(PrintAttributes.MediaSize.ISO_A4).setMinMargins(PrintAttributes.Margins.NO_MARGINS).build();
              pm.print(title,v.createPrintDocumentAdapter(title),attrs);
            }catch(Exception e){message("Print failed: "+e.getMessage());}
          }
        });
        printView.loadDataWithBaseURL(null,h.toString(),"text/html","UTF-8",null);
      }catch(Exception e){message("Could not prepare bill: "+e.getMessage());}
    });
   }catch(Exception e){message("Bill error: "+e.getMessage());}
  }).addOnFailureListener(e->message("Could not load order for printing: "+e.getClass().getSimpleName()+" — "+e.getMessage())));
 }
 public class Bridge{@JavascriptInterface public boolean ready(){return auth!=null&&db!=null;}@JavascriptInterface public void login(String e,String p){auth.signInWithEmailAndPassword(e,p).addOnSuccessListener(x->checkAdmin()).addOnFailureListener(x->js("window.loginError("+JSONObject.quote("Login failed: "+x.getMessage())+")"));}@JavascriptInterface public void refresh(){runOnUiThread(()->refresh());}@JavascriptInterface public void updateStatus(String id,String st){runOnUiThread(()->updateStatus(id,st));}@JavascriptInterface public void reject(String id){runOnUiThread(()->reject(id));}@JavascriptInterface public void logout(){runOnUiThread(()->{if(ordersListener!=null)ordersListener.remove();auth.signOut();js("window.showLogin()");});}@JavascriptInterface public void navigate(String ad){runOnUiThread(()->nav(ad));}@JavascriptInterface public void call(String n){runOnUiThread(()->call(n));}@JavascriptInterface public void whatsapp(String n){runOnUiThread(()->whatsapp(n));}@JavascriptInterface public void menuPrices(){runOnUiThread(()->loadMenuPrices());}@JavascriptInterface public void setMenuPrice(String id,String price){runOnUiThread(()->saveMenuPrice(id,price));}@JavascriptInterface public void setMenuAvailability(String id,boolean enabled){runOnUiThread(()->saveMenuAvailability(id,enabled));}}
 @Override public void onBackPressed(){if(w!=null&&w.canGoBack())w.goBack();else super.onBackPressed();}
 @Override protected void onDestroy(){if(ordersListener!=null)ordersListener.remove();if(printView!=null)printView.destroy();super.onDestroy();}
}
