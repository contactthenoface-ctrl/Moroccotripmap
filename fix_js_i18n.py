import glob, re

# Code JavaScript robuste pour gérer les clés imbriquées (ex: footer.link_marrakech)
js_patch = """
// --- Correctif i18n dynamique pour les clés imbriquées (footer, etc.) ---
function getNestedTranslation(obj, path) {
    if (!obj || !path) return null;
    return path.split('.').reduce((prev, curr) => (prev && prev[curr] !== undefined) ? prev[curr] : null, obj);
}

function applyI18nTranslations(translationsObj) {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = getNestedTranslation(translationsObj, key);
        if (translation) {
            if (translation.includes('\\n')) {
                element.innerHTML = translation.replace(/\\n/g, '<br>');
            } else {
                element.innerText = translation;
            }
        }
    });
}
"""

js_files = glob.glob("js/**/*.js", recursive=True) + glob.glob("*.js")
js_files = [f for f in js_files if "node_modules" not in f and "fix_" not in f]

updated = 0
for filepath in js_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Injection si le fichier contient la logique de traduction/JSON
    if "i18n" in content.lower() or "json" in content.lower() or "fetch" in content.lower() or "lang" in content.lower():
        if "getNestedTranslation" not in content:
            new_content = content + "\n" + js_patch
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Correction appliquee dans : {filepath}")
            updated += 1

if updated == 0:
    print("Aucun fichier JS cible trouve automatiquement. Verification des dossiers...")
