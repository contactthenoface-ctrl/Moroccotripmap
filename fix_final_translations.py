import json, glob

complete_translations = {
    "en": {
        "footer": {
            "about_text": "Discover. Plan. Experience Morocco.\nThe premier tourism directory and cultural travel guide for visitors exploring Morocco.",
            "recommended_title": "Recommended Pages",
            "destinations_title": "Top Destinations",
            "categories_title": "Travel Categories",
            "connect_title": "Connect",
            "youtube_text": "Follow our YouTube channel for video travel guides:",
            "copyright": "© MoroccoTripMap. All rights reserved.",
            "link_marrakech": "Marrakech Travel Guide",
            "link_chefchaouen": "Chefchaouen Blue City",
            "link_fes": "Fes Ancient Medina",
            "link_merzouga": "Sahara Desert & Merzouga",
            "link_rabat": "Rabat Imperial Capital",
            "link_all_destinations": "All Destinations →",
            "link_stays": "Authentic Riads & Hotels",
            "link_restaurants": "Moroccan Gastronomy & Food",
            "link_experiences": "Desert Tours & Activities",
            "link_transport": "Transport & Rental Cars",
            "link_itineraries": "Circuits & Itineraries",
            "link_history": "History of Morocco",
            "link_blog": "Travel Blog & Tips"
        }
    },
    "fr": {
        "footer": {
            "about_text": "Découvrez. Planifiez. Vivez le Maroc.\nLe premier annuaire touristique et guide culturel pour explorer le Maroc.",
            "recommended_title": "Pages Recommandées",
            "destinations_title": "Meilleures Destinations",
            "categories_title": "Catégories de Voyage",
            "connect_title": "Suivez-nous",
            "youtube_text": "Suivez notre chaîne YouTube pour nos guides vidéo :",
            "copyright": "© MoroccoTripMap. Tous droits réservés.",
            "link_marrakech": "Guide Voyage Marrakech",
            "link_chefchaouen": "Chefchaouen la Ville Bleue",
            "link_fes": "Ancienne Médina de Fès",
            "link_merzouga": "Désert du Sahara & Merzouga",
            "link_rabat": "Rabat Capitale Impériale",
            "link_all_destinations": "Toutes les Destinations →",
            "link_stays": "Riads & Hôtels Authentiques",
            "link_restaurants": "Gastronomie & Cuisine Marocaine",
            "link_experiences": "Excursions & Activités Désert",
            "link_transport": "Transport & Location de Voitures",
            "link_itineraries": "Circuits & Itinéraires",
            "link_history": "Histoire du Maroc",
            "link_blog": "Blog Voyage & Conseils"
        }
    },
    "es": {
        "footer": {
            "about_text": "Descubre. Planifica. Vive Marruecos.\nEl directorio turístico y guía cultural para explorar Marruecos.",
            "recommended_title": "Páginas Recomendadas",
            "destinations_title": "Principales Destinos",
            "categories_title": "Categorías de Viaje",
            "connect_title": "Conéctate",
            "youtube_text": "Sigue nuestro canal de YouTube para guías en video:",
            "copyright": "© MoroccoTripMap. Todos los derechos reservados.",
            "link_marrakech": "Guía de Viaje a Marrakech",
            "link_chefchaouen": "Chefchaouen Ciudad Azul",
            "link_fes": "Antigua Medina de Fez",
            "link_merzouga": "Desierto del Sáhara y Merzouga",
            "link_rabat": "Rabat Capital Imperial",
            "link_all_destinations": "Todos los Destinos →",
            "link_stays": "Riads y Hoteles Auténticos",
            "link_restaurants": "Gastronomía y Comida Marroquí",
            "link_experiences": "Tours y Actividades en el Desierto",
            "link_transport": "Transporte y Alquiler de Coches",
            "link_itineraries": "Circuitos e Itinerarios",
            "link_history": "Historia de Marruecos",
            "link_blog": "Blog de Viajes y Consejos"
        }
    },
    "ar": {
        "footer": {
            "about_text": "اكتشف. خطط. عِش تجربة المغرب.\nالدليل السياحي والأنثروبولوجي الأبرز لزوار المغرب.",
            "recommended_title": "صفحات مقترحة",
            "destinations_title": "أبرز الوجهات",
            "categories_title": "تصنيفات السفر",
            "connect_title": "تواصل معنا",
            "youtube_text": "تابع قناتنا على يوتيوب لمشاهدة أدلة السفر المرئية:",
            "copyright": "© MoroccoTripMap. جميع الحقوق محفوظة.",
            "link_marrakech": "دليل السفر إلى مراكش",
            "link_chefchaouen": "شفشاون المدينة الزرقاء",
            "link_fes": "فاس المدينة القديمة",
            "link_merzouga": "دليل سفر مرزوكة",
            "link_rabat": "الرباط العاصمة الإمبراطورية",
            "link_all_destinations": "جميع الوجهات ←",
            "link_stays": "رياضات وفنادق أصيلة",
            "link_restaurants": "مطاعم مغربية",
            "link_experiences": "تجارب الصحراء والثقافة",
            "link_transport": "المواصلات والسائقين الخاصين",
            "link_itineraries": "البرامج والجولات السياحية",
            "link_history": "تاريخ المغرب",
            "link_blog": "مدونة السفر والنصائح"
        }
    }
}

for lang, data in complete_translations.items():
    matches = glob.glob(f"**/{lang}.json", recursive=True)
    matches = [m for m in matches if "node_modules" not in m]
    if matches:
        for filepath in matches:
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    content = json.load(f)
                except:
                    content = {}
            content.setdefault("footer", {}).update(data["footer"])
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"JSON parfaitement mis à jour : {filepath}")
