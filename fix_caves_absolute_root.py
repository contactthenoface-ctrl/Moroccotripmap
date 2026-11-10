filepath = "places/tanger-places/caves.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# On remplace tous les chemins d images par le chemin absolu propre du dépôt GitHub Pages
content = content.replace('../../images/places/tanger-caves/', '/Moroccotripmap/images/places/tanger-caves/')
content = content.replace('../..//Moroccotripmap/images/places/tanger-caves/', '/Moroccotripmap/images/places/tanger-caves/')
content = content.replace('images/places/tanger-caves/', '/Moroccotripmap/images/places/tanger-caves/')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Chemins absolus appliqués avec succès pour caves.html !")
