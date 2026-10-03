if(window.__skSettingsFixInstalled){/* already installed */}else{window.__skSettingsFixInstalled=true;
(function(){
function q(s){return document.querySelector(s)} function id(s){return document.getElementById(s)}
function show(s){var x=id(s);if(x){x.style.setProperty('display','block','important');x.style.setProperty('visibility','visible','important');x.style.setProperty('opacity','1','important');x.style.setProperty('pointer-events','auto','important');x.style.setProperty('z-index','999999','important')}}
function hide(s){var x=id(s);if(x){x.style.setProperty('display','none','important');x.style.setProperty('pointer-events','none','important')}}
function act(t){t=(t||'').toLowerCase();if(t.indexOf('payment')>=0){hide('settingsModal');show('paymentSettingsModal');return}if(t.indexOf('about')>=0){hide('settingsModal');show('aboutModal');return}if(t.indexOf('log out')>=0){hide('settingsModal');if(window.AndroidBridge&&AndroidBridge.logout)AndroidBridge.logout();else{localStorage.clear();alert('Logged out successfully.')}return}if(t.indexOf('profile')>=0&&typeof openProfile==='function'){hide('settingsModal');openProfile();return}if(t.indexOf('order')>=0&&typeof openHistoryFromSettings==='function'){hide('settingsModal');openHistoryFromSettings();return}if(t.indexOf('address')>=0&&typeof openAddressBook==='function'){hide('settingsModal');openAddressBook();return}if(t.indexOf('collection')>=0&&typeof openCollection==='function'){hide('settingsModal');openCollection();return}if(t.indexOf('feedback')>=0&&typeof openFeedback==='function'){hide('settingsModal');openFeedback();return}}
function install(){document.querySelectorAll('.settingsMainBtn').forEach(function(b){b.style.setProperty('position','relative','important');b.style.setProperty('z-index','1000001','important');b.style.setProperty('pointer-events','auto','important')});document.querySelectorAll('.settingsPanel,.settingsList,.settingsList button,.payOptions,.payOptions button').forEach(function(b){b.style.setProperty('pointer-events','auto','important')});document.addEventListener('click',function(e){var t=e.target;var main=t.closest&&t.closest('.settingsMainBtn');if(main){e.preventDefault();e.stopImmediatePropagation();show('settingsModal');return}var b=t.closest&&t.closest('#settingsModal .settingsList button');if(b){e.preventDefault();e.stopImmediatePropagation();act(b.textContent);return}var p=t.closest&&t.closest('#paymentSettingsModal .payOptions button');if(p){e.preventDefault();e.stopImmediatePropagation();var z=(p.textContent||'').toLowerCase();var bridge=window.AndroidBridge;if(z.indexOf('phonepe')>=0&&bridge&&typeof bridge.openUpi==='function')bridge.openUpi('phonepe');else if(z.indexOf('cred')>=0&&bridge&&typeof bridge.openUpi==='function')bridge.openUpi('cred');else if(z.indexOf('whatsapp')>=0&&bridge&&typeof bridge.openUpi==='function')bridge.openUpi('whatsapp');else if(z.indexOf('qr')>=0&&typeof showPaymentQr==='function')showPaymentQr();else if(z.indexOf('cash')>=0){localStorage.setItem('skPaymentMethod','COD');alert('Cash on Delivery selected.')}return}var c=t.closest&&t.closest('.modal .close');if(c){e.preventDefault();e.stopImmediatePropagation();var mm=c.closest('.modal');if(mm)hide(mm.id)}},true)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
}
(function(){
function removeOtpUi(){
 var badText=['send otp','verify otp','help center','order/help:'];
 document.querySelectorAll('input,button,a,label,span,div,p').forEach(function(el){
  var t=(el.textContent||'').trim().toLowerCase();
  var ph=((el.getAttribute&&el.getAttribute('placeholder'))||'').toLowerCase();
  var val=((el.getAttribute&&el.getAttribute('value'))||'').toLowerCase();
  if(el.tagName==='INPUT'&&(ph.indexOf('+91')>=0||ph.indexOf('otp')>=0||val.indexOf('+91')>=0)){var p=el.closest('.login,.otpbox,.help')||el.parentElement;if(p&&p!==document.body)p.remove();else el.remove();return}
  if((t==='send otp'||t==='verify otp')){var p=el.closest('div,section,.login,.help')||el;p.remove();return}
  if(t.indexOf('help center')>=0&&t.indexOf('order/help')>=0){var p=el.closest('.help,.services,.info,div')||el;p.remove();return}
  if(t==='help center'){var p=el.closest('.help,.services,.info,div')||el;p.remove();return}
 });
 document.querySelectorAll('.otpbox,#otpbox,[id*=otp],[class*=otp]').forEach(function(el){el.remove()});
}
function installOtpRemoval(){removeOtpUi();var o=new MutationObserver(function(){removeOtpUi()});o.observe(document.documentElement,{childList:true,subtree:true});window.__skOtpObserver=o}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',installOtpRemoval);else installOtpRemoval();
})();