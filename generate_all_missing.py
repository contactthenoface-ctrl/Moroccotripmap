import os, re
from pathlib import Path

# 1. Analyse des liens manquants dans le projet
html_files = list(Path('.').rglob('*.html'))
missing_paths = set()

for file_path in html_files:
    if 'node_modules' in file_path.parts:
        continue
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        links = re.findall(r'href=["\']([^"\']+\.html)["\']', content)
        for link in links:
            if link.startswith(('http://', 'https://', 'mailto:')):
                continue
            target_path = (file_path.parent / link).resolve()
            if not target_path.exists():
                # On conserve le chemin relatif par rapport à la racine du projet
                try:
                    rel_p = target_path.relative_to(Path('.').resolve())
                    missing_paths.add(rel_p)
                except ValueError:
                    pass

print(f"🔍 {len(missing_paths)} fichiers uniques à générer.")

# 2. Modèle HTML standardisé avec maillage interne
def get_template(rel_path):
    parts = rel_path.parts
    filename = rel_path.name
    clean_name = filename.replace('.html', '').replace('-', ' ').title()
    
    # Calcul de la profondeur pour les chemins relatifs CSS et Liens
    depth = len(parts) - 1
    prefix = "../" * depth if depth > 0 else ""

    # Catégorie et métadonnées adaptées
    if 'blog' in parts or 'food-guide' in filename or 'first-time' in filename:
        category = "Travel Blog & Food Guide"
        h1_title = clean_name
        subtitle = "Authentic Local Insights & Culinary Highlights"
        intro = f"Welcome to our detailed guide on {clean_name}. Discover the best local flavors, hidden spots, and practical tips verified on the ground in Morocco."
    elif 'places' in parts:
        category = "Must-Visit Attractions"
        h1_title = clean_name
        subtitle = "Explore Top Landmarks & Cultural Gems"
        intro = f"{clean_name} is one of the most remarkable sights to visit. Experience the rich history, architecture, and authentic atmosphere of this unique location."
    elif 'restaurants' in parts:
        category = "Dining & Gastronomy"
        h1_title = clean_name
        subtitle = "Traditional Flavors & Local Cuisine"
        intro = f"Experience authentic Moroccan dining at {clean_name}. From traditional tajines and couscous to rooftop views and warm hospitality."
    else:
        category = "Moroccan Destinations"
        h1_title = clean_name
        subtitle = "Discover, Plan & Experience"
        intro = f"Explore {clean_name}, a captivating destination offering unforgettable landscapes, historical heritage, and rich cultural experiences in Morocco."

    return f"""<!DOCTYPE html>
<html class="scroll-smooth" dir="ltr" lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{prefix}css/styles.css" />
  <link rel="stylesheet" href="{prefix}css/style.css" />
  <title>{h1_title} | MoroccoTripMap Travel Guide</title>
  <meta name="description" content="{intro}" />
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%23185336' d='M12 1.5C7.44 1.5 3.75 5.19 3.75 9.75c0 6.12 7.13 12.24 7.72 12.73a.85.85 0 0 0 1.06 0c.59-.49 7.72-6.61 7.72-12.73C20.25 5.19 16.56 1.5 12 1.5Zm0 11.63a3.38 3.38 0 1 1 0-6.76 3.38 3.38 0 0 1 0 6.76Z'/></svg>"/>
</head>
<body class="bg-creme text-sombre antialiased flex flex-col min-h-screen">

<!-- Header Navigation -->
<header class="sticky top-0 z-50 bg-creme/90 backdrop-blur-md border-b border-sable/10 transition-all">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
    <a class="flex items-center gap-3 group shrink-0" href="{prefix}index.html" aria-label="MoroccoTripMap Home">
      <span class="text-xl font-bold text-vert">Morocco<span class="text-sable">TripMap</span></span>
    </a>
    <nav class="hidden md:flex items-center gap-6 lg:gap-8 text-base font-medium text-sombre/80">
      <a class="hover:text-vert transition" href="{prefix}destinations.html">Destinations</a>
      <a class="hover:text-vert transition" href="{prefix}guides/index.html">Travel Guides</a>
      <a class="hover:text-vert transition" href="{prefix}blog/index.html">Blog</a>
      <a class="hover:text-vert transition" href="{prefix}contact.html">Contact</a>
    </nav>
    <a class="bg-vert text-creme text-sm font-semibold px-5 py-2.5 rounded-xl hover:bg-vert/90 transition shadow-sm" href="{prefix}index.html#map">Interactive Map</a>
  </div>
</header>

<!-- Main Content -->
<main class="flex-grow max-w-4xl mx-auto px-4 py-12">
  <div class="mb-6">
    <span class="text-xs font-bold uppercase tracking-widest text-sable bg-sable/10 px-3 py-1 rounded-full">{category}</span>
    <h1 class="text-3xl sm:text-4xl font-bold text-sombre mt-3">{h1_title}</h1>
    <p class="text-lg text-sable font-medium mt-1">{subtitle}</p>
  </div>

  <div class="bg-white rounded-3xl p-8 border border-sable/15 shadow-sm space-y-6 text-sombre/80 leading-relaxed">
    <p class="text-lg font-medium text-sombre">{intro}</p>
    <p>This page is part of the <a href="{prefix}index.html" class="text-vert font-semibold underline hover:text-sable">MoroccoTripMap</a> directory, providing curated and verified travel insights across all regions of Morocco.</p>
    
    <h2 class="text-2xl font-bold text-sombre pt-4">Explore More Options</h2>
    <p>Plan your perfect itinerary by combining cultural landmarks, traditional stays, and authentic experiences. Check our <a href="{prefix}guides/index.html" class="text-vert font-semibold underline hover:text-sable">Travel Guides</a> or explore articles on our <a href="{prefix}blog/index.html" class="text-vert font-semibold underline hover:text-sable">Morocco Travel Blog</a>.</p>
    
    <div class="pt-6 border-t border-sable/10 flex flex-wrap gap-4">
      <a href="{prefix}destinations.html" class="bg-vert text-white px-6 py-3 rounded-xl font-semibold text-sm hover:bg-vert/90 transition">Explore All Destinations</a>
      <a href="{prefix}blog/index.html" class="border-2 border-vert text-vert px-6 py-3 rounded-xl font-semibold text-sm hover:bg-vert hover:text-white transition">Read Blog Articles</a>
    </div>
  </div>
</main>

<!-- Footer -->
<footer class="bg-vert text-creme pt-12 pb-8 px-4 sm:px-6 lg:px-8 mt-16 rounded-t-3xl">
<div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
<div>
<h3 class="text-xl font-bold mb-3 text-white">Morocco<span class="text-sable">TripMap</span></h3>
<p class="text-xs text-creme/80 leading-relaxed">Discover. Plan. Experience Morocco. The premier tourism directory and cultural travel guide.</p>
</div>
<div>
<h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider">Popular Cities</h4>
<ul class="text-xs space-y-2 text-creme/80">
<li><a class="hover:text-white transition" href="{prefix}marrakech.html">Marrakech Guide</a></li>
<li><a class="hover:text-white transition" href="{prefix}chefchaouen.html">Chefchaouen Highlights</a></li>
<li><a class="hover:text-white transition" href="{prefix}fes.html">Fès Medina</a></li>
<li><a class="hover:text-white transition" href="{prefix}rabat.html">Rabat Capital</a></li>
</ul>
</div>
<div>
<h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider">Guides & Categories</h4>
<ul class="text-xs space-y-2 text-creme/80">
<li><a class="hover:text-white transition" href="{prefix}riads/index.html">Riads & Stays</a></li>
<li><a class="hover:text-white transition" href="{prefix}gastronomy/index.html">Gastronomy & Food</a></li>
<li><a class="hover:text-white transition" href="{prefix}blog/index.html">Travel Blog</a></li>
</ul>
</div>
<div>
<h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider">Connect</h4>
<a class="inline-flex items-center gap-2 bg-red-600 text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-red-700 transition" href="https://youtube.com/@moroccotripmap" target="_blank">YouTube Channel</a>
</div>
</div>
<div class="max-w-7xl mx-auto border-t border-creme/10 pt-6 flex justify-between items-center text-xs text-creme/70">
<p>© MoroccoTripMap. All rights reserved.</p>
<p>Created by <a class="text-sable underline font-semibold" href="https://kamliseo.com" target="_blank">Kamliseo</a></p>
</div>
</footer>
</body>
</html>
"""

# 3. Création effective des fichiers
count = 0
for rel_path in missing_paths:
    full_path = Path('.').resolve() / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    html_content = get_template(rel_path)
    full_path.write_text(html_content, encoding='utf-8')
    count += 1
    print(f"✅ Created ({count}/{len(missing_paths)}): {rel_path}")

print("\n🎉 Génération terminée avec succès !")
