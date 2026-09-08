package com.samosaking.nawalgarh;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.ListenerRegistration;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {

    private static final int LOCATION_REQUEST = 1001;
    private static final int DELIVERY_FEE = 30;
    private static final String PREFS = "samosa_king";
    private static final String LAST_ORDER = "last_order_id";

    private FirebaseAuth auth;
    private FirebaseFirestore db;
    private FusedLocationProviderClient fusedLocation;
    private WebView webView;
    private SharedPreferences prefs;
    private ListenerRegistration orderListener;

    private String pendingName;
    private String pendingMobile;
    private String pendingAddress;
    private String pendingItemsJson;
    private int pendingSubtotal;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();
        fusedLocation = LocationServices.getFusedLocationProviderClient(this);
        prefs = getSharedPreferences(PREFS, MODE_PRIVATE);

        setupWebView();

        if (auth.getCurrentUser() == null) {
            auth.signInAnonymously().addOnCompleteListener(task -> {
                if (task.isSuccessful()) {
                    webView.loadUrl("file:///android_asset/index.html");
                } else {
                    webView.evaluateJavascript("orderError('Firebase connection failed')", null);
                }
            });
        } else {
            webView.loadUrl("file:///android_asset/index.html");
        }
    }

    private void setupWebView() {
        webView = new WebView(this);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        webView.addJavascriptInterface(new AndroidBridge(), "AndroidBridge");
        setContentView(webView);
    }

    public class AndroidBridge {
        @JavascriptInterface
        public void placeOrder(String name, String mobile, String address, String itemsJson, int subtotal) {
            runOnUiThread(() -> {
                if (auth.getCurrentUser() == null) {
                    webView.evaluateJavascript("orderError('Firebase connection is not ready')", null);
                    return;
                }

                if (subtotal < 100) {
                    webView.evaluateJavascript("orderError('Minimum order ₹100 hai')", null);
                    return;
                }

                pendingName = name;
                pendingMobile = mobile;
                pendingAddress = address;
                pendingItemsJson = itemsJson;
                pendingSubtotal = subtotal;

                if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
                        && checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                    }, LOCATION_REQUEST);
                } else {
                    savePendingOrder();
                }
            });
        }

        @JavascriptInterface
        public void loadLastOrder() {
            runOnUiThread(() -> {
                String orderId = prefs.getString(LAST_ORDER, "");
                if (orderId == null || orderId.isEmpty()) {
                    webView.evaluateJavascript("statusUpdate('NO ORDER')", null);
                    return;
                }
                listenToOrder(orderId);
            });
        }

        @JavascriptInterface
        public void cancelLastOrder() {
            runOnUiThread(() -> {
                String orderId = prefs.getString(LAST_ORDER, "");
                if (orderId == null || orderId.isEmpty()) return;

                db.collection("orders").document(orderId).get()
                        .addOnSuccessListener(doc -> {
                            if (!doc.exists()) return;
                            String status = doc.getString("status");
                            if (!"PLACED".equals(status)) {
                                webView.evaluateJavascript("orderError('Order ab cancel nahi ho sakta')", null);
                                return;
                            }
                            db.collection("orders").document(orderId)
                                    .update("status", "CANCELLED")
                                    .addOnSuccessListener(v -> webView.evaluateJavascript("statusUpdate('CANCELLED')", null))
                                    .addOnFailureListener(e -> webView.evaluateJavascript("orderError('Cancel failed')", null));
                        })
                        .addOnFailureListener(e -> webView.evaluateJavascript("orderError('Order load failed')", null));
            });
        }
    }

    private void savePendingOrder() {
        if (pendingName == null) return;

        int total = pendingSubtotal + DELIVERY_FEE;
        Map<String, Object> items = new HashMap<>();

        try {
            JSONArray array = new JSONArray(pendingItemsJson);
            for (int i = 0; i < array.length(); i++) {
                JSONObject item = array.getJSONObject(i);
                String id = item.getString("id");
                int qty = item.getInt("qty");
                items.put(id, qty);
            }
        } catch (Exception e) {
            webView.evaluateJavascript("orderError('Invalid cart data')", null);
            return;
        }

        Map<String, Object> order = new HashMap<>();
        order.put("userId", auth.getCurrentUser().getUid());
        order.put("customerName", pendingName);
        order.put("mobile", pendingMobile);
        order.put("address", pendingAddress);
        order.put("items", items);
        order.put("subtotal", pendingSubtotal);
        order.put("deliveryFee", DELIVERY_FEE);
        order.put("total", total);
        order.put("paymentMethod", "COD");
        order.put("status", "PLACED");
        order.put("createdAt", FieldValue.serverTimestamp());

        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
                || checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            fusedLocation.getLastLocation().addOnSuccessListener(location -> {
                if (location != null) {
                    order.put("latitude", location.getLatitude());
                    order.put("longitude", location.getLongitude());
                }
                writeOrder(order);
            }).addOnFailureListener(e -> writeOrder(order));
        } else {
            writeOrder(order);
        }
    }

    private void writeOrder(Map<String, Object> order) {
        db.collection("orders").add(order)
                .addOnSuccessListener(ref -> {
                    prefs.edit().putString(LAST_ORDER, ref.getId()).apply();
                    webView.evaluateJavascript("orderCreated('" + ref.getId() + "')", null);
                    listenToOrder(ref.getId());
                    pendingName = null;
                    pendingMobile = null;
                    pendingAddress = null;
                    pendingItemsJson = null;
                })
                .addOnFailureListener(e -> webView.evaluateJavascript(
                        "orderError(" + JSONObject.quote("Order save failed: " + e.getMessage()) + ")", null));
    }

    private void listenToOrder(String orderId) {
        if (orderListener != null) orderListener.remove();
        orderListener = db.collection("orders").document(orderId)
                .addSnapshotListener((snapshot, error) -> {
                    if (error != null || snapshot == null || !snapshot.exists()) return;
                    String status = snapshot.getString("status");
                    if (status == null) status = "PLACED";
                    String js = "statusUpdate(" + JSONObject.quote(status) + ")";
                    webView.evaluateJavascript(js, null);
                });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == LOCATION_REQUEST) {
            savePendingOrder();
        }
    }

    @Override
    protected void onDestroy() {
        if (orderListener != null) orderListener.remove();
        if (webView != null) webView.destroy();
        super.onDestroy();
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}

