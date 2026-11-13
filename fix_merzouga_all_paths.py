import os
import re

target_file = "merzouga_2.html" if os.path.exists("merzouga_2.html") else "merzouga.html"
with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Lieux incontournables -> images/places/merzouga-[slug]/[slug]-hero.webp
places = [
    "erg-chebbi",
    "merzouga-village",
    "camel-trek",
    "desert-camp",
    "khamlia",
    "dayet-srji",
    "rissani",
    "hassilabied",
    "fossils",
]

for slug in places:
    folder = f"images/places/merzouga-{slug}"
    candidates = [
        f"{folder}/{slug}-hero.webp",
        f"{folder}/village-hero.webp",
        f"{folder}/{slug}.webp",
    ]
    chosen = candidates[0]
    for c in candidates:
        if os.path.exists(c):
            chosen = c
            break

    pattern = rf'(<a[^>]+href="places/merzouga-places/{re.escape(slug)}\.html"[^>]*>.*?<img[^>]+src=")[^"]*("[^>]*>)'
    content = re.sub(pattern, rf"\g<1>{chosen}\g<2>", content, flags=re.DOTALL)

# 2. Autres images de la page -> images/merzouga/...
other_map = {
    'alt="Desert camp Erg Chebbi"': "images/merzouga/stay-camp.webp",
    'alt="Kasbah hotel Merzouga"': "images/merzouga/stay-kasbah.webp",
    'alt="Hassi Labied auberge"': "images/merzouga/stay-hassilabied.webp",
    'alt="Restaurant Yasmina"': "images/merzouga/restau-yasmina.webp",
    'alt="Cafe du Sud Merzouga"': "images/merzouga/restau-cafe-du-sud.webp",
    'alt="Kasbah Mohayut restaurant"': "images/merzouga/restau-kasbah-mohayut.webp",
    'alt="Restaurant Berbere Hassilabied"': "images/merzouga/restau-berbere.webp",
    'alt="Camp dinner Merzouga"': "images/merzouga/restau-camp-dinner.webp",
    'alt="Erfoud and Draa Valley"': "images/merzouga/trip-erfoud-draa.webp",
    'alt="Erfoud town"': "images/merzouga/trip-erfoud.webp",
    'alt="Dades and Todra Gorges"': "images/merzouga/trip-dades-todra.webp",
    'alt="Marrakech Tichka pass"': "images/merzouga/trip-marrakech.webp",
}

for alt_attr, new_src in other_map.items():
    # Remplace src que src soit avant ou après alt dans la balise <img>
    p1 = rf'(<img\b[^>]*\b{re.escape(alt_attr)}[^>]*\bsrc=")[^"]*("[^>]*>)'
    p2 = rf'(<img\b[^>]*\bsrc=")[^"]*("[^>]*\b{re.escape(alt_attr)}[^>]*>)'
    content = re.sub(p1, rf"\g<1>{new_src}\g<2>", content)
    content = re.sub(p2, rf"\g<1>{new_src}\g<2>", content)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Mise à jour terminée sur {target_file}")
