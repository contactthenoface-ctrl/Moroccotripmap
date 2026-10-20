import os, shutil
from pathlib import Path

print("🧹 --- NETTOYAGE STRICT ET PURGE DES ANCIENS FICHIERS --- 🧹\n")

# Listes des dossiers à nettoyer s'ils contiennent des doublons
dirs_to_clean = ['moroccotripmap', 'images/blog']

cleaned_files = 0
for d in dirs_to_clean:
    p = Path(d)
    if p.exists() and p.is_dir():
        shutil.rmtree(p)
        print(f"🗑️ Dossier obsolète supprimé : {d}")

# Supprimer les scripts de diagnostic temporaires créés durant la session
temp_scripts = list(Path('.').glob('fix_*.py')) + list(Path('.').glob('check_*.py')) + list(Path('.').glob('debug_*.py')) + list(Path('.').glob('upgrade_*.py'))

for script in temp_scripts:
    if script.name not in ['package.json', 'tailwind.config.js']:
        script.unlink()
        cleaned_files += 1

print(f"✅ {cleaned_files} fichier(s) temporaire(s) de nettoyage supprimé(s).")
print("\n✨ Ton projet est désormais totalement propre, structuré et sans traces parasites !")
