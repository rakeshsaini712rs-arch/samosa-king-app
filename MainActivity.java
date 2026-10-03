package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
  private WebView web;
  private static final String FIX_CSS = "<style>html{scroll-behavior:smooth}.section{display:block!important;visibility:visible!important;opacity:1!important;content-visibility:visible!important;scroll-margin-top:175px}.cards{display:grid!important;visibility:visible!important;opacity:1!important}.card,.photo,.photo img{visibility:visible!important;opacity:1!important}.photo img{display:block!important;height:132px!important;width:100%!important;object-fit:cover!important}.section.hidden,.section[hidden]{display:block!important}.section.selected{display:block!important}#cats .cat{overflow:hidden!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;min-height:100px!important;background:#211914!important;border:1px solid #49392e!important;border-radius:14px!important}#cats .skCategoryPhoto{display:block!important;width:100%!important;height:68px!important;min-height:68px!important;flex:0 0 68px!important;overflow:hidden!important;border-radius:11px 11px 0 0!important;background:#f4e4c5!important}#cats .skCategoryPhoto img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;visibility:visible!important;opacity:1!important}#cats .skCategoryLabel{display:block!important;padding:7px 4px 9px!important;text-align:center!important;line-height:1.15!important;font-weight:900!important;font-size:11px!important;color:#fff!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}</style>";

  private static final String CATEGORY_JS = "" +
    "(function(){if(window.__SK_CAT_PHOTO_V4__)return;window.__SK_CAT_PHOTO_V4__=true;"+
    "var map=[['all','samosa.jpg','All'],['fast food','pizza.jpg','Fast Food'],['snacks','mirchi-bada.jpg','Snacks'],['chaat special','dahi-bhalla-1.jpg','Chaat & Special'],['indian thali','manchurian.jpg','Indian Thali'],['desi rasoi','pasta.jpg','Desi Rasoi'],['birthday special','gulab-jamun.jpg','Birthday Special'],['beverages','burger.jpg','Beverages'],['sweets','kaju-katli.jpg','Sweets'],['restaurant hotel','wraps.jpg','Restaurant / Hotel']];"+
    "var base='file:///android_asset/product-images/';"+
    "function norm(v){return String(v||'').toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim().replace(/\\s+/g,' ')}"+
    "function key(t){t=norm(t);for(var i=0;i<map.length;i++){if(t===map[i][0])return i;if(t.indexOf(map[i][0])>=0)return i}return 0}"+
    "function apply(){var root=document.getElementById('cats')||document.querySelector('.cats');if(!root)return;root.querySelectorAll('.cat').forEach(function(c){var raw=c.getAttribute('data-label')||c.textContent||'';var idx=key(raw);var holder=document.createElement('span');holder.className='skCategoryPhoto';var im=document.createElement('img');im.src=base+map[idx][1];im.alt='';im.loading='eager';im.decoding='sync';im.onerror=function(){if(im.dataset.fallback==='1')return;im.dataset.fallback='1';im.src=base+'samosa.jpg'};holder.appendChild(im);var lab=document.createElement('span');lab.className='skCategoryLabel';lab.textContent=map[idx][2];c.innerHTML='';c.appendChild(holder);c.appendChild(lab);c.setAttribute('data-sk-category',map[idx][0]);});}"+
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
    web.loadDataWithBaseURL(null,"<!doctype html><html><head><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Samosa King</title></head><body><div id=\"app\"></div><script>document.addEventListener('click',function(e){var c=e.target.closest('.cat');if(!c)return;setTimeout(function(){document.querySelectorAll('.section').forEach(function(x){x.style.display='block';x.style.visibility='visible';x.style.opacity='1'});document.querySelectorAll('.cards,.card,.photo,.photo img').forEach(function(x){x.style.visibility='visible';x.style.opacity='1'});},50)},true);</script><!-- CLEAN_HELP_CENTER_CALL_WHATSAPP_V1 --><script>(function(){function clean(){const needles=['Delivery ₹30 up to 5 km','PaymentCash on Delivery','Open8:30 AM–6:00 PM','Help7891851475','☎ Help Center','Order/help: 7891851475','Call💬 WhatsApp','📍 Nansa Gate, Nawalgarh  •  🚚 Delivery ₹30  •  ₹100 minimum  •  💵 COD'];document.querySelectorAll('body *').forEach(function(el){if(el.children.length===0){const t=(el.textContent||'').replace(/\\s+/g,' ').trim();if(needles.some(function(n){return t===n||t.includes(n)}) ){const box=el.closest('.helpbox')||el.parentElement;if(box&&box.id==='helpSection')box.remove();else if(box&&!box.id&&box.children.length<=4)box.remove();else el.remove();}}});document.querySelectorAll('.helpbox').forEach(function(el){const t=(el.textContent||'').replace(/\\s+/g,' ').trim();if(t.includes('Order/help: 7891851475')||t.includes('Delivery ₹30 up to 5 km'))el.remove();});}new MutationObserver(clean).observe(document.documentElement,{childList:true,subtree:true});window.addEventListener('load',clean);setTimeout(clean,200);setTimeout(clean,1000);})();</script><script>/* CUSTOMER_FOOTER_CLEANUP_V1 */
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
