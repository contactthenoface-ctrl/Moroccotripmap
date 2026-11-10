import glob

# On cible le fichier HTML des grottes (caves.html)
html_files = [f for f in glob.glob("**/*.html", recursive=True) if "caves" in f.lower()]

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # On corrige les chemins pour qu'ils pointent bien vers le dossier racine correct
    # Si le fichier est dans places/tanger-places/, les images doivent être root-relative (/images/... ou ../../images/...)
    updated = content
    
    # Remplacement des chemins erronés par le chemin absolu/root correct
    updated = updated.replace('images/tanger-caves/', '../../images/places/tanger-caves/')
    updated = updated.replace('images/caves/', '../../images/places/tanger-caves/')
    updated = updated.replace('images/places/tanger-caves/', '../../images/places/tanger-caves/')
    
    # Si la page est à la racine, on gère aussi le cas simple
    if filepath.count("/") == 0:
        updated = updated.replace('../../images/places/tanger-caves/', 'images/places/tanger-caves/')

    if updated != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Chemins corrigés dans : {filepath}")

