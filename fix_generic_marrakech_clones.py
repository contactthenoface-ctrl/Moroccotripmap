import os, json, re
from pathlib import Path

print("🛠️ --- NETTOYAGE SÉCURISÉ (EXCLUSION DE VOS PAGES MANUELLES) --- 🛠️\n")

trans_dir = Path('js/translations')

# Liste des pages à NE SURTOUT PAS TOUCHER (vos pages créées manuellement + pages principales)
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

    # On ne traite que les fichiers qui contiennent des traces du clone de Marrakech
    if 'marrakech' in content.lower() or 'marrakech_page' in content:
        
        content = content.replace('marrakech_page.', f'{city_slug}_page.')
        content = content.replace('destinations.marrakech.name', f'destinations.{city_slug}.name')

        content = re.sub(r'<title.*?>.*?</title>', f'<title data-i18n="{city_slug}_page.seo.title">{city_name} Travel Guide | MoroccoTripMap</title>', content, count=1, flags=re.IGNORECASE)
        
        content = re.sub(
            r'name="description" content=".*?"',
            f'name="description" content="Plan your trip to {city_name}: top attractions, historic sights, local food, and travel tips." data-i18n-attr="content:{city_slug}_page.seo.description"',
            content,
            flags=re.IGNORECASE
        )

        overview_section = f"""<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="max-w-3xl">
                <h2 class="text-2xl sm:text-3xl font-bold text-vert mb-4" data-i18n="{city_slug}_page.overview.title">Welcome to {city_name}</h2>
                <p class="text-sombre/80 leading-relaxed text-base mb-4" data-i18n="{city_slug}_page.overview.p1">
                    {city_name} is a magnificent destination in Morocco, offering a unique blend of cultural heritage, authentic local traditions, and stunning landscapes that promise an unforgettable journey.
                </p>
                <p class="text-sombre/80 leading-relaxed text-base" data-i18n="{city_slug}_page.overview.p2">
                    Whether you are exploring historical monuments, discovering local artisan markets, or enjoying the warm hospitality of the region, {city_name} has something special for every traveler.
                </p>
            </div>
        </section>"""
        
        content = re.sub(r'<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">[\s\S]*?</section>', overview_section, content, count=1)
        content = content.replace('city/ma/marrakesh.html', f'searchresults.html?ss={city_name}+Morocco')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        for lang in ['en', 'fr', 'es', 'ar']:
            lang_dir = trans_dir / lang
            lang_dir.mkdir(parents=True, exist_ok=True)
            json_file = lang_dir / f"{city_slug}_page.json"

            seo_titles = {
                "en": f"{city_name} Travel Guide 2026 | Things to Do & Tips | MoroccoTripMap",
                "fr": f"Guide de Voyage {city_name} 2026 | Choses à faire & Conseils | MoroccoTripMap",
                "es": f"Guía de Viaje {city_name} 2026 | Cosas que hacer | MoroccoTripMap",
                "ar": f"دليل سفر {city_name} 2026 | أهم المعالم ونقاط اهتمام | MoroccoTripMap"
            }

            data = {
                f"{city_slug}_page": {
                    "seo": {
                        "title": seo_titles[lang],
                        "description": f"Plan your trip to {city_name}: top attractions, local food, and travel tips."
                    },
                    "hero_subtitle": f"Discover the authentic charm, culture, and heritage of {city_name}.",
                    "overview": {
                        "title": f"Welcome to {city_name}" if lang != 'fr' else f"Bienvenue à {city_name}",
                        "p1": f"Explore {city_name} and its unique cultural and geographical treasures.",
                        "p2": "Enjoy an authentic experience discovering local landmarks."
                    },
                    "places": {
                        "badge": "Sightseeing" if lang != 'fr' else "À voir",
                        "title": f"Must-Visit Places in {city_name}" if lang != 'fr' else f"Les incontournables à {city_name}",
                        "subtitle": f"Discover top points of interest in {city_name}."
                    }
                }
            }

            with open(json_file, 'w', encoding='utf-8') as jf:
                json.dump(data, jf, ensure_ascii=False, indent=2)

        updated_count += 1

print(f"\n✅ Terminé ! {updated_count} pages automatiques ont été corrigées, et vos pages manuelles ont été totalement épargnées !")
