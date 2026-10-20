import os, json, re
from pathlib import Path

print("🚀 --- DUPLICATION EXACTE DE LA STRUCTURE MARRAKECH --- 🚀\n")

# Read full original marrakech.html
with open('marrakech.html', 'r', encoding='utf-8') as f:
    marrakech_template = f.read()

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts and f.name not in ['index.html', 'destinations.html', 'marrakech.html', 'contact.html']]
trans_dir = Path('js/translations')

updated = 0

for file_path in html_files:
    # Skip deep nested files except direct places
    depth = len(file_path.relative_to('.').parts) - 1
    prefix = '../' * depth if depth > 0 else ''
    
    city_slug = file_path.stem
    city_name = city_slug.replace('-', ' ').title()
    
    # Custom replaces to adapt template without losing HTML elements
    page_content = marrakech_template
    
    # Adjust asset relative paths
    if prefix:
        page_content = page_content.replace('href="css/', f'href="{prefix}css/')
        page_content = page_content.replace('src="images/', f'src="{prefix}images/')
        page_content = page_content.replace('src="js/', f'src="{prefix}js/')
        page_content = page_content.replace('href="index.html"', f'href="{prefix}index.html"')
        page_content = page_content.replace('href="destinations.html"', f'href="{prefix}destinations.html"')
        page_content = page_content.replace('href="contact.html"', f'href="{prefix}contact.html"')
        page_content = page_content.replace('href="riads/index.html"', f'href="{prefix}riads/index.html"')
        page_content = page_content.replace('href="gastronomy/index.html"', f'href="{prefix}gastronomy/index.html"')
        page_content = page_content.replace('href="experiences/index.html"', f'href="{prefix}experiences/index.html"')
        page_content = page_content.replace('href="transport/index.html"', f'href="{prefix}transport/index.html"')
        page_content = page_content.replace('href="programmes/index.html"', f'href="{prefix}programmes/index.html"')
        page_content = page_content.replace('href="guides/', f'href="{prefix}guides/')
        page_content = page_content.replace('href="blog/', f'href="{prefix}blog/')

    # Replace specific Marrakech strings for title and headers
    page_content = re.sub(r'<title>.*?</title>', f'<title data-i18n="{city_slug}_page.seo.title">{city_name} Travel Guide | Things to Do &amp; Tips | MoroccoTripMap</title>', page_content, flags=re.IGNORECASE)
    page_content = page_content.replace('Marrakech', city_name)
    page_content = page_content.replace('marrakech', city_slug)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page_content)
        
    # Build complete JSON translation files for en, fr, es, ar
    for lang in ['en', 'fr', 'es', 'ar']:
        lang_dir = trans_dir / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        json_file = lang_dir / f"{city_slug}_page.json"
        
        # Load existing or create new JSON
        data = {}
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
            except Exception:
                data = {}

        if f"{city_slug}_page" not in data:
            data[f"{city_slug}_page"] = {}

        # Set fallback structure to ensure language switcher reads keys
        data[f"{city_slug}_page"]["seo"] = {
            "title": f"{city_name} Travel Guide 2026 | MoroccoTripMap",
            "description": f"Explore {city_name} in Morocco: attractions, stays, food, and day trips."
        }
        data[f"{city_slug}_page"]["hero_subtitle"] = f"Discover the authentic charm and unique experiences of {city_name}."

        with open(json_file, 'w', encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)

    updated += 1

print(f"✅ {updated} pages HTML ont été fidèlement clonées depuis le master Marrakech avec header, mobile-menu, footer et traductions !")
