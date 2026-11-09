import glob

# On cible tous les fichiers JSON dans les dossiers de langue arabe (ar)
json_files = glob.glob("js/translations/ar/**/*.json", recursive=True) + glob.glob("js/translations/ar/*.json", recursive=True)

for filepath in json_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remplacement de مقهى حافة par مقهى الحافة
    if "مقهى حافة" in content:
        updated = content.replace("مقهى حافة", "مقهى الحافة")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Mis à jour : {filepath}")

