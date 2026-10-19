import os, json
from pathlib import Path

# Langues gérées
languages = ['en', 'fr', 'es', 'ar']
trans_dir = Path('js/translations')

# S'assurer que le dossier translations existe
if not trans_dir.exists():
    print("❌ Le dossier js/translations n'a pas été trouvé.")
    exit()

# Trouver toutes les pages HTML créées à la racine ou dans des sous-dossiers
html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]

created_count = 0

for html_file in html_files:
    # Nom de base pour le json (ex: ait-ben-haddou.html -> ait_ben_haddou_page.json ou ait-ben-haddou_page.json)
    base_name = html_file.stem.replace('-', '_') + '_page.json'
    
    for lang in languages:
        lang_folder = trans_dir / lang
        lang_folder.mkdir(parents=True, exist_ok=True)
        json_path = lang_folder / base_name
        
        # Si le fichier JSON n'existe pas, on le crée avec une structure de base
        if not json_path.exists():
            default_data = {
                "seo": {
                    "title": f"MoroccoTripMap - {html_file.stem.replace('-', ' ').title()}",
                    "description": f"Discover insights and details about {html_file.stem.replace('-', ' ')} in Morocco."
                }
            }
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(default_data, jf, ensure_ascii=False, indent=2)
            created_count += 1
            print(f"✅ Créé : {json_path}")

print(f"\n🎉 {created_count} fichiers JSON de traduction manquants ont été générés avec succès !")
