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
var scheduled=false;
function paintImages(){
 scheduled=false;
 var cards=document.querySelectorAll('.card');
 for(var i=0;i<cards.length;i++){
  var card=cards[i],h=card.querySelector('h3'),v=card.querySelector('.visual');
  if(!h||!v)continue;
  var file=imageMap[h.textContent.trim()];
  if(!file)continue;
  var img=v.querySelector('img');
  if(!img){
   img=document.createElement('img');
   img.className='photo';
   img.alt=h.textContent.trim();
   img.loading='lazy';
   img.decoding='async';
   img.style.cssText='width:100%;height:100%;object-fit:cover;border-radius:13px;display:block;image-rendering:auto;-webkit-backface-visibility:hidden;backface-visibility:hidden;transform:translateZ(0)';
   v.innerHTML='';
   v.appendChild(img);
  }
  var src='product-images/'+file;
  if(img.getAttribute('src')!==src)img.src=src;
 }
}
function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(paintImages);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});else schedule();
setTimeout(schedule,700);
var observer=new MutationObserver(function(mutations){
 for(var i=0;i<mutations.length;i++){
  if(mutations[i].addedNodes&&mutations[i].addedNodes.length){schedule();break;}
 }
});
observer.observe(document.documentElement,{childList:true,subtree:true});
})();