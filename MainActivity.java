package com.samosaking.nawalgarh;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
  private WebView web;
  private static final String FIX_CSS = "<style>html{scroll-behavior:smooth}.section{display:block!important;visibility:visible!important;opacity:1!important;content-visibility:visible!important;scroll-margin-top:175px}.cards{display:grid!important;visibility:visible!important;opacity:1!important}.card,.photo,.photo img{visibility:visible!important;opacity:1!important}.photo img{display:block!important;height:132px!important;width:100%!important;object-fit:cover!important}.section.hidden,.section[hidden]{display:block!important}.section.selected{display:block!important}</style>";
  @Override public void onCreate(Bundle b){super.onCreate(b);web=new WebView(this);setContentView(web);WebSettings s=web.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setLoadWithOverviewMode(false);web.setWebViewClient(new WebViewClient(){@Override public void onPageFinished(WebView v,String url){v.evaluateJavascript("(function(){var st=document.createElement('style');st.textContent="+q(FIX_CSS)+";document.head.appendChild(st);document.querySelectorAll('.section').forEach(function(x){x.style.display='block';x.style.visibility='visible';x.style.opacity='1'});document.querySelectorAll('.cards,.card,.photo,.photo img').forEach(function(x){x.style.visibility='visible';x.style.opacity='1'});})();",null);}});web.loadDataWithBaseURL(null,"<!doctype html><html><head><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Samosa King</title></head><body><div id=\"app\"></div><script>document.addEventListener('click',function(e){var c=e.target.closest('.cat');if(!c)return;setTimeout(function(){document.querySelectorAll('.section').forEach(function(x){x.style.display='block';x.style.visibility='visible';x.style.opacity='1'});document.querySelectorAll('.cards,.card,.photo,.photo img').forEach(function(x){x.style.visibility='visible';x.style.opacity='1'});},50)},true);</script><!-- CLEAN_HELP_CENTER_CALL_WHATSAPP_V1 --></body></html>","text/html","UTF-8",null);}
  private static String q(String x){return "'"+x.replace("\\","\\\\").replace("'","\\'").replace("\n","\\n")+"'";}
}
