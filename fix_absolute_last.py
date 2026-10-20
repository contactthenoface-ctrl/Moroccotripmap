import os, re
from pathlib import Path

print("🛠️ --- HARMONISATION DES 2 DERNIÈRES PAGES --- 🛠️\n")

source_page = Path('marrakech.html')
if not source_page.exists():
    source_page = Path('index.html')

with open(source_page, 'r', encoding='utf-8', errors='ignore') as f:
    official_header = re.search(r'(<header[\s\S]*?</header>)', f.read(), re.IGNORECASE).group(1)

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
fixed = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if 'lang-menu-button' not in content and '<header' in content:
        new_content = re.sub(r'<header[\s\S]*?</header>', official_header, content, flags=re.IGNORECASE)
        html_file.write_text(new_content, encoding='utf-8')
        print(f"✅ Header appliqué sur : {html_file}")
        fixed += 1

print(f"\n✨ {fixed} page(s) harmonisée(s) avec succès !")
