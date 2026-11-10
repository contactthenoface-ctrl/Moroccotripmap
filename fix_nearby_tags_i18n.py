import glob

# On cible toutes les pages de lieux de Tanger
files = glob.glob("places/tanger-places/*.html")

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    updated = content
    
    # On associe chaque type de lieu à sa clé i18n existante dans tanger_nearby.json
    # Par exemple, pour la médina, la clé dans tanger_nearby est tanger_nearby.medina.name
    # On peut créer un attribut data-i18n propre sur le badge de catégorie.
    
    # Remplacements ciblés sur les cartes de lieux suggérés
    replacements = [
        ('">Medina</span>', '" data-i18n="tanger_nearby.medina.name">Medina</span>'),
        ('">Square</span>', '" data-i18n="tanger_nearby.socco.name">Grand Socco</span>'),
        ('">Museum</span>', '" data-i18n="tanger_nearby.kasbah.name">Kasbah Museum</span>'),
        ('">Café</span>', '" data-i18n="tanger_nearby.hafa.name">Café Hafa</span>'),
        ('">Beach</span>', '" data-i18n="tanger_nearby.beach.name">Tangier Beach</span>'),
        ('">Cape</span>', '" data-i18n="tanger_nearby.spartel.name">Cap Spartel</span>'),
        ('">Caves</span>', '" data-i18n="tanger_nearby.caves.name">Hercules Caves</span>'),
    ]
    
    for old_str, new_str in replacements:
        # On évite de dupliquer si data-i18n est déjà présent
        if 'data-i18n="tanger_nearby' not in updated:
            updated = updated.replace(old_str, new_str)

    if updated != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Tags i18n mis à jour pour : {filepath}")

