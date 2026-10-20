import os, re
from pathlib import Path

html_files = list(Path('.').rglob('*.html'))
missing_links = set()

for file_path in html_files:
    if 'node_modules' in file_path.parts:
        continue
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        links = re.findall(r'href=["\']([^"\']+\.html)["\']', content)
        for link in links:
            if link.startswith(('http://', 'https://', 'mailto:')):
                continue
            target_path = (file_path.parent / link).resolve()
            if not target_path.exists():
                missing_links.add((link, str(file_path)))

print('=== RÉSULTAT DU SCAN DES LIENS 404 ===')
if missing_links:
    for link, source in sorted(missing_links):
        print(f'❌ [Manquant] {link} (appelé depuis {source})')
else:
    print('✅ Aucun lien cassé trouvé !')
