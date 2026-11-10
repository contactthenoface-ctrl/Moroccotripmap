import glob

# On cible toutes les pages de lieux de Tanger
files = glob.glob("places/tanger-places/*.html")

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    updated = content
    
    # On remplace les textes bruts des badges par des attributs data-i18n spécifiques aux catégories
    categories = [
        ('Medina', 'tanger_categories.medina'),
        ('Square', 'tanger_categories.square'),
        ('Museum', 'tanger_categories.museum'),
        ('Café', 'tanger_categories.cafe'),
        ('Beach', 'tanger_categories.beach'),
        ('Cape', 'tanger_categories.cape'),
        ('Caves', 'tanger_categories.caves'),
    ]
    
    for cat, key in categories:
        # Cible le bloc du badge de catégorie
        old_pattern = f'text-[10px] font-bold uppercase tracking-wider text-sable">{cat}</span>'
        new_pattern = f'text-[10px] font-bold uppercase tracking-wider text-sable" data-i18n="{key}">{cat}</span>'
        if old_pattern in updated and 'data-i18n' not in updated.split(old_pattern)[0][-30:]:
            updated = updated.replace(old_pattern, new_pattern)

    if updated != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Badges i18n appliqués sur : {filepath}")

