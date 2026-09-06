package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.view.Gravity;
import android.widget.*;

public class MainActivity extends Activity {

    int samosa = 0, kachori = 0, mirchi = 0;

    TextView totalText;

    @Override
    public void onCreate(Bundle b) {
        super.onCreate(b);

        LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(25, 25, 25, 25);
        main.setBackgroundColor(Color.rgb(255,248,239));

        TextView title = new TextView(this);
        title.setText("👑 Samosa King");
        title.setTextSize(30);
        title.setGravity(Gravity.CENTER);
        main.addView(title);

        TextView address = new TextView(this);
        address.setText("Nansa Gate, Nawalgarh");
        address.setTextSize(18);
        address.setGravity(Gravity.CENTER);
        main.addView(address);

        main.addView(item("Samosa ₹20", 20, 1));
        main.addView(item("Kachori ₹30", 30, 2));
        main.addView(item("Mirchi Bada ₹30", 30, 3));

        totalText = new TextView(this);
        totalText.setTextSize(22);
        totalText.setGravity(Gravity.CENTER);
        totalText.setPadding(0, 20, 0, 20);
        updateTotal();
        main.addView(totalText);

        EditText name = new EditText(this);
        name.setHint("Customer Name");
        main.addView(name);

        EditText customerAddress = new EditText(this);
        customerAddress.setHint("Delivery Address");
        main.addView(customerAddress);

        Button order = new Button(this);
        order.setText("PLACE ORDER - COD");
        main.addView(order);

        order.setOnClickListener(v -> {

            int total = samosa * 20 + kachori * 30 + mirchi * 30;

            if (total < 100) {
                Toast.makeText(this,
                        "Minimum order ₹100 hai",
                        Toast.LENGTH_LONG).show();
                return;
            }

            total += 30;

            String message =
                    "👑 SAMOSA KING ORDER\n\n" +
                    "Customer: " + name.getText().toString() + "\n" +
                    "Address: " + customerAddress.getText().toString() + "\n\n" +
                    "Samosa: " + samosa + "\n" +
                    "Kachori: " + kachori + "\n" +
                    "Mirchi Bada: " + mirchi + "\n\n" +
                    "Delivery: ₹30\n" +
                    "Total: ₹" + total + "\n" +
                    "Payment: Cash on Delivery";

            try {
                Intent intent = new Intent(
                        Intent.ACTION_VIEW,
                        Uri.parse("https://wa.me/917891851475?text="
                                + Uri.encode(message))
                );
                startActivity(intent);
            } catch (Exception e) {
                Toast.makeText(this,
                        "WhatsApp available nahi hai",
                        Toast.LENGTH_LONG).show();
            }
        });

        setContentView(main);
    }

    LinearLayout item(String name, int price, int type) {

        LinearLayout row = new LinearLayout(this);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(0, 15, 0, 15);

        TextView text = new TextView(this);
        text.setText(name);
        text.setTextSize(20);
        row.addView(text, new LinearLayout.LayoutParams(
                0, -2, 1));

        Button minus = new Button(this);
        minus.setText("-");
        row.addView(minus);

        TextView qty = new TextView(this);
        qty.setText("0");
        qty.setTextSize(20);
        qty.setGravity(Gravity.CENTER);
        row.addView(qty, new LinearLayout.LayoutParams(70, -2));

        Button plus = new Button(this);
        plus.setText("+");
        row.addView(plus);

        minus.setOnClickListener(v -> {
            if (type == 1 && samosa > 0) samosa--;
            if (type == 2 && kachori > 0) kachori--;
            if (type == 3 && mirchi > 0) mirchi--;

            updateQty(qty, type);
            updateTotal();
        });

        plus.setOnClickListener(v -> {
            if (type == 1) samosa++;
            if (type == 2) kachori++;
            if (type == 3) mirchi++;

            updateQty(qty, type);
            updateTotal();
        });

        return row;
    }

    void updateQty(TextView qty, int type) {
        if (type == 1) qty.setText(String.valueOf(samosa));
        if (type == 2) qty.setText(String.valueOf(kachori));
        if (type == 3) qty.setText(String.valueOf(mirchi));
    }

    void updateTotal() {
        if (totalText != null) {
            int total = samosa * 20 + kachori * 30 + mirchi * 30;
            totalText.setText("Cart Total: ₹" + total);
        }
    }
}
