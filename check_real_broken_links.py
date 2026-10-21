import os, glob, re

html_files = glob.glob("**/*.html", recursive=True)
real_broken = 0

for filepath in html_files:
    if "node_modules" in filepath:
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    hrefs = re.findall(r'href=["\x27](.*?)["\x27]', content)
    dir_name = os.path.dirname(filepath)
    
    for href in hrefs:
        # Ignorer les liens externes, ancres, javascript et surtout les data: URIs
        if not href or href.startswith(("http", "mailto:", "#", "javascript:", "data:")):
            continue
            
        clean_href = href.split("#")[0].split("?")[0]
        if not clean_href:
            continue
            
        target_path = os.path.normpath(os.path.join(dir_name, clean_href))
        
        # Vérification si le fichier ou le dossier index.html existe
        exists = os.path.exists(target_path) or os.path.exists(target_path + ".html") or os.path.exists(os.path.join(target_path, "index.html"))
        
        if not exists:
            # Filtrer pour ne garder que les pages .html internes suspectes
            if clean_href.endswith(".html") or "/" in clean_href:
                print(f"[VRAI LIEN CASSÉ] {filepath} -> {href}")
                real_broken += 1

print(f"\nScan terminé. Vrais liens cassés détectés : {real_broken}")
