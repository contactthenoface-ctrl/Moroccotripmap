import re

filepath = "agadir.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Les 6 images exactes et dans l ordre des 6 cartes de restaurants d Agadir
correct_agadir_eat_images = [
    "images/agadir/restau-pure-passion.webp",    # 1. Pure Passion
    "images/agadir/restau-la-scala.webp",       # 2. La Scala
    "images/agadir/restau-le-17.webp",          # 3. Le 17 Café Restaurant
    "images/agadir/restau-du-port.webp",        # 4. Restaurant du Port
    "images/agadir/restau-jour-et-nuit.webp",   # 5. Jour et Nuit
    "images/agadir/restau-les-blancs.webp"      # 6. Les Blancs
]

current_idx = [0]

def replace_img(m):
    img_tag = m.group(1)
    if current_idx[0] < len(correct_agadir_eat_images):
        new_src = f'src="{correct_agadir_eat_images[current_idx[0]]}"'
        current_idx[0] += 1
        return re.sub(r'src="[^"]*?"', new_src, img_tag)
    return img_tag

# On cible précisément la section "Where to eat in Agadir" et sa grille de 6 cartes
eat_section_pattern = r'(Where to eat in Agadir.*?<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">)(.*?)(<\/section>)'

match = re.search(eat_section_pattern, html, re.DOTALL)
if match:
    header = match.group(1)
    grid_content = match.group(2)
    footer = match.group(3)
    
    # Remplacement des balises img de la grille de manière séquentielle
    new_grid_content = re.sub(r'(<img[^>]*?>)', replace_img, grid_content)
    new_html = html.replace(match.group(0), header + new_grid_content + footer)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Succès : Les bonnes images ont été associées aux restaurants d Agadir !")
else:
    print("Erreur : Section Where to eat introuvable dans agadir.html")
