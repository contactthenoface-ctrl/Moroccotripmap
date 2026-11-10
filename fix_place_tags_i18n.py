import glob

# On cible la page principale de Tanger (tanger.html) et toutes les pages de lieux
files_to_fix = ["tanger.html"] + glob.glob("places/tanger-places/*.html")

for filepath in files_to_fix:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated = content
        
        # Remplacement des tags fixes par des tags avec data-i18n dynamiques
        # On couvre les catégories courantes : Medina, Square, Café, Beach, Museum, Cape
        replacements = [
            ('>Medina</span>', ' data-i18n="tanger.tags.medina">Medina</span>'),
            ('>Square</span>', ' data-i18n="tanger.tags.square">Square</span>'),
            ('>Café</span>', ' data-i18n="tanger.tags.cafe">Café</span>'),
            ('>Beach</span>', ' data-i18n="tanger.tags.beach">Beach</span>'),
            ('>Museum</span>', ' data-i18n="tanger.tags.museum">Museum</span>'),
            ('>Cape</span>', ' data-i18n="tanger.tags.cape">Cape</span>'),
            ('>Caves</span>', ' data-i18n="tanger.tags.caves">Caves</span>'),
        ]
        
        for old_str, new_str in replacements:
            # On cherche les lignes de tags (ex: <span class="...">Medina</span>)
            # Pour éviter de modifier autre chose, on cible précisément la structure uppercase des badges de cartes
            target = f'uppercase text-sable">{old_str[1:]}'
            replacement_val = f'uppercase text-sable" {new_str}'
            updated = updated.replace(target, replacement_val)
            
            # Variante alternative de structure HTML
            target2 = f'text-[10px] font-bold uppercase tracking-wider text-sable">{old_str[1:]}'
            replacement_val2 = f'text-[10px] font-bold uppercase tracking-wider text-sable" {new_str}'
            updated = updated.replace(target2, replacement_val2)

        if updated != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"Tags i18n ajoutés dans : {filepath}")
    except FileNotFoundError:
        pass

