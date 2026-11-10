import glob

files = glob.glob("places/*-places/*.html") + ["tanger.html"]

for filepath in files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated = content
        # On s'assure que les tags ont bien le format data-i18n propre et que le texte intérieur correspond
        # Par exemple transformer <span class="..." data-i18n="tanger.tags.museum">Museum</span>
        # en s'assurant que le mécanisme de i18n lit bien la clé.
        
        # Vérifions si les tags ont déjà data-i18n, sinon on les ajoute
        tags_map = {
            'Medina': 'tanger.tags.medina',
            'Square': 'tanger.tags.square',
            'Café': 'tanger.tags.cafe',
            'Beach': 'tanger.tags.beach',
            'Museum': 'tanger.tags.museum',
            'Cape': 'tanger.tags.cape',
            'Caves': 'tanger.tags.caves'
        }
        
        for text, key in tags_map.items():
            # Cherche les spans de type class="... text-sable">Text</span> sans data-i18n ou avec un vieux format
            old_pattern = f'>{text}</span>'
            # On remplace par le format géré par i18n s'il ne l'est pas déjà
            if f'data-i18n="{key}"' not in updated and old_pattern in updated:
                # On remplace la portion
                target = f'text-sable">{text}</span>'
                replacement = f'text-sable" data-i18n="{key}">{text}</span>'
                updated = updated.replace(target, replacement)

        if updated != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"Fichier mis à jour : {filepath}")
    except Exception as e:
        print(e)

