import re

filepath = "agadir.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

images_agadir_eat = [
    "images/agadir/restau-pure-passion.webp",
    "images/agadir/restau-jardin.webp",
    "images/agadir/restau-al-jardin.webp",
    "images/agadir/restau-grills.webp",
    "images/agadir/restau-cafe.webp",
    "images/agadir/restau-villa-atlantique.webp"
]

# On utilise une liste d un seul élément pour contourner le scope nonlocal en Python
current_idx = [0]

def replace_img(m):
    img_tag = m.group(1)
    if current_idx[0] < len(images_agadir_eat):
        new_src = f'src="{images_agadir_eat[current_idx[0]]}"'
        current_idx[0] += 1
        return re.sub(r'src="[^"]*?"', new_src, img_tag)
    return img_tag

# Recherche globale des balises img dans le fichier agadir.html pour les cartes de restaurants
# On cible spécifiquement les images situées dans la section Eat
eat_section_pattern = r'(<!-- Where to Eat Section.*?<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">)(.*?)(<\/section>)'

match = re.search(eat_section_pattern, html, re.DOTALL)
if match:
    header = match.group(1)
    grid_content = match.group(2)
    footer = match.group(3)
    
    new_grid_content = re.sub(r'(<img[^>]*?>)', replace_img, grid_content)
    new_html = html.replace(match.group(0), header + new_grid_content + footer)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Succès : Les 6 images de restaurants d Agadir ont été injectées !")
else:
    print("Erreur : Section Where to Eat introuvable dans agadir.html")
