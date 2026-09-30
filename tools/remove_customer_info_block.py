from pathlib import Path
import re

p = Path('app/src/main/assets/index.html')
text = p.read_text(encoding='utf-8')
pattern = r'<div id="info" class="info">.*?</div>\s*(?=<div class="section"><h2>📦 Your latest order</h2>)'
new_text, count = re.subn(pattern, '', text, count=1, flags=re.S)
if count != 1:
    raise SystemExit('ERROR: customer info block was not found exactly once')
p.write_text(new_text, encoding='utf-8')
print('Removed customer #info block containing Delivery/Payment/Open/Help rows.')
