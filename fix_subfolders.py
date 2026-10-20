import os, re
from pathlib import Path

print("🔧 --- CORRECTION DES CHEMINS POUR LES SOUS-DOSSIERS --- 🔧\n")

# Pages principales protégées (à la racine)
PROTECTED_ROOT = [
    'index.html', 'destinations.html', 'marrakech.html', 'contact.html',
    'agadir.html', 'essaouira.html', 'rabat.html', 'casablanca.html', 'fes.html',
    'chefchaouen.html', 'ouarzazate.html', 'tangier.html', 'tanger.html', 'meknes.html'
]

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
count = 0

for file_path in html_files:
    # Si le fichier est dans un sous-dossier (ex: restaurants/, hotels/, etc.)
    if len(file_path.parts) > 1 and file_path.name not in PROTECTED_ROOT:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Ajustement des chemins pour pointer vers la racine (../)
        # Logo
        content = re.sub(r'src=["\']images/logo\.webp["\']', 'src="../images/logo.webp"', content)
        content = re.sub(r'href=["\']index\.html["\']', 'href="../index.html"', content)
        content = re.sub(r'href=["\']destinations\.html["\']', 'href="../destinations.html"', content)
        content = re.sub(r'href=["\']contact\.html["\']', 'href="../contact.html"', content)
        
        # Feuilles de style et scripts
        content = re.sub(r'href=["\']css/', 'href="../css/', content)
        content = re.sub(r'src=["\']js/', 'src="../js/', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        count += 1

print(f"✅ Terminé ! {count} fichiers dans des sous-dossiers ont eu leurs chemins corrigés.")
