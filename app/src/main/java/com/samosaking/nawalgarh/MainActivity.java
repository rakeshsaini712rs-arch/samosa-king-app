package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.net.Uri;
import android.graphics.Color;
import android.view.Gravity;
import android.view.View;
import android.widget.*;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {

    private static final String ADMIN_UID = "vJCq3yQDe0QcCg5EoEPnjVKwUgJ2";
    private static final int DELIVERY_FEE = 30;

    FirebaseAuth auth;
    FirebaseFirestore db;

    EditText name, mobile, address;
    TextView totalText;

    int samosaQty = 0;
    int kachoriQty = 0;
    int mirchiQty = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();

        showCustomerScreen();

        if (auth.getCurrentUser() == null) {
            auth.signInAnonymously();
        }
    }

    void showCustomerScreen() {

        LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(30, 30, 30, 30);
        main.setBackgroundColor(Color.WHITE);

        TextView title = new TextView(this);
        title.setText("👑 SAMOSA KING");
        title.setTextSize(28);
        title.setTextColor(Color.BLACK);
        title.setGravity(Gravity.CENTER);
        main.addView(title);

        TextView shop = new TextView(this);
        shop.setText("Nansa Gate, Nawalgarh\nDelivery ₹30 • Minimum Order ₹100");
        shop.setTextSize(16);
        shop.setGravity(Gravity.CENTER);
        shop.setPadding(0, 10, 0, 20);
        main.addView(shop);

        main.addView(addItem("Samosa", 20, 1));
        main.addView(addItem("Kachori", 30, 2));
        main.addView(addItem("Mirchi Bada", 30, 3));

        totalText = new TextView(this);
        totalText.setTextSize(20);
        totalText.setPadding(0, 25, 0, 25);
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

        Button orderButton = new Button(this);
        orderButton.setText("PLACE COD ORDER");
        main.addView(orderButton);

        orderButton.setOnClickListener(v -> placeOrder());

        Button adminButton = new Button(this);
        adminButton.setText("ADMIN LOGIN");
        main.addView(adminButton);

        adminButton.setOnClickListener(v -> showAdminLogin());

        setContentView(main);

        updateTotal();
    }

    LinearLayout addItem(String itemName, int price, int itemNumber) {

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

        row.addView(item, new LinearLayout.LayoutParams(0, 70, 1));
        row.addView(minus);
        row.addView(qty);
        row.addView(plus);

        plus.setOnClickListener(v -> {

            if (itemNumber == 1) samosaQty++;
            if (itemNumber == 2) kachoriQty++;
            if (itemNumber == 3) mirchiQty++;

            updateQty(qty, itemNumber);
            updateTotal();
        });

        minus.setOnClickListener(v -> {

            if (itemNumber == 1 && samosaQty > 0) samosaQty--;
            if (itemNumber == 2 && kachoriQty > 0) kachoriQty--;
            if (itemNumber == 3 && mirchiQty > 0) mirchiQty--;

            updateQty(qty, itemNumber);
            updateTotal();
        });

        return row;
    }

    void updateQty(TextView qty, int itemNumber) {

        if (itemNumber == 1) {
            qty.setText(String.valueOf(samosaQty));
        }

        if (itemNumber == 2) {
            qty.setText(String.valueOf(kachoriQty));
        }

        if (itemNumber == 3) {
            qty.setText(String.valueOf(mirchiQty));
        }
    }

    int getSubtotal() {

        return (samosaQty * 20)
                + (kachoriQty * 30)
                + (mirchiQty * 30);
    }

    void updateTotal() {

        if (totalText == null) return;

        int subtotal = getSubtotal();

        if (subtotal == 0) {
            totalText.setText("Subtotal: ₹0");
            return;
        }

        int total = subtotal + DELIVERY_FEE;

        totalText.setText(
                "Subtotal: ₹" + subtotal
                        + "\nDelivery: ₹" + DELIVERY_FEE
                        + "\nTotal: ₹" + total
        );
    }

    void placeOrder() {

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
                    Toast.LENGTH_SHORT
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
        order.put("createdAt", FieldValue.serverTimestamp());

        db.collection("orders")
                .add(order)
                .addOnSuccessListener(documentReference -> {

                    String orderId = documentReference.getId();

                    Toast.makeText(
                            this,
                            "Order placed! ID: " + orderId,
                            Toast.LENGTH_LONG
                    ).show();

                    String message =
                            "Samosa King Order\n"
                                    + "Order ID: " + orderId + "\n"
                                    + "Name: " + customerName + "\n"
                                    + "Mobile: " + customerMobile + "\n"
                                    + "Address: " + customerAddress + "\n"
                                    + "Samosa: " + samosaQty + "\n"
                                    + "Kachori: " + kachoriQty + "\n"
                                    + "Mirchi Bada: " + mirchiQty + "\n"
                                    + "Total: ₹" + total + "\n"
                                    + "Payment: COD";

                    try {

                        Intent intent = new Intent(
                                Intent.ACTION_VIEW,
                                Uri.parse(
                                        "https://wa.me/917891851475?text="
                                                + Uri.encode(message)
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
                .addOnFailureListener(e -> {

                    Toast.makeText(
                            this,
                            "Order save failed: " + e.getMessage(),
                            Toast.LENGTH_LONG
                    ).show();
                });
    }

    void showAdminLogin() {

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(30, 30, 30, 30);

        TextView title = new TextView(this);
        title.setText("👑 ADMIN LOGIN");
        title.setTextSize(26);
        title.setGravity(Gravity.CENTER);

        layout.addView(title);

        EditText email = new EditText(this);
        email.setHint("Admin Email");
        email.setInputType(
                android.text.InputType.TYPE_CLASS_TEXT
                        | android.text.InputType.TYPE_TEXT_VARIATION_EMAIL_ADDRESS
        );

        layout.addView(email);

        EditText password = new EditText(this);
        password.setHint("Password");
        password.setInputType(
                android.text.InputType.TYPE_CLASS_TEXT
                        | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD
        );

        layout.addView(password);

        Button login = new Button(this);
        login.setText("LOGIN");
        layout.addView(login);

        Button back = new Button(this);
        back.setText("BACK");
        layout.addView(back);

        setContentView(layout);

        login.setOnClickListener(v -> {

            String adminEmail = email.getText().toString().trim();
            String adminPassword = password.getText().toString();

            if (adminEmail.isEmpty() || adminPassword.isEmpty()) {

                Toast.makeText(
                        this,
                        "Email aur password bharo",
                        Toast.LENGTH_SHORT
                ).show();

                return;
            }

            auth.signInWithEmailAndPassword(
                            adminEmail,
                            adminPassword
                    )
                    .addOnSuccessListener(result -> {

                        if (auth.getCurrentUser() != null
                                && auth.getCurrentUser()
                                .getUid()
                                .equals(ADMIN_UID)) {

                            showAdminPanel();

                        } else {

                            auth.signOut();

                            Toast.makeText(
                                    this,
                                    "Admin access denied",
                                    Toast.LENGTH_LONG
                            ).show();

                            showCustomerScreen();
                        }
                    })
                    .addOnFailureListener(e -> {

                        Toast.makeText(
                                this,
                                "Login failed",
                                Toast.LENGTH_LONG
                        ).show();
                    });
        });

        back.setOnClickListener(v -> showCustomerScreen());
    }

    void showAdminPanel() {

        LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(20, 20, 20, 20);

        TextView title = new TextView(this);
        title.setText("👑 SAMOSA KING ADMIN");
        title.setTextSize(26);
        title.setGravity(Gravity.CENTER);
        main.addView(title);

        Button refresh = new Button(this);
        refresh.setText("REFRESH ORDERS");
        main.addView(refresh);

        Button logout = new Button(this);
        logout.setText("LOGOUT");
        main.addView(logout);

        ScrollView scrollView = new ScrollView(this);

        LinearLayout ordersLayout = new LinearLayout(this);
        ordersLayout.setOrientation(LinearLayout.VERTICAL);

        scrollView.addView(ordersLayout);
        main.addView(
                scrollView,
                new LinearLayout.LayoutParams(
                        -1,
                        0,
                        1
                )
        );

        setContentView(main);

        loadOrders(ordersLayout);

        refresh.setOnClickListener(v ->
                loadOrders(ordersLayout)
        );

        logout.setOnClickListener(v -> {

            auth.signOut();

            auth.signInAnonymously()
                    .addOnCompleteListener(task ->
                            showCustomerScreen()
                    );
        });
    }

    void loadOrders(LinearLayout ordersLayout) {

        ordersLayout.removeAllViews();

        TextView loading = new TextView(this);
        loading.setText("Orders loading...");
        loading.setTextSize(18);
        ordersLayout.addView(loading);

        db.collection("orders")
                .orderBy(
                        "createdAt",
                        com.google.firebase.firestore.Query.Direction.DESCENDING
                )
                .get()
                .addOnSuccessListener(querySnapshot -> {

                    ordersLayout.removeAllViews();

                    if (querySnapshot.isEmpty()) {

                        TextView empty = new TextView(this);
                        empty.setText("No orders found");
                        empty.setTextSize(18);
                        ordersLayout.addView(empty);

                        return;
                    }

                    for (DocumentSnapshot doc : querySnapshot.getDocuments()) {

                        addAdminOrderCard(
                                ordersLayout,
                                doc
                        );
                    }
                })
                .addOnFailureListener(e -> {

                    ordersLayout.removeAllViews();

                    TextView error = new TextView(this);
                    error.setText(
                            "Orders load failed:\n"
                                    + e.getMessage()
                    );
                    error.setTextSize(16);

                    ordersLayout.addView(error);
                });
    }

    void addAdminOrderCard(
            LinearLayout parent,
            DocumentSnapshot doc
    ) {

        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(20, 20, 20, 20);
        card.setBackgroundColor(Color.LTGRAY);

        TextView orderText = new TextView(this);
        orderText.setTextSize(17);

        String orderId = doc.getId();

        String customerName = doc.getString("customerName");
        String mobileNumber = doc.getString("mobile");
        String customerAddress = doc.getString("address");
        String status = doc.getString("status");
        String payment = doc.getString("paymentMethod");

        Long subtotal = doc.getLong("subtotal");
        Long deliveryFee = doc.getLong("deliveryFee");
        Long total = doc.getLong("total");

        Map<String, Object> items =
                (Map<String, Object>) doc.get("items");

        String itemText = "";

        if (items != null) {

            Object samosa = items.get("samosa");
            Object kachori = items.get("kachori");
            Object mirchi = items.get("mirchiBada");

            itemText =
                    "Samosa: " + String.valueOf(samosa)
                            + "\nKachori: " + String.valueOf(kachori)
                            + "\nMirchi Bada: " + String.valueOf(mirchi);
        }

        orderText.setText(
                "ORDER: " + orderId
                        + "\n\nCustomer: " + customerName
                        + "\nMobile: " + mobileNumber
                        + "\nAddress: " + customerAddress
                        + "\n\n" + itemText
                        + "\n\nSubtotal: ₹" + subtotal
                        + "\nDelivery: ₹" + deliveryFee
                        + "\nTotal: ₹" + total
                        + "\nPayment: " + payment
                        + "\nStatus: " + status
        );

        card.addView(orderText);

        Button placed = new Button(this);
        placed.setText("PLACED");
        card.addView(placed);

        Button preparing = new Button(this);
        preparing.setText("PREPARING");
        card.addView(preparing);

        Button outForDelivery = new Button(this);
        outForDelivery.setText("OUT FOR DELIVERY");
        card.addView(outForDelivery);

        Button delivered = new Button(this);
        delivered.setText("DELIVERED");
        card.addView(delivered);

        Button cancelled = new Button(this);
        cancelled.setText("CANCELLED");
        card.addView(cancelled);

        placed.setOnClickListener(v ->
                updateOrderStatus(doc.getId(), "PLACED")
        );

        preparing.setOnClickListener(v ->
                updateOrderStatus(doc.getId(), "PREPARING")
        );

        outForDelivery.setOnClickListener(v ->
                updateOrderStatus(doc.getId(), "OUT_FOR_DELIVERY")
        );

        delivered.setOnClickListener(v ->
                updateOrderStatus(doc.getId(), "DELIVERED")
        );

        cancelled.setOnClickListener(v ->
                updateOrderStatus(doc.getId(), "CANCELLED")
        );

        parent.addView(card);

        Space space = new Space(this);

        parent.addView(
                space,
                new LinearLayout.LayoutParams(
                        1,
                        30
                )
        );
    }

    void updateOrderStatus(
            String orderId,
            String newStatus
    ) {

        db.collection("orders")
                .document(orderId)
                .update("status", newStatus)
                .addOnSuccessListener(unused -> {

                    Toast.makeText(
                            this,
                            "Status updated: " + newStatus,
                            Toast.LENGTH_SHORT
                    ).show();

                    showAdminPanel();
                })
                .addOnFailureListener(e -> {

                    Toast.makeText(
                            this,
                            "Status update failed: " + e.getMessage(),
                            Toast.LENGTH_LONG
                    ).show();
                });
    }
                                      }
