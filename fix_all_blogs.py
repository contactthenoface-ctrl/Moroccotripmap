import glob

# On cible tous les sous-dossiers de lieux (ex: places/tanger-places/, places/agadir-places/, etc.)
place_dirs = glob.glob("places/*-places/")

for d in place_dirs:
    # On extrait le nom de la ville (ex: tanger, agadir...) à partir du nom du dossier
    city = d.split("/")[1].split("-")[0]
    
    html_files = glob.glob(f"{d}*.html")
    for filepath in html_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Le chemin relatif depuis places/[ville]-places/ vers images/[ville]/hero.webp nécessite ../../
        old_tag = '<img src="" alt="" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy"/>'
        new_tag = f'<img src="../../images/{city}/hero.webp" alt="First time in {city}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy"/>'
        
        # Gestion au cas où le src est vide mais avec des attributs légèrement différents
        if old_tag in content:
            content = content.replace(old_tag, new_tag)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Blog mis à jour pour la ville ({city}) : {filepath}")

