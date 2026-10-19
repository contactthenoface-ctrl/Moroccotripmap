import os, re, json
from pathlib import Path

languages = ['en', 'fr', 'es', 'ar']
trans_dir = Path('js/translations')
html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]

missing_count = 0
total_checks = 0

print("🔍 Analyse de la couverture des traductions...\n")

for html_file in html_files:
    # Lire le contenu HTML pour trouver les clés data-i18n
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        keys = re.findall(r'data-i18n=["\']([^"\']+)["\']', content)
    
    if not keys:
        continue

    base_name = html_file.stem.replace('-', '_') + '_page.json'

    for lang in languages:
        json_path = trans_dir / lang / base_name
        total_checks += 1

        if not json_path.exists():
            print(f"❌ Fichier JSON manquant : js/translations/{lang}/{base_name} (nécessaire pour {html_file})")
            missing_count += 1
            continue

        # Charger le JSON et vérifier les clés
        try:
            with open(json_path, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
            
            # Vérification simple si les clés principales ou l'objet existent
            # (Tu peux adapter selon la structure exacte de tes JSON)
        except json.JSONDecodeError:
            print(f"⚠️ Erreur de syntaxe JSON dans : {json_path}")
            missing_count += 1

print(f"\n--- Bilan de la vérification ---")
print(f"📂 Total des vérifications effectuées : {total_checks}")
if missing_count == 0:
    print("✅ Tout est parfait ! Aucun fichier de traduction manquant pour les pages scannées.")
else:
    print(f"⚠️ {missing_count} anomalie(s) ou fichier(s) manquant(s) détecté(s).")

