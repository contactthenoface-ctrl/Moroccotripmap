import re

with open('js/i18n.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Dictionnaire de secours embarqué directement dans le code JS
inline_footers = """
const INLINE_FOOTER_TRANSLATIONS = {
  en: {
    destinations_title: "Destinations",
    categories_title: "Categories",
    connect_title: "Connect With Us",
    youtube_text: "Subscribe to our YouTube channel for travel video guides:",
    copyright: "© 2026 MoroccoTripMap. All rights reserved.",
    link_merzouga: "Merzouga Travel Guide",
    link_rabat: "Rabat Travel Guide",
    link_meknes: "Meknes Travel Guide",
    link_agadir: "Agadir Beaches",
    link_tangier: "Tangier Guide",
    link_all_destinations: "All Destinations",
    link_stays: "Stays & Riads",
    link_restaurants: "Moroccan Restaurants",
    link_culture: "Culture & Desert",
    link_transport: "Transport & Drivers",
    link_circuits: "Circuits & Itineraries",
    link_history: "History of Morocco",
    link_guides: "Travel Guides",
    link_blog: "Blog",
    link_contact: "Contact",
    about_text: "Discover. Plan. Experience Morocco.\\nThe premier tourism directory and cultural travel guide for visitors exploring Morocco."
  },
  fr: {
    destinations_title: "Destinations",
    categories_title: "Catégories",
    connect_title: "Suivez-nous",
    youtube_text: "Abonnez-vous à notre chaîne YouTube pour nos guides vidéo :",
    copyright: "© 2026 MoroccoTripMap. Tous droits réservés.",
    link_merzouga: "Guide de Voyage Merzouga",
    link_rabat: "Guide de Voyage Rabat",
    link_meknes: "Guide de Voyage Meknès",
    link_agadir: "Plages d'Agadir",
    link_tangier: "Guide de Tanger",
    link_all_destinations: "Toutes les Destinations",
    link_stays: "Riads & Hébergements",
    link_restaurants: "Restaurants Marocains",
    link_culture: "Culture & Désert",
    link_transport: "Transport & Chauffeurs",
    link_circuits: "Circuits & Itinéraires",
    link_history: "Histoire du Maroc",
    link_guides: "Guides de Voyage",
    link_blog: "Blog",
    link_contact: "Contact",
    about_text: "Découvrez. Planifiez. Vivez le Maroc.\\nLe premier annuaire touristique et guide culturel pour les visiteurs explorant le Maroc."
  },
  es: {
    destinations_title: "Destinos",
    categories_title: "Categorías",
    connect_title: "Conéctate con Nosotros",
    youtube_text: "Suscríbete a nuestro canal de YouTube para ver guías en vídeo:",
    copyright: "© 2026 MoroccoTripMap. Todos los derechos reservados.",
    link_merzouga: "Guía de Viaje de Merzouga",
    link_rabat: "Guía de Viaje de Rabat",
    link_meknes: "Guía de Viaje de Meknes",
    link_agadir: "Playas de Agadir",
    link_tangier: "Guía de Tánger",
    link_all_destinations: "Todos los Destinos",
    link_stays: "Riad y Alojamiento",
    link_restaurants: "Restaurantes Marroquíes",
    link_culture: "Cultura y Desierto",
    link_transport: "Transporte y Conductores",
    link_circuits: "Circuitos e Itinerarios",
    link_history: "Historia de Marruecos",
    link_guides: "Guías de Viaje",
    link_blog: "Blog",
    link_contact: "Contacto",
    about_text: "Descubre. Planifica. Vive Marruecos.\\nEl directorio turístico y guía cultural de referencia para los visitantes de Marruecos."
  },
  ar: {
    destinations_title: "الوجهات",
    categories_title: "الفئات",
    connect_title: "تواصل معنا",
    youtube_text: "تابع قناتنا على يوتيوب لمشاهدة أدلة السفر بالفيديو:",
    copyright: "© 2026 MoroccoTripMap. جميع الحقوق محفوظة.",
    link_merzouga: "دليل سفر مرزوقة",
    link_rabat: "دليل الرباط",
    link_meknes: "دليل سفر مكناس",
    link_agadir: "شواطئ أغادير",
    link_tangier: "دليل طنجة",
    link_all_destinations: "جميع الوجهات",
    link_stays: "رياض وفنادق أصيلة",
    link_restaurants: "مطاعم مغربية",
    link_culture: "تجارب الصحراء والثقافة",
    link_transport: "المواصلات والسائقين الخاصين",
    link_circuits: "الرحلات والمسارات",
    link_history: "تاريخ المغرب",
    link_guides: "أدلة السفر",
    link_blog: "المدونة",
    link_contact: "اتصل بنا",
    about_text: "اكتشف. خطط. عش تجربة المغرب.\\nالدليل السياحي والثقافي الأول للزوار لاستكشاف المغرب."
  }
};
"""

# Injection au début du fichier
if "INLINE_FOOTER_TRANSLATIONS" not in code:
    code = inline_footers + "\n" + code

# Modifier ensureLangData pour toujours fusionner le footer en mémoire
target = "const dict = allTranslations[lang] || (allTranslations[lang] = {});"
replacement = """const dict = allTranslations[lang] || (allTranslations[lang] = {});
    dict.footer = INLINE_FOOTER_TRANSLATIONS[lang] || INLINE_FOOTER_TRANSLATIONS['fr'];"""

if target in code and "dict.footer = INLINE_FOOTER_TRANSLATIONS" not in code:
    code = code.replace(target, replacement)

with open('js/i18n.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Translations du Footer intégrées directement dans js/i18n.js !")
