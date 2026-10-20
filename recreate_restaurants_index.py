import os, re
from pathlib import Path

print("🛠️ --- RECRÉATION PROPRE DES PAGES RESTAURANTS --- 🛠️\n")

source_page = Path('marrakech.html')
if not source_page.exists():
    source_page = Path('index.html')

with open(source_page, 'r', encoding='utf-8', errors='ignore') as f:
    source_html = f.read()

# Extraire le header et le footer de la page modèle
header_match = re.search(r'(<header[\s\S]*?</header>)', source_html, re.IGNORECASE)
footer_match = re.search(r'(<footer[\s\S]*?</footer>)', source_html, re.IGNORECASE)

header = header_match.group(1) if header_match else ""
footer = footer_match.group(1) if footer_match else ""

# Adapter les chemins pour le sous-dossier restaurants/
header_sub = header.replace('href="', 'href="../').replace('href="../http', 'href="http').replace('href="../#', 'href="#')
footer_sub = footer.replace('href="', 'href="../').replace('href="../http', 'href="http').replace('href="../#', 'href="#')

complete_html = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoroccoTripMap - Moroccan Restaurants Directory</title>
    <meta name="description" content="Discover the best traditional Moroccan restaurants, cafes, and culinary experiences.">
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body class="bg-creme text-vert font-sans">
    {header_sub}
    
    <main class="max-w-7xl mx-auto px-4 py-12 min-h-[60vh]">
        <div class="text-center mb-12">
            <span class="text-xs uppercase tracking-widest bg-sable/20 px-3 py-1 rounded-full font-semibold" data-i18n="badge.gastronomy">Gastronomy</span>
            <h1 class="text-4xl font-bold mt-3 mb-4 text-vert">Moroccan Restaurants</h1>
            <p class="text-gray-600 max-w-2xl mx-auto">Explore authentic dining experiences, local flavors, and top-rated restaurants across Morocco.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <h3 class="font-bold text-lg mb-2">Traditional Cuisine</h3>
                <p class="text-sm text-gray-600 mb-4">Savor authentic tajines, couscous, and pastilla prepared with local spices.</p>
                <a href="index.html" class="text-vert font-semibold text-sm underline">View guides &rarr;</a>
            </div>
        </div>
    </main>

    {footer_sub}
    <script src="../js/i18n.js"></script>
</body>
</html>
"""

targets = [
    Path('restaurants/index.html'),
    Path('moroccotripmap/restaurants/index.html')
]

for file_path in targets:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(complete_html, encoding='utf-8')
    print(f"✅ Page régénérée avec succès : {file_path}")

print("\n✨ Fini ! Relance le check.")
