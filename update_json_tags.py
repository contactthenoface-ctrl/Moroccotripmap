import json
import os

translations = {
    "en": {
        "tanger.tags.medina": "Medina",
        "tanger.tags.square": "Square",
        "tanger.tags.cafe": "Café",
        "tanger.tags.beach": "Beach",
        "tanger.tags.museum": "Museum",
        "tanger.tags.cape": "Cape",
        "tanger.tags.caves": "Caves"
    },
    "fr": {
        "tanger.tags.medina": "Medina",
        "tanger.tags.square": "Place",
        "tanger.tags.cafe": "Café",
        "tanger.tags.beach": "Plage",
        "tanger.tags.museum": "Musée",
        "tanger.tags.cape": "Cap",
        "tanger.tags.caves": "Grottes"
    },
    "ar": {
        "tanger.tags.medina": "مدينة عتيقة",
        "tanger.tags.square": "ساحة",
        "tanger.tags.cafe": "مقهى",
        "tanger.tags.beach": "شاطئ",
        "tanger.tags.museum": "متحف",
        "tanger.tags.cape": "رأس",
        "tanger.tags.caves": "مغارة"
    },
    "es": {
        "tanger.tags.medina": "Medina",
        "tanger.tags.square": "Plaza",
        "tanger.tags.cafe": "Café",
        "tanger.tags.beach": "Playa",
        "tanger.tags.museum": "Museo",
        "tanger.tags.cape": "Cabo",
        "tanger.tags.caves": "Cuevas"
    }
}

for lang, keys in translations.items():
    json_path = f"js/translations/{lang}.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # S'assurer que la structure supporte tanger -> tags ou les clés directes
            # Si ton i18n utilise des clés plates ou imbriquées :
            if "tanger" not in data:
                data["tanger"] = {}
            if "tags" not in data["tanger"]:
                data["tanger"]["tags"] = {}
                
            data["tanger"]["tags"].update({k.split(".")[-1]: v for k, v in keys.items()})
            # Ajout aussi en clé plate au cas où le script i18n cherche la clé exacte
            data.update(keys)
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Traduction mise à jour pour : {lang}")
        except Exception as e:
            print(f"Erreur sur {json_path}: {e}")

