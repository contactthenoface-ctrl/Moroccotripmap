import re

filepath = "agadir.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Association directe et explicite entre le nom de la structure (ou clé i18n) et son image
mapping = {
    "agadir_page.eat.nomad.title": "images/agadir/restau-pure-passion.webp",
    "agadir_page.eat.jardin.title": "images/agadir/restau-la-scala.webp",
    "agadir_page.eat.fassia.title": "images/agadir/restau-le-17.webp",
    "agadir_page.eat.moha.title": "images/agadir/restau-du-port.webp",
    "agadir_page.eat.bacha.title": "images/agadir/restau-jour-et-nuit.webp",
    "agadir_page.eat.elfenn.title": "images/agadir/restau-les-blancs.webp"
}

# On parcourt chaque clé pour remplacer l'image située juste au-dessus du bloc correspondant
for key, img_path in mapping.items():
    # Trouve la balise img située dans la même carte que la clé i18n
    pattern = rf'(<div class="relative h-48 w-full overflow-hidden[^"]*">\s*<img\s+src=")[^"]*("[^>]*?>.*?data-i18n="{key}")'
    html = re.sub(pattern, rf'\1{img_path}\2', html, flags=re.DOTALL)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)

print("Mapping exact des restaurants d'Agadir appliqué avec succès !")
