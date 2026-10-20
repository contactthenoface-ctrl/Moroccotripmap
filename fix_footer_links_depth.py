import os, re
from pathlib import Path

print("🛠️ --- CORRECTION DES CHEMINS DU FOOTER SELON LA PROFONDEUR --- 🛠️\n")

html_files = [f for f in Path('.').rglob('*.html') if 'node_modules' not in f.parts]
updated_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Calculer la profondeur pour adapter les liens relatifs
    # ex: root = 0, places/foo.html = 1, places/bar/baz.html = 2
    parts = html_file.relative_to('.').parts
    depth = len(parts) - 1
    prefix = '../' * depth if depth > 0 else ''

    # Nouveau footer avec des liens relatifs intelligents basés sur la profondeur
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
      <h4 class="text-sm font-semibold text-sable mb-3 uppercase tracking-wider" data-i18n="footer.col_practical">Practical Guides &amp; Stays</h4>
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
    <p>Optimized for discovery &amp; authentic travel</p>
  </div>
</footer>"""

    # Remplacer le footer existant
    new_content = re.sub(r'<footer[\s\S]*?</footer>', new_footer, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1

print(f"✅ {updated_count} fichiers HTML mis à jour avec des liens de footer adaptés à leur profondeur.")
