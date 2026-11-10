filepath = "places/tanger-places/caves.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# On normalise TOUTES les variantes d'images erronées vers le format standard fonctionnel '../../images/...'
import re
# Remplace n'importe quel préfixe erroné (ex: ../..//Moroccotripmap/images/ ou images/) par '../../images/'
content = re.sub(r'(\.\./)*(\./)?(Moroccotripmap/)?images/', '../../images/', content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("caves.html est désormais aligné sur le modèle de hafa.html !")
