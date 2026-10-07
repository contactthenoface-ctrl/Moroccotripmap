#!/usr/bin/env python3
"""
Découpe ar/en/es/fr.json en petits fichiers par section, sans toucher au HTML.

Usage :
    python3 split_translations.py SOURCE_DIR OUT_DIR

SOURCE_DIR contient ar.json, en.json, es.json, fr.json (les fichiers que tu édites ; ils servent aussi de secours
si les dossiers découpés sont absents).
OUT_DIR reçoit (en général js/translations/ lui-même) :
    {lang}/_core.json      -> sections communes à toutes les pages
    {lang}/{section}.json  -> une section par fichier (ex. tanger_page.json)
"""
import json, sys, shutil
from pathlib import Path

LANGS = ["ar", "en", "es", "fr"]
# Sections présentes sur (presque) toutes les pages : regroupées en 1 seule requête
CORE = ["nav", "footer", "breadcrumb", "mobile_menu", "destinations", "common"]

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

def main(src, out):
    src, out = Path(src), Path(out)
    for lang in LANGS:
        f = src / f"{lang}.json"
        if not f.exists():
            f = src / f"{lang}.txt"
        data = json.loads(f.read_text(encoding="utf-8"))
        if lang in data and isinstance(data[lang], dict) and "nav" not in data:
            data = data[lang]
        d = out / lang
        if d.exists():
            shutil.rmtree(d)
        dump(d / "_core.json", {k: data[k] for k in CORE if k in data})
        for k, v in data.items():
            if k not in CORE:
                dump(d / f"{k}.json", v)
        print(lang, len(data), "sections")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
