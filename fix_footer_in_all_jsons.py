import os, json
from pathlib import Path

print("🛠️ --- INJECTION FORCÉE DU FOOTER DANS TOUS LES JSON --- 🛠️\n")

footer_data = {
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
updated_files = 0

for lang, translations in footer_data.items():
    lang_folder = trans_dir / lang
    if not lang_folder.exists():
        continue
    
    for json_file in lang_folder.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, dict):
                data = {}
            
            # S'assurer que l'objet footer existe et contient toutes les clés
            if 'footer' not in data or not isinstance(data['footer'], dict):
                data['footer'] = {}
            
            for k, v in translations.items():
                data['footer'][k] = v
            
            # Réécrire le fichier proprement
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            updated_files += 1
        except Exception as e:
            print(f"⚠️ Erreur sur {json_file}: {e}")

print(f"\n✨ Succès ! {updated_files} fichiers JSON ont été mis à jour avec le bloc footer complet.")
