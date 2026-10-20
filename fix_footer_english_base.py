import os, re, json
from pathlib import Path

print("🛠️ --- PASSAGE DU FOOTER EN ANGLAIS AVEC TRADUCTIONS DYNAMIQUES --- 🛠️\n> ")

# 1. Traductions des nouvelles colonnes pour les 4 langues
column_translations = {
    "en": {
        "col_imperial": "Imperial Cities & Culture",
        "col_desert": "Desert & Deep South",
        "col_practical": "Practical Guides & Stays"
    },
    "fr": {
        "col_imperial": "Villes Impériales & Culture",
        "col_desert": "Désert & Grand Sud",
        "col_practical": "Guides Pratiques & Séjour"
    },
    "es": {
        "col_imperial": "Ciudades Imperiales y Cultura",
        "col_desert": "Desierto y Gran Sur",
        "col_practical": "Guías Prácticas y Estancias"
    },
    "ar": {
        "col_imperial": "المدن الإمبراطورية والثقافة",
        "col_desert": "الصحراء والجنوب الكبير",
        "col_practical": "أدلة عملية وإقامة"
    }
}

trans_dir = Path('js/translations')

# Mettre à jour tous les fichiers JSON de traduction
for lang, cols in column_translations.items():
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
            for k, v in cols.items():
                data['footer'][k] = v
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

print("✅ Fichiers JSON mis à jour avec les titres de colonnes.")

# 2. Mettre à jour les fichiers HTML pour avoir les titres en anglais par défaut + data-i18n
new_footer_html = """<footer class="bg-vert text-creme pt-12 pb-8 px-4 sm:px-6 lg:px-8 mt-16 rounded-t-3xl">
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
        <li><a class="hover:text-white transition" href="/marrakech.html" data-i18n="footer.link_marrakech">Marrakech Travel Guide</a></li>
        <li><a class="hover:text-white transition" href="/fes.html" data-i18n="footer.link_fes">Fes Medina Guide</a></li>
        <li><a class="hover:text-white transition" href="/rabat.html" data-i18n="footer.link_rabat">Rabat Travel Guide</a></li>
        <li><a class="hover:text-white transition" href="/meknes.html" data-i18n="footer.link_meknes">Meknes Travel Guide</a></li>
        <li><a class="hover:text-white transition" href="/guides/histoire.html" data-i18n="footer.link_history">History of Morocco</a></li>
      </ul>
    </div>
    <div>
      <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.col_desert">Desert &amp; Deep South</h4>
      <ul class="text-xs space-y-2 text-creme/80">
        <li><a class="hover:text-white transition" href="/merzouga.html" data-i18n="footer.link_merzouga">Merzouga Desert &amp; Dunes</a></li>
        <li><a class="hover:text-white transition" href="/zagora.html" data-i18n="footer.link_zagora">Zagora &amp; Drâa Valley</a></li>
        <li><a class="hover:text-white transition" href="/ouarzazate.html" data-i18n="footer.link_ouarzazate">Ouarzazate Cinema Guide</a></li>
        <li><a class="hover:text-white transition" href="/experiences/index.html" data-i18n="footer.link_experiences">Desert Tours &amp; Activities</a></li>
        <li><a class="hover:text-white transition" href="destinations.html" data-i18n="footer.link_all_destinations">All Destinations</a></li>
      </ul>
    </div>
    <div>
      <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.col_practical">Practical Guides &amp; Stays</h4>
      <ul class="text-xs space-y-2 text-creme/80">
        <li><a class="hover:text-white transition" href="/riads/index.html" data-i18n="footer.link_stays">Authentic Riads &amp; Hotels</a></li>
        <li><a class="hover:text-white transition" href="/gastronomy/index.html" data-i18n="footer.link_restaurants">Moroccan Restaurants</a></li>
        <li><a class="hover:text-white transition" href="/transport/index.html" data-i18n="footer.link_transport">Transport &amp; Car Rental</a></li>
        <li><a class="hover:text-white transition" href="/blog/index.html" data-i18n="footer.link_blog">Travel Blog</a></li>
        <li><a class="hover:text-white transition" href="/contact.html" data-i18n="footer.link_contact">Contact Us</a></li>
      </ul>
    </div>
  </div>
  <div class="max-w-7xl mx-auto border-t border-creme/10 pt-6 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-creme/70">
    <p data-i18n="footer.copyright">© 2026 MoroccoTripMap. All rights reserved.</p>
    <p>Optimized for discovery &amp; authentic travel</p>
  </div>
</footer>"""

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
updated_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    new_content = re.sub(r'<footer[\s\S]*?</footer>', new_footer_html, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1

print(f"✅ {updated_count} fichiers HTML mis à jour avec le footer en anglais et dynamique.")
