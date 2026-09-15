package com.samosaking.nawalgarh;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.PhoneAuthCredential;
import com.google.firebase.auth.PhoneAuthOptions;
import com.google.firebase.auth.PhoneAuthProvider;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.ListenerRegistration;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {
    private WebView web;
    private FirebaseAuth auth;
    private FirebaseFirestore db;
    private ListenerRegistration statusListener;

    private String pendingName, pendingPhone, pendingAddress, pendingItems;
    private int pendingSubtotal;
    private boolean authInProgress = false;
    private boolean orderInProgress = false;
    private String verificationId;

    @Override
    public void onCreate(Bundle b) {
        super.onCreate(b);
        web = new WebView(this);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, String url) {
                try {
                    if (url.startsWith("tel:") || url.startsWith("https://wa.me/") || url.startsWith("whatsapp:")) {
                        startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
                        return true;
                    }
                } catch (Exception ignored) {}
                return false;
            }
        });
        web.addJavascriptInterface(new AndroidBridge(), "AndroidBridge");
        setContentView(web);

        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();

        auth.addAuthStateListener(firebaseAuth -> {
            if (firebaseAuth.getCurrentUser() != null) {
                authInProgress = false;
                runJs("window.authReady&&window.authReady();");
                if (pendingName != null && !orderInProgress) createOrder();
            }
        });

        if (auth.getCurrentUser() == null) signIn();
        web.loadUrl("file:///android_asset/index.html");
    }

    private void signIn() {
        if (authInProgress) return;
        authInProgress = true;
        auth.signInAnonymously()
                .addOnSuccessListener(r -> {
                    authInProgress = false;
                    runJs("window.authReady&&window.authReady();");
                    if (pendingName != null && !orderInProgress) createOrder();
                })
                .addOnFailureListener(e -> {
                    authInProgress = false;
                    runJs("window.orderError(" + JSONObject.quote("Firebase sign-in failed: " + e.getMessage()) + ");");
                });
    }

    private void sendOtp(String phone) {
        PhoneAuthOptions options = PhoneAuthOptions.newBuilder(auth)
                .setPhoneNumber(phone)
                .setTimeout(60L, java.util.concurrent.TimeUnit.SECONDS)
                .setActivity(this)
                .setCallbacks(new PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
                    @Override public void onVerificationCompleted(PhoneAuthCredential credential) {
                        auth.signInWithCredential(credential).addOnSuccessListener(r ->
                                runJs("window.otpVerified(" + JSONObject.quote(phone) + ");"))
                                .addOnFailureListener(e -> runJs("window.otpError(" + JSONObject.quote(e.getMessage()) + ");"));
                    }
                    @Override public void onVerificationFailed(com.google.firebase.FirebaseException e) {
                        runJs("window.otpError(" + JSONObject.quote(e.getMessage()) + ");");
                    }
                    @Override public void onCodeSent(String id, PhoneAuthProvider.ForceResendingToken token) {
                        verificationId = id;
                        runJs("window.otpSent();");
                    }
                }).build();
        PhoneAuthProvider.verifyPhoneNumber(options);
    }

    private void verifyOtp(String code) {
        if (verificationId == null) {
            runJs("window.otpError('Please request OTP first.');");
            return;
        }
        PhoneAuthCredential credential = PhoneAuthProvider.getCredential(verificationId, code);
        auth.signInWithCredential(credential)
                .addOnSuccessListener(r -> {
                    String phone = r.getUser() != null ? r.getUser().getPhoneNumber() : "";
                    runJs("window.otpVerified(" + JSONObject.quote(phone == null ? "" : phone) + ");");
                })
                .addOnFailureListener(e -> runJs("window.otpError(" + JSONObject.quote(e.getMessage()) + ");"));
    }

    private void runJs(String js) {
        runOnUiThread(() -> {
            if (web != null) web.evaluateJavascript(js, null);
        });
    }

    private void beginOrder(String n, String p, String a, String items, int sub) {
        if (orderInProgress) return;
        pendingName = n;
        pendingPhone = p;
        pendingAddress = a;
        pendingItems = items;
        pendingSubtotal = sub;

        if (sub < 100) {
            runJs("window.orderError('Minimum order is ₹100.');");
            return;
        }

        if (auth.getCurrentUser() == null) {
            signIn();
            return;
        }
        createOrder();
    }

    private void createOrder() {
        if (orderInProgress) return;
        if (auth.getCurrentUser() == null) {
            signIn();
            return;
        }
        orderInProgress = true;
        int delivery = 30;
        int total = pendingSubtotal + delivery;
        writeOrder(total, delivery);
    }

    private void writeOrder(int total, int delivery) {
        try {
            Map<String, Object> order = new HashMap<>();
            order.put("userId", auth.getCurrentUser().getUid());
            order.put("customerName", pendingName);
            order.put("mobile", pendingPhone);
            order.put("address", pendingAddress);
            order.put("paymentMethod", "COD");
            order.put("subtotal", pendingSubtotal);
            order.put("deliveryFee", delivery);
            order.put("total", total);
            order.put("status", "PLACED");
            order.put("createdAt", FieldValue.serverTimestamp());

            JSONArray arr = new JSONArray(pendingItems);
            Map<String, Object> items = new HashMap<>();
            for (int i = 0; i < arr.length(); i++) {
                JSONObject item = arr.getJSONObject(i);
                items.put(item.getString("id"), item.getInt("qty"));
            }
            order.put("items", items);

            db.collection("orders").add(order)
                    .addOnSuccessListener(ref -> {
                        getPreferences(Context.MODE_PRIVATE).edit()
                                .putString("lastOrderId", ref.getId()).apply();
                        listenStatus(ref.getId());
                        orderInProgress = false;
                        pendingName = null;
                        runJs("window.orderCreated(" + JSONObject.quote(ref.getId()) + ");");
                    })
                    .addOnFailureListener(e -> {
                        orderInProgress = false;
                        runJs("window.orderError(" + JSONObject.quote("Order save failed: " + e.getMessage()) + ");");
                    });
        } catch (Exception e) {
            orderInProgress = false;
            runJs("window.orderError(" + JSONObject.quote("Order error: " + e.getMessage()) + ");");
        }
    }

    private void listenStatus(String id) {
        if (statusListener != null) statusListener.remove();
        statusListener = db.collection("orders").document(id)
                .addSnapshotListener((snapshot, error) -> {
                    if (error != null || snapshot == null || !snapshot.exists()) return;
                    String status = snapshot.getString("status");
                    if (status == null) status = "PLACED";
                    runJs("window.statusUpdate(" + JSONObject.quote(status) + ");");
                });
    }

    public class AndroidBridge {
        @JavascriptInterface
        public void sendOtp(String phone) {
            runOnUiThread(() -> sendOtp(phone));
        }

        @JavascriptInterface
        public void verifyOtp(String code) {
            runOnUiThread(() -> verifyOtp(code));
        }

        @JavascriptInterface
        public void placeOrder(String n, String p, String a, String items, int subtotal) {
            runOnUiThread(() -> beginOrder(n, p, a, items, subtotal));
        }

        @JavascriptInterface
        public void loadLastOrder() {
            runOnUiThread(() -> {
                String id = getPreferences(Context.MODE_PRIVATE).getString("lastOrderId", null);
                if (id != null) listenStatus(id);
            });
        }

        @JavascriptInterface
        public void cancelLastOrder() {
            runOnUiThread(() -> {
                String id = getPreferences(Context.MODE_PRIVATE).getString("lastOrderId", null);
                if (id != null) {
                    db.collection("orders").document(id).update("status", "CANCELLED");
                }
            });
        }
    }
}
