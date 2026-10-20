import os, re
from pathlib import Path

print("🔧 --- HARMONISATION DU HEADER RESPONSIVE & MENU LINGUISTIQUE --- 🔧\n")

html_files = [
    f for f in Path('.').rglob('*.html') 
    if 'node_modules' not in f.parts
]

count = 0

for file_path in html_files:
    depth = len(file_path.parts) - 1
    prefix = "../" * depth

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Template Header Complet avec Hamburger + Selecteur de langues + Menu Mobile
    full_header_template = f"""    <!-- Header -->
    <header class="sticky top-0 z-50 bg-creme/90 backdrop-blur-md border-b border-sable/10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <!-- Logo -->
            <a class="flex items-center gap-3 group shrink-0" href="{prefix}index.html">
                <img alt="MoroccoTripMap Logo" class="h-12 sm:h-14 w-auto object-contain" src="{prefix}images/logo.webp"/>
            </a>

            <!-- Navigation Desktop -->
            <nav class="hidden md:flex items-center gap-6 lg:gap-8 text-base font-medium text-sombre/80">
                <a class="hover:text-vert transition" href="{prefix}destinations.html" data-i18n="nav.destinations">Destinations</a>
                <a class="hover:text-vert transition" href="{prefix}contact.html" data-i18n="nav.contact">Contact</a>
            </nav>

            <!-- Language Selector & Mobile Hamburger -->
            <div class="flex items-center gap-3 sm:gap-4">
                <!-- Selecteur de langue i18n -->
                <div class="relative inline-block text-left" id="lang-selector"></div>

                <!-- Bouton Hamburger Mobile -->
                <button id="mobile-menu-btn" type="button" class="md:hidden inline-flex items-center justify-center p-2 rounded-xl text-sombre/80 hover:text-vert hover:bg-sable/10 focus:outline-none" aria-label="Toggle Menu">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                </button>
            </div>
        </div>

        <!-- Menu Mobile Dépliant -->
        <div id="mobile-menu" class="hidden md:hidden border-t border-sable/10 bg-creme px-4 pt-3 pb-6 space-y-2">
            <a class="block px-3 py-2 rounded-lg text-base font-medium text-sombre/80 hover:text-vert hover:bg-sable/10 transition" href="{prefix}destinations.html" data-i18n="nav.destinations">Destinations</a>
            <a class="block px-3 py-2 rounded-lg text-base font-medium text-sombre/80 hover:text-vert hover:bg-sable/10 transition" href="{prefix}contact.html" data-i18n="nav.contact">Contact</a>
        </div>
    </header>"""

    # Script d'activation du menu hamburger si non présent
    hamburger_script = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const btn = document.getElementById('mobile-menu-btn');
            const menu = document.getElementById('mobile-menu');
            if (btn && menu) {
                btn.addEventListener('click', () => {
                    menu.classList.toggle('hidden');
                });
            }
        });
    </script>
    """

    # Remplacement du header
    if '<header' in content:
        content = re.sub(r'<header.*?</header>', full_header_template, content, flags=re.DOTALL)
        
        # Ajout du script hamburger s'il manque
        if 'mobile-menu-btn' not in content:
            content = content.replace('</body>', f'{hamburger_script}\n</body>')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        count += 1

print(f"✅ Terminé ! {count} pages ont été équipées de l'en-tête responsive complet.")
