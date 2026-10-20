import json, os, glob, re

translations = {
    "en": {
        "footer": {
            "about_text": "Discover. Plan. Experience Morocco.\nThe premier tourism directory and cultural travel guide for visitors exploring Morocco.",
            "destinations_title": "Top Destinations",
            "categories_title": "Travel Categories",
            "connect_title": "Connect",
            "youtube_text": "Follow our YouTube channel for video travel guides:",
            "copyright": "© MoroccoTripMap. All rights reserved.",
            "link_marrakech": "Marrakech Travel Guide",
            "link_chefchaouen": "Chefchaouen Blue City",
            "link_fes": "Fes Ancient Medina",
            "link_merzouga": "Sahara Desert & Merzouga",
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
            "destinations_title": "Meilleures Destinations",
            "categories_title": "Catégories de Voyage",
            "connect_title": "Suivez-nous",
            "youtube_text": "Suivez notre chaîne YouTube pour nos guides vidéo :",
            "copyright": "© MoroccoTripMap. Tous droits réservés.",
            "link_marrakech": "Guide Voyage Marrakech",
            "link_chefchaouen": "Chefchaouen la Ville Bleue",
            "link_fes": "Ancienne Médina de Fès",
            "link_merzouga": "Désert du Sahara & Merzouga",
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
            "destinations_title": "Principales Destinos",
            "categories_title": "Categorías de Viaje",
            "connect_title": "Conéctate",
            "youtube_text": "Sigue nuestro canal de YouTube para guías en video:",
            "copyright": "© MoroccoTripMap. Todos los derechos reservados.",
            "link_marrakech": "Guía de Viaje a Marrakech",
            "link_chefchaouen": "Chefchaouen Ciudad Azul",
            "link_fes": "Antigua Medina de Fez",
            "link_merzouga": "Desierto del Sáhara y Merzouga",
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
            "destinations_title": "أبرز الوجهات",
            "categories_title": "تصنيفات السفر",
            "connect_title": "تواصل معنا",
            "youtube_text": "تابع قناتنا على يوتيوب لمشاهدة أدلة السفر المرئية:",
            "copyright": "© MoroccoTripMap. جميع الحقوق محفوظة.",
            "link_marrakech": "دليل سفر مراكش",
            "link_chefchaouen": "شفشاون المدينة الزرقاء",
            "link_fes": "فاس المدينة القديمة",
            "link_merzouga": "صحراء مرزوكة",
            "link_all_destinations": "جميع الوجهات ←",
            "link_stays": "رياضات وفنادق أصيلة",
            "link_restaurants": "المطبخ والأكلات المغربية",
            "link_experiences": "رحلات وأنشطة الصحراء",
            "link_transport": "النقل وتأجير السيارات",
            "link_itineraries": "برامج وجولات سياحية",
            "link_history": "تاريخ المغرب",
            "link_blog": "مدونة السفر والنصائح"
        }
    }
}

for lang, data in translations.items():
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
            print(f"Traduction mise a jour : {filepath}")

def get_footer_html(depth):
    prefix = "../" * depth
    return f"""<footer class="bg-vert text-creme pt-12 pb-8 px-4 sm:px-6 lg:px-8 mt-16 rounded-t-3xl">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
        <div>
            <h3 class="text-xl font-bold mb-3 text-white">Morocco<span class="text-sable">TripMap</span></h3>
            <p class="text-xs text-creme/80 leading-relaxed" data-i18n="footer.about_text">
                Discover. Plan. Experience Morocco.<br/>
                The premier tourism directory and cultural travel guide for visitors exploring Morocco.
            </p>
        </div>
        <div>
            <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.destinations_title">Top Destinations</h4>
            <ul class="text-xs space-y-2 text-creme/80">
                <li><a class="hover:text-white transition" href="{prefix}marrakech.html" data-i18n="footer.link_marrakech">Marrakech Travel Guide</a></li>
                <li><a class="hover:text-white transition" href="{prefix}chefchaouen.html" data-i18n="footer.link_chefchaouen">Chefchaouen Blue City</a></li>
                <li><a class="hover:text-white transition" href="{prefix}fes.html" data-i18n="footer.link_fes">Fes Ancient Medina</a></li>
                <li><a class="hover:text-white transition" href="{prefix}merzouga.html" data-i18n="footer.link_merzouga">Sahara Desert & Merzouga</a></li>
                <li><a class="hover:text-white transition font-semibold text-sable" href="{prefix}destinations.html" data-i18n="footer.link_all_destinations">All Destinations →</a></li>
            </ul>
        </div>
        <div>
            <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.categories_title">Travel Categories</h4>
            <ul class="text-xs space-y-2 text-creme/80">
                <li><a class="hover:text-white transition" href="{prefix}riads/index.html" data-i18n="footer.link_stays">Authentic Riads & Hotels</a></li>
                <li><a class="hover:text-white transition" href="{prefix}gastronomy/index.html" data-i18n="footer.link_restaurants">Moroccan Gastronomy & Food</a></li>
                <li><a class="hover:text-white transition" href="{prefix}experiences/index.html" data-i18n="footer.link_experiences">Desert Tours & Activities</a></li>
                <li><a class="hover:text-white transition" href="{prefix}transport/index.html" data-i18n="footer.link_transport">Transport & Rental Cars</a></li>
                <li><a class="hover:text-white transition" href="{prefix}programmes/index.html" data-i18n="footer.link_itineraries">Circuits & Itineraries</a></li>
                <li><a class="hover:text-white transition" href="{prefix}guides/histoire.html" data-i18n="footer.link_history">History of Morocco</a></li>
                <li><a class="hover:text-white transition" href="{prefix}blog/index.html" data-i18n="footer.link_blog">Travel Blog & Tips</a></li>
            </ul>
        </div>
        <div>
            <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.connect_title">Connect</h4>
            <p class="text-xs text-creme/80 mb-3" data-i18n="footer.youtube_text">Follow our YouTube channel for video travel guides:</p>
            <a class="inline-flex items-center gap-2 bg-red-600 text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-red-700 transition" href="https://youtube.com/@moroccotripmap" rel="noopener noreferrer" target="_blank">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"></path></svg>
                @moroccotripmap
            </a>
        </div>
    </div>
    <div class="max-w-7xl mx-auto border-t border-creme/10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-creme/70">
        <p data-i18n="footer.copyright">© MoroccoTripMap. All rights reserved.</p>
        <p>Created by <a class="text-sable underline font-semibold hover:text-white transition" href="https://kamliseo.com" rel="noopener noreferrer" target="_blank">Kamliseo</a></p>
    </div>
</footer>"""

html_files = glob.glob("**/*.html", recursive=True)
updated_count = 0

for filepath in html_files:
    if "node_modules" in filepath:
        continue
    rel_path = os.path.relpath(filepath)
    depth = rel_path.count(os.sep)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = re.compile(r'<footer[\s\S]*?</footer>', re.IGNORECASE)
    if pattern.search(content):
        new_footer = get_footer_html(depth)
        new_content = pattern.sub(new_footer, content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_count += 1

print(f"Footer enrichi applique sur {updated_count} fichiers HTML avec succes !")
