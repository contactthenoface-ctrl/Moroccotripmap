import os
from pathlib import Path

print("🛠️ --- CORRECTION DES TITRES HTML --- 🛠️\n")

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
fixed_titles = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Vérifier si la balise title est absente ou vide
    if '<title>' not in content or '</title>' not in content:
        page_name = html_file.stem.replace('-', ' ').title()
        new_title = f"<title>MoroccoTripMap - {page_name}</title>"
        
        # Insérer après <head>
        if '<head>' in content:
            content = content.replace('<head>', f'<head>\n    {new_title}')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Titre ajouté pour : {html_file}")
            fixed_titles += 1

print(f"\n✨ Terminé ! {fixed_titles} titre(s) corrigé(s).")
