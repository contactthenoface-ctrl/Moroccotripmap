import os, glob, json, re

# 1. Collecter toutes les clés data-i18n uniques des fichiers HTML
html_files = glob.glob("**/*.html", recursive=True)
required_keys = set()

for filepath in html_files:
    if "node_modules" in filepath:
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        keys = re.findall(r'data-i18n=["\x27](.*?)["\x27]', content)
        for k in keys:
            required_keys.add(k)

print(f"-> {len(required_keys)} clés i18n uniques trouvées dans les fichiers HTML.")

# 2. Localiser les fichiers de traduction principaux (en.json, fr.json, es.json, ar.json)
translation_files = [f for f in glob.glob("**/*.json", recursive=True) if os.path.basename(f) in ["en.json", "fr.json", "es.json", "ar.json"]]

if not translation_files:
    # Recherche élargie si les fichiers sont à la racine ou dans un dossier spécifique
    translation_files = [f for f in glob.glob("*.json")]

def set_nested_dict(d, keys, value):
    for key in keys[:-1]:
        if key not in d or not isinstance(d[key], dict):
            d[key] = {}
        d = d[key]
    if keys[-1] not in d or not d[keys[-1]]:
        d[keys[-1]] = value

def get_nested_dict(d, keys):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d

# 3. Remplir les clés manquantes dans chaque fichier JSON de langue
for jfile in translation_files:
    if "package" in jfile or "config" in jfile or "node_modules" in jfile:
        continue
        
    try:
        with open(jfile, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Erreur de lecture {jfile}: {e}")
        continue
        
    if not isinstance(data, dict):
        data = {}
        
    added_count = 0
    lang_code = os.path.basename(jfile).lower()
    
    for full_key in sorted(required_keys):
        parts = full_key.split(".")
        existing = get_nested_dict(data, parts)
        
        if existing is None:
            # Définir un texte par défaut propre selon la langue
            last_part = parts[-1].replace("_", " ").capitalize()
            if "ar" in lang_code:
                default_val = f"قيد الإعداد ({last_part})"
            elif "fr" in lang_code:
                default_val = f"En cours ({last_part})"
            elif "es" in lang_code:
                default_val = f"En preparación ({last_part})"
            else:
                default_val = f"{last_part}"
                
            set_nested_dict(data, parts, default_val)
            added_count += 1
            
    with open(jfile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"-> {jfile} : {added_count} clés manquantes ajoutées et synchronisées.")

print("\nMise à jour de toutes les traductions terminée avec succès !")
