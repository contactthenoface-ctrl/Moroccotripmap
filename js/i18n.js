/* =========================================================
   MOROCCO TRIP MAP — I18N ENGINE (CORRECTIF UNIVERSEL MULTI-PAGES)
   ========================================================= */

const SUPPORTED_LANGS = ['fr', 'en', 'es', 'ar'];
const DEFAULT_LANG = 'fr';

const allTranslations = {};
const pendingTasks = {};

let currentLang = null;
let currentTranslations = {};

/* =========================================================
   DRAPEAUX SVG NETS (SANS CONFLIT D'ID)
   ========================================================= */

const I18N_FLAG_SVGS = {
    fr: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" class="w-5 h-3.5 rounded-sm shadow-sm object-cover" aria-hidden="true"><rect width="900" height="600" fill="#ED2939"/><rect width="600" height="600" fill="#fff"/><rect width="300" height="600" fill="#002395"/></svg>`,
    en: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" class="w-5 h-3.5 rounded-sm shadow-sm object-cover" aria-hidden="true"><rect width="60" height="30" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#C8102E" stroke-width="2"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></svg>`,
    es: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 500" class="w-5 h-3.5 rounded-sm shadow-sm object-cover" aria-hidden="true"><rect width="750" height="500" fill="#c60b1e"/><rect width="750" height="250" y="125" fill="#ffc400"/></svg>`,
    ar: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" class="w-5 h-3.5 rounded-sm shadow-sm object-cover" aria-hidden="true"><rect width="900" height="600" fill="#c1272d"/><path d="M450,195 L480,287 L577,287 L498,344 L528,436 L450,379 L372,436 L402,344 L323,287 L420,287 Z" fill="none" stroke="#006233" stroke-width="14" stroke-linejoin="round"/></svg>`
};

const I18N_BASE_URL = (() => {
    const script = document.currentScript;
    if (script && script.src) {
        return script.src.replace(/i18n\.js(\?.*)?$/, '');
    }
    return 'js/';
})();

function getNestedTranslation(object, path) {
    if (!object || !path) return null;
    return path.split('.').reduce((accumulator, key) => accumulator?.[key], object) ?? null;
}

