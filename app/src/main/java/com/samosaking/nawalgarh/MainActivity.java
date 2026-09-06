package com.samosaking.nawalgarh;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.core.content.ContextCompat;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.ListenerRegistration;
import com.google.firebase.messaging.FirebaseMessaging;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {

    private static final int LOCATION_PERMISSION_REQUEST = 1001;
    private static final int NOTIFICATION_PERMISSION_REQUEST = 1002;

    private static final String PREFS = "samosa_king";
    private static final String LAST_ORDER_ID = "last_order_id";
    private static final int DELIVERY_FEE = 30;

    private FirebaseAuth auth;
    private FirebaseFirestore db;
    private FusedLocationProviderClient locationClient;

    private EditText name;
    private EditText mobile;
    private EditText address;

    private TextView totalText;
    private TextView statusText;
    private TextView locationText;

    private int samosaQty = 0;
    private int kachoriQty = 0;
    private int mirchiQty = 0;

    private ListenerRegistration orderListener;

    private Double customerLatitude = null;
    private Double customerLongitude = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();
        locationClient = LocationServices.getFusedLocationProviderClient(this);

        createNotificationChannel();
        requestNotificationPermission();
        buildScreen();

        if (auth.getCurrentUser() == null) {
            auth.signInAnonymously()
                    .addOnSuccessListener(result -> loadLastOrder())
                    .addOnFailureListener(e ->
                            Toast.makeText(
                                    this,
                                    "Firebase connection failed: " + e.getMessage(),
                                    Toast.LENGTH_LONG
                            ).show()
                    );
        } else {
            loadLastOrder();
        }
    }

    private void buildScreen() {
        LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(30, 30, 30, 30);
        main.setBackgroundColor(Color.WHITE);

        ScrollView scrollView = new ScrollView(this);
        scrollView.addView(main);

        TextView title = new TextView(this);
        title.setText("👑 SAMOSA KING");
        title.setTextSize(28);
        title.setTextColor(Color.BLACK);
        title.setGravity(Gravity.CENTER);
        main.addView(title);

        TextView shop = new TextView(this);
        shop.setText(
                "Nansa Gate, Nawalgarh\n" +
                "8:30 AM - 6:00 PM\n" +
                "Delivery ₹30 • Minimum Order ₹100"
        );
        shop.setTextSize(16);
        shop.setGravity(Gravity.CENTER);
        shop.setPadding(0, 10, 0, 20);
        main.addView(shop);

        main.addView(addItem("Samosa", 20, 1));
        main.addView(addItem("Kachori", 30, 2));
        main.addView(addItem("Mirchi Bada", 30, 3));

        totalText = new TextView(this);
        totalText.setTextSize(20);
        totalText.setPadding(0, 25, 0, 20);
        main.addView(totalText);

        name = new EditText(this);
        name.setHint("Customer Name");
        main.addView(name);

        mobile = new EditText(this);
        mobile.setHint("Mobile Number");
        mobile.setInputType(android.text.InputType.TYPE_CLASS_PHONE);
        main.addView(mobile);

        address = new EditText(this);
        address.setHint("Delivery Address");
        address.setMinLines(3);
        main.addView(address);

        Button locationButton = new Button(this);
        locationButton.setText("📍 GET MY CURRENT LOCATION");
        main.addView(locationButton);

        locationText = new TextView(this);
        locationText.setText("Location not selected");
        locationText.setTextSize(15);
        locationText.setPadding(0, 10, 0, 15);
        main.addView(locationText);

        locationButton.setOnClickListener(v -> getCurrentLocation());

        Button orderButton = new Button(this);
        orderButton.setText("PLACE COD ORDER");
        main.addView(orderButton);
        orderButton.setOnClickListener(v -> placeOrder());

        statusText = new TextView(this);
        statusText.setTextSize(18);
        statusText.setPadding(0, 25, 0, 15);
        main.addView(statusText);

        Button trackingButton = new Button(this);
        trackingButton.setText("📦 TRACK MY ORDER");
        main.addView(trackingButton);
        trackingButton.setOnClickListener(v -> startOrderListener());

        Button cancelButton = new Button(this);
        cancelButton.setText("❌ CANCEL MY ORDER");
        main.addView(cancelButton);
        cancelButton.setOnClickListener(v -> cancelLatestOrder());

        Button historyButton = new Button(this);
        historyButton.setText("🧾 ORDER HISTORY");
        main.addView(historyButton);
        historyButton.setOnClickListener(v -> showOrderHistory());

        setContentView(scrollView);
        updateTotal();
    }

    private LinearLayout addItem(String itemName, int price, int itemNumber) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);

        TextView item = new TextView(this);
        item.setText(itemName + "  ₹" + price);
        item.setTextSize(18);

        Button minus = new Button(this);
        minus.setText("-");

        TextView qty = new TextView(this);
        qty.setText("0");
        qty.setTextSize(18);
        qty.setGravity(Gravity.CENTER);
        qty.setPadding(20, 0, 20, 0);

        Button plus = new Button(this);
        plus.setText("+");

        row.addView(
                item,
                new LinearLayout.LayoutParams(0, 70, 1)
        );
        row.addView(minus);
        row.addView(qty);
        row.addView(plus);

        plus.setOnClickListener(v -> {
            if (itemNumber == 1) {
                samosaQty++;
            } else if (itemNumber == 2) {
                kachoriQty++;
            } else {
                mirchiQty++;
            }
            updateQty(qty, itemNumber);
            updateTotal();
        });

        minus.setOnClickListener(v -> {
            if (itemNumber == 1 && samosaQty > 0) {
                samosaQty--;
            } else if (itemNumber == 2 && kachoriQty > 0) {
                kachoriQty--;
            } else if (itemNumber == 3 && mirchiQty > 0) {
                mirchiQty--;
            }
            updateQty(qty, itemNumber);
            updateTotal();
        });

        return row;
    }

    private void updateQty(TextView qty, int itemNumber) {
        if (itemNumber == 1) {
            qty.setText(String.valueOf(samosaQty));
        } else if (itemNumber == 2) {
            qty.setText(String.valueOf(kachoriQty));
        } else {
            qty.setText(String.valueOf(mirchiQty));
        }
    }

    private int getSubtotal() {
        return (samosaQty * 20)
                + (kachoriQty * 30)
                + (mirchiQty * 30);
    }

    private void updateTotal() {
        if (totalText == null) {
            return;
        }

        int subtotal = getSubtotal();

        if (subtotal == 0) {
            totalText.setText("Subtotal: ₹0");
            return;
        }

        int total = subtotal + DELIVERY_FEE;

        totalText.setText(
                "Subtotal: ₹" + subtotal +
                "\nDelivery: ₹" + DELIVERY_FEE +
                "\nTotal: ₹" + total
        );
    }

    private void getCurrentLocation() {
        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
        ) != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(
                    this,
                    new String[]{
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                    },
                    LOCATION_PERMISSION_REQUEST
            );
            return;
        }

        locationText.setText("Getting current location...");

        locationClient.getCurrentLocation(
                com.google.android.gms.location.Priority.PRIORITY_HIGH_ACCURACY,
                null
        ).addOnSuccessListener(location -> {
            if (location == null) {
                locationText.setText("Location nahi mili");
                return;
            }

            customerLatitude = location.getLatitude();
            customerLongitude = location.getLongitude();

            locationText.setText(
                    "📍 Location captured\n" +
                    "Latitude: " + customerLatitude +
                    "\nLongitude: " + customerLongitude
            );
        }).addOnFailureListener(e ->
                locationText.setText("Location failed: " + e.getMessage())
        );
    }

    @Override
    public void onRequestPermissionsResult(
            int requestCode,
            String[] permissions,
            int[] grantResults
    ) {
        super.onRequestPermissionsResult(
                requestCode,
                permissions,
                grantResults
        );

        if (requestCode == LOCATION_PERMISSION_REQUEST) {
            if (grantResults.length > 0
                    && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getCurrentLocation();
            } else {
                Toast.makeText(
                        this,
                        "Location permission denied",
                        Toast.LENGTH_LONG
                ).show();
            }
        }
    }

    private void placeOrder() {
        if (auth.getCurrentUser() == null) {
            Toast.makeText(
                    this,
                    "Please wait, connecting...",
                    Toast.LENGTH_SHORT
            ).show();
            return;
        }

        int subtotal = getSubtotal();

        if (subtotal < 100) {
            Toast.makeText(
                    this,
                    "Minimum order ₹100 hai",
                    Toast.LENGTH_SHORT
            ).show();
            return;
        }

        String customerName = name.getText().toString().trim();
        String customerMobile = mobile.getText().toString().trim();
        String customerAddress = address.getText().toString().trim();

        if (customerName.isEmpty()
                || customerMobile.isEmpty()
                || customerAddress.isEmpty()) {
            Toast.makeText(
                    this,
                    "Name, mobile aur address bharo",
                    Toast.LENGTH_LONG
            ).show();
            return;
        }

        int total = subtotal + DELIVERY_FEE;

        Map<String, Object> items = new HashMap<>();
        items.put("samosa", samosaQty);
        items.put("kachori", kachoriQty);
        items.put("mirchiBada", mirchiQty);

        Map<String, Object> order = new HashMap<>();
        order.put("userId", auth.getCurrentUser().getUid());
        order.put("customerName", customerName);
        order.put("mobile", customerMobile);
        order.put("address", customerAddress);
        order.put("items", items);
        order.put("subtotal", subtotal);
        order.put("deliveryFee", DELIVERY_FEE);
        order.put("total", total);
        order.put("paymentMethod", "COD");
        order.put("status", "PLACED");

        if (customerLatitude != null && customerLongitude != null) {
            order.put("latitude", customerLatitude);
            order.put("longitude", customerLongitude);
        }

        order.put("createdAt", FieldValue.serverTimestamp());

        db.collection("orders")
                .add(order)
                .addOnSuccessListener(documentReference -> {
                    String orderId = documentReference.getId();

                    getSharedPreferences(PREFS, MODE_PRIVATE)
                            .edit()
                            .putString(LAST_ORDER_ID, orderId)
                            .apply();

                    Toast.makeText(
                            this,
                            "Order placed!\nID: " + orderId,
                            Toast.LENGTH_LONG
                    ).show();

                    startOrderListener();

                    String message =
                            "Samosa King Order\n" +
                            "Order ID: " + orderId + "\n" +
                            "Name: " + customerName + "\n" +
                            "Mobile: " + customerMobile + "\n" +
                            "Address: " + customerAddress + "\n" +
                            "Samosa: " + samosaQty + "\n" +
                            "Kachori: " + kachoriQty + "\n" +
                            "Mirchi Bada: " + mirchiQty + "\n" +
                            "Total: ₹" + total + "\n" +
                            "Payment: COD";

                    try {
                        Intent intent = new Intent(
                                Intent.ACTION_VIEW,
                                Uri.parse(
                                        "https://wa.me/917891851475?text=" +
                                        Uri.encode(message)
                                )
                        );
                        startActivity(intent);
                    } catch (Exception e) {
                        Toast.makeText(
                                this,
                                "Order saved successfully",
                                Toast.LENGTH_LONG
                        ).show();
                    }
                })
                .addOnFailureListener(e ->
                        Toast.makeText(
                                this,
                                "Order save failed: " + e.getMessage(),
                                Toast.LENGTH_LONG
                        ).show()
                );
    }

    private void loadLastOrder() {
        SharedPreferences prefs =
                getSharedPreferences(PREFS, MODE_PRIVATE);

        String orderId =
                prefs.getString(LAST_ORDER_ID, null);

        if (orderId != null) {
            startOrderListener();
        }
    }

    private void startOrderListener() {
        if (statusText == null) {
            return;
        }

        SharedPreferences prefs =
                getSharedPreferences(PREFS, MODE_PRIVATE);

        String orderId =
                prefs.getString(LAST_ORDER_ID, null);

        if (orderId == null) {
            statusText.setText("No order found");
            return;
        }

        if (orderListener != null) {
            orderListener.remove();
        }

        orderListener = db.collection("orders")
                .document(orderId)
                .addSnapshotListener((snapshot, error) -> {
                    if (error != null) {
                        statusText.setText(
                                "Tracking failed: " + error.getMessage()
                        );
                        return;
                    }

                    if (snapshot == null || !snapshot.exists()) {
                        statusText.setText("Order not found");
                        return;
                    }

                    String status = snapshot.getString("status");

                    if (status == null) {
                        status = "UNKNOWN";
                    }

                    statusText.setText(
                            "📦 ORDER STATUS\n" + status
                    );
                });
    }

    private void cancelLatestOrder() {
        SharedPreferences prefs =
                getSharedPreferences(PREFS, MODE_PRIVATE);

        String orderId =
                prefs.getString(LAST_ORDER_ID, null);

        if (orderId == null) {
            Toast.makeText(
                    this,
                    "No order found",
                    Toast.LENGTH_LONG
            ).show();
            return;
        }

        db.collection("orders")
                .document(orderId)
                .get()
                .addOnSuccessListener(order -> {
                    if (!order.exists()) {
                        Toast.makeText(
                                this,
                                "Order not found",
                                Toast.LENGTH_LONG
                        ).show();
                        return;
                    }

                    String status = order.getString("status");

                    if (!"PLACED".equals(status)) {
                        Toast.makeText(
                                this,
                                "Order ab cancel nahi ho sakta",
                                Toast.LENGTH_LONG
                        ).show();
                        return;
                    }

                    db.collection("orders")
                            .document(orderId)
                            .update("status", "CANCELLED")
                            .addOnSuccessListener(unused -> {
                                Toast.makeText(
                                        this,
                                        "Order cancelled",
                                        Toast.LENGTH_LONG
                                ).show();
                                startOrderListener();
                            })
                            .addOnFailureListener(e ->
                                    Toast.makeText(
                                            this,
                                            "Cancel failed: " + e.getMessage(),
                                            Toast.LENGTH_LONG
                                    ).show()
                            );
                })
                .addOnFailureListener(e ->
                        Toast.makeText(
                                this,
                                "Cancel failed: " + e.getMessage(),
                                Toast.LENGTH_LONG
                        ).show()
                );
    }

    private void showOrderHistory() {
        if (auth.getCurrentUser() == null) {
            return;
        }

        db.collection("orders")
                .whereEqualTo(
                        "userId",
                        auth.getCurrentUser().getUid()
                )
                .get()
                .addOnSuccessListener(querySnapshot -> {
                    if (querySnapshot.isEmpty()) {
                        Toast.makeText(
                                this,
                                "No order history",
                                Toast.LENGTH_LONG
                        ).show();
                        return;
                    }

                    StringBuilder history = new StringBuilder();

                    for (DocumentSnapshot doc :
                            querySnapshot.getDocuments()) {

                        String status = doc.getString("status");
                        Long total = doc.getLong("total");

                        history.append("Order: ")
                                .append(doc.getId())
                                .append("\nStatus: ")
                                .append(status == null ? "UNKNOWN" : status)
                                .append("\nTotal: ₹")
                                .append(total == null ? 0 : total)
                                .append("\n\n");
                    }

                    new AlertDialog.Builder(this)
                            .setTitle("Order History")
                            .setMessage(history.toString())
                            .setPositiveButton("OK", null)
                            .show();
                })
                .addOnFailureListener(e ->
                        Toast.makeText(
                                this,
                                "History failed: " + e.getMessage(),
                                Toast.LENGTH_LONG
                        ).show()
                );
    }

    private void requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= 33) {
            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.POST_NOTIFICATIONS
            ) != PackageManager.PERMISSION_GRANTED) {

                ActivityCompat.requestPermissions(
                        this,
                        new String[]{
                                Manifest.permission.POST_NOTIFICATIONS
                        },
                        NOTIFICATION_PERMISSION_REQUEST
                );
            }
        }

        saveFirebaseMessagingToken();
    }

    private void saveFirebaseMessagingToken() {
        FirebaseMessaging.getInstance()
                .getToken()
                .addOnSuccessListener(token -> {
                    // Real FCM token obtained.
                });
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel =
                    new NotificationChannel(
                            "samosa_king_orders",
                            "Samosa King Orders",
                            NotificationManager.IMPORTANCE_HIGH
                    );

            NotificationManager manager =
                    getSystemService(NotificationManager.class);

            if (manager != null) {
                manager.createNotificationChannel(channel);
            }
        }
    }

    private void showLocalNotification(
            String title,
            String message
    ) {
        if (Build.VERSION.SDK_INT >= 33
                && ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.POST_NOTIFICATIONS
        ) != PackageManager.PERMISSION_GRANTED) {
            return;
        }

        NotificationCompat.Builder builder =
                new NotificationCompat.Builder(
                        this,
                        "samosa_king_orders"
                )
                        .setSmallIcon(
                                android.R.drawable.ic_dialog_info
                        )
                        .setContentTitle(title)
                        .setContentText(message)
                        .setPriority(
                                NotificationCompat.PRIORITY_HIGH
                        )
                        .setAutoCancel(true);

        NotificationManager manager =
                (NotificationManager) getSystemService(
                        Context.NOTIFICATION_SERVICE
                );

        if (manager != null) {
            manager.notify(1001, builder.build());
        }
    }

    @Override
    protected void onDestroy() {
        if (orderListener != null) {
            orderListener.remove();
            orderListener = null;
        }

        super.onDestroy();
    }
}
