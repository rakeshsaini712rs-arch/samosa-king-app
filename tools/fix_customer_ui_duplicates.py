from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')

# The customer product ticker was literally rendered twice inside every card.
old = '''function skProductTicker(){return '<div class="skProductTicker"><div class="skTickerTrack"><span class="skTickerItem">⏱ 20–30 min</span><span class="skTickerDot">•</span><span class="skTickerItem">⚡ Near & Fast</span><span class="skTickerDot">•</span><span class="skTickerItem">🔥 Fresh & Hot</span><span class="skTickerDot">•</span><span class="skTickerItem">🚴 Fast Delivery</span><span class="skTickerDot">•</span><span class="skTickerItem">⏱ 20–30 min</span><span class="skTickerDot">•</span><span class="skTickerItem">⚡ Near & Fast</span><span class="skTickerDot">•</span><span class="skTickerItem">🔥 Fresh & Hot</span><span class="skTickerDot">•</span><span class="skTickerItem">🚴 Fast Delivery</span></div></div>'}'''
new = '''function skProductTicker(){return '<div class="skProductTicker"><div class="skTickerTrack"><span class="skTickerItem">⏱ 20–30 min</span><span class="skTickerDot">•</span><span class="skTickerItem">⚡ Near & Fast</span><span class="skTickerDot">•</span><span class="skTickerItem">🔥 Fresh & Hot</span><span class="skTickerDot">•</span><span class="skTickerItem">🚴 Fast Delivery</span></div></div>'}'''
if old not in s:
    raise SystemExit('Expected duplicated skProductTicker source was not found')
s = s.replace(old, new, 1)

# Remove the obsolete customer OTP block from the home page. Ordering does not use this login flow.
old_login = '<input id="loginPhone" class="input" placeholder="+91XXXXXXXXXX" inputmode="tel"><button class="primary" onclick="sendOtp()">Send OTP</button><div id="otpbox" class="otpbox"><input id="otp" class="input" placeholder="6 digit OTP" inputmode="numeric"><button class="primary" onclick="verifyOtp()">Verify OTP</button></div><div id="loginMsg" class="notice"></div>'
if old_login in s:
    s = s.replace(old_login, '', 1)
else:
    raise SystemExit('Expected OTP block was not found')

# The store no longer uses a 5 km delivery rule; keep the ₹30 delivery information.
s = s.replace('₹30 up to 5 km', '₹30')
s = s.replace('Delivery ₹30 up to 5 km', 'Delivery ₹30')

p.write_text(s, encoding='utf-8')
print('Customer UI duplicate fix applied: single delivery ticker, no obsolete OTP block, no 5 km wording.')
