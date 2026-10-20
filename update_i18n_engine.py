import re

with open('js/i18n.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Modifier la fonction collectI18nSections pour inclure automatiquement la page courante
old_code = """function collectI18nSections() {
    const sections = new Set();"""

new_code = """function collectI18nSections() {
    const sections = new Set();
    // Charger la page courante basée sur l'URL (ex: destinations.html -> destinations_page)
    let pageName = window.location.pathname.split('/').pop().replace('.html', '');
    if (!pageName || pageName === '/') pageName = 'index';
    sections.add(pageName + '_page');"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('js/i18n.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ js/i18n.js mis à jour avec succès !")
else:
    print("⚠️ Pattern non trouvé dans i18n.js")
