import os, json
from pathlib import Path

print("🔍 --- AUDIT COMPLET DES PAGES DE DESTINATIONS ET LEURS TRADUCTIONS --- 🔍\n")

trans_dir = Path('js/translations')
html_files = [
    f for f in Path('.').rglob('*.html') 
    if 'node_modules' not in f.parts and f.name not in ['index.html', 'destinations.html', 'contact.html']
]

results = []

for file_path in html_files:
    city_slug = file_path.stem
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Détection des éléments clés
    has_data_i18n = 'data-i18n=' in content
    has_marrakech_leftovers = 'jemaa' in content.lower() or 'koutoubia' in content.lower() if city_slug != 'marrakech' else False
    
    # Vérification des fichiers JSON de traduction pour chaque langue
    json_status = {}
    for lang in ['en', 'fr', 'es', 'ar']:
        json_file = trans_dir / lang / f"{city_slug}_page.json"
        json_status[lang] = json_file.exists()

    results.append({
        'slug': city_slug,
        'path': str(file_path),
        'i18n_keys': has_data_i18n,
        'marrakech_bugs': has_marrakech_leftovers,
        'json_status': json_status
    })

# Affichage du rapport
print(f"{'Ville / Page':<20} | {'i18n HTML':<10} | {'Reste Marrakech':<16} | {'JSON (EN/FR/ES/AR)':<20}")
print("-" * 75)

missing_jsons = []

for r in sorted(results, key=lambda x: x['slug']):
    i18n_str = "✅ Oui" if r['i18n_keys'] else "❌ Non"
    marrakech_str = "⚠️ TRACES" if r['marrakech_bugs'] else "✅ Propre"
    
    langs_ok = [lang.upper() for lang, ok in r['json_status'].items() if ok]
    langs_missing = [lang.upper() for lang, ok in r['json_status'].items() if not ok]
    
    json_str = f"✅ {','.join(langs_ok)}" if not langs_missing else f"❌ Manque {','.join(langs_missing)}"
    
    print(f"{r['slug']:<20} | {i18n_str:<10} | {marrakech_str:<16} | {json_str:<20}")

print("\n💡 Légende :")
print("• i18n HTML = La page contient des balises dynamiques data-i18n")
print("• Reste Marrakech = Indique s'il y a du texte résiduel de Marrakech dans la page")
print("• JSON = Fichiers de traduction présents dans js/translations/")
