filepath = "places/tanger-places/caves.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Remplacement de tous les chemins relatifs des images du dossier tanger-caves par un chemin absolu propre
# On s'assure que le chemin commence par /Moroccotripmap/images/ ou /images/ selon la structure GitHub Pages
content = content.replace('../../images/places/tanger-caves/', '/Moroccotripmap/images/places/tanger-caves/')
content = content.replace('../../../images/places/tanger-caves/', '/Moroccotripmap/images/places/tanger-caves/')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Chemins absolus appliqués pour caves.html !")
