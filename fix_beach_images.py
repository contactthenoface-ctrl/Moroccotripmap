import glob

# On cherche tous les fichiers HTML du projet
html_files = glob.glob("**/*.html", recursive=True)

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # On corrige les éventuelles variations de chemins pour la plage de Tanger
    updated = content
    updated = updated.replace('images/tanger/beach/', 'images/places/tanger-beach/')
    updated = updated.replace('images/beach/', 'images/places/tanger-beach/')
    
    if updated != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Chemins de la plage corrigés dans : {filepath}")

