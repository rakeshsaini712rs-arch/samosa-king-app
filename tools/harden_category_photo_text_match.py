from pathlib import Path

p=Path('app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
marker='SK_CATEGORY_PHOTOS_MATCH_HARDEN_20261002'
if marker in s:
    print('Category photo text-match hardening already present.')
    raise SystemExit(0)

needle="/* SK_CATEGORY_PHOTOS_REAL_LOCAL_20261002 */"
if needle not in s:
    raise SystemExit('Real category photo patch is not present in index.html')

# Make the runtime category-name lookup tolerant of whitespace and slash formatting.
s=s.replace("function cleanText(el){return (el.textContent||'').replace(/\\\\s+/g,' ').trim();}", "/* SK_CATEGORY_PHOTOS_MATCH_HARDEN_20261002 */ function cleanText(el){return (el.textContent||'').replace(/\\s+/g,' ').trim().replace(/\\s*\\/\\s*/g,' / ');}")
s=s.replace("var key=cleanText(el);\n      var src=MAP[key];", "var key=cleanText(el);\n      var src=MAP[key];\n      if(!src){var compact=key.replace(/\\s*\\/\\s*/g,'/');Object.keys(MAP).some(function(k){if(k.replace(/\\s*\\/\\s*/g,'/')===compact){src=MAP[k];return true;}return false;});}")

p.write_text(s,encoding='utf-8')
print('Category photo matching hardened.')
