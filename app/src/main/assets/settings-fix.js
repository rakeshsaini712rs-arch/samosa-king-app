(function(){
function el(id){return document.getElementById(id)}
function show(id){var x=el(id);if(!x)return;x.style.display='block';x.style.zIndex='9999';x.style.pointerEvents='auto'}
function hide(id){var x=el(id);if(x){x.style.display='none';x.style.pointerEvents='none'}}
function bind(id,fn){var x=el(id);if(x&&!x.__skBound){x.__skBound=1;x.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();fn()})}}
function init(){
 bind('settingsOpenFix',function(){show('settingsModal')});
 var main=document.querySelector('.settingsMainBtn');if(main&&!main.__skBound){main.__skBound=1;main.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();show('settingsModal')})}
 var list=document.querySelectorAll('#settingsModal .settingsList button');
 list.forEach(function(b){if(b.__skBound)return;b.__skBound=1;b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();var t=(b.textContent||'').trim();
  if(t.indexOf('Payment')>=0){hide('settingsModal');show('paymentSettingsModal')}
  else if(t.indexOf('About')>=0){hide('settingsModal');show('aboutModal')}
  else if(t.indexOf('Log out')>=0){hide('settingsModal');if(window.AndroidBridge&&AndroidBridge.logout)AndroidBridge.logout();else{localStorage.clear();alert('Logged out successfully.')}} 
  else if(t.indexOf('Profile')>=0){hide('settingsModal');if(typeof openProfile==='function')openProfile();else show('profileModal')}
  else if(t.indexOf('Order')>=0){hide('settingsModal');if(typeof openHistory==='function')openHistory()}
  else if(t.indexOf('Address')>=0){hide('settingsModal');show('addressBookModal')}
  else if(t.indexOf('Collection')>=0){hide('settingsModal');show('collectionModal')}
  else if(t.indexOf('Feedback')>=0){hide('settingsModal');show('feedbackModal')}
 })});
 var closeIds=['settingsModal','paymentSettingsModal','aboutModal','profileModal','addressBookModal','collectionModal','feedbackModal'];
 closeIds.forEach(function(mid){var m=el(mid);if(m){var b=m.querySelector('.close');if(b&&!b.__skBound){b.__skBound=1;b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();hide(mid)})}}});
 var pay=document.querySelectorAll('#paymentSettingsModal .payOptions button');
 pay.forEach(function(b){if(b.__skBound)return;b.__skBound=1;b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();var t=(b.textContent||'').toLowerCase();
  if(t.indexOf('phonepe')>=0){if(window.AndroidBridge&&AndroidBridge.openUpi)AndroidBridge.openUpi('phonepe');}
  else if(t.indexOf('cred')>=0){if(window.AndroidBridge&&AndroidBridge.openUpi)AndroidBridge.openUpi('cred');}
  else if(t.indexOf('whatsapp')>=0){if(window.AndroidBridge&&AndroidBridge.openUpi)AndroidBridge.openUpi('whatsapp');}
  else if(t.indexOf('qr')>=0){show('paymentQr');if(typeof showPaymentQr==='function')showPaymentQr()}
  else if(t.indexOf('cash')>=0){localStorage.setItem('skPaymentMethod','COD');alert('Cash on Delivery selected.')}
 })});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();