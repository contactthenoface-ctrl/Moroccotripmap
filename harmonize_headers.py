import os, re
from pathlib import Path

print("🛠️ --- HARMONISATION DES HEADERS ET DU DESIGN --- 🛠️\n")

# 1. Extraire le Header officiel complet depuis marrakech.html ou index.html
source_page = Path('marrakech.html')
if not source_page.exists():
    source_page = Path('index.html')

with open(source_page, 'r', encoding='utf-8', errors='ignore') as f:
    source_content = f.read()

header_match = re.search(r'(<header[\s\S]*?</header>)', source_content, re.IGNORECASE)

if not header_match:
    print("❌ Impossible de trouver la balise <header> source.")
    exit()

official_header = header_match.group(1)

# 2. Scanner tous les fichiers HTML et remplacer leur header s'il est simplifié
html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
updated_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Si la page contient l'ancien header simplifié (par exemple sans le sélecteur de langue lang-menu-button)
    if 'lang-menu-button' not in content and '<header' in content:
        # Remplacer le header existant par le header officiel
        new_content = re.sub(r'<header[\s\S]*?</header>', official_header, content, flags=re.IGNORECASE)
        
        # Ajuster les chemins relatifs si la page est dans un sous-dossier (ex: places/ ou restaurants/)
        depth = len(html_file.parent.parts)
        if depth > 0 and html_file.parent != Path('.'):
            prefix = '../' * depth
            # Ajuster les liens principaux dans le header injecté
            # Ex: href="index.html" -> href="../index.html"
            def fix_paths(m):
                attr = m.group(1)
                path = m.group(2)
                if not path.startswith('http') and not path.startswith('#') and not path.startswith('/'):
                    return f'{attr}="{prefix}{path}"'
                return m.group(0)
            
            # Application sur href et src du header
            # (simple précaution pour la navigation)

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1
        print(f"✅ Header officiel injecté dans : {html_file}")

print(f"\n✨ Terminé ! {updated_count} pages ont été harmonisées avec le vrai Header officiel du site.")
