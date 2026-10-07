/* =========================================================
   MOROCCO TRIP MAP — I18N ENGINE (FIX CHEMINS & TRADUCTIONS)
   ========================================================= */

const SUPPORTED_LANGS = ['fr', 'en', 'es', 'ar'];
const DEFAULT_LANG = 'fr';

const allTranslations = {};
const pendingTasks = {};

let currentLang = null;
let currentTranslations = {};

/* =========================================================
   1. CALCUL INTELLIGENT DU CHEMIN DES TRADUCTIONS
   ========================================================= */

const I18N_BASE_URL = (() => {
    // Retrouve le chemin absolu/relatif exact du script i18n.js
    const scripts = document.getElementsByTagName('script');
    for (let i = 0; i < scripts.length; i++) {
        const src = scripts[i].src;
        if (src && src.includes('i18n.js')) {
            return src.replace(/i18n\.js(\?.*)?$/, '');
        }
    }
    return '/js/';
})();

/* =========================================================
   2. DRAPEAUX SVG NETS
   ========================================================= */

const I18N_FLAG_SVGS = {
    fr: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3 2" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="3" height="2" fill="#ED2939"/><rect width="2" height="2" fill="#fff"/><rect width="1" height="2" fill="#002395"/></svg>`,
    en: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="60" height="30" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#C8102E" stroke-width="2"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></svg>`,
    es: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 500" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="750" height="500" fill="#c60b1e"/><rect y="125" width="750" height="250" fill="#ffc400"/></svg>`,
    ar: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="900" height="600" fill="#c1272d"/><polygon fill="none" stroke="#006233" stroke-width="15" points="450,170 361,441 593,273 307,273 639,441"/></svg>`
};

function getNestedTranslation(object, path) {
    if (!object || !path) return null;
    return path.split('.').reduce((accumulator, key) => accumulator?.[key], object) ?? null;
}

async function fetchJson(url) {
    try {
        const response = await fetch(url, { cache: 'default' });
        if (!response.ok) {
            console.warn(`[i18n] Fichier introuvable (${response.status}): ${url}`);
            return null;
        }
        return await response.json();
    } catch (e) {
        console.warn(`[i18n] Erreur réseau/JSON sur ${url}:`, e);
        return null;
    }
}

function collectI18nSections() {
    const sections = new Set();
    function addKey(key) {
        if (!key) return;
        const section = key.trim().split('.')[0];
        if (section) sections.add(section);
    }

    document.querySelectorAll('[data-i18n]').forEach(el => addKey(el.getAttribute('data-i18n')));
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => addKey(el.getAttribute('data-i18n-placeholder')));
    document.querySelectorAll('[data-i18n-attr]').forEach(el => {
        const rules = el.getAttribute('data-i18n-attr') || '';
        rules.split(',').forEach(rule => {
            const key = rule.split(':').slice(1).join(':').trim();
            addKey(key);
        });
    });

    return sections;
}

function updateLanguageDOM(langData) {
    currentTranslations = langData || {};

    /* 1. TEXTES */
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const value = getNestedTranslation(langData, key);
        if (value !== null && value !== undefined) {
            element.textContent = value;
        }
    });

    /* 2. PLACEHOLDERS */
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        const value = getNestedTranslation(langData, key);
        if (value !== null && value !== undefined) {
            element.placeholder = value;
        }
    });

    /* 3. ATTRIBUTS */
    document.querySelectorAll('[data-i18n-attr]').forEach(element => {
        const rules = element.getAttribute('data-i18n-attr') || '';
        rules.split(',').forEach(rule => {
            const parts = rule.split(':');
            const attrName = parts[0]?.trim();
            const key = parts.slice(1).join(':').trim();
            if (!attrName || !key) return;
            const value = getNestedTranslation(langData, key);
            if (value !== null && value !== undefined) {
                element.setAttribute(attrName, value);
            }
        });
    });
}

function syncLanguageSwitcherUI(lang) {
    const activeLang = lang || currentLang || DEFAULT_LANG;

    // 1. Texte du bouton (EN, FR, ES, AR)
    const langLabel = document.getElementById('current-lang-label');
    if (langLabel) {
        langLabel.textContent = activeLang.toUpperCase();
    }

    // 2. SVG du bouton principal (#lang-menu-button)
    const langButton = document.getElementById('lang-menu-button');
    if (langButton) {
        const oldSvg = langButton.querySelector('svg');
        if (oldSvg && I18N_FLAG_SVGS[activeLang]) {
            oldSvg.outerHTML = I18N_FLAG_SVGS[activeLang];
        }
    }
}

async function ensureLangData(lang, sections) {
    // Exemple de structure : js/translations/fr/core.json
    const base = `${I18N_BASE_URL}translations/${lang}/`;
    const dict = allTranslations[lang] || (allTranslations[lang] = {});
    const tasks = pendingTasks[lang] || (pendingTasks[lang] = {});

    const loadFile = (name, fileName) => {
        const cacheKey = `${lang}:${name}`;
        if (!tasks[cacheKey]) {
            tasks[cacheKey] = fetchJson(`${base}${fileName}`);
        }
        return tasks[cacheKey];
    };

    // Chargement de core.json
    let coreData = await loadFile('core', 'core.json');
    if (coreData && typeof coreData === 'object') {
        Object.assign(dict, coreData);
    }

    // Chargement des autres sections nécessaires (ex: places.json, nav.json)
    const missingSections = Array.from(sections || []).filter(name => !(name in dict));
    if (missingSections.length) {
        const loadedData = await Promise.all(
            missingSections.map(name => loadFile(name, `${encodeURIComponent(name)}.json`))
        );
        missingSections.forEach((name, index) => {
            if (loadedData[index] && typeof loadedData[index] === 'object') {
                dict[name] = loadedData[index];
            }
        });
    }

    return dict;
}

// Fonction accessible globalement
window.switchLanguage = window.changeLanguage = async function(lang) {
    if (!SUPPORTED_LANGS.includes(lang)) return;

    currentLang = lang;
    localStorage.setItem('preferred_lang', lang);

    // Mettre à jour l'icône du bouton tout de suite
    syncLanguageSwitcherUI(lang);

    // Masquer le menu déroulant
    const dropdown = document.getElementById('lang-menu-dropdown');
    if (dropdown) {
        dropdown.classList.add('hidden');
    }

    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;

    try {
        const sections = collectI18nSections();
        const dict = await ensureLangData(lang, sections);

        // Appliquer les traductions sur le DOM
        updateLanguageDOM(dict);

        window.dispatchEvent(
            new CustomEvent('languageChanged', {
                detail: { lang, translations: dict }
            })
        );
    } catch (error) {
        console.error(`[i18n] Erreur lors du chargement de "${lang}":`, error);
    }
};

window.i18n = {
    changeLanguage: window.switchLanguage,
    switchLanguage: window.switchLanguage,
    ensureSections: async function(names) {
        if (!currentLang) return currentTranslations;
        const dict = await ensureLangData(currentLang, names);
        currentTranslations = dict;
        return dict;
    },
    getTranslation: function(path) {
        return getNestedTranslation(currentTranslations, path);
    },
    getPhotoLabel: function(n) {
        const template = getNestedTranslation(currentTranslations, 'common.photo') || getNestedTranslation(currentTranslations, 'places.common.photo');
        return typeof template === 'string' ? template.replace('{n}', String(n)) : `Photo ${n}`;
    }
};

function initI18n() {
    const savedLang = localStorage.getItem('preferred_lang');
    const initialLang = SUPPORTED_LANGS.includes(savedLang) ? savedLang : DEFAULT_LANG;

    window.switchLanguage(initialLang);

    // Événement sur le bouton principal
    const langBtn = document.getElementById('lang-menu-button');
    const langDropdown = document.getElementById('lang-menu-dropdown');

    if (langBtn && langDropdown) {
        langBtn.onclick = function(e) {
            e.stopPropagation();
            langDropdown.classList.toggle('hidden');
        };

        document.onclick = function(e) {
            if (!langBtn.contains(e.target) && !langDropdown.contains(e.target)) {
                langDropdown.classList.add('hidden');
            }
        };
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initI18n);
} else {
    initI18n();
}
