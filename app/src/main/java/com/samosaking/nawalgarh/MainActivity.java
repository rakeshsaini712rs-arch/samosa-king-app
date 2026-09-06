package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends Activity {

    @Override
    public void onCreate(Bundle b) {
        super.onCreate(b);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        layout.setPadding(32, 32, 32, 32);
        layout.setBackgroundColor(Color.rgb(255, 248, 239));

        TextView title = new TextView(this);
        title.setText("👑 Samosa King");
        title.setTextSize(30);
        title.setGravity(Gravity.CENTER);

        TextView info = new TextView(this);
        info.setText(
            "\nNansa Gate, Nawalgarh\n\n" +
            "Samosa ₹20\n" +
            "Kachori ₹30\n" +
            "Mirchi Bada ₹30\n\n" +
            "Delivery ₹30 up to 5 km\n" +
            "Minimum Order ₹100\n" +
            "Cash on Delivery\n\n" +
            "Order: 7891851475"
        );
        info.setTextSize(18);
        info.setGravity(Gravity.CENTER);

        layout.addView(title);
        layout.addView(info);

        setContentView(layout);
    }
}
