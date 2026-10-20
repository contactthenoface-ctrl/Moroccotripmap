import os, json
from pathlib import Path

print("🛠️ --- STRUCTURATION UNIVERSELLE DES CLÉS DE TRADUCTION --- 🛠️\n")

trans_dir = Path('js/translations')
json_files = list(trans_dir.rglob('*.json'))

count = 0

for jf in json_files:
    try:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict):
            continue
        
        modified = False
        
        # S'assurer que le bloc footer existe
        if 'footer' not in data or not isinstance(data['footer'], dict):
            data['footer'] = {}
            modified = True
        
        # Si des clés étaient enregistrées en format plat "footer.link_stays", on les convertit dans l'objet footer
        keys_to_delete = []
        for key, value in list(data.items()):
            if key.startswith('footer.'):
                sub_key = key.split('footer.')[1]
                data['footer'][sub_key] = value
                keys_to_delete.append(key)
                modified = True
                
        for k in keys_to_delete:
            del data[k]
            
        if modified:
            with open(jf, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            count += 1
    except Exception as e:
        pass

print(f"✅ {count} fichiers JSON restructurés avec succès !")
