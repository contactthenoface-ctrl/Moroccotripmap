import os, re
from pathlib import Path

print("🔧 --- HARMONISATION DES NOUVELLES PAGES UNIQUEMENT --- 🔧\n")

# Vos pages manuelles et principales à NE PAS TOUCHER sous aucun prétexte
PROTECTED_PAGES = [
    'index.html', 'destinations.html', 'marrakech.html', 'contact.html',
    'agadir.html', 'essaouira.html', 'rabat.html', 'casablanca.html', 'fes.html',
    'chefchaouen.html', 'ouarzazate.html', 'tangier.html', 'tanger.html', 'meknes.html'
]

# Modèle standard d'Header + Scripts i18n
HEADER_TEMPLATE = """    <!-- Header -->
    <header class="sticky top-0 z-50 bg-creme/90 backdrop-blur-md border-b border-sable/10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <a class="flex items-center gap-3 group shrink-0" href="index.html">
                <img alt="MoroccoTripMap Logo" class="h-12 sm:h-14 w-auto object-contain" src="images/logo.webp"/>
            </a>
            <nav class="hidden md:flex items-center gap-6 lg:gap-8 text-base font-medium text-sombre/80">
                <a class="hover:text-vert transition" href="destinations.html" data-i18n="nav.destinations">Destinations</a>
                <a class="hover:text-vert transition" href="contact.html" data-i18n="nav.contact">Contact</a>
            </nav>
            <div class="flex items-center gap-4">
                <!-- Selecteur de langue i18n -->
                <div class="relative inline-block text-left" id="lang-selector">
                    <!-- Généré dynamiquement par i18n.js -->
                </div>
            </div>
        </div>
    </header>"""

html_files = [
    f for f in Path('.').rglob('*.html') 
    if 'node_modules' not in f.parts and f.name not in PROTECTED_PAGES
]

count = 0

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Détecte si la page contient le sélecteur de langue défectueux ou une structure hybride
    if 'Explore Larache' in content or 'Discover, Plan & Experience' in content or 'الصفحة قيد الإعداد' in content or '<header' in content:
        
        # 1. Remplacement/Vérification du chargement de i18n.js à la fin du body
        if 'js/i18n.js' not in content:
            content = content.replace('</body>', '    <script src="js/i18n.js"></script>\n</body>')

        # 2. Remplacement du Header défectueux par le Header standard
        content = re.sub(r'<header.*?</header>', HEADER_TEMPLATE, content, flags=re.DOTALL)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        count += 1

print(f"✅ Terminé ! {count} nouvelles pages ont été harmonisées avec le header officiel et le sélecteur de langue réparé.")
