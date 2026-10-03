package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
  private WebView web;
  private static final String FIX_CSS = "<style>html{scroll-behavior:smooth}.section{display:block!important;visibility:visible!important;opacity:1!important;content-visibility:visible!important;scroll-margin-top:175px}.cards{display:grid!important;visibility:visible!important;opacity:1!important}.card,.photo,.photo img{visibility:visible!important;opacity:1!important}.photo img{display:block!important;height:132px!important;width:100%!important;object-fit:cover!important}.section.hidden,.section[hidden]{display:block!important}.section.selected{display:block!important}#cats .cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;min-height:100px!important;background:#fff!important}.skCategoryPhoto{display:block!important;width:100%!important;height:68px!important;min-height:68px!important;flex:0 0 68px!important;overflow:hidden!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}.skCategoryPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}.skCategoryLabel{display:block!important;padding:6px 3px 8px!important;text-align:center!important;line-height:1.15!important;font-weight:800!important;font-size:11px!important;color:inherit!important}</style>";

  private static final String CATEGORY_JS = "" +
    "(function(){if(window.__SK_CAT_PHOTO_V2__)return;window.__SK_CAT_PHOTO_V2__=true;"+
    "var map=[['all','samosa'],['fast food','pizza'],['snacks','samosa'],['chaat special','dahi'],['indian thali','thali'],['desi rasoi','sabji'],['birthday special','cake'],['beverages','drink'],['sweets','laddu'],['restaurant hotel','dosa']];"+
    "function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\\s+/g,' ')}"+
    "function key(t){t=norm(t);for(var i=0;i<map.length;i++){if(t===map[i][0])return i;if(t.indexOf(map[i][0])>=0)return i}return 0}"+
    "function art(i){var foods=[['#f6d49b','#fff4d6','SAMOSA'],['#f3c2a2','#fff0dc','PIZZA'],['#f7d7a8','#fff3dc','SNACKS'],['#cce8d0','#eff9ef','CHAAT'],['#f4d6a0','#fff5df','THALI'],['#d9e7c7','#f2f8ec','DESI'],['#f7c7d5','#fff0f5','CAKE'],['#cce8f4','#eff9ff','DRINK'],['#ead2f0','#faf0ff','SWEET'],['#ddd8cc','#f6f4ef','FOOD']][i%10];var svg='<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 600 260\"><defs><linearGradient id=\"g\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"><stop stop-color=\"'+art[0]+'\"/><stop offset=\"1\" stop-color=\"'+art[1]+'\"/></linearGradient></defs><rect width=\"600\" height=\"260\" rx=\"28\" fill=\"url(#g)\"/><ellipse cx=\"300\" cy=\"185\" rx=\"150\" ry=\"30\" fill=\"#00000018\"/><circle cx=\"300\" cy=\"125\" r=\"78\" fill=\"#fff\" opacity=\".72\"/><text x=\"300\" y=\"145\" text-anchor=\"middle\" font-family=\"Arial,sans-serif\" font-size=\"38\" font-weight=\"900\" fill=\"#6b421d\">'+art[2]+'</text></svg>';return 'data:image/svg+xml;charset=UTF-8,'+encodeURIComponent(svg)}"+
    "function product(cat,i){var k=map[i][1];var found='';document.querySelectorAll('.card').forEach(function(c){if(found)return;var tx=norm(c.textContent||'');if(tx.indexOf(k)>=0){var im=c.querySelector('.visual img,img');if(im)found=im.currentSrc||im.src||''}});return found}"+
    "function apply(){var root=document.getElementById('cats')||document.querySelector('.cats');if(!root)return;root.querySelectorAll('.cat').forEach(function(c,i){var idx=key(c.textContent);var old=c.querySelector('.skCategoryPhoto');var holder=old||document.createElement('span');holder.className='skCategoryPhoto';var im=holder.querySelector('img')||document.createElement('img');var src=product(c,idx)||art(idx);im.src=src;im.alt='';im.loading='eager';im.decoding='sync';im.onerror=function(){im.src=art(idx)};if(!im.parentNode)holder.appendChild(im);var lab=c.querySelector('.skCategoryLabel')||document.createElement('span');lab.className='skCategoryLabel';lab.textContent=(c.getAttribute('data-label')||c.textContent||'').replace(/\\s+/g,' ').trim().replace(/category/ig,'').trim();if(holder.parentNode!==c)c.insertBefore(holder,c.firstChild);if(lab.parentNode!==c)c.appendChild(lab);})}"+
    "function run(){apply();[100,400,900,1800,3500,7000].forEach(function(t){setTimeout(apply,t)})}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();new MutationObserver(function(){clearTimeout(window.__skct);window.__skct=setTimeout(apply,150)}).observe(document.documentElement,{childList:true,subtree:true});})();";

  @Override public void onCreate(Bundle b){
    super.onCreate(b);
    web=new WebView(this);
    setContentView(web);
    WebSettings s=web.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    s.setLoadWithOverviewMode(false);
    web.setWebViewClient(new WebViewClient(){
      @Override public void onPageFinished(WebView v,String url){
        v.evaluateJavascript("(function(){var st=document.createElement('style');st.textContent="+q(FIX_CSS)+";document.head.appendChild(st);"+CATEGORY_JS+"document.querySelectorAll('.section').forEach(function(x){x.style.display='block';x.style.visibility='visible';x.style.opacity='1'});document.querySelectorAll('.cards,.card,.photo,.photo img').forEach(function(x){x.style.visibility='visible';x.style.opacity='1'});})();",null);
      }
    });
    web.loadDataWithBaseURL(null,"<!doctype html><html><head><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Samosa King</title></head><body><div id=\"app\"></div><script>document.addEventListener('click',function(e){var c=e.target.closest('.cat');if(!c)return;setTimeout(function(){document.querySelectorAll('.section').forEach(function(x){x.style.display='block';x.style.visibility='visible';x.style.opacity='1'});document.querySelectorAll('.cards,.card,.photo,.photo img').forEach(function(x){x.style.visibility='visible';x.style.opacity='1'});},50)},true);</script><!-- CLEAN_HELP_CENTER_CALL_WHATSAPP_V1 --><script>/* CUSTOMER_FOOTER_CLEANUP_V1 */
(function(){
  function clean(){
    const needles=[
      'Delivery ₹30 up to 5 km','PaymentCash on Delivery','Open8:30 AM–6:00 PM','Help7891851475',
      '☎ Help Center','Order/help: 7891851475','Call💬 WhatsApp',
      '📍 Nansa Gate, Nawalgarh  •  🚚 Delivery ₹30  •  ₹100 minimum  •  💵 COD'
    ];
    document.querySelectorAll('body *').forEach(function(el){
      if(el.children.length===0){
        const t=(el.textContent||'').replace(/\\s+/g,' ').trim();
        if(needles.some(function(n){return t===n || t.includes(n)})){
          const box=el.closest('.helpbox') || el.parentElement;
          if(box && box.id==='helpSection') box.remove();
          else if(box && !box.id && box.children.length<=4) box.remove();
          else el.remove();
        }
      }
    });
    document.querySelectorAll('.helpbox').forEach(function(el){
      const t=(el.textContent||'').replace(/\\s+/g,' ').trim();
      if(t.includes('Order/help: 7891851475') || t.includes('Delivery ₹30 up to 5 km')) el.remove();
    });
  }
  new MutationObserver(clean).observe(document.documentElement,{childList:true,subtree:true});
  window.addEventListener('load',clean); setTimeout(clean,200); setTimeout(clean,1000);
})();</script></body></html>","text/html","UTF-8",null);
  }
  private static String q(String x){return "'"+x.replace("\\","\\\\").replace("'","\\'").replace("\n","\\n")+"'";}
}
