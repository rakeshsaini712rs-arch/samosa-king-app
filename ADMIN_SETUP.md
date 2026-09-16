# Samosa King Admin setup

The repository now contains a separate `:admin` Android application. It uses the same Firebase project as the customer app, but it only opens the dashboard after Firebase Authentication succeeds **and** `admins/{uid}` exists.

## One-time Firebase setup
1. Firebase Console → Authentication → Sign-in method → enable **Email/Password**.
2. Authentication → Users → add the owner's admin email/password.
3. Copy that user's **UID**.
4. Firestore Database → create collection `admins`.
5. Create a document whose **document ID is exactly the admin UID**.
6. Add optional fields such as `name: Samosa King Owner` and `role: admin`.
7. Do not create admin access by putting a password in the Android source.

The Firestore rules already use the existence of `admins/{request.auth.uid}` as the admin authorization check. Customers cannot write to the `admins` collection.

## Admin app
Package: `com.samosaking.admin`

It provides:
- real-time Firestore order list
- customer name and mobile
- full delivery address
- ordered items and quantities
- subtotal, delivery fee, discount, total and payment method
- live order status
- Accept → Preparing → Out for Delivery → Delivered
- Reject / Cancel
- Call customer
- WhatsApp customer
- Navigate to delivery address in Google Maps
- pending/total/today sales/delivered sales dashboard

The app does not create fake orders or fake payment confirmations. Online payment verification remains separate until a real payment gateway/backend is connected.

## Build
The final GitHub Actions workflow builds both:
- `app-debug.apk` — Customer
- `admin-debug.apk` — Admin