function fetchJson(url) {
    return fetch(url, { cache: 'default' }).then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status} for ${url}`);
        return response.json();
    });
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
        if (value !== null && value !== undefined) element.textContent = value;
    });

    /* 2. PLACEHOLDERS */
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        const value = getNestedTranslation(langData, key);
        if (value !== null && value !== undefined) element.placeholder = value;
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
            if (value !== null && value !== undefined) element.setAttribute(attrName, value);
        });
    });
}

/* =========================================================
   FORCE LA REPLACEMENT RADICALE ET SYSTÉMATIQUE
   ========================================================= */

function syncLanguageSwitcherUI(lang) {
    const activeLang = lang || currentLang || DEFAULT_LANG;

    // 1. Label texte (ex: FR, EN, AR)
    const langLabel = document.getElementById('current-lang-label');
    if (langLabel) {
        langLabel.textContent = activeLang.toUpperCase();
    }

    // 2. Drapeau bouton principal
    const currentFlagContainer = document.getElementById('current-flag');
    if (currentFlagContainer && I18N_FLAG_SVGS[activeLang]) {
        currentFlagContainer.innerHTML = I18N_FLAG_SVGS[activeLang];
    }

    // 3. Forcer le remplacement des drapeaux dans les éléments du menu déroulant
    document.querySelectorAll('[data-lang]').forEach(option => {
        const optionLang = option.getAttribute('data-lang');
        if (!I18N_FLAG_SVGS[optionLang]) return;

        // Vider TOUS les SVG existants dans l'option
        option.querySelectorAll('svg').forEach(svg => svg.remove());

        // Nettoyer les spans d'icônes préexistants
        option.querySelectorAll('.lang-flag, .flag-icon').forEach(el => el.remove());

        // Réinjecter le propre SVG au début
        const flagSpan = document.createElement('span');
        flagSpan.className = 'lang-flag inline-flex items-center me-2';
        flagSpan.innerHTML = I18N_FLAG_SVGS[optionLang];
        option.insertBefore(flagSpan, option.firstChild);
    });

    // 4. Fermer le menu déroulant s'il existe
    const langDropdown = document.getElementById('lang-menu-dropdown');
    if (langDropdown) {
        langDropdown.classList.add('hidden');
    }
}

async function ensureLangData(lang, sections) {
    const base = `${I18N_BASE_URL}translations/${lang}/`;
    const dict = allTranslations[lang] || (allTranslations[lang] = {});
    const tasks = pendingTasks[lang] || (pendingTasks[lang] = {});

    const loadFile = (name, fileName, required = false) => {
        const cacheKey = `${lang}:${name}`;
        if (!tasks[cacheKey]) {
            tasks[cacheKey] = fetchJson(`${base}${fileName}`).catch(error => {
                if (required) throw error;
                console.warn(`[i18n] Échec : ${fileName}`, error);
                return null;
            });
        }
        return tasks[cacheKey];
    };

    let coreData = await loadFile('core', 'core.json', true);
    if (!coreData || typeof coreData !== 'object') throw new Error(`[i18n] core.json invalide pour "${lang}".`);
    Object.assign(dict, coreData);

    const missingSections = Array.from(sections || []).filter(name => !(name in dict));
    if (missingSections.length) {
        const loadedData = await Promise.all(
            missingSections.map(name => loadFile(name, `${encodeURIComponent(name)}.json`, false))
        );
        missingSections.forEach((name, index) => {
            if (loadedData[index] && typeof loadedData[index] === 'object') {
                dict[name] = loadedData[index];
            }
        });
    }

    return dict;
}

async function loadLanguage(lang) {
    if (!SUPPORTED_LANGS.includes(lang)) return;

    currentLang = lang;
    localStorage.setItem('preferred_lang', lang);

    // Appliquer direct au UI
    syncLanguageSwitcherUI(lang);

    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;

    try {
        const sections = collectI18nSections();
        const dict = await ensureLangData(lang, sections);

        updateLanguageDOM(dict);

        window.dispatchEvent(
            new CustomEvent('languageChanged', {
                detail: { lang, translations: dict }
            })
        );
    } catch (error) {
        console.error(`[i18n] Erreur pour "${lang}":`, error);
    }
}

/* =========================================================
   INITIALISATION ET SURVEILLANCE ACTIVE DU DOM
   ========================================================= */

window.i18n = {
    changeLanguage: loadLanguage,
    switchLanguage: loadLanguage,
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

window.changeLanguage = window.i18n.changeLanguage;
window.switchLanguage = window.i18n.switchLanguage;

function initI18n() {
    const savedLang = localStorage.getItem('preferred_lang');
    const initialLang = SUPPORTED_LANGS.includes(savedLang) ? savedLang : DEFAULT_LANG;

    loadLanguage(initialLang);

    // Écouteur global pour les clics de changement de langue
    document.addEventListener('click', event => {
        const langButton = event.target.closest('[data-lang]');
        if (!langButton) return;

        event.preventDefault();
        const selectedLang = langButton.getAttribute('data-lang');

        if (selectedLang && SUPPORTED_LANGS.includes(selectedLang)) {
            loadLanguage(selectedLang);
        }
    });

    // Observer pour écraser automatiquement si d'autres JS injectent le header après coup
    const observer = new MutationObserver(() => {
        if (currentLang) {
            syncLanguageSwitcherUI(currentLang);
        }
    });

    const targetNode = document.getElementById('lang-menu-container') || document.body;
    observer.observe(targetNode, { childList: true, subtree: true });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initI18n);
} else {
    initI18n();
}
