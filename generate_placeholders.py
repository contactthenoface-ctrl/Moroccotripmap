import os, glob, re

# Modèle de page temporaire aux couleurs de MoroccoTripMap
def get_template_html(title, depth):
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="fr" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — MoroccoTripMap</title>
    <link rel="stylesheet" href="{prefix}css/style.css">
</head>
<body class="bg-creme text-vert font-sans min-h-screen flex flex-col justify-between">

    <!-- HEADER / NAVIGATION -->
    <header class="bg-vert text-creme shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <a href="{prefix}index.html" class="text-2xl font-bold tracking-tight text-white">
                Morocco<span class="text-sable">TripMap</span>
            </a>
            <div class="flex items-center gap-4">
                <a href="{prefix}destinations.html" class="text-sm font-medium hover:text-sable transition" data-i18n="nav.destinations">Destinations</a>
                <a href="{prefix}blog/index.html" class="text-sm font-medium hover:text-sable transition" data-i18n="nav.blog">Blog</a>
            </div>
        </div>
    </header>

    <!-- HERO SECTION TEMPORAIRE -->
    <main class="flex-grow flex items-center justify-center px-4 py-16">
        <div class="max-w-2xl text-center bg-white p-8 sm:p-12 rounded-3xl shadow-xl border border-creme">
            <span class="inline-block bg-sable/20 text-vert font-semibold text-xs px-3 py-1 rounded-full mb-4 uppercase tracking-wider">Bientôt disponible</span>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-vert mb-4">{title}</h1>
            <p class="text-sm text-gray-600 mb-8 leading-relaxed">
                Cette page est actuellement en cours de préparation par nos équipes pour vous offrir le meilleur guide possible. Revenez très bientôt !
            </p>
            <div class="flex flex-col sm:flex-row justify-center gap-4">
                <a href="{prefix}index.html" class="bg-vert text-creme font-semibold px-6 py-3 rounded-xl hover:bg-vert/90 transition text-sm">
                    ← Retour à l'accueil
                </a>
                <a href="{prefix}destinations.html" class="bg-sable text-vert font-semibold px-6 py-3 rounded-xl hover:bg-sable/80 transition text-sm">
                    Explorer les destinations
                </a>
            </div>
        </div>
    </main>

    <!-- FOOTER ENRICHI & MULTILINGUE -->
    <footer class="bg-vert text-creme pt-12 pb-8 px-4 sm:px-6 lg:px-8 mt-16 rounded-t-3xl">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
            <div>
                <h3 class="text-xl font-bold mb-3 text-white">Morocco<span class="text-sable">TripMap</span></h3>
                <p class="text-xs text-creme/80 leading-relaxed" data-i18n="footer.about_text">
                    Discover. Plan. Experience Morocco.<br/>
                    The premier tourism directory and cultural travel guide for visitors exploring Morocco.
                </p>
            </div>
            <div>
                <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.recommended_title">Recommended Pages</h4>
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
                    <li><a class="hover:text-white transition" href="{prefix}blog/index.html" data-i18n="footer.link_blog">Blog Voyage & Conseils</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.connect_title">Connect</h4>
                <p class="text-xs text-creme/80 mb-3" data-i18n="footer.youtube_text">Follow our YouTube channel for video travel guides:</p>
                <a class="inline-flex items-center gap-2 bg-red-600 text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-red-700 transition" href="https://youtube.com/@moroccotripmap" rel="noopener noreferrer" target="_blank">
                    @moroccotripmap
                </a>
            </div>
        </div>
        <div class="max-w-7xl mx-auto border-t border-creme/10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-creme/70">
            <p data-i18n="footer.copyright">© MoroccoTripMap. All rights reserved.</p>
            <p>Created by <a class="text-sable underline font-semibold hover:text-white transition" href="https://kamliseo.com" rel="noopener noreferrer" target="_blank">Kamliseo</a></p>
        </div>
    </footer>

</body>
</html>
"""

# Scan des fichiers HTML existants pour trouver les liens cibles introuvables
html_files = glob.glob("**/*.html", recursive=True)
created_count = 0

for filepath in html_files:
    if "node_modules" in filepath:
        continue
    
    dir_name = os.path.dirname(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    hrefs = re.findall(r'href=["\x27](.*?)["\x27]', content)
    for href in hrefs:
        if not href or href.startswith(("http", "mailto:", "#", "javascript:", "data:")):
            continue
            
        clean_href = href.split("#")[0].split("?")[0]
        if not clean_href.endswith(".html"):
            continue
            
        target_path = os.path.normpath(os.path.join(dir_name, clean_href))
        
        # Si la cible n'existe pas, on la crée automatiquement !
        if not os.path.exists(target_path):
            target_dir = os.path.dirname(target_path)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            
            # Nom propre pour le titre basé sur le nom du fichier
            file_name_core = os.path.splitext(os.path.basename(target_path))[0]
            readable_title = file_name_core.replace("-", " ").capitalize()
            
            # Calcul de la profondeur pour les liens relatifs (../)
            depth = target_path.replace("\\", "/").count("/")
            
            html_code = get_template_html(readable_title, depth)
            with open(target_path, "w", encoding="utf-8") as target_file:
                target_file.write(html_code)
            
            print(f"Page temporaire créée : {target_path}")
            created_count += 1

print(f"\nGénération terminée ! {created_count} pages temporaires créées avec succès.")
