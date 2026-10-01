from pathlib import Path
import re

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')

# 1) Product delivery ticker: keep one copy only.
old = '''function skProductTicker(){return '<div class="skProductTicker"><div class="skTickerTrack"><span class="skTickerItem">⏱ 20–30 min</span><span class="skTickerDot">•</span><span class="skTickerItem">⚡ Near & Fast</span><span class="skTickerDot">•</span><span class="skTickerItem">🔥 Fresh & Hot</span><span class="skTickerDot">•</span><span class="skTickerItem">🚴 Fast Delivery</span><span class="skTickerDot">•</span><span class="skTickerItem">⏱ 20–30 min</span><span class="skTickerDot">•</span><span class="skTickerItem">⚡ Near & Fast</span><span class="skTickerDot">•</span><span class="skTickerItem">🔥 Fresh & Hot</span><span class="skTickerDot">•</span><span class="skTickerItem">🚴 Fast Delivery</span></div></div>'}'''
new = '''function skProductTicker(){return '<div class="skProductTicker"><div class="skTickerTrack"><span class="skTickerItem">⏱ 20–30 min</span><span class="skTickerDot">•</span><span class="skTickerItem">⚡ Near & Fast</span><span class="skTickerDot">•</span><span class="skTickerItem">🔥 Fresh & Hot</span><span class="skTickerDot">•</span><span class="skTickerItem">🚴 Fast Delivery</span></div></div>'}'''
if old in s:
    s = s.replace(old, new, 1)

# 2) Remove obsolete customer OTP/login UI completely.
old_login = '<input id="loginPhone" class="input" placeholder="+91XXXXXXXXXX" inputmode="tel"><button class="primary" onclick="sendOtp()">Send OTP</button><div id="otpbox" class="otpbox"><input id="otp" class="input" placeholder="6 digit OTP" inputmode="numeric"><button class="primary" onclick="verifyOtp()">Verify OTP</button></div><div id="loginMsg" class="notice"></div>'
s = s.replace(old_login, '', 1)

# 3) Remove obsolete 5 km wording.
s = s.replace('₹30 up to 5 km', '₹30')
s = s.replace('Delivery ₹30 up to 5 km', 'Delivery ₹30')

# 4) Sold Out must appear only once: the availability label. Remove the duplicate disabled button text.
s = s.replace(":`<button class=\"add\" disabled>Sold Out</button>`}", ":''}")

# 5) Remove the duplicate service metadata row; the hero already carries delivery/minimum/COD information.
s = s.replace('<div class="serviceMeta">📍 Nansa Gate, Nawalgarh &nbsp;•&nbsp; 🚚 Delivery ₹30 &nbsp;•&nbsp; ₹100 minimum &nbsp;•&nbsp; 💵 COD</div>', '', 1)

# 6) Remove the duplicate help block that repeats Call Support/WhatsApp and the support number.
s = s.replace('<div class="help"><b>☎ Help Center</b><div class="small">Order/help: 7891851475</div><button class="link" onclick="callShop()">📞 Call</button><button class="link" onclick="waShop()">💬 WhatsApp</button></div>', '', 1)

p.write_text(s, encoding='utf-8')
print('Customer duplicate cleanup applied: single product ticker, single Sold Out label, no OTP UI, no 5 km wording, no duplicate service metadata, no duplicate Help Center block.')
