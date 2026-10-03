from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text(encoding='utf-8')

# Category menu stays available, but category PHOTOS are intentionally removed for now.
# Delete the old embedded-photo implementation if a previous build inserted it.
for style_id in ('categoryPhotoEmbeddedFinalCss', 'skRemoveCategoryBar'):
    marker = f'<style id="{style_id}">'
    start = s.find(marker)
    if start >= 0:
        end = s.find('</style>', start)
        if end >= 0:
            s = s[:start] + s[end + len('</style>'):]

script_marker = '<script id="categoryPhotoEmbeddedFinal">'
start = s.find(script_marker)
if start >= 0:
    end = s.find('</script>', start)
    if end >= 0:
        s = s[:start] + s[end + len('</script>'):]

# Keep a simple, stable text-only category bar. No category image assets are injected.
css = '''<style id="categoryPhotoRemovedFinalCss">
#cats{display:flex!important;overflow-x:auto!important;overflow-y:hidden!important;gap:8px!important;padding:10px 12px!important;visibility:visible!important;opacity:1!important;min-height:0!important}
#cats .cat{display:flex!important;flex:0 0 auto!important;width:auto!important;height:auto!important;min-height:44px!important;padding:9px 12px!important;box-sizing:border-box!important;flex-direction:row!important;align-items:center!important;justify-content:center!important;gap:0!important;overflow:hidden!important;visibility:visible!important;opacity:1!important}
#cats .skCategoryPhoto,#cats .skEmbeddedPhoto{display:none!important}
#cats .skCategoryLabel,#cats .skEmbeddedLabel{display:block!important;padding:0!important;text-align:center!important;font-size:11px!important;line-height:1.15!important;font-weight:900!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
</style>'''

old = '<style id="categoryPhotoRemovedFinalCss">'
if old in s:
    a = s.find(old)
    b = s.find('</style>', a)
    if a >= 0 and b >= 0:
        s = s[:a] + s[b + len('</style>'):]

head = s.lower().rfind('</head>')
if head < 0:
    raise RuntimeError('index.html has no </head> marker')
s = s[:head] + css + s[head:]
html.write_text(s, encoding='utf-8')
print('CATEGORY_PHOTOS_REMOVED_FINAL_V1: category menu retained, category photos removed')
