import os
from pathlib import Path

print("🔍 --- VÉRIFICATION DES HEADERS SUR TOUTES LES PAGES --- 🔍\n")

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
missing_header_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # On vérifie la présence du sélecteur de langue ou d'un élément clé du header officiel
    if 'lang-menu-button' not in content:
        print(f"⚠️ Page sans le header officiel : {html_file}")
        missing_header_count += 1

print(f"\n--- BILAN DE LA VÉRIFICATION ---")
print(f"📂 Total des pages HTML scannées : {len(html_files)}")
if missing_header_count == 0:
    print("✨ Parfait ! 100% des pages du site possèdent le header officiel et harmonisé.")
else:
    print(f"🚨 Il reste {missing_header_count} page(s) à harmoniser.")

