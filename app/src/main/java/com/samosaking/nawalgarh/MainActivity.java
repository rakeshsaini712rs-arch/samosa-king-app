package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.*;

public class MainActivity extends Activity {

    LinearLayout main;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(30, 30, 30, 30);
        main.setBackgroundColor(Color.WHITE);

        TextView title = new TextView(this);
        title.setText("👑 SAMOSA KING");
        title.setTextSize(28);
        title.setTextColor(Color.BLACK);
        title.setGravity(Gravity.CENTER);

        main.addView(title);

        TextView info = new TextView(this);
        info.setText(
                "\nNansa Gate, Nawalgarh\n" +
                "Delivery ₹30 • Minimum Order ₹100\n\n" +
                "Samosa ₹20\n" +
                "Kachori ₹30\n" +
                "Mirchi Bada ₹30"
        );
        info.setTextSize(18);

        main.addView(info);

        setContentView(main);
    }
}
