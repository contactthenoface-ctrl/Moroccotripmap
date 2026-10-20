// Variable globale pour stocker les traductions de la langue active
let currentTranslations = {};
// Cache par langue : chaque fichier langue chargé une seule fois
let allTranslations = {};

const I18N_FLAG_SVGS = {
    en: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="20" height="15" class="rounded-sm shadow-sm"><clipPath id="s"><path d="M0,0 v30 h60 v-30 z"/></clipPath><clipPath id="t"><path d="M30,15 h30 v15 z v-15 h-30 z h-30 v-15 z v15 h30 z"/></clipPath><g clip-path="url(#s)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
    fr: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3 2" width="20" height="15" class="rounded-sm shadow-sm"><rect width="3" height="2" fill="#ED2939"/><rect width="2" height="2" fill="#fff"/><rect width="1" height="2" fill="#002395"/></svg>',
    es: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 500" width="20" height="15" class="rounded-sm shadow-sm"><rect width="750" height="500" fill="#c60b1e"/><rect y="125" width="750" height="250" fill="#ffc400"/></svg>',
    ar: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="20" height="15" class="rounded-sm shadow-sm"><rect width="900" height="600" fill="#c1272d"/><polygon fill="none" stroke="#006233" stroke-width="15" points="450,170 361,441 593,273 307,273 639,441"/></svg>'
};

function getNestedTranslation(obj, path) {
    return path.split('.').reduce((prev, curr) => (prev ? prev[curr] : null), obj);
}

function updateLanguage(langData) {
    currentTranslations = langData;

    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = getNestedTranslation(langData, key);
        if (translation !== null && translation !== undefined) {
            element.textContent = translation;
        }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        const translation = getNestedTranslation(langData, key);
        if (translation !== null && translation !== undefined) {
            element.placeholder = translation;
        }
    });

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

// Dossier de ce script (js/) — marche depuis la racine ET places/ville-places/
const I18N_BASE_URL = (function () {
    const current = document.currentScript;
    if (current && current.src) {
        return current.src.replace(/i18n\.js(\?.*)?$/, '');
    }
    return 'js/';
})();

// Langue active (utile pour i18nEnsureSections)
let currentLang = null;
// Suivi par langue : { full: true si le fichier complet est chargé, tasks: requêtes déjà lancées }
const i18nMeta = {};

/** Liste les sections (1er segment des clés) réellement utilisées par la page. */
function collectI18nSections() {
    const sections = new Set();
    const add = (key) => {
        if (!key) return;
        const name = key.trim().split('.')[0];
        if (name) sections.add(name);
    };
    document.querySelectorAll('[data-i18n]').forEach(el => add(el.getAttribute('data-i18n')));
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => add(el.getAttribute('data-i18n-placeholder')));
    document.querySelectorAll('[data-i18n-attr]').forEach(el => {
        const parts = (el.getAttribute('data-i18n-attr') || '').split(':');
        if (parts.length > 1) add(parts[1]);
    });
    return sections;
}

function i18nFetchJson(url) {
    return fetch(url).then(response => {
        if (!response.ok) {
            throw new Error('HTTP ' + response.status + ' for ' + url);
        }
        return response.json();
    });
}

/**
 * Charge uniquement ce qu'il faut pour la page :
 *   translations/{lang}/_core.json  (nav, footer, breadcrumb, mobile_menu, destinations, common)
 *   translations/{lang}/{section}.json pour chaque section utilisée par la page
 * Si le dossier {lang}/ n'existe pas, retombe sur translations/{lang}.json (fichier complet).
 */
async function ensureLangData(lang, sections) {
    const base = I18N_BASE_URL + 'translations/';
    const dict = allTranslations[lang] || (allTranslations[lang] = {});
    const meta = i18nMeta[lang] || (i18nMeta[lang] = { full: false, tasks: {} });
    if (meta.full) return dict;

    const once = (name, url, apply) => {
        if (!meta.tasks[name]) {
            meta.tasks[name] = i18nFetchJson(url).then(apply);
        }
        return meta.tasks[name];
    };

    try {
        await once('_core', base + lang + '/_core.json', data => Object.assign(dict, data));
    } catch (coreError) {
        // Secours : ancien fichier unique
        let langData = await i18nFetchJson(base + lang + '.json');
        // Filet de sécurité si le fichier contient encore { "fr": { ... } }
        if (langData && langData[lang] && typeof langData[lang] === 'object' && !langData.nav) {
            langData = langData[lang];
        }
        Object.assign(dict, langData);
        meta.full = true;
        return dict;
    }

    const missing = Array.from(sections || []).filter(name => !(name in dict));
    await Promise.all(missing.map(name =>
        once(name, base + lang + '/' + encodeURIComponent(name) + '.json', data => { dict[name] = data; })
            .catch(err => console.warn('Section de traduction introuvable : ' + name + ' (' + lang + ')', err))
    ));
    return dict;
}

/**
 * Pour du JS qui lit currentTranslations.xxx sans passer par data-i18n :
 *   await i18nEnsureSections(['hero', 'cities']);
 */
window.i18nEnsureSections = async function (names) {
    if (!currentLang) return currentTranslations;
    const dict = await ensureLangData(currentLang, names);
    currentTranslations = dict;
    return dict;
};

async function loadLanguage(lang) {
    try {
        const dict = await ensureLangData(lang, collectI18nSections());
        if (!dict || typeof dict !== 'object') {
            console.error('Langue "' + lang + '" introuvable ou fichier invalide');
            return;
        }

        currentLang = lang;
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
        document.documentElement.lang = lang;
        localStorage.setItem('preferred_lang', lang);

        updateLanguage(dict);
        syncLanguageSwitcherUI(lang);
    } catch (error) {
        console.error('Erreur de chargement de la langue ' + lang + ':', error);
    }
}

function changeLanguage(lang) {
    loadLanguage(lang);
}
function switchLanguage(lang) {
    loadLanguage(lang);
}

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


window.i18nPhotoLabel = function (n) {
    var tpl = null;
    try {
        tpl = (currentTranslations.common && currentTranslations.common.photo)
           || (currentTranslations.places && currentTranslations.places.common && currentTranslations.places.common.photo)
           || null;
    } catch (e) {}
    if (tpl && typeof tpl === 'string') return tpl.replace('{n}', String(n));
    return 'Photo ' + n;
};
