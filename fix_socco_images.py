import os, glob

# On cherche le fichier HTML du Grand Socco (souvent dans places/tanger-places/socco.html ou similaire)
html_files = glob.glob("**/socco.html", recursive=True) + glob.glob("**/grand-socco.html", recursive=True)

if not html_files:
    # Recherche plus large si le nom exact diffère
    html_files = [f for f in glob.glob("**/*.html", recursive=True) if "socco" in f.lower()]

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remplacement des anciens chemins par les bons fichiers du dossier images/places/tanger-socco/
    # On s'assure que les balises img pointent vers le bon dossier
    content = content.replace('images/tanger/socco/', 'images/places/tanger-socco/')
    content = content.replace('images/socco/', 'images/places/tanger-socco/')
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fichier mis à jour : {filepath}")

