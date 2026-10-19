import os, re, json
from pathlib import Path

print("🛠️ --- CORRECTION AUTOMATIQUE DES CLÉS MANQUANTES --- 🛠️\n")

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
trans_dir = Path('js/translations')
languages = ['en', 'fr', 'es', 'ar']

fixed_count = 0

def set_nested_key(d, keys_list, value):
    for key in keys_list[:-1]:
        if key not in d or not isinstance(d[key], dict):
            d[key] = {}
        d = d[key]
    if keys_list[-1] not in d:
        d[keys_list[-1]] = value
        return True
    return False

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        keys = re.findall(r'data-i18n=["\']([^"\']+)["\']', content)

    if not keys:
        continue

    base_name = html_file.stem.replace('-', '_') + '_page.json'

    for lang in languages:
        json_path = trans_dir / lang / base_name
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {}
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
            except Exception:
                data = {}

        modified = False
        for k in keys:
            keys_list = k.split('.')
            default_val = f"[{lang.upper()}] {k.split('.')[-1].replace('_', ' ').capitalize()}"
            
            if set_nested_key(data, keys_list, default_val):
                modified = True
                fixed_count += 1

        if modified:
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(data, jf, ensure_ascii=False, indent=2)

print(f"\n✨ Correction terminée ! {fixed_count} clés manquantes ont été injectées dans les fichiers JSON.")
