from pathlib import Path

p = Path('app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
old = '<style id="skRemoveCategoryBar">/* FINAL_REMOVE_CATEGORY_BAR_20261003 */ #cats,.cats{display:none!important;height:0!important;min-height:0!important;margin:0!important;padding:0!important;border:0!important;overflow:hidden!important}</style>'
if old in s:
    s = s.replace(old, '')
elif 'id="skRemoveCategoryBar"' in s:
    import re
    s = re.sub(r'<style id="skRemoveCategoryBar">.*?</style>', '', s, count=1, flags=re.S)
else:
    print('Category hide rule not present; nothing to remove.')
p.write_text(s, encoding='utf-8')
print('CATEGORY BAR HIDE RULE REMOVED')
