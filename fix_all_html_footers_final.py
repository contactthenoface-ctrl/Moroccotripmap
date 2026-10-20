import os, re
from pathlib import Path

print("🛠️ --- CORRECTION DÉFINITIVE DES LIENS DU FOOTER --- 🛠️\n")

# Mapping des textes de liens vers leurs clés i18n
link_mapping = {
    "Meknes Travel Guide": "footer.link_meknes",
    "Agadir Beaches": "footer.link_agadir",
    "Tangier Guide": "footer.link_tanger",
    "Marrakech Travel Guide": "footer.link_marrakech",
    "Fes Medina Guide": "footer.link_fes",
    "Chefchaouen Guide": "footer.link_chefchaouen",
    "Essaouira Guide": "footer.link_essaouira",
    "Merzouga Desert": "footer.link_merzouga",
    "Rabat Travel Guide": "footer.link_rabat",
    "Authentic Riads & Hotels": "footer.link_stays",
    "Moroccan Restaurants": "footer.link_restaurants",
    "Desert Tours & Activities": "footer.link_experiences",
    "Transport & Car Rental": "footer.link_transport",
    "Circuits & Itineraries": "footer.link_itineraries",
    "History of Morocco": "footer.link_history",
    "Travel Guides": "footer.link_guides",
    "Blog": "footer.link_blog",
    "Contact": "footer.link_contact"
}

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
modified_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    file_modified = [False]
    for text, key in link_mapping.items():
        # Chercher les balises <a> contenant le texte exact sans data-i18n
        pattern = rf'(<a\s+)([^>]*?)(\bhref=["\'][^"\']*["\'])([^>]*?>)(\s*{re.escape(text)}\s*)(</a>)'
        
        def make_repl(k):
            def repl(match):
                prefix = match.group(1)
                attrs1 = match.group(2)
                href = match.group(3)
                attrs2 = match.group(4)
                inner_text = match.group(5)
                suffix = match.group(6)
                
                full_attrs = attrs1 + href + attrs2
                if 'data-i18n' not in full_attrs:
                    file_modified[0] = True
                    return f'{prefix}{attrs1}{href} data-i18n="{k}"{attrs2}{inner_text}{suffix}'
                return match.group(0)
            return repl

        html = re.sub(pattern, make_repl(key), html, flags=re.IGNORECASE)

    if file_modified[0]:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        modified_count += 1

print(f"✅ Attributs data-i18n injectés avec succès dans {modified_count} fichiers HTML !")
