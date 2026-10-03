from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text(encoding='utf-8')
marker = 'FINAL_REMOVE_CATEGORY_BAR'
if marker in s:
    start = s.find('<style id="skRemoveCategoryBar">')
    end = s.find('</style>', start)
    if start >= 0 and end >= 0:
        s = s[:start] + s[end + len('</style>'):]
html.write_text(s, encoding='utf-8')
print('FINAL_CATEGORY_BAR_FIX: category bar hide rule removed; existing category-photo renderer preserved')
