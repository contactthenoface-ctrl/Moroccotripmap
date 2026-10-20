import os, json, re
from pathlib import Path

print("🚀 --- GÉNÉRATION DU CONTENU UNIQUE & OPTIMISÉ SEO --- 🚀\n")

html_files = [
    f for f in Path('.').rglob('*.html') 
    if 'node_modules' not in f.parts and f.name not in ['index.html', 'destinations.html', 'contact.html']
]

trans_dir = Path('js/translations')
updated_count = 0

for html_file in html_files:
    # Ignorer si ce n'est pas un fichier HTML pertinent
    raw_name = html_file.stem
    clean_title = raw_name.replace('-', ' ').replace('_', ' ').title()
    json_base_name = raw_name.replace('-', '_') + '_page.json'
    
    # Prédire le type de contenu (Place, Restaurant, Ville)
    category = "destination"
    if "restaurant" in str(html_file) or "gastronomy" in str(html_file):
        category = "restaurant"
    elif "place" in str(html_file) or "attraction" in str(html_file):
        category = "attraction"

    # 1. Génération des blocs de texte SEO multilingues uniques
    seo_data = {
        "en": {
            "seo_title": f"{clean_title} Travel Guide - Best Things to Do | MoroccoTripMap",
            "seo_desc": f"Explore {clean_title} in Morocco. Discover top attractions, cultural landmarks, local cuisine, and essential travel tips for an unforgettable trip.",
            "hero_title": clean_title,
            "hero_subtitle": f"Discover the authentic charm and unique experiences of {clean_title}.",
            "sec1_title": "Overview & Cultural Heritage",
            "sec1_text": f"Located in one of Morocco's most picturesque regions, {clean_title} offers visitors an immersive journey into rich heritage, stunning architecture, and warm local hospitality.",
            "sec2_title": "Things to See & Local Experiences",
            "sec2_text": f"Whether you are exploring historical sites, tasting traditional Moroccan flavors, or discovering surrounding natural landscapes, {clean_title} provides memorable moments for every traveler.",
            "sec3_title": "Practical Travel Tips",
            "sec3_text": f"To make the most of your visit to {clean_title}, plan your itinerary during optimal seasons, connect with certified local guides, and experience authentic local accommodations."
        },
        "fr": {
            "seo_title": f"Guide de Voyage {clean_title} - Incontournables | MoroccoTripMap",
            "seo_desc": f"Découvrez {clean_title} au Maroc. Conseils de voyage, culture, gastronomie locale et monuments incontournables pour réussir votre séjour.",
            "hero_title": clean_title,
            "hero_subtitle": f"Découvrez le charme authentique et les expériences uniques de {clean_title}.",
            "sec1_title": "Aperçu & Patrimoine Culturel",
            "sec1_text": f"Situé dans l'une des plus belles régions du Maroc, {clean_title} offre aux visiteurs une immersion au cœur d'un patrimoine riche, d'une architecture remarquable et d'un accueil chaleureux.",
            "sec2_title": "À Voir & Expériences Locales",
            "sec2_text": f"Que vous exploriez des sites historiques, goûtiez aux saveurs marocaines traditionnelles ou découvriez les paysages environnants, {clean_title} propose des souvenirs inoubliables.",
            "sec3_title": "Conseils Pratiques de Voyage",
            "sec3_text": f"Pour profiter pleinement de votre séjour à {clean_title}, organisez votre itinéraire aux meilleures périodes, privilégiez les guides locaux certifiés et séjournez dans des hébergements authentiques."
        },
        "es": {
            "seo_title": f"Guía de Viaje {clean_title} - Qué Ver y Hacer | MoroccoTripMap",
            "seo_desc": f"Descubre {clean_title} en Marruecos. Encuentra atracciones, cultura, gastronomía local y consejos prácticos para una experiencia inolvidable.",
            "hero_title": clean_title,
            "hero_subtitle": f"Descubre el encanto auténtico y las experiencias únicas de {clean_title}.",
            "sec1_title": "Visión General y Patrimonio Cultural",
            "sec1_text": f"Ubicado en una de las regiones más cautivadoras de Marruecos, {clean_title} ofrece a los visitantes un viaje inmersivo en una rica herencia cultural e historia.",
            "sec2_title": "Qué Ver y Experiencias Locales",
            "sec2_text": f"Ya sea explorando monumentos históricos, degustando platos tradicionales o descubriendo la naturaleza circundante, {clean_title} promete momentos memorables.",
            "sec3_title": "Consejos Prácticos de Viaje",
            "sec3_text": f"Para aprovechar al máximo tu visita a {clean_title}, planifica tu itinerario en la mejor temporada y elige alojamientos y guías locales auténticos."
        },
        "ar": {
            "seo_title": f"دليل سفر {clean_title} - أهم المعالم والأنشطة | MoroccoTripMap",
            "seo_desc": f"استكشف {clean_title} في المغرب. اكتشف أهم المعالم السياحية، الثقافة، المأكولات المحلية، ونصائح السفر لرحلة لا تُنسى.",
            "hero_title": clean_title,
            "hero_subtitle": f"اكتشف السحر الأصيل والتجارب الفريدة في {clean_title}.",
            "sec1_title": "نظرة عامة والتراث الثقافي",
            "sec1_text": f"تقع {clean_title} في واحدة من أجمل المناطق في المغرب، وتقدم للزوار رحلة ممتعة في أعمق أسرار التراث المعماري والثقافي الضارب في التاريخ.",
            "sec2_title": "أبرز المعالم والتجارب المحلية",
            "sec2_text": f"سواء كنت تستكشف المواقع التاريخية، أو تتذوق النكهات المغربية الأصيلة، أو تكتشف الطبيعة المحيطة، فإن {clean_title} تضمن لك ذكريات لا تُنسى.",
            "sec3_title": "نصائح عمليّة للسفر",
            "sec3_text": f"للإستمتاع بزيارتك إلى {clean_title}، يُنصح بتخطيط مسارك خلال أفضل الفصول، والتعامل مع مرشدين محليين معتمدين والإقامة في دور ضيافة تقليدية."
        }
    }

    # 2. Mettre à jour les fichiers JSON pour chaque langue
    for lang, content_dict in seo_data.items():
        lang_dir = trans_dir / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        json_file = lang_dir / json_base_name
        
        data = {}
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
            except Exception:
                data = {}

        if not isinstance(data, dict):
            data = {}

        # Fusion des traductions SEO
        data["seo"] = {
            "title": content_dict["seo_title"],
            "description": content_dict["seo_desc"]
        }
        data["content"] = {
            "hero_title": content_dict["hero_title"],
            "hero_subtitle": content_dict["hero_subtitle"],
            "sec1_title": content_dict["sec1_title"],
            "sec1_text": content_dict["sec1_text"],
            "sec2_title": content_dict["sec2_title"],
            "sec2_text": content_dict["sec2_text"],
            "sec3_title": content_dict["sec3_title"],
            "sec3_text": content_dict["sec3_text"]
        }

        with open(json_file, 'w', encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)

    # 3. Restructurer le HTML de la page avec un layout riche SEO
    depth = len(html_file.relative_to('.').parts) - 1
    prefix = '../' * depth if depth > 0 else ''

    rich_html_layout = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-i18n="seo.title">{seo_data['en']['seo_title']}</title>
    <meta name="description" content="{seo_data['en']['seo_desc']}" data-i18n-attr="content:seo.description">
    <link rel="stylesheet" href="{prefix}css/styles.css">
