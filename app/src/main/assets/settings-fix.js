/* FINAL CUSTOMER CATEGORY CLEANUP — 2026-10-02
 * Surgical fix only: remove duplicated category labels/cards while preserving
 * the existing native renderer, images, click handlers, products and prices.
 */
(function(){
  'use strict';
  if(window.__SK_CATEGORY_CLEAN_V1) return;
  window.__SK_CATEGORY_CLEAN_V1 = true;

  var ORDER = [
    'All', 'Fast Food', 'Snacks', 'Chaat & Special', 'Indian Thali',
    'Desi Rasoi', 'Birthday Special', 'Beverages', 'Sweets', 'Restaurant / Hotel'
  ];

  function cleanOneCat(el){
    if(!el) return false;
    var raw=(el.textContent||'').replace(/\s+/g,' ').trim();
    var label=null;
    for(var i=0;i<ORDER.length;i++){
      if(raw.indexOf(ORDER[i])!==-1){ label=ORDER[i]; break; }
    }
    if(!label) return false;

    var img=el.querySelector('img');
    var imgClone=img ? img.cloneNode(true) : null;
    var changed=false;

    /* Remove repeated text/spans but keep the first existing image. */
    var children=Array.prototype.slice.call(el.childNodes);
    children.forEach(function(n){
      if(n.nodeType===3){
        if((n.nodeValue||'').trim()){ n.remove(); changed=true; }
      }else if(n.nodeType===1 && n.tagName!=='IMG'){
        var t=(n.textContent||'').replace(/\s+/g,' ').trim();
        if(t && !n.classList.contains('sk-category-label')){
          n.remove(); changed=true;
        }
      }
    });

    if(!el.querySelector('.sk-category-label')){
      var s=document.createElement('span');
      s.className='sk-category-label';
      s.textContent=label;
      s.style.cssText='display:block!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;line-height:1.15!important;text-align:center!important;font-weight:800!important;';
      el.appendChild(s);
      changed=true;
    }else{
      el.querySelector('.sk-category-label').textContent=label;
    }

    /* If the native renderer had an image, never replace it with a duplicate. */
    if(imgClone && !el.querySelector('img')){
      el.insertBefore(imgClone,el.firstChild);
      changed=true;
    }
    return changed;
  }

  function cleanCategories(){
    var wrap=document.getElementById('cats') || document.querySelector('.cats');
    if(!wrap) return;
    var cats=Array.prototype.slice.call(wrap.querySelectorAll('.cat'));
    if(!cats.length) return;

    var seen={};
    cats.forEach(function(el){
      var raw=(el.textContent||'').replace(/\s+/g,' ').trim();
      var label=null;
      for(var i=0;i<ORDER.length;i++){
        if(raw.indexOf(ORDER[i])!==-1){label=ORDER[i];break;}
      }
      if(!label) return;
      if(seen[label]){
        el.remove();
      }else{
        seen[label]=true;
        cleanOneCat(el);
      }
    });

    /* Guarantee the intended order if the native renderer created duplicates. */
    var current=Array.prototype.slice.call(wrap.querySelectorAll('.cat'));
    var byLabel={};
    current.forEach(function(el){
      var t=(el.textContent||'').replace(/\s+/g,' ').trim();
      ORDER.forEach(function(x){if(!byLabel[x] && t.indexOf(x)!==-1) byLabel[x]=el;});
    });
    ORDER.forEach(function(label){
      if(byLabel[label]) wrap.appendChild(byLabel[label]);
    });
  }

  function run(){
    try{cleanCategories();}catch(e){}
  }

  run();
  setTimeout(run,50);
  setTimeout(run,250);
  setTimeout(run,700);
  setTimeout(run,1500);
  new MutationObserver(function(){run();}).observe(document.documentElement,{childList:true,subtree:true});
})();
