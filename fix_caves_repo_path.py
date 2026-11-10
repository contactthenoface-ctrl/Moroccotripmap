filepath = "places/tanger-places/caves.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# On remplace les chemins relatifs ou erronés par le chemin absolu incluant /Moroccotripmap/
content = content.replace('../../images/', '/Moroccotripmap/images/')
content = content.replace('../..//Moroccotripmap/images/', '/Moroccotripmap/images/')
content = content.replace('/images/', '/Moroccotripmap/images/')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Chemins avec /Moroccotripmap/ appliqués pour caves.html !")
