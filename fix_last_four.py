import os, re
from pathlib import Path

print("🛠️ --- NETTOYAGE ET HARMONISATION FINALE --- 🛠️\n")

source_page = Path('marrakech.html')
if not source_page.exists():
    source_page = Path('index.html')

with open(source_page, 'r', encoding='utf-8', errors='ignore') as f:
    official_header = re.search(r'(<header[\s\S]*?</header>)', f.read(), re.IGNORECASE).group(1)

target_files = [
    Path('restaurants/index.html'),
    Path('images/blog/index.html'),
    Path('moroccotripmap/restaurants/index.html'),
    Path('moroccotripmap/images/blog/index.html')
]

for file_path in target_files:
    if file_path.exists():
        # Si c'est un faux index dans un dossier d'images, on peut le supprimer s'il n'a pas de contenu
        if 'images' in file_path.parts:
            file_path.unlink()
            print(f"🗑️ Supprimé (faux fichier dans dossier images) : {file_path}")
        else:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            new_content = re.sub(r'<header[\s\S]*?</header>', official_header, content, flags=re.IGNORECASE)
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✅ Header officiel appliqué : {file_path}")

print("\n✨ Nettoyage terminé !")
