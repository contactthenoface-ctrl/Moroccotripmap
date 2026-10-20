import os, json
from pathlib import Path

print("🔍 --- INSPECTION DES TRADUCTIONS ET DU CODE --- 🔍\n")

# Check json
json_path = Path('js/translations/ar/destinations_page.json')
if json_path.exists():
    with open(json_path, 'r', encoding='utf-8') as f:
        print("Contenu de ar/destinations_page.json :")
        print(f.read()[:500]) # Afficher les 500 premiers caractères
else:
    print("❌ Fichier ar/destinations_page.json introuvable !")

print("\n--- Extrait du footer dans destinations.html ---")
dest_path = Path('destinations.html')
if dest_path.exists():
    with open(dest_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Trouver la partie footer
        footer_match = content[content.find('<footer'):content.find('</footer>')+9] if '<footer' in content else "Footer introuvable"
        print(footer_match[:600])

