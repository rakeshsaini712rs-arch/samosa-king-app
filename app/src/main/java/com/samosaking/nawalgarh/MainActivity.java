package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.net.Uri;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.*;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.ListenerRegistration;
import com.google.firebase.firestore.Query;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {

    private static final String ADMIN_UID =
            "vJCq3yQDe0QcCg5EoEPnjVKwUgJ2";

    private static final int DELIVERY_FEE = 30;

    FirebaseAuth auth;
    FirebaseFirestore db;

    EditText name, mobile, address;
    TextView totalText;

    int samosaQty = 0;
    int kachoriQty = 0;
    int mirchiQty = 0;

    String latestOrderId = null;

    ListenerRegistration orderListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();

        if (auth.getCurrentUser() == null) {
            auth.signInAnonymously()
                    .addOnCompleteListener(task -> showCustomerScreen());
        } else {
            showCustomerScreen();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        if (orderListener != null) {
            orderListener.remove();
            orderListener = null;
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
        shop.setText(
                "Nansa Gate, Nawalgarh\n"
                        + "Delivery ₹30 • Minimum Order ₹100"
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
        totalText.setPadding(0, 25, 0, 25);

        main.addView(totalText);

        name = new EditText(this);
        name.setHint("Customer Name");
        main.addView(name);

        mobile = new EditText(this);
        mobile.setHint("Mobile Number");
        mobile.setInputType(
                android.text.InputType.TYPE_CLASS_PHONE
        );
        main.addView(mobile);

        address = new EditText(this);
        address.setHint("Delivery Address");
        address.setMinLines(3);

        main.addView(address);

        Button orderButton = new Button(this);
        orderButton.setText("PLACE COD ORDER");

        main.addView(orderButton);

        orderButton.setOnClickListener(v -> placeOrder());

        Button trackingButton = new Button(this);
        trackingButton.setText("MY LATEST ORDER");

        main.addView(trackingButton);

        trackingButton.setOnClickListener(
                v -> showLatestOrder()
        );

        Button adminButton = new Button(this);
        adminButton.setText("ADMIN LOGIN");

        main.addView(adminButton);

        adminButton.setOnClickListener(
                v -> showAdminLogin()
        );

        setContentView(main);

        updateTotal();
    }

    LinearLayout addItem(
            String itemName,
            int price,
            int itemNumber
    ) {

        LinearLayout row = new LinearLayout(this);
        row.setOrientation(
                LinearLayout.HORIZONTAL
        );
        row.setGravity(
                Gravity.CENTER_VERTICAL
        );

        TextView item = new TextView(this);
        item.setText(
                itemName + "  ₹" + price
        );
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
                new LinearLayout.LayoutParams(
                        0,
                        70,
                        1
                )
        );

        row.addView(minus);
        row.addView(qty);
        row.addView(plus);

        plus.setOnClickListener(v -> {

            if (itemNumber == 1) {
                samosaQty++;
            }

            if (itemNumber == 2) {
                kachoriQty++;
            }

            if (itemNumber == 3) {
                mirchiQty++;
            }

            updateQty(qty, itemNumber);
            updateTotal();
        });

        minus.setOnClickListener(v -> {

            if (itemNumber == 1
                    && samosaQty > 0) {
                samosaQty--;
            }

            if (itemNumber == 2
                    && kachoriQty > 0) {
                kachoriQty--;
            }

            if (itemNumber == 3
                    && mirchiQty > 0) {
                mirchiQty--;
            }

            updateQty(qty, itemNumber);
            updateTotal();
        });

        return row;
    }

    void updateQty(
            TextView qty,
            int itemNumber
    ) {

        if (itemNumber == 1) {
            qty.setText(
                    String.valueOf(samosaQty)
            );
        }

        if (itemNumber == 2) {
            qty.setText(
                    String.valueOf(kachoriQty)
            );
        }

        if (itemNumber == 3) {
            qty.setText(
                    String.valueOf(mirchiQty)
            );
        }
    }

    int getSubtotal() {

        return
                (samosaQty * 20)
                        + (kachoriQty * 30)
                        + (mirchiQty * 30);
    }

    void updateTotal() {

        if (totalText == null) {
            return;
        }

        int subtotal = getSubtotal();

        if (subtotal == 0) {

            totalText.setText(
                    "Subtotal: ₹0"
            );

            return;
        }

        int total =
                subtotal + DELIVERY_FEE;

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

        String customerName =
                name.getText().toString().trim();

        String customerMobile =
                mobile.getText().toString().trim();

        String customerAddress =
                address.getText().toString().trim();

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

        int total =
                subtotal + DELIVERY_FEE;

        Map<String, Object> items =
                new HashMap<>();

        items.put("samosa", samosaQty);
        items.put("kachori", kachoriQty);
        items.put("mirchiBada", mirchiQty);

        Map<String, Object> order =
                new HashMap<>();

        order.put(
                "userId",
                auth.getCurrentUser().getUid()
        );

        order.put(
                "customerName",
                customerName
        );

        order.put(
                "mobile",
                customerMobile
        );

        order.put(
                "address",
                customerAddress
        );

        order.put(
                "items",
                items
        );

        order.put(
                "subtotal",
                subtotal
        );

        order.put(
                "deliveryFee",
                DELIVERY_FEE
        );

        order.put(
                "total",
                total
        );

        order.put(
                "paymentMethod",
                "COD"
        );

        order.put(
                "status",
                "PLACED"
        );

        order.put(
                "createdAt",
                FieldValue.serverTimestamp()
        );

        db.collection("orders")
                .add(order)
                .addOnSuccessListener(
                        documentReference -> {

                            latestOrderId =
                                    documentReference.getId();

                            Toast.makeText(
                                    this,
                                    "Order placed!\nID: "
                                            + latestOrderId,
                                    Toast.LENGTH_LONG
                            ).show();

                            String message =
                                    "Samosa King Order\n"
                                            + "Order ID: "
                                            + latestOrderId
                                            + "\n"
                                            + "Name: "
                                            + customerName
                                            + "\n"
                                            + "Mobile: "
                                            + customerMobile
                                            + "\n"
                                            + "Address: "
                                            + customerAddress
                                            + "\n"
                                            + "Samosa: "
                                            + samosaQty
                                            + "\n"
                                            + "Kachori: "
                                            + kachoriQty
                                            + "\n"
                                            + "Mirchi Bada: "
                                            + mirchiQty
                                            + "\n"
                                            + "Total: ₹"
                                            + total
                                            + "\n"
                                            + "Payment: COD";

                            try {

                                Intent intent =
                                        new Intent(
                                                Intent.ACTION_VIEW,
                                                Uri.parse(
                                                        "https://wa.me/917891851475?text="
                                                                + Uri.encode(
                                                                message
                                                        )
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

                        }
                )
                .addOnFailureListener(
                        e -> Toast.makeText(
                                this,
                                "Order save failed: "
                                        + e.getMessage(),
                                Toast.LENGTH_LONG
                        ).show()
                );
    }

    void showLatestOrder() {

        if (auth.getCurrentUser() == null) {

            Toast.makeText(
                    this,
                    "Please wait, connecting...",
                    Toast.LENGTH_SHORT
            ).show();

            return;
        }

        db.collection("orders")
                .whereEqualTo(
                        "userId",
                        auth.getCurrentUser().getUid()
                )
                .orderBy(
                        "createdAt",
                        Query.Direction.DESCENDING
                )
                .limit(1)
                .get()
                .addOnSuccessListener(
                        querySnapshot -> {

                            if (querySnapshot.isEmpty()) {

                                Toast.makeText(
                                        this,
                                        "No order found",
                                        Toast.LENGTH_LONG
                                ).show();

                                return;
                            }

                            DocumentSnapshot doc =
                                    querySnapshot
                                            .getDocuments()
                                            .get(0);

                            latestOrderId =
                                    doc.getId();

                            showOrderTracking(doc);
                        }
                )
                .addOnFailureListener(
                        e -> Toast.makeText(
                                this,
                                "Order load failed: "
                                        + e.getMessage(),
                                Toast.LENGTH_LONG
                        ).show()
                );
    }

    void showOrderTracking(
            DocumentSnapshot doc
    ) {

        String status =
                doc.getString("status");

        String customerName =
                doc.getString("customerName");

        String addressText =
                doc.getString("address");

        Long total =
                doc.getLong("total");

        LinearLayout main =
                new LinearLayout(this);

        main.setOrientation(
                LinearLayout.VERTICAL
        );

        main.setPadding(
                30,
                30,
                30,
                30
        );

        TextView title =
                new TextView(this);

        title.setText(
                "👑 MY ORDER"
        );

        title.setTextSize(26);
        title.setGravity(Gravity.CENTER);

        main.addView(title);

        TextView orderInfo =
                new TextView(this);

        orderInfo.setTextSize(18);

        orderInfo.setText(
                "Order ID:\n"
                        + doc.getId()
                        + "\n\n"
                        + "Name: "
                        + customerName
                        + "\n"
                        + "Address: "
                        + addressText
                        + "\n"
                        + "Total: ₹"
                        + total
                        + "\n\n"
                        + "STATUS: "
                        + status
        );

        main.addView(orderInfo);

        if ("PLACED".equals(status)) {

            Button cancel =
                    new Button(this);

            cancel.setText(
                    "CANCEL ORDER"
            );

            main.addView(cancel);

            cancel.setOnClickListener(
                    v -> cancelOrder(doc.getId())
            );
        }

        Button back =
                new Button(this);

        back.setText("BACK");

        main.addView(back);

        back.setOnClickListener(
                v -> showCustomerScreen()
        );

        setContentView(main);

        listenToOrder(doc.getId(), orderInfo);
    }

    void listenToOrder(
            String orderId,
            TextView orderInfo
    ) {

        if (orderListener != null) {
            orderListener.remove();
        }

        orderListener =
                db.collection("orders")
                        .document(orderId)
                        .addSnapshotListener(
                                (snapshot, error) -> {

                                    if (error != null
                                            || snapshot == null
                                            || !snapshot.exists()) {
                                        return;
                                    }

                                    String status =
                                            snapshot.getString(
                                                    "status"
                                            );

                                    orderInfo.setText(
                                            "Order ID:\n"
                                                    + snapshot.getId()
                                                    + "\n\n"
                                                    + "STATUS: "
                                                    + status
                                    );
                                }
                        );
    }

    void cancelOrder(
            String orderId
    ) {

        db.collection("orders")
                .document(orderId)
                .get()
                .addOnSuccessListener(
                        doc -> {

                            if (!doc.exists()) {
                                return;
                            }

                            String status =
                                    doc.getString("status");

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
                                    .update(
                                            "status",
                                            "CANCELLED"
                                    )
                                    .addOnSuccessListener(
                                            unused -> {

                                                Toast.makeText(
                                                        this,
                                                        "Order cancelled",
                                                        Toast.LENGTH_LONG
                                                ).show();

                                                showLatestOrder();
                                            }
                                    )
                
