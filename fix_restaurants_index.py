import os, re
from pathlib import Path

print("🛠️ --- HARMONISATION DES FICHIERS RESTAURANTS/INDEX --- 🛠️\n")

source_page = Path('marrakech.html')
if not source_page.exists():
    source_page = Path('index.html')

with open(source_page, 'r', encoding='utf-8', errors='ignore') as f:
    official_header = re.search(r'(<header[\s\S]*?</header>)', f.read(), re.IGNORECASE).group(1)

# Ajuster le chemin relatif pour les sous-dossiers (href="../index.html" etc.)
header_for_subfolder = official_header.replace('href="', 'href="../').replace('href="../http', 'href="http').replace('href="../#', 'href="#')

targets = [
    Path('restaurants/index.html'),
    Path('moroccotripmap/restaurants/index.html')
]

for file_path in targets:
    if file_path.exists():
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        if '<header' in content:
            new_content = re.sub(r'<header[\s\S]*?</header>', header_for_subfolder, content, flags=re.IGNORECASE)
        else:
            # Insérer directement après <body> si pas de balise header
            new_content = re.sub(r'(<body[^>]*?>)', r'\1\n' + header_for_subfolder, content, flags=re.IGNORECASE)
            
        file_path.write_text(new_content, encoding='utf-8')
        print(f"✅ Header appliqué avec succès : {file_path}")

print("\n✨ Traitement terminé !")
