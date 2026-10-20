import os, re, json
from pathlib import Path

print("🛠️ --- RESTAURATION COMPLÈTE DU FOOTER (YOUTUBE & KAMLISEO) --- 🛠️\n")

# 1. Traductions complètes pour les 4 langues
footer_translations = {
    "en": {
        "col_imperial": "Imperial Cities & Culture",
        "col_desert": "Desert & Deep South",
        "connect_title": "Connect With Us",
        "youtube_text": "Subscribe to our YouTube channel for travel video guides:",
        "created_by": "Created by",
        "copyright": "© 2026 MoroccoTripMap. All rights reserved."
    },
    "fr": {
        "col_imperial": "Villes Impériales & Culture",
        "col_desert": "Désert & Grand Sud",
        "connect_title": "Suivez-nous",
        "youtube_text": "Abonnez-vous à notre chaîne YouTube pour nos guides vidéo :",
        "created_by": "Créé par",
        "copyright": "© 2026 MoroccoTripMap. Tous droits réservés."
    },
    "es": {
        "col_imperial": "Ciudades Imperiales y Cultura",
        "col_desert": "Desierto y Gran Sur",
        "connect_title": "Conéctate con Nosotros",
        "youtube_text": "Suscríbete a nuestro canal de YouTube para ver guías en vídeo:",
        "created_by": "Creado por",
        "copyright": "© 2026 MoroccoTripMap. Todos los derechos reservados."
    },
    "ar": {
        "col_imperial": "المدن الإمبراطورية والثقافة",
        "col_desert": "الصحراء والجنوب الكبير",
        "connect_title": "تواصل معنا",
        "youtube_text": "تابع قناتنا على يوتيوب لمشاهدة أدلة السفر بالفيديو:",
        "created_by": "تم الإنشاء بواسطة",
        "copyright": "© 2026 MoroccoTripMap. جميع الحقوق محفوظة."
    }
}

trans_dir = Path('js/translations')
for lang, trans in footer_translations.items():
    lang_path = trans_dir / lang
    if not lang_path.exists():
        continue
    for json_file in lang_path.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                data = {}
            if 'footer' not in data:
                data['footer'] = {}
            for k, v in trans.items():
                data['footer'][k] = v
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

print("✅ Traductions JSON du footer mises à jour.")

# 2. Mettre à jour tous les fichiers HTML avec le template complet
html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
updated_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    parts = html_file.relative_to('.').parts
    depth = len(parts) - 1
    prefix = '../' * depth if depth > 0 else ''

    new_footer = f"""<footer class="bg-vert text-creme pt-12 pb-8 px-4 sm:px-6 lg:px-8 mt-16 rounded-t-3xl">
  <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
    <div>
      <h3 class="text-xl font-bold mb-3 text-white">Morocco<span class="text-sable">TripMap</span></h3>
      <p class="text-xs text-creme/80 leading-relaxed" data-i18n="footer.about_text">
        Discover. Plan. Experience Morocco.<br/>
        The premier tourism directory and cultural travel guide for visitors exploring Morocco.
      </p>
    </div>
    <div>
      <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.col_imperial">Imperial Cities &amp; Culture</h4>
      <ul class="text-xs space-y-2 text-creme/80">
        <li><a class="hover:text-white transition" href="{prefix}marrakech.html" data-i18n="footer.link_marrakech">Marrakech Travel Guide</a></li>
        <li><a class="hover:text-white transition" href="{prefix}fes.html" data-i18n="footer.link_fes">Fes Medina Guide</a></li>
        <li><a class="hover:text-white transition" href="{prefix}rabat.html" data-i18n="footer.link_rabat">Rabat Travel Guide</a></li>
        <li><a class="hover:text-white transition" href="{prefix}meknes.html" data-i18n="footer.link_meknes">Meknes Travel Guide</a></li>
        <li><a class="hover:text-white transition" href="{prefix}guides/histoire.html" data-i18n="footer.link_history">History of Morocco</a></li>
      </ul>
    </div>
    <div>
      <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.col_desert">Desert &amp; Deep South</h4>
      <ul class="text-xs space-y-2 text-creme/80">
        <li><a class="hover:text-white transition" href="{prefix}merzouga.html" data-i18n="footer.link_merzouga">Merzouga Desert &amp; Dunes</a></li>
        <li><a class="hover:text-white transition" href="{prefix}zagora.html" data-i18n="footer.link_zagora">Zagora &amp; Drâa Valley</a></li>
        <li><a class="hover:text-white transition" href="{prefix}ouarzazate.html" data-i18n="footer.link_ouarzazate">Ouarzazate Cinema Guide</a></li>
        <li><a class="hover:text-white transition" href="{prefix}experiences/index.html" data-i18n="footer.link_experiences">Desert Tours &amp; Activities</a></li>
        <li><a class="hover:text-white transition" href="{prefix}destinations.html" data-i18n="footer.link_all_destinations">All Destinations</a></li>
      </ul>
    </div>
    <div>
      <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.connect_title">Connect With Us</h4>
      <p class="text-xs text-creme/80 mb-3" data-i18n="footer.youtube_text">Subscribe to our YouTube channel for travel video guides:</p>
      <a class="inline-flex items-center gap-2 bg-red-600 text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-red-700 transition mb-4" href="https://youtube.com/@moroccotripmap" rel="noopener noreferrer" target="_blank">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
        @moroccotripmap
      </a>
      <ul class="text-xs space-y-2 text-creme/80">
        <li><a class="hover:text-white transition" href="{prefix}riads/index.html" data-i18n="footer.link_stays">Authentic Riads &amp; Hotels</a></li>
        <li><a class="hover:text-white transition" href="{prefix}gastronomy/index.html" data-i18n="footer.link_restaurants">Moroccan Restaurants</a></li>
        <li><a class="hover:text-white transition" href="{prefix}transport/index.html" data-i18n="footer.link_transport">Transport &amp; Car Rental</a></li>
        <li><a class="hover:text-white transition" href="{prefix}blog/index.html" data-i18n="footer.link_blog">Travel Blog</a></li>
        <li><a class="hover:text-white transition" href="{prefix}contact.html" data-i18n="footer.link_contact">Contact Us</a></li>
      </ul>
    </div>
  </div>
  <div class="max-w-7xl mx-auto border-t border-creme/10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-creme/70">
    <p data-i18n="footer.copyright">© 2026 MoroccoTripMap. All rights reserved.</p>
    <p><span data-i18n="footer.created_by">Created by</span> <a class="text-sable underline font-semibold hover:text-white transition" href="https://kamliseo.com" rel="noopener noreferrer" target="_blank">Kamliseo</a></p>
  </div>
</footer>"""

    new_content = re.sub(r'<footer[\s\S]*?</footer>', new_footer, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1

print(f"✅ {updated_count} fichiers HTML mis à jour avec le footer complet (YouTube + Kamliseo).")
