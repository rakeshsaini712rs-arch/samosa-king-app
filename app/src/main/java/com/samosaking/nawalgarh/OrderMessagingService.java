package com.samosaking.nawalgarh;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.os.Build;
import androidx.core.app.NotificationCompat;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class OrderMessagingService extends FirebaseMessagingService {
    private static final String CHANNEL = "order_status";

    @Override public void onMessageReceived(RemoteMessage message) {
        String title = message.getNotification() != null && message.getNotification().getTitle() != null
                ? message.getNotification().getTitle() : "Samosa King";
        String body = message.getNotification() != null && message.getNotification().getBody() != null
                ? message.getNotification().getBody() : "Your order has been updated.";
        show(title, body);
    }

    @Override public void onNewToken(String token) {
        // MainActivity stores the current token for the signed-in customer.
    }

    private void show(String title, String body) {
        NotificationManager nm = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26) nm.createNotificationChannel(
                new NotificationChannel(CHANNEL, "Order status", NotificationManager.IMPORTANCE_DEFAULT));
        Intent i = new Intent(this, MainActivity.class);
        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        PendingIntent pi = PendingIntent.getActivity(this, 0, i,
                PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= 23 ? PendingIntent.FLAG_IMMUTABLE : 0));
        nm.notify((int)(System.currentTimeMillis() % 100000), new NotificationCompat.Builder(this, CHANNEL)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentTitle(title).setContentText(body).setAutoCancel(true).setContentIntent(pi).build());
    }
}
