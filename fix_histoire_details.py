import os, re
from pathlib import Path

print("🛠️ --- CORRECTION FINALE DES VARIANTES DU FOOTER --- 🛠️\n")

# Variantes exactes trouvées dans histoire.html
variants = [
    (r"Moroccan\s+Restaurants\s*&\s*Food", "footer.link_restaurants"),
    (r"Moroccan\s+Restaurants\s*&amp;\s*Food", "footer.link_restaurants"),
    (r"Transport\s*&\s*Rental\s+Cars", "footer.link_transport"),
    (r"Transport\s*&amp;\s*Rental\s+Cars", "footer.link_transport"),
]

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
modified_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    file_modified = [False]
    for pattern_str, key in variants:
        pattern = rf'(<a\s+)([^>]*?>)(\s*{pattern_str}\s*)(</a>)'
        
        def make_repl(k):
            def repl(match):
                prefix = match.group(1)
                attrs = match.group(2)
                inner = match.group(3)
                suffix = match.group(4)
                
                if 'data-i18n' not in attrs:
                    file_modified[0] = True
                    return f'{prefix}data-i18n="{k}" {attrs}{inner}{suffix}'
                return match.group(0)
            return repl

        html = re.sub(pattern, make_repl(key), html, flags=re.IGNORECASE)

    if file_modified[0]:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        modified_count += 1
        print(f"✅ Mis à jour : {html_file}")

print(f"\n✨ Correction appliquée sur {modified_count} fichier(s) HTML !")
