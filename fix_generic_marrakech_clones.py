import os, json, re
from pathlib import Path

print("🛠️ --- NETTOYAGE DES MENTIONS DE MARRAKECH ET ADAPTATION PAR VILLE --- 🛠️\n")

trans_dir = Path('js/translations')

# Liste des fichiers à exclure (les vraies pages spécifiques)
EXCLUDED = ['index.html', 'destinations.html', 'marrakech.html', 'contact.html']

html_files = [
    f for f in Path('.').rglob('*.html') 
    if 'node_modules' not in f.parts and f.name not in EXCLUDED
]

updated_count = 0

for file_path in html_files:
    # Ignorer les sous-fichiers trop profonds pour l'instant sauf les pages directes
    depth = len(file_path.relative_to('.').parts) - 1
    prefix = '../' * depth if depth > 0 else ''

    city_slug = file_path.stem
    city_name = city_slug.replace('-', ' ').title()

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Mise à jour des clés i18n spécifiques pour éviter de charger le JSON de Marrakech
    content = content.replace('marrakech_page.', f'{city_slug}_page.')
    content = content.replace('destinations.marrakech.name', f'destinations.{city_slug}.name')

    # 2. Adaptation des titres et textes d'introduction
    content = re.sub(r'<title>.*?</title>', f'<title data-i18n="{city_slug}_page.seo.title">{city_name} Travel Guide | MoroccoTripMap</title>', content, flags=re.IGNORECASE)
    
    # 3. Réécriture de la section "Must-Visit Places" pour pointer vers les lieux propres à la ville
    places_section = f"""<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 border-t border-sable/10">
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
            <span class="text-xs font-bold text-sable uppercase tracking-wider" data-i18n="{city_slug}_page.places.badge">Top Sightseeing</span>
            <h2 class="text-3xl font-bold text-vert" data-i18n="{city_slug}_page.places.title">Must-Visit Places in {city_name}</h2>
        </div>
        <p class="text-sm text-sombre/70 max-w-md" data-i18n="{city_slug}_page.places.subtitle">Explore the top historical landmarks and iconic sites in {city_name}.</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <a class="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition duration-300 border border-sable/10 flex flex-col p-5" href="{prefix}places/{city_slug}/historic-center.html">
            <h3 class="text-lg font-bold text-sombre group-hover:text-vert transition">{city_name} Historic Medina</h3>
            <p class="text-xs text-sombre/70 mt-2">Discover the traditional markets, historical alleys, and local life in {city_name}.</p>
            <span class="mt-4 text-xs font-semibold text-sable group-hover:text-vert transition">Explore Place →</span>
        </a>
    </div>
</section>"""

    # Remplacer la grille de 9 lieux de Marrakech par la section adaptée à la ville
    content = re.sub(r'<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 border-t border-sable/10">[\s\S]*?</section>', places_section, content, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 4. Générer les traductions propres dans les 4 dossiers JSON (en, fr, es, ar)
    for lang in ['en', 'fr', 'es', 'ar']:
        lang_dir = trans_dir / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        json_file = lang_dir / f"{city_slug}_page.json"

        seo_titles = {
            "en": f"{city_name} Travel Guide 2026 | MoroccoTripMap",
            "fr": f"Guide de Voyage {city_name} 2026 | MoroccoTripMap",
            "es": f"Guía de Viaje {city_name} 2026 | MoroccoTripMap",
            "ar": f"دليل سفر {city_name} 2026 | MoroccoTripMap"
        }

        seo_descs = {
            "en": f"Plan your trip to {city_name}: top attractions, historic sights, local food, and travel tips.",
            "fr": f"Préparez votre voyage à {city_name} : incontournables, monuments historiques, gastronomie locale et conseils.",
            "es": f"Planifica tu viaje a {city_name}: atracciones principales, monumentos históricos, comida local y consejos.",
            "ar": f"خطط لرحلتك إلى {city_name}: أهم المعالم السياحية، المواقع التاريخية، المأكولات المحلية ونصائح السفر."
        }

        data = {
            f"{city_slug}_page": {
                "seo": {
                    "title": seo_titles[lang],
                    "description": seo_descs[lang]
                },
                "hero_subtitle": f"Discover {city_name} - Authentic charm & culture.",
                "overview": {
                    "title": f"Welcome to {city_name}",
                    "p1": f"Explore {city_name}, a unique destination in Morocco known for its cultural heritage and stunning landscapes."
                },
                "places": {
                    "badge": "Sightseeing",
                    "title": f"Must-Visit Places in {city_name}",
                    "subtitle": f"Discover top points of interest in {city_name}."
                }
            }
        }

        with open(json_file, 'w', encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)

    updated_count += 1

print(f"✅ {updated_count} pages ont été purgées du contenu de Marrakech et réassignées à leur propre ville !")
