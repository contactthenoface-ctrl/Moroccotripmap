import os, glob, re

def get_true_unique_footer(rel_path, depth):
    prefix = "../" * depth
    
        # Dictionnaire des liens spécifiques par fichier exact
    links_map = {
        "index.html": [
            ("Marrakech Travel Guide", "marrakech.html"),
            ("Chefchaouen Blue City", "chefchaouen.html"),
            ("Fes Ancient Medina", "fes.html"),
            ("Sahara Desert & Merzouga", "merzouga.html")
        ],
        "marrakech.html": [
            ("Chefchaouen Blue City", "chefchaouen.html"),
            ("Sahara Desert Merzouga", "merzouga.html"),
            ("Authentic Riads & Hotels", "riads/index.html"),
            ("Moroccan Gastronomy & Food", "gastronomy/index.html")
        ],
        "chefchaouen.html": [
            ("Marrakech Travel Guide", "marrakech.html"),
            ("Fes Ancient Medina", "fes.html"),
            ("Desert Tours & Activities", "experiences/index.html"),
            ("Travel Blog & Tips", "blog/index.html")
        ],
        "fes.html": [
            ("History of Morocco", "guides/histoire.html"),
            ("Chefchaouen Blue City", "chefchaouen.html"),
            ("Cultural Itineraries", "programmes/index.html"),
            ("Riads in Morocco", "riads/index.html")
        ],
        "merzouga.html": [
            ("Marrakech Travel Guide", "marrakech.html"),
            ("Desert Tours & Activities", "experiences/index.html"),
            ("Transport & Rental Cars", "transport/index.html"),
            ("Travel Blog & Tips", "blog/index.html")
        ],
        "destinations.html": [
            ("Marrakech Travel Guide", "marrakech.html"),
            ("Chefchaouen Blue City", "chefchaouen.html"),
            ("Fes Ancient Medina", "fes.html"),
            ("Sahara Desert & Merzouga", "merzouga.html")
        ],
        "riads/index.html": [
            ("Marrakech Stays & Riads", "marrakech.html"),
            ("Chefchaouen Blue City", "chefchaouen.html"),
            ("Moroccan Gastronomy & Food", "gastronomy/index.html"),
            ("Desert Tours & Activities", "experiences/index.html")
        ],
        "gastronomy/index.html": [
            ("Marrakech Food Guide", "marrakech.html"),
            ("Fes Ancient Medina", "fes.html"),
            ("Authentic Riads & Hotels", "riads/index.html"),
            ("Travel Blog & Tips", "blog/index.html")
        ],
        "experiences/index.html": [
            ("Sahara Desert Merzouga", "merzouga.html"),
            ("Marrakech Travel Guide", "marrakech.html"),
            ("Transport & Rental Cars", "transport/index.html"),
            ("Circuits & Itineraries", "programmes/index.html")
        ],
        "transport/index.html": [
            ("Sahara Desert Merzouga", "merzouga.html"),
            ("Marrakech Travel Guide", "marrakech.html"),
            ("Desert Tours & Activities", "experiences/index.html"),
            ("All Destinations", "destinations.html")
        ],
        "programmes/index.html": [
            ("History of Morocco", "guides/histoire.html"),
            ("Sahara Desert Merzouga", "merzouga.html"),
            ("Marrakech Travel Guide", "marrakech.html"),
            ("Travel Blog & Tips", "blog/index.html")
        ],
        "guides/histoire.html": [
            ("Fes Ancient Medina", "fes.html"),
            ("Marrakech Imperial Guide", "marrakech.html"),
            ("Cultural Itineraries", "programmes/index.html"),
            ("Travel Blog & Tips", "blog/index.html")
        ],
        "blog/index.html": [
            ("History of Morocco", "guides/histoire.html"),
            ("Explore All Destinations", "destinations.html"),
            ("Authentic Riads & Hotels", "riads/index.html"),
            ("Itineraries & Circuits", "programmes/index.html")
        ]
    }

    # Récupération des liens spécifiques ou d'un set par défaut si non listé
    page_links = links_map.get(rel_path, [
        ("Marrakech Travel Guide", "marrakech.html"),
        ("Chefchaouen Blue City", "chefchaouen.html"),
        ("Travel Blog & Tips", "blog/index.html"),
        ("History of Morocco", "guides/histoire.html")
    ])

    context_links_html = ""
    for title, link in page_links:
        context_links_html += f'                <li><a class="hover:text-white transition" href="{prefix}{link}">{title}</a></li>\n'

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
            <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider">Recommended Pages</h4>
            <ul class="text-xs space-y-2 text-creme/80">
{context_links_html}
                <li><a class="hover:text-white transition font-semibold text-sable" href="{prefix}destinations.html">All Destinations →</a></li>
            </ul>
        </div>
        <div>
            <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.categories_title">Travel Categories</h4>
            <ul class="text-xs space-y-2 text-creme/80">
                <li><a class="hover:text-white transition" href="{prefix}riads/index.html">Authentic Riads & Hotels</a></li>
                <li><a class="hover:text-white transition" href="{prefix}gastronomy/index.html">Moroccan Gastronomy & Food</a></li>
                <li><a class="hover:text-white transition" href="{prefix}experiences/index.html">Desert Tours & Activities</a></li>
                <li><a class="hover:text-white transition" href="{prefix}transport/index.html">Transport & Rental Cars</a></li>
                <li><a class="hover:text-white transition" href="{prefix}programmes/index.html">Circuits & Itineraries</a></li>
                <li><a class="hover:text-white transition" href="{prefix}blog/index.html">Travel Blog & Tips</a></li>
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
    rel_path = os.path.relpath(filepath).replace("\\", "/")
    depth = rel_path.count("/")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = re.compile(r'<footer[\s\S]*?</footer>', re.IGNORECASE)
    if pattern.search(content):
        new_footer = get_true_unique_footer(rel_path, depth)
        new_content = pattern.sub(new_footer, content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_count += 1

print(f"Footers 100% uniques appliques avec succes sur {updated_count} fichiers HTML !")
