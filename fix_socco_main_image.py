import glob

# On cherche tous les fichiers HTML du projet (tanger.html, pages de lieux, etc.)
html_files = glob.glob("**/*.html", recursive=True)

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Si le fichier mentionne le socco avec socco-01.webp comme image principale
    if "socco-01.webp" in content:
        # On remplace par socco.webp uniquement pour les miniatures principales / hero liées au socco
        # On garde les autres (socco-02, socco-03...) pour la galerie
        updated = content.replace('images/places/tanger-socco/socco-01.webp', 'images/places/tanger-socco/socco.webp')
        updated = updated.replace('images/tanger/socco/socco-01.webp', 'images/places/tanger-socco/socco.webp')
        
        if updated != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"Image principale mise à jour dans : {filepath}")

