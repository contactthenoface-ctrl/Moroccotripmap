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

print(f"{len(required_keys)} clés i18n uniques trouvées dans les fichiers HTML.")

# 2. Cibler uniquement les fichiers de traduction principaux (ex: en.json, fr.json, etc.)
translation_files = [f for f in glob.glob("**/*.json", recursive=True) if any(lang in os.path.basename(f) for lang in ["en.json", "fr.json", "es.json", "ar.json", "core.json", "footer.json"])]

def set_nested_dict(d, keys, value):
    for key in keys[:-1]:
        if not isinstance(d, dict):
            return
        d = d.setdefault(key, {})
    if isinstance(d, dict):
        if keys[-1] not in d or not d[keys[-1]]:
            d[keys[-1]] = value

def get_nested_dict(d, keys):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d

# 3. Mise à jour sécurisée des fichiers JSON
for jfile in translation_files:
    if "node_modules" in jfile:
        continue
        
    try:
        with open(jfile, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue
        
    if not isinstance(data, dict):
        continue
        
    added_count = 0
    lang_code = os.path.basename(jfile).lower()
    
    for full_key in sorted(required_keys):
        parts = full_key.split(".")
        existing = get_nested_dict(data, parts)
        
        if existing is None:
            if "ar" in lang_code:
                default_val = "قيد الإعداد"
            elif "fr" in lang_code:
                default_val = "En cours de préparation"
            elif "es" in lang_code:
                default_val = "En preparación"
            else:
                default_val = "In preparation"
                
            set_nested_dict(data, parts, default_val)
            added_count += 1
            
    with open(jfile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"-> {jfile} : {added_count} clés ajoutées.")

print("\nSynchronisation des traductions terminée avec succès !")
