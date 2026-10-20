#!/usr/bin/env python3
"""
Remplace le CDN Tailwind par css/styles.css + css/style.css
sur tous les fichiers HTML du projet MoroccoTripMap.

À lancer depuis la racine du repo :
  python3 tools/switch_to_local_tailwind.py
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
if not (ROOT / "css" / "styles.css").exists():
    # fallback si script lancé depuis la racine
    if (Path.cwd() / "css" / "styles.css").exists():
        ROOT = Path.cwd()
    else:
        print("ERREUR: css/styles.css introuvable. Lance d'abord: npm run css:build")
        sys.exit(1)

CDN_SCRIPT = re.compile(
    r'\s*<script\s+src=["\']https://cdn\.tailwindcss\.com["\'][^>]*>\s*</script>\s*',
    re.I,
)
CONFIG_SCRIPT = re.compile(
    r'\s*<script>\s*tailwind\.config\s*=\s*\{.*?\}\s*;?\s*</script>\s*',
    re.I | re.S,
)
ALREADY = re.compile(r'href=["\'][^"\']*css/styles\.css["\']', re.I)


def depth_prefix(html_path: Path) -> str:
    rel = html_path.parent.relative_to(ROOT)
    parts = [p for p in rel.parts if p != "."]
    if not parts:
        return ""
    return "../" * len(parts)


def link_block(prefix: str) -> str:
    return (
        "<!-- Tailwind build local -->\n"
        f'<link rel="stylesheet" href="{prefix}css/styles.css" />\n'
        f'<link rel="stylesheet" href="{prefix}css/style.css" />\n'
    )


def process(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    if ALREADY.search(text) and not CDN_SCRIPT.search(text) and not CONFIG_SCRIPT.search(text):
        return "skip"

    text2 = CDN_SCRIPT.sub("\n", text)
    text2 = CONFIG_SCRIPT.sub("\n", text2)
    changed = text2 != text
    text = text2

    if not ALREADY.search(text):
        prefix = depth_prefix(path)
        block = link_block(prefix)
        m = re.search(r"</head>", text, re.I)
        if m:
            text = text[: m.start()] + "\n" + block + "\n" + text[m.start() :]
            changed = True
        else:
            m2 = re.search(r"<meta[^>]+charset[^>]*>", text, re.I)
            if m2:
                text = text[: m2.end()] + "\n" + block + text[m2.end() :]
                changed = True
            else:
                return "no-head"

    if not changed and text == original:
        return "skip"

    path.write_text(text, encoding="utf-8")
    return "ok"


def main():
    html_files = sorted(ROOT.rglob("*.html"))
    html_files = [
        p
        for p in html_files
        if "node_modules" not in p.parts and ".git" not in p.parts
    ]

    stats = {"ok": 0, "skip": 0, "no-head": 0}
    for p in html_files:
        rel = p.relative_to(ROOT)
        status = process(p)
        stats[status] = stats.get(status, 0) + 1
        mark = {"ok": "OK", "skip": "--", "no-head": "!!"}.get(status, status)
        print(f"  [{mark}] {rel}")

    print()
    print(f"Modifies : {stats.get('ok', 0)}")
    print(f"Deja OK  : {stats.get('skip', 0)}")
    print(f"Sans head: {stats.get('no-head', 0)}")
    print("Termine. Verifie une page dans le navigateur.")


if __name__ == "__main__":
    main()
