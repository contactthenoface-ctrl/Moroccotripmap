filepath = "places/tanger-places/caves.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# On remplace les chemins erronés par le bon chemin relatif (../../images/places/tanger-caves/)
content = content.replace('../../../images/places/tanger-caves/', '../../images/places/tanger-caves/')
content = content.replace('../images/places/tanger-caves/', '../../images/places/tanger-caves/')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Chemins de caves.html corrigés avec succès !")
