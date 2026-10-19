import os, re, json
from pathlib import Path

print("🩺 --- DÉBUT DU DIAGNOSTIC DU SITE --- 🩺\n")

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
trans_dir = Path('js/translations')
languages = ['en', 'fr', 'es', 'ar']

issues_found = 0

# 1. Vérification des Méta-balises et des Images cassées
print("1️⃣ Vérification des balises SEO & Images...")
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Méta-balises
    if '<title>' not in content or '</title>' not in content:
        print(f"  ⚠️ Titre manquante ou mal formée : {html_file}")
        issues_found += 1
    if 'name="description"' not in content:
        print(f"  ⚠️ Méta description manquante : {html_file}")
        issues_found += 1

    # Images cassées
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    for src in img_srcs:
        if src.startswith('http') or src.startswith('//') or src.startswith('data:'):
            continue
        # Résolution du chemin relatif
        clean_src = src.split('?')[0].split('#')[0]
        if clean_src.startswith('/'):
            img_path = Path('.') / clean_src.lstrip('/')
        else:
            img_path = (html_file.parent / clean_src).resolve()

        if not img_path.exists():
            print(f"  🖼️ Image introuvable ({src}) dans : {html_file}")
            issues_found += 1

# 2. Vérification de la cohérence des clés i18n
print("\n2️⃣ Vérification des clés de traduction data-i18n...")
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        keys = re.findall(r'data-i18n=["\']([^"\']+)["\']', content)

    if not keys:
        continue

    base_name = html_file.stem.replace('-', '_') + '_page.json'

    for lang in languages:
        json_path = trans_dir / lang / base_name
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)

                # Fonction pour récupérer toutes les clés imbriquées (ex: header.title)
                def get_all_keys(d, prefix=''):
                    k_set = set()
                    if isinstance(d, dict):
                        for k, v in d.items():
                            full_k = f"{prefix}.{k}" if prefix else k
                            k_set.add(full_k)
                            k_set.update(get_all_keys(v, full_k))
                    return k_set

                available_keys = get_all_keys(data)

                for k in keys:
                    if k not in available_keys:
                        print(f"  🔑 Clé manquante '{k}' dans [{lang}/{base_name}] pour {html_file}")
                        issues_found += 1
            except Exception:
                pass

print("\n--- BILAN DU DIAGNOSTIC ---")
if issues_found == 0:
    print("✨ Aucun bug critique, aucune image cassée, et toutes les métadonnées/traductions sont nickels !")
else:
    print(f"🚨 Total de petites anomalies ou points à corriger : {issues_found}")

