import glob, re

ALL_PLACES = [
    {
        "filename": "koutoubia.html",
        "img": "../../images/marrakech/koutoubia.webp",
        "alt": "Koutoubia Mosque",
        "tag_i18n": "marrakech_page.places.koutoubia.tag",
        "title_i18n": "marrakech_page.places.koutoubia.title",
        "desc_i18n": "marrakech_page.places.koutoubia.desc",
        "default_tag": "Landmark",
        "default_title": "Koutoubia Mosque",
        "default_desc": "The minaret of this 12th-century mosque stands 77 meters tall."
    },
    {
        "filename": "medersa-ben-youssef.html",
        "img": "../../images/marrakech/medersa-ben-youssef.webp",
        "alt": "Ben Youssef Madrasa",
        "tag_i18n": "marrakech_page.places.ben_youssef.tag",
        "title_i18n": "marrakech_page.places.ben_youssef.title",
        "desc_i18n": "marrakech_page.places.ben_youssef.desc",
        "default_tag": "Islamic Heritage",
        "default_title": "Ben Youssef Madrasa",
        "default_desc": "An ancient Islamic college and a jewel of Arab-Andalusian art."
    },
    {
        "filename": "palais-bahia.html",
        "img": "../../images/marrakech/palais-bahia.webp",
        "alt": "Bahia Palace",
        "tag_i18n": "marrakech_page.places.bahia.tag",
        "title_i18n": "marrakech_page.places.bahia.title",
        "desc_i18n": "marrakech_page.places.bahia.desc",
        "default_tag": "Royal Architecture",
        "default_title": "Bahia Palace",
        "default_desc": "A masterpiece of Moroccan architecture featuring painted ceilings and zellige courtyards."
    },
    {
        "filename": "palais-el-badi.html",
        "img": "../../images/marrakech/el-badi-palace.webp",
        "alt": "El Badi Palace",
        "tag_i18n": "marrakech_page.places.elbadi.tag",
        "title_i18n": "marrakech_page.places.elbadi.title",
        "desc_i18n": "marrakech_page.places.elbadi.desc",
        "default_tag": "Ancient Ruins",
        "default_title": "El Badi Palace",
        "default_desc": "Grand ruins of a 16th-century palace home to nesting storks."
    },
    {
        "filename": "tombeaux-saadiens.html",
        "img": "../../images/marrakech/saadian-tombs.webp",
        "alt": "Saadian Tombs",
        "tag_i18n": "marrakech_page.places.saadian.tag",
        "title_i18n": "marrakech_page.places.saadian.title",
        "desc_i18n": "marrakech_page.places.saadian.desc",
        "default_tag": "History",
        "default_title": "Saadian Tombs",
        "default_desc": "Richly decorated mausoleums with Carrara marble in the Kasbah district."
    },
    {
        "filename": "jardin-majorelle.html",
        "img": "../../images/marrakech/jardin-majorelle.webp",
        "alt": "Jardin Majorelle",
        "tag_i18n": "marrakech_page.places.majorelle.tag",
        "title_i18n": "marrakech_page.places.majorelle.title",
        "desc_i18n": "marrakech_page.places.majorelle.desc",
        "default_tag": "Botanical Garden",
        "default_title": "Jardin Majorelle & YSL",
        "default_desc": "A peaceful botanical haven famous for its cobalt blue villa."
    },
    {
        "filename": "jardin-menara.html",
        "img": "../../images/marrakech/menara-garden.webp",
        "alt": "Menara Gardens",
        "tag_i18n": "marrakech_page.places.jardin_menara.tag",
        "title_i18n": "marrakech_page.places.jardin_menara.title",
        "desc_i18n": "marrakech_page.places.jardin_menara.desc",
        "default_tag": "Menara Gardens",
        "default_title": "Les Jardins de la Menara",
        "default_desc": "A historic 12th-century olive orchard with a large basin and a green-roofed pavilion."
    },
    {
        "filename": "jemaa-el-fnaa.html",
        "img": "../../images/marrakech/jemaa-el-fnaa.webp",
        "alt": "Jemaa el-Fnaa",
        "tag_i18n": "marrakech_page.places.jemaa.tag",
        "title_i18n": "marrakech_page.places.jemaa.title",
        "desc_i18n": "marrakech_page.places.jemaa.desc",
        "default_tag": "Historic Square",
        "default_title": "Jemaa el-Fnaa & Souks",
        "default_desc": "The beating heart of Marrakech, an open-air theater and labyrinth of artisan souks."
    },
    {
        "filename": "el-bacha-museum.html",
        "img": "../../images/marrakech/dar-el-bacha.webp",
        "alt": "Dar El Bacha",
        "tag_i18n": "marrakech_page.places.dar_el_bacha.tag",
        "title_i18n": "marrakech_page.places.dar_el_bacha.title",
        "desc_i18n": "marrakech_page.places.dar_el_bacha.desc",
        "default_tag": "Dar El Bacha",
        "default_title": "Dar El Bacha",
        "default_desc": "A stunning 1910 palace showcasing Moorish architecture and the famous Bacha Coffee."
    }
]

html_files = glob.glob("places/marrakech-places/*.html")

for file_path in html_files:
    current_filename = file_path.split("/")[-1]
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    filtered_places = [p for p in ALL_PLACES if p["filename"] != current_filename]
    
    # Utilisation de styles CSS in-line stricts pour garantir l'alignement et le format portrait indépendamment de tout
    cards_html = ""
    for p in filtered_places:
        cards_html += f'''                <a class="group bg-white rounded-2xl p-4 shadow-sm hover:shadow-xl transition duration-300 border border-sable/10" style="display: flex; align-items: center; gap: 1rem;" href="{p['filename']}">
                    <img src="{p['img']}" alt="{p['alt']}" style="width: 80px; height: 112px; object-fit: cover; border-radius: 0.75rem; flex-shrink: 0;" loading="lazy"/>
                    <div style="display: flex; flex-direction: column; flex-grow: 1; min-width: 0;">
                        <span class="bg-vert text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider mb-1.5" style="width: fit-content;" data-i18n="{p['tag_i18n']}">{p['default_tag']}</span>
                        <h3 class="text-base font-bold text-sombre group-hover:text-vert transition" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" data-i18n="{p['title_i18n']}">{p['default_title']}</h3>
                        <p class="text-xs text-sombre/70 mt-1" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;" data-i18n="{p['desc_i18n']}">{p['default_desc']}</p>
                        <span class="mt-2 text-xs font-semibold text-sable group-hover:text-vert transition flex items-center gap-1" data-i18n="marrakech_page.places.explore">Explore Place →</span>
                    </div>
                </a>\n'''

    # Ciblage sécurisé de la grille sans toucher au reste de la page
    pattern = re.compile(
        r'(<!--\s*Other must-visit places\s*-->\s*<section[^>]*>.*?<div class="grid grid-cols-1[^"]*">)(.*?)(?=\s*</div>\s*</section>)',
        re.DOTALL
    )
    
    match = pattern.search(content)
    if match:
        new_content = content[:match.start(2)] + "\n" + cards_html + "            " + content[match.end(2):]
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[Strict & Sécurisé] {file_path}")

print("Mise à jour stricte terminée avec succès !")
