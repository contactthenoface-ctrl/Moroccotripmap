import glob, re

# Le dictionnaire exact associant chaque page HTML de destination à sa propre image
mapping = {
    "souk.html": "../../images/places/agadir-souk/agadir-souk-02.webp",
    "crocoparc.html": "../../images/places/agadir-crocoparc/crocoparc-02.webp",
    "marina.html": "../../images/places/agadir-marina/agadir-marina-05.webp",
    "taghazout.html": "../../images/places/agadir-taghazout/taghazout-01.webp",
    "paradise.html": "../../images/places/agadir-paradise-valley/paradise-valley-03.webp",
    "beach.html": "../../images/places/agadir-beach/agadir-beach.webp",
    "birds.html": "../../images/places/agadir-souss-massa-birds/souss-massa-birds-04.webp",
    "kasbah.html": "../../images/places/agadir-kasbah/agadir-kasbah-01.webp",
    "corniche.html": "../../images/places/agadir-corniche/agadir-corniche-04.webp"
}

for filepath in glob.glob("places/agadir-places/*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content
    # Pour chaque carte "Keep Exploring", on cible son href spécifique et on lui met son image dédiée
    for target_page, img_path in mapping.items():
        # Expression régulière qui cible le bloc image situé juste après le lien vers target_page
        pattern = r'(href=["\']' + target_page + r'["\'][^>]*?>\s*<div[^>]*?>\s*<img\s+src=["\'])[^"\']*["\']'
        new_content = re.sub(pattern, r'\1' + img_path + r'"', new_content, flags=re.DOTALL)

    if content != new_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Corrigé avec succès : {filepath}")

print("Mise en place des images spécifiques terminée !")
