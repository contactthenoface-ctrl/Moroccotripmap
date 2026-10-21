import os, glob, re

# Détection automatique de la racine HTML
html_files = glob.glob("**/*.html", recursive=True)
real_broken = []

for filepath in html_files:
    if "node_modules" in filepath:
        continue
    
    dir_name = os.path.dirname(filepath)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extraire tous les hrefs
    hrefs = re.findall(r'href=["\x27](.*?)["\x27]', content)
    
    for href in hrefs:
        # Ignorer ancres, scripts, URLs externes et données SVG
        if not href or href.startswith(("http", "mailto:", "#", "javascript:", "data:")):
            continue
            
        clean_href = href.split("#")[0].split("?")[0]
        if not clean_href:
            continue
            
        # Résolution du chemin relatif exact
        target_path = os.path.normpath(os.path.join(dir_name, clean_href))
        
        # Test de l'existence réelle sur le disque
        exists = (
            os.path.exists(target_path) or 
            os.path.exists(target_path + ".html") or 
            os.path.exists(os.path.join(target_path, "index.html"))
        )
        
        if not exists:
            # On ne garde que les liens .html ou .css qui posent vraiment problème
            real_broken.append((filepath, href, target_path))

print(f"--- RAPPORT DE VÉRIFICATION EXACTE ---")
print(f"Total de vrais liens internes cassés : {len(real_broken)}")

if real_broken:
    print("\nÉchantillon des 10 premiers vrais liens introuvables :")
    for src, href, target in real_broken[:10]:
        print(f"Dans '{src}'\n  └── Lien : '{href}'\n  └── Cible introuvable : '{target}'\n")
