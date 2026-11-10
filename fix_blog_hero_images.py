import glob

# On cible toutes les pages HTML de lieux à l'intérieur de places/tanger-places/
html_files = glob.glob("places/tanger-places/*.html")

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remplacement de l'image de blog vide par l'image hero de Tanger avec le bon chemin relatif
    # Dans places/tanger-places/, pour aller à la racine puis dans images/tanger/hero.webp, il faut '../../images/tanger/hero.webp'
    old_tag = '<img src="" alt="" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy"/>'
    new_tag = '<img src="../../images/tanger/hero.webp" alt="First time in Tangier" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy"/>'
    
    if old_tag in content:
        content = content.replace(old_tag, new_tag)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Image du blog corrigée dans : {filepath}")

