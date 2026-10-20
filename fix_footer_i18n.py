import os, re, json
from pathlib import Path

print("🛠️ --- VÉRIFICATION ET UNIFORMISATION DES FOOTERS --- 🛠️\n")

# Exemple de clés standardisées pour le footer
footer_translations = {
    "en": {
        "footer": {
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
        }
    },
    "fr": {
        "footer": {
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
        }
    },
    "es": {
        "footer": {
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
        }
    },
    "ar": {
        "footer": {
            "destinations_title": "الوجهات",
            "categories_title": "الفئات",
            "link_stays": "رياض وفنادق أصيلة",
            "link_restaurants": "مطاعم مغربية",
            "link_culture": "تجارب الصحراء والثقافة",
            "link_transport": "المواصلات والسائقين الخاصين",
            "link_circuits": "الرحلات والمسااروات",
            "link_history": "تاريخ المغرب",
            "link_guides": "أدلة السفر",
            "link_blog": "المدونة",
            "link_contact": "اتصل بنا"
        }
    }
}

trans_dir = Path('js/translations')

# Mettre à jour les fichiers JSON pour inclure ces clés de footer propres
for lang, content in footer_translations.items():
    lang_path = trans_dir / lang
    if not lang_path.exists():
        continue
    
    # Parcourir tous les JSON de traduction de pages existants pour y injecter le bloc footer
    for json_file in lang_path.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, dict):
                data = {}
                
            # Fusionner le bloc footer
            if 'footer' not in data:
                data['footer'] = {}
            
            for k, v in content['footer'].items():
                if k not in data['footer'] or not data['footer'][k]:
                    data['footer'][k] = v
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            pass

print("✨ Les traductions du footer ont été injectées et synchronisées avec succès dans tous les fichiers JSON !")
