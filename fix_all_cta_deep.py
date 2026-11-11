import os
import glob
import re
import json

# Balayer absolument tous les fichiers HTML du projet récursivement
all_html = glob.glob("**/*.html", recursive=True)

count = 0
for path in all_html:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    updated = content
    
    # Remplacer toutes les variantes possibles de boutons avec Booking.com (en anglais et français)
    updated = re.sub(r'View All (?:Riads|Hotels|Stays|Places to Stay)[^<]*on Booking\.com', 'View All Stays', updated, flags=re.IGNORECASE)
    updated = re.sub(r'Voir tous les (?:riads|hôtels|hébergements)[^<]*sur Booking\.com', 'Voir tous les hébergements', updated, flags=re.IGNORECASE)
    
    # Nettoyer aussi si le texte est directement dans un attribut ou un span
    updated = re.sub(r'on Booking\.com', '', updated, flags=re.IGNORECASE)
    updated = re.sub(r'sur Booking\.com', '', updated, flags=re.IGNORECASE)
    
    if updated != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Mis à jour en profondeur : {path}")
        count += 1

print(f"Total des fichiers HTML nettoyés : {count}")
