/* FINAL CATEGORY PHOTO FIX - one image per category, persistent after taps */
(function(){
  if(window.__SK_CATEGORY_PHOTO_FINAL_JS__) return;
  window.__SK_CATEGORY_PHOTO_FINAL_JS__=true;
  var MAP={
    'all':'samosa','fast food':'pizza','snacks':'samosa','chaat special':'dahi-bhalla-1',
    'indian thali':'paneer-tikka','desi rasoi':'manchurian','birthday special':'milk-cake',
    'beverages':'burger','sweets':'gulab-jamun','restaurant hotel':'pizza'
  };
  function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ')}
  function label(cat){
    var saved=cat.getAttribute('data-sk-category-label'); if(saved)return saved;
    var c=cat.cloneNode(true);
    c.querySelectorAll('img,picture,svg,.skFinalCatPhoto,.skCatPhoto,.skCatPhotoV4').forEach(function(x){x.remove()});
    return (c.textContent||'').replace(/\s+/g,' ').trim();
  }
  function srcFor(name){
    var key=MAP[norm(name)],data=window.SK_IMAGES&&key?window.SK_IMAGES[key]:'';
    if(!data)return '';
    return data.indexOf('data:')===0?data:'data:image/jpeg;base64,'+data;
  }
  function fix(){
    var root=document.getElementById('cats'); if(!root)return;
    root.querySelectorAll('.cat').forEach(function(cat){
      var name=label(cat); if(!name)return;
      cat.setAttribute('data-sk-category-label',name);
      var src=srcFor(name); if(!src)return;
      while(cat.firstChild)cat.removeChild(cat.firstChild);
      var box=document.createElement('span'); box.className='skFinalCatPhoto';
      box.style.cssText='display:block!important;width:100%;height:68px;overflow:hidden;border-radius:11px 11px 0 0;background:#f4e4c5';
      var img=document.createElement('img'); img.src=src; img.alt=name; img.loading='eager'; img.decoding='sync';
      img.style.cssText='display:block!important;width:100%;height:100%;object-fit:cover;visibility:visible;opacity:1';
      var text=document.createElement('span'); text.className='skFinalCatLabel'; text.textContent=name;
      text.style.cssText='display:block!important;padding:5px 4px 7px;text-align:center;font-weight:800;font-size:11px;line-height:1.15';
      box.appendChild(img); cat.appendChild(box); cat.appendChild(text);
    });
  }
  function run(){fix();[100,300,700,1500,3000,6000].forEach(function(t){setTimeout(fix,t)})}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#cats .cat'))setTimeout(fix,50)},true);
  new MutationObserver(function(){setTimeout(fix,50)}).observe(document.documentElement,{childList:true,subtree:true});
})();
