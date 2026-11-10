import json
import os

category_translations = {
    "en": {
        "medina": "Medina",
        "square": "Square",
        "museum": "Museum",
        "cafe": "Café",
        "beach": "Beach",
        "cape": "Cape",
        "caves": "Caves"
    },
    "fr": {
        "medina": "Medina",
        "square": "Place",
        "museum": "Musée",
        "cafe": "Café",
        "beach": "Plage",
        "cape": "Cap",
        "caves": "Grottes"
    },
    "ar": {
        "medina": "مدينة عتيقة",
        "square": "ساحة",
        "museum": "متحف",
        "cafe": "مقهى",
        "beach": "شاطئ",
        "cape": "رأس",
        "caves": "مغارة"
    },
    "es": {
        "medina": "Medina",
        "square": "Plaza",
        "museum": "Museo",
        "cafe": "Café",
        "beach": "Playa",
        "cape": "Cabo",
        "caves": "Cuevas"
    }
}

for lang, cats in category_translations.items():
    json_path = f"js/translations/{lang}.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "tanger_categories" not in data:
                data["tanger_categories"] = {}
            
            data["tanger_categories"].update(cats)
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"JSON mis à jour : {json_path}")
        except Exception as e:
            print(e)

