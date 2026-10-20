import os, re, json
from pathlib import Path

print("🛠️ --- AJOUT DES BALISES I18N SUR LES PAGES DE DESTINATIONS --- 🛠️\n")

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts and f.name != 'index.html' and f.name != 'destinations.html']
trans_dir = Path('js/translations')

updated_pages = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Vérifier si c'est une page de destination type "stub" (contient "Explore ... , a captivating destination")
    if 'captivating destination' in content or 'Explore' in content:
        # Extraire le nom de la ville depuis le titre ou le nom du fichier
        city_name = html_file.stem.replace('-', ' ').title()
        
        # Modifier le HTML pour ajouter les data-i18n si pas présents
        # 1. Titre h1
        content = re.sub(
            r'(<h1[^>]*?>)(.*?)(</h1>)',
            rf'\1<span data-i18n="page.title">{city_name}</span>\3',
            content,
            flags=re.IGNORECASE
        )
        
        # 2. Paragraphe d'introduction
        content = re.sub(
            r'(<p[^>]*?>)(Explore\s+[^,]+,\s+a captivating destination[^<]*?)(</p>)',
            rf'\1<span data-i18n="page.intro">Explore {city_name}, a captivating destination offering unforgettable landscapes, historical heritage, and rich cultural experiences in Morocco.</span>\3',
            content,
            flags=re.IGNORECASE
        )

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Mettre à jour les fichiers JSON correspondants dans en, fr, es, ar
        base_name = html_file.stem.replace('-', '_') + '_page.json'
        
        translations = {
            "en": {"page": {"title": city_name, "intro": f"Explore {city_name}, a captivating destination offering unforgettable landscapes, historical heritage, and rich cultural experiences in Morocco."}},
            "fr": {"page": {"title": city_name, "intro": f"Explorez {city_name}, une destination captivante offrant des paysages inoubliables, un patrimoine historique et de riches expériences culturelles au Maroc."}},
            "es": {"page": {"title": city_name, "intro": f"Explore {city_name}, un destino cautivador que ofrece paisajes inolvidables, patrimonio histórico y ricas experiencias culturales en Marruecos."}},
            "ar": {"page": {"title": city_name, "intro": f"استكشف {city_name}، وجهة ساحرة توفر مناظر طبيعية لا تنسى، وتراثاً تاريخياً، وتجارب ثقافية غنية في المغرب."}}
        }

        for lang, trans_data in translations.items():
            json_path = trans_dir / lang / base_name
            json_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Charger ou créer le JSON
            data = {}
            if json_path.exists():
                try:
                    with open(json_path, 'r', encoding='utf-8') as jf:
                        data = json.load(jf)
                except Exception:
                    data = {}
            
            if 'page' not in data:
                data['page'] = {}
            data['page']['title'] = trans_data['page']['title']
            data['page']['intro'] = trans_data['page']['intro']
            
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(data, jf, ensure_ascii=False, indent=2)

        updated_pages += 1

print(f"✅ {updated_pages} pages de destinations mises à jour avec les balises i18n et leurs JSON !")
