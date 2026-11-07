import os
import re

mapping = {
    "corniche.html": ("corniche.webp", "Corniche & Ain Diab"),
    "quartier-habous.html": ("quartier-habous.webp", "Quartier Habous"),
    "old-medina.html": ("old-medina.webp", "Old Medina"),
    "place-mohammed-v.html": ("place-mohammed-v.webp", "Place Mohammed V"),
    "ricks-cafe.html": ("restau-ricks.webp", "Rick's Café"),
    "villa-des-arts.html": ("villa-des-arts.webp", "Villa des Arts"),
    "marche-central.html": ("marche-central.webp", "Marché Central"),
    "hassan-ii.html": ("hassan-ii.webp", "Hassan II Mosque")
}

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated = False
            for href_key, (img_filename, alt_text) in mapping.items():
                pattern = rf'(href="[^"]*{re.escape(href_key)}"[^>]*>.*?<img\s+src=")([^"]*)("[^>]*alt=")([^"]*)("[^>]*>)'
                
                # Recherche et remplacement direct
                new_content, count = re.subn(
                    pattern,
                    rf'\1../../images/casablanca/{img_filename}\3{alt_text}\5',
                    content,
                    flags=re.DOTALL
                )
                if count > 0:
                    content = new_content
                    updated = True

            if updated:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Mis à jour avec succès : {filepath}")

print("Correction des images terminée !")
