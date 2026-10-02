from pathlib import Path
import re

P = Path('app/src/main/assets/index.html')
s = P.read_text(encoding='utf-8')

# Remove every experimental category-photo patch. The app already has a native
# renderCats() implementation that creates one image + one label per category.
# The injected observers were repeatedly mutating that DOM and caused the
# AllAllAll / Fast FoodFast Food duplication.
ids = [
    'skRealCategoryPhotoStyle','skRealCategoryPhotoScript',
    'skCategoryPhotoDedupV2','skCategoryPhotoDedupV2Script',
    'skCategoryPhotoMatchV3','skCategoryPhotoMatchV3Script',
    'skCategoryPhotoMatchV4','skCategoryPhotoMatchV4Script',
    'skCategoryPhotoFinalStyle','skCategoryPhotoFinalScript',
    'customerCategoryPhotoDedupStyle','customerCategoryPhotoDedupScript'
]
for ident in ids:
    s = re.sub(r'<style id="' + re.escape(ident) + r'">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script id="' + re.escape(ident) + r'">.*?</script>', '', s, flags=re.S)

# Remove any duplicate marker blocks left by previous category experiments.
s = re.sub(r'<style id="skCategoryPhotoFinalStyle">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<script id="skCategoryPhotoFinalScript">.*?</script>', '', s, flags=re.S)

# Native renderCats() is now the only category renderer. Do not add observers.
P.write_text(s, encoding='utf-8')
print('Category photo experimental patches removed; native renderCats() preserved.')
