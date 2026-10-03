package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
  private WebView web;
  private static final String FIX_CSS = "<style>html{scroll-behavior:smooth}.section{display:block!important;visibility:visible!important;opacity:1!important;content-visibility:visible!important;scroll-margin-top:175px}.cards{display:grid!important;visibility:visible!important;opacity:1!important}.card,.photo,.photo img{visibility:visible!important;opacity:1!important}.photo img{display:block!important;height:132px!important;width:100%!important;object-fit:cover!important}.section.hidden,.section[hidden]{display:block!important}.section.selected{display:block!important}#cats,#cats *,.cats,.cats *,.category-bar,.categoryBar,.categories,.category-chips,.category-nav{display:none!important;visibility:hidden!important;height:0!important;min-height:0!important;max-height:0!important;overflow:hidden!important;padding:0!important;margin:0!important;border:0!important}</style>";

  private static final String CATEGORY_JS = "(function(){if(window.__SK_CAT_BAR_REMOVED__)return;window.__SK_CAT_BAR_REMOVED__=true;function remove(){document.querySelectorAll('#cats,.cats,.category-bar,.categoryBar,.categories,.category-chips,.category-nav').forEach(function(x){x.remove()});}function clean(){remove();document.querySelectorAll('[class*=category],[id*=category]').forEach(function(x){var t=(x.textContent||'').trim();if(t.length>0&&t.length<300&&/All|Fast Food|Snacks|Chaat & Special|Indian Thali|Desi Rasoi|Birthday Special|Beverages|Sweets|Restaurant \/ Hotel/.test(t))x.remove();});}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',clean);else clean();new MutationObserver(function(){clean()}).observe(document.documentElement,{childList:true,subtree:true});})();";

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
    web.loadDataWithBaseURL(null,"<!doctype html><html><head><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Samosa King</title></head><body><div id=\"app\"></div><script>document.addEventListener('click',function(e){setTimeout(function(){document.querySelectorAll('#cats,.cats,.category-bar,.categoryBar,.categories,.category-chips,.category-nav').forEach(function(x){x.remove()});},50)},true);</script><script>/* CUSTOMER_FOOTER_CLEANUP_V1 */
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
