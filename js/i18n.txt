// Variable globale pour stocker les traductions chargées
let currentTranslations = {};
let allTranslations = {}; // cache du fichier complet, chargé une seule fois

// Drapeaux SVG utilisés pour synchroniser visuellement le sélecteur de langue
// (bouton #lang-menu-button + libellé #current-lang-label), quelle que soit la page.
const I18N_FLAG_SVGS = {
    en: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="20" height="15" class="rounded-sm shadow-sm"><clipPath id="s"><path d="M0,0 v30 h60 v-30 z"/></clipPath><clipPath id="t"><path d="M30,15 h30 v15 z v-15 h-30 z h-30 v-15 z v15 h30 z"/></clipPath><g clip-path="url(#s)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
    fr: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3 2" width="20" height="15" class="rounded-sm shadow-sm"><rect width="3" height="2" fill="#ED2939"/><rect width="2" height="2" fill="#fff"/><rect width="1" height="2" fill="#002395"/></svg>',
    es: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 500" width="20" height="15" class="rounded-sm shadow-sm"><rect width="750" height="500" fill="#c60b1e"/><rect y="125" width="750" height="250" fill="#ffc400"/></svg>',
    ar: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="20" height="15" class="rounded-sm shadow-sm"><rect width="900" height="600" fill="#c1272d"/><polygon fill="none" stroke="#006233" stroke-width="15" points="450,170 361,441 593,273 307,273 639,441"/></svg>'
};

// 1. Fonction utilitaire pour lire les clés imbriquées (ex: "nav.destinations")
function getNestedTranslation(obj, path) {
    return path.split('.').reduce((prev, curr) => (prev ? prev[curr] : null), obj);
}

// 2. Fonction principale de mise à jour du DOM (Texte + Placeholders + Attributs)
function updateLanguage(langData) {
    currentTranslations = langData;

    // Traduction du texte des éléments
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = getNestedTranslation(langData, key);
        if (translation !== null && translation !== undefined) {
            element.textContent = translation;
        }
    });

    // Traduction des placeholders (champs de recherche / formulaires)
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        const translation = getNestedTranslation(langData, key);
        if (translation !== null && translation !== undefined) {
            element.placeholder = translation;
        }
    });

    // Traduction d'attributs arbitraires, ex: data-i18n-attr="content:seo.description"
    document.querySelectorAll('[data-i18n-attr]').forEach(element => {
        const rule = element.getAttribute('data-i18n-attr');
        const [attrName, key] = rule.split(':').map(s => s.trim());
        if (!attrName || !key) return;
        const translation = getNestedTranslation(langData, key);
        if (translation !== null && translation !== undefined) {
            element.setAttribute(attrName, translation);
        }
    });
}

// 3. Synchronise l'affichage du sélecteur de langue (drapeau + libellé "EN"/"FR"...)
//    quelle que soit la page : marche pour le bouton #lang-menu-button partout sur le site.
function syncLanguageSwitcherUI(lang) {
    const langLabel = document.getElementById('current-lang-label');
    if (langLabel) {
        langLabel.textContent = lang.toUpperCase();
    }

    const langButton = document.getElementById('lang-menu-button');
    if (langButton && I18N_FLAG_SVGS[lang]) {
        const svgElement = langButton.querySelector('svg');
        if (svgElement) {
            svgElement.outerHTML = I18N_FLAG_SVGS[lang];
        }
    }

    const langDropdown = document.getElementById('lang-menu-dropdown');
    if (langDropdown) {
        langDropdown.classList.add('hidden');
    }
}

// 4bis. Dossier réel où se trouve ce script (déduit de sa propre balise <script src="...">),
//       pour construire le chemin vers translations.json quelle que soit la profondeur de la
//       page qui charge i18n.js (racine, places/, restaurants/, etc.).
const I18N_BASE_URL = (function () {
    const current = document.currentScript;
    if (current && current.src) {
        return current.src.replace(/i18n\.js(\?.*)?$/, '');
    }
    return 'js/'; // repli si document.currentScript n'est pas disponible
})();

// 4. Charger (une seule fois) le fichier JSON complet, puis appliquer la langue
async function loadLanguage(lang) {
    try {
        if (Object.keys(allTranslations).length === 0) {
            const response = await fetch(I18N_BASE_URL + 'translations.json');
            allTranslations = await response.json();
        }

        const langData = allTranslations[lang];
        if (!langData) {
            console.error(`Langue "${lang}" introuvable dans translations.json`);
            return;
        }

        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
        document.documentElement.lang = lang;
        localStorage.setItem('preferred_lang', lang);

        updateLanguage(langData);
        syncLanguageSwitcherUI(lang);
    } catch (error) {
        console.error(`Erreur de chargement de la langue ${lang}:`, error);
    }
}

// 5. Alias appelé par les pages utilisant onclick="changeLanguage('fr')" ou switchLanguage(...)
function changeLanguage(lang) {
    loadLanguage(lang);
}
function switchLanguage(lang) {
    loadLanguage(lang);
}

// 6. Initialisation et association des clics sur les boutons data-lang="fr" (utilisés par
//    certaines pages du site, ex: destinations.html) — pour que le sélecteur fonctionne
//    quelle que soit la convention utilisée par la page (onclick ou data-lang).
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferred_lang') || 'fr';
    loadLanguage(savedLang);

    document.querySelectorAll('[data-lang]').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const selectedLang = button.getAttribute('data-lang');
            if (selectedLang) {
                loadLanguage(selectedLang);
            }
        });
    });
});
