package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.net.Uri;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.*;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {

    FirebaseAuth auth;
    FirebaseFirestore db;

    EditText name, mobile, address;
    TextView totalText;

    int samosaQty = 0;
    int kachoriQty = 0;
    int mirchiQty = 0;

    final int DELIVERY_FEE = 30;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();

        if (auth.getCurrentUser() == null) {
            auth.signInAnonymously();
        }

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
                "Nansa Gate, Nawalgarh\n" +
                "Delivery ₹30 • Minimum Order ₹100"
        );
        shop.setTextSize(16);
        shop.setGravity(Gravity.CENTER);
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

        setContentView(main);

        updateTotal();
    }

    LinearLayout addItem(
            String itemName,
            int price,
            int itemNumber
    ) {

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

            if (itemNumber == 1 && samosaQty > 0) {
                samosaQty--;
            }

            if (itemNumber == 2 && kachoriQty > 0) {
                kachoriQty--;
            }

            if (itemNumber == 3 && mirchiQty > 0) {
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

        int total = subtotal + DELIVERY_FEE;

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

        order.put("customerName", customerName);
        order.put("mobile", customerMobile);
        order.put("address", customerAddress);
        order.put("items", items);
        order.put("subtotal", subtotal);
        order.put("deliveryFee", DELIVERY_FEE);
        order.put("total", total);
        order.put("paymentMethod", "COD");
        order.put("status", "PLACED");
        order.put(
                "createdAt",
                FieldValue.serverTimestamp()
        );

        db.collection("orders")
                .add(order)
                .addOnSuccessListener(
                        documentReference -> {

                            String orderId =
                                    documentReference.getId();

                            Toast.makeText(
                                    this,
                                    "Order placed! ID: "
                                            + orderId,
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

                                Intent intent =
                                        new Intent(
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
                        }
                )
                .addOnFailureListener(
                        e -> {

                            Toast.makeText(
                                    this,
                                    "Order save failed: "
                                            + e.getMessage(),
                                    Toast.LENGTH_LONG
                            ).show();
                        }
                );
    }
}
