import os, glob
from urllib.parse import urlparse

html_files = glob.glob("**/*.html", recursive=True)
broken_count = 0

for filepath in html_files:
    if "node_modules" in filepath:
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Recherche basique des attributs href="..."
    import re
    hrefs = re.findall(r'href=["\'](.*?)["\']', content)
    
    dir_name = os.path.dirname(filepath)
    
    for href in hrefs:
        # Ignorer les liens externes, ancres et scripts
        if href.startswith("http") or href.startswith("mailto:") or href.startswith("#") or href.startswith("javascript:"):
            continue
        
        # Gérer les chemins relatifs
        clean_href = href.split("#")[0].split("?")[0]
        if not clean_href:
            continue
            
        target_path = os.path.normpath(os.path.join(dir_name, clean_href))
        
        # Vérification si le fichier cible existe physiquement
        if not os.path.exists(target_path) and not os.path.exists(target_path + ".html"):
            print(f"[LIEN CASSÉ] Dans '{filepath}' -> pointe vers '{href}' (Introuvable)")
            broken_count += 1

print(f"\nScan terminé. {broken_count} liens cassés détectés.")
