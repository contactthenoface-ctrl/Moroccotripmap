import os, json, re
from pathlib import Path

print("🛠️ --- CORRECTION FINALE : ITINÉRAIRES & HISTOIRE --- 🛠️\n")

# 1. Unriformiser link_circuits et link_itineraries dans tous les JSON de traduction
trans_dir = Path('js/translations')
for json_file in trans_dir.rglob('*.json'):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict) and 'footer' in data and isinstance(data['footer'], dict):
            # Assurer la compatibilité entre les deux noms de clés
            val = data['footer'].get('link_circuits') or data['footer'].get('link_itineraries')
            if val:
                data['footer']['link_circuits'] = val
                data['footer']['link_itineraries'] = val
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# 2. Vérifier et corriger les balises dans tous les fichiers histoire.html ou similaires
for html_file in Path('.').rglob('*histoire*.html'):
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # S'assurer que les liens du footer sur la page d'histoire ont bien les data-i18n
    html = html.replace('href="programmes/index.html">Circuits & Itineraries</a>', 'href="programmes/index.html" data-i18n="footer.link_itineraries">Circuits & Itineraries</a>')
    html = html.replace('href="programmes/index.html">Circuits &amp; Itineraries</a>', 'href="programmes/index.html" data-i18n="footer.link_itineraries">Circuits &amp; Itineraries</a>')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Mis à jour : {html_file}")

print("\n✨ Synchronisation des dernières clés terminée !")