</head>
<body class="bg-creme text-vert font-sans leading-relaxed">
    <header class="bg-white/90 backdrop-blur-md sticky top-0 z-50 border-b border-gray-100">
        <!-- Header standard sera inséré dynamiquement ou conservé -->
    </header>

    <main class="max-w-5xl mx-auto px-4 py-12">
        <!-- Hero Section -->
        <div class="text-center mb-12">
            <span class="text-xs uppercase tracking-widest bg-sable/20 text-vert px-4 py-1.5 rounded-full font-semibold" data-i18n="badge.destination">Morocco Travel Guide</span>
            <h1 class="text-4xl md:text-5xl font-extrabold mt-4 mb-3 text-vert" data-i18n="content.hero_title">{clean_title}</h1>
            <p class="text-lg text-gray-600 max-w-2xl mx-auto" data-i18n="content.hero_subtitle">{seo_data['en']['hero_subtitle']}</p>
        </div>

        <!-- Structure SEO en 3 Colonnes/Articles -->
        <div class="space-y-8">
            <article class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                <h2 class="text-2xl font-bold mb-4 text-vert" data-i18n="content.sec1_title">{seo_data['en']['sec1_title']}</h2>
                <p class="text-gray-700 leading-relaxed" data-i18n="content.sec1_text">{seo_data['en']['sec1_text']}</p>
            </article>

            <article class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                <h2 class="text-2xl font-bold mb-4 text-vert" data-i18n="content.sec2_title">{seo_data['en']['sec2_title']}</h2>
                <p class="text-gray-700 leading-relaxed" data-i18n="content.sec2_text">{seo_data['en']['sec2_text']}</p>
            </article>

            <article class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                <h2 class="text-2xl font-bold mb-4 text-vert" data-i18n="content.sec3_title">{seo_data['en']['sec3_title']}</h2>
                <p class="text-gray-700 leading-relaxed" data-i18n="content.sec3_text">{seo_data['en']['sec3_text']}</p>
            </article>
        </div>
    </main>

    <footer class="bg-vert text-creme pt-12 pb-8 px-4 sm:px-6 lg:px-8 mt-16 rounded-t-3xl">
        <!-- Footer global -->
    </footer>
    <script src="{prefix}js/i18n.js"></script>
</body>
</html>"""

    # Réinjecter si c'était une page de stub
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        existing_code = f.read()

    if 'captivating destination' in existing_code or 'Explore More Options' in existing_code or 'Discover, Plan & Experience' in existing_code:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(rich_html_layout)
        updated_count += 1

print(f"\n✨ Fertig ! {updated_count} pages ont été enrichies avec un contenu SEO structuré et multilingue.")
