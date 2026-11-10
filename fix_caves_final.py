filepath = "places/tanger-places/caves.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# On remplace toutes les variations erronées par le chemin relatif propre : ../../images/
content = content.replace('../..//Moroccotripmap/images/', '../../images/')
content = content.replace('../../Moroccotripmap/images/', '../../images/')
content = content.replace('../../../../images/', '../../images/')
content = content.replace('../../../images/', '../../images/')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Chemins de caves.html corrigés à la perfection !")
