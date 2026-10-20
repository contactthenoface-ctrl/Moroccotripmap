import os, re
from pathlib import Path

print("🛠️ --- NETTOYAGE ULTIME DES FOOTERS (DESTINATIONS & HISTOIRE) --- 🛠️\n")

# Variations possibles des textes dans le HTML
mappings = [
    (r"Circuits\s*&\s*Itineraries", "footer.link_circuits"),
    (r"Circuits\s*&amp;\s*Itineraries", "footer.link_circuits"),
    (r"History\s+of\s+Morocco", "footer.link_history"),
    (r"Travel\s+Guides", "footer.link_guides"),
    (r"Desert\s+Tours\s*&\s*Activities", "footer.link_culture"),
    (r"Desert\s+Tours\s*&amp;\s*Activities", "footer.link_culture"),
    (r"Authentic\s+Riads\s*&\s*Hotels", "footer.link_stays"),
    (r"Authentic\s+Riads\s*&amp;\s*Hotels", "footer.link_stays"),
    (r"Moroccan\s+Restaurants", "footer.link_restaurants"),
    (r"Transport\s*&\s*Car\s+Rental", "footer.link_transport"),
    (r"Transport\s*&amp;\s*Car\s+Rental", "footer.link_transport"),
    (r"Blog", "footer.link_blog"),
    (r"Contact", "footer.link_contact"),
    (r"Categories", "footer.categories_title"),
    (r"Destinations", "footer.destinations_title")
]

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
modified_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    file_modified = [False]

    for pattern_str, key in mappings:
        # Remplacer dans les balises <a> ou <h4> qui n'ont pas encore data-i18n
        pattern = rf'(<(?:a|h4)\s+)([^>]*?>)(\s*{pattern_str}\s*)(</(?:a|h4)>)'
        
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
