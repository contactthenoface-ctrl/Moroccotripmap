import os, json, re
from pathlib import Path

print("🛠️ --- NETTOYAGE COMPLET ET SUR MESURE DES PAGES DE DESTINATION --- 🛠️\n")

trans_dir = Path('js/translations')

EXCLUDED = [
    'index.html', 'destinations.html', 'marrakech.html', 'contact.html',
    'agadir.html', 'essaouira.html', 'rabat.html', 'casablanca.html', 'fes.html'
]

html_files = [
    f for f in Path('.').rglob('*.html') 
    if 'node_modules' not in f.parts and f.name not in EXCLUDED
]

updated_count = 0

for file_path in html_files:
    city_slug = file_path.stem
    city_name = city_slug.replace('-', ' ').title()

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # On cible les fichiers qui contiennent encore des références à Marrakech
    if 'marrakech' in content.lower() or 'jemaa' in content.lower() or 'koutoubia' in content.lower():
        print(f"🧹 Nettoyage en profondeur de : {file_path.name}")

        # 1. Suppression des références à Marrakech / Jemaa el-Fnaa / Jardin Majorelle dans le texte brut
        content = re.sub(r'Jemaa el-Fnaa', f'{city_name} Medina', content)
        content = re.sub(r'Jardin Majorelle', f'{city_name} Coastal Views', content)
        content = re.sub(r'Koutoubia Mosque', f'Historic Ramparts', content)
        content = re.sub(r'Ochre City', 'Coastal Gem', content)
        content = re.sub(r'Hivernage', 'City Center', content)
        content = re.sub(r'RAK \(Menara\)', 'Tangier / Rabat Airport', content)
        content = re.sub(r'RAK airport', 'Nearest Airport', content)

        # 2. Correction des liens d'hôtels et d'images erronés
        content = content.replace('La+Mamounia', f'{city_name}+Hotel')
        content = content.replace('The+Oberoi', f'{city_name}+Resort')
        content = content.replace('Royal+Mansour', f'{city_name}+Riad')
        content = content.replace('El+Fenn', f'{city_name}+Boutique')
        content = content.replace('city/ma/marrakesh.html', f'searchresults.html?ss={city_name}+Morocco')

        # 3. Correction des balises i18n
        content = content.replace('marrakech_page.', f'{city_slug}_page.')
        content = content.replace('destinations.marrakech.name', f'destinations.{city_slug}.name')

        # 4. Ajustement des balises Meta SEO
        content = re.sub(r'<title.*?>.*?</title>', f'<title data-i18n="{city_slug}_page.seo.title">{city_name} Travel Guide | MoroccoTripMap</title>', content, count=1, flags=re.IGNORECASE)
        
        content = re.sub(
            r'name="description" content=".*?"',
            f'name="description" content="Plan your trip to {city_name}: top attractions, historic sights, local food, and travel tips." data-i18n-attr="content:{city_slug}_page.seo.description"',
            content,
            flags=re.IGNORECASE
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        updated_count += 1

print(f"\n✅ Terminé ! {updated_count} pages ont été complètement purgées des restes de Marrakech !")
