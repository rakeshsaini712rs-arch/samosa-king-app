(function(){'use strict';
var imageMap={
 'Samosa':'samosa.jpg','Kachori':'samosa.jpg','Mirchi Bada':'mirchi-bada.jpg',
 'Dahi Bhalla Plate 1':'dahi-bhalla-1.jpg','Dahi Bhalla Plate 2':'dahi-bhalla-2.jpg',
 'Pizza':'pizza.jpg','Wraps':'wraps.jpg','Momos':'momos.jpg','Burger':'burger.jpg',
 'Pasta':'pasta.jpg','Manchurian':'manchurian.jpg','Kaju Katli':'kaju-katli.jpg',
 'Rasgulla':'rasgulla.jpg','Rajbhog':'rasgulla.jpg','Gulab Jamun':'gulab-jamun.jpg',
 'Sohan Papdi':'sohan-papdi.jpg','Milk Cake':'milk-cake.jpg','Kalakand':'kalakand.jpg',
 'Dilkushal':'dilkushal.jpg','Peda':'milk-cake.jpg','Petha':'kalakand.jpg',
 'Namkin':'sohan-papdi.jpg','Rasmalai':'dahi-bhalla-1.jpg','Dahi (Curd)':'dahi-bhalla-2.jpg'
};
function paintImages(){document.querySelectorAll('.card').forEach(function(card){var h=card.querySelector('h3'),v=card.querySelector('.visual');if(!h||!v)return;var file=imageMap[h.textContent.trim()];if(!file)return;var img=v.querySelector('img');if(!img){img=document.createElement('img');v.innerHTML='';v.appendChild(img)}img.className='photo';img.alt=h.textContent.trim();img.loading='eager';img.decoding='async';img.style.cssText='width:100%;height:100%;object-fit:cover;border-radius:13px;display:block;image-rendering:auto;-webkit-backface-visibility:hidden;backface-visibility:hidden;transform:translateZ(0)';img.src='product-images/'+file;});}
function bindOrder(){var b=document.querySelector('.order');if(!b||b.dataset.skRuntime==='1')return;b.dataset.skRuntime='1';b.removeAttribute('onclick');b.addEventListener('click',function(){var n=(document.getElementById('name')?.value||'').trim(),p=(document.getElementById('phone')?.value||'').trim(),ad=(document.getElementById('address')?.value||'').trim(),msg=document.getElementById('msg');function err(t){if(msg){msg.textContent=t;msg.style.color='#c62828';msg.style.fontWeight='800';}return false;}if(typeof subtotal==='function'&&subtotal()<100)return err('Minimum order is ₹100.');if(!/^[\\p{L} ]{2,50}$/u.test(n))return err('Please enter a valid name (letters and spaces only).');if(!/^[6-9]\\d{9}$/.test(p))return err('Please enter a valid 10-digit mobile number.');if(!ad)return err('Please enter the delivery address.');if(msg){msg.textContent='';msg.style.color='';}if(typeof closeCart==='function')closeCart();var pm=document.getElementById('paymentChoiceModal'),op=document.getElementById('onlinePaymentBox');if(pm)pm.style.display='block';if(op)op.style.display='none';});}
function bind(){paintImages();bindOrder();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind);else bind();
setTimeout(bind,500);setTimeout(bind,1500);new MutationObserver(bind).observe(document.documentElement,{childList:true,subtree:true});
})();
