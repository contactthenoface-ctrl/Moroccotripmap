import os, re, json
from pathlib import Path

print("🛠️ --- TRAITEMENT GLOBAL DE TOUTES LES TRADUCTIONS ET FOOTERS --- 🛠️\n")

footer_translations = {
    "en": {
        "destinations_title": "Destinations",
        "categories_title": "Categories",
        "link_stays": "Stays & Riads",
        "link_restaurants": "Moroccan Restaurants",
        "link_culture": "Culture & Desert",
        "link_transport": "Transport & Drivers",
        "link_circuits": "Circuits & Itineraries",
        "link_history": "History of Morocco",
        "link_guides": "Travel Guides",
        "link_blog": "Blog",
        "link_contact": "Contact"
    },
    "fr": {
        "destinations_title": "Destinations",
        "categories_title": "Catégories",
        "link_stays": "Riads & Hébergements",
        "link_restaurants": "Restaurants Marocains",
        "link_culture": "Culture & Désert",
        "link_transport": "Transport & Chauffeurs",
        "link_circuits": "Circuits & Itinéraires",
        "link_history": "Histoire du Maroc",
        "link_guides": "Guides de Voyage",
        "link_blog": "Blog",
        "link_contact": "Contact"
    },
    "es": {
        "destinations_title": "Destinos",
        "categories_title": "Categorías",
        "link_stays": "Riad y Alojamiento",
        "link_restaurants": "Restaurantes Marroquíes",
        "link_culture": "Cultura y Desierto",
        "link_transport": "Transporte y Conductores",
        "link_circuits": "Circuitos e Itinerarios",
        "link_history": "Historia de Marruecos",
        "link_guides": "Guías de Viaje",
        "link_blog": "Blog",
        "link_contact": "Contacto"
    },
    "ar": {
        "destinations_title": "الوجهات",
        "categories_title": "الفئات",
        "link_stays": "رياض وفنادق أصيلة",
        "link_restaurants": "مطاعم مغربية",
        "link_culture": "تجارب الصحراء والثقافة",
        "link_transport": "المواصلات والسائقين الخاصين",
        "link_circuits": "الرحلات والمسارات",
        "link_history": "تاريخ المغرب",
        "link_guides": "أدلة السفر",
        "link_blog": "المدونة",
        "link_contact": "اتصل بنا"
    }
}

trans_dir = Path('js/translations')

# 1. Injecter le footer dans TOUS les fichiers JSON de TOUTES les langues
json_count = 0
for lang, translations in footer_translations.items():
    lang_path = trans_dir / lang
    if not lang_path.exists():
        continue
    for json_file in lang_path.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
            if not isinstance(data, dict):
                data = {}
            if 'footer' not in data:
                data['footer'] = {}
            for k, v in translations.items():
                data['footer'][k] = v
            with open(json_file, 'w', encoding='utf-8') as jf:
                json.dump(data, jf, ensure_ascii=False, indent=2)
            json_count += 1
        except Exception:
            pass

print(f"✅ Bloc footer synchronisé dans {json_count} fichiers JSON (toutes langues confondues).")

# 2. Injecter les data-i18n dans TOUTES les pages HTML du site
html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
mapping = [
    ("Stays & Riads", 'footer.link_stays'),
    ("Moroccan Restaurants", 'footer.link_restaurants'),
    ("Culture & Desert", 'footer.link_culture'),
    ("Transport & Drivers", 'footer.link_transport'),
    ("Circuits & Itineraries", 'footer.link_circuits'),
    ("History of Morocco", 'footer.link_history'),
    ("Travel Guides", 'footer.link_guides'),
    ("Blog", 'footer.link_blog'),
    ("Contact", 'footer.link_contact'),
    ("Categories", 'footer.categories_title'),
    ("Destinations", 'footer.destinations_title')
]

html_modified_count = 0
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    mod = [False]
    for text, key in mapping:
        pattern = rf'<a\s+([^>]*?)>(\s*{text}\s*)</a>'
        def make_repl(k):
            def repl(match):
                attrs = match.group(1)
                inner = match.group(2)
                if 'data-i18n' not in attrs:
                    mod[0] = True
                    return f'<a {attrs} data-i18n="{k}">{inner}</a>'
                return match.group(0)
            return repl

        html = re.sub(pattern, make_repl(key), html, flags=re.IGNORECASE)

    if mod[0]:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        html_modified_count += 1

print(f"✅ Attributs data-i18n mis à jour dans {html_modified_count} fichiers HTML.")
print("\n✨ Opération globale terminée avec succès !")
