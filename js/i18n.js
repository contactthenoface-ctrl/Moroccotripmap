/* =========================================================
   MOROCCO TRIP MAP — I18N ENGINE
   ========================================================= */

/* =========================================================
   CONFIGURATION
   ========================================================= */

const SUPPORTED_LANGS = ['fr', 'en', 'es', 'ar'];
const DEFAULT_LANG = 'fr';


/* =========================================================
   CACHE GLOBAL
   ========================================================= */

const allTranslations = {};
const pendingTasks = {};

let currentLang = null;
let currentTranslations = {};


/* =========================================================
   DRAPEAUX SVG (OFFICIELS)
   ========================================================= */

const I18N_FLAG_SVGS = {

    // France
    fr: `
        <svg viewBox="0 0 900 600" aria-hidden="true">
            <rect width="900" height="600" fill="#ED2939"/>
            <rect width="600" height="600" fill="#fff"/>
            <rect width="300" height="600" fill="#002395"/>
        </svg>
    `,

    // Royaume-Uni (Union Jack)
    en: `
        <svg viewBox="0 0 600 300" aria-hidden="true">
            <clipPath id="s">
                <path d="M0,0 v300 h600 v-300 z"/>
            </clipPath>
            <clipPath id="t">
                <path d="M0,0 L600,300 M600,0 L0,300"/>
            </clipPath>
            <g clip-path="url(#s)">
                <path d="M0,0 L600,300 M600,0 L0,300" stroke="#fff" stroke-width="60"/>
                <path d="M0,0 L600,300 M600,0 L0,300" stroke="#012169" stroke-width="60" clip-path="url(#t)"/>
                <path d="M0,0 L600,300 M600,0 L0,300" stroke="#C8102E" stroke-width="20" clip-path="url(#t)"/>
                <path d="M300,0 v300 M0,150 h600" stroke="#fff" stroke-width="100"/>
                <path d="M300,0 v300 M0,150 h600" stroke="#C8102E" stroke-width="60"/>
            </g>
        </svg>
    `,

    // Espagne
    es: `
        <svg viewBox="0 0 750 500" aria-hidden="true">
            <rect width="750" height="500" fill="#c60b1e"/>
            <rect width="750" height="250" y="125" fill="#ffc400"/>
        </svg>
    `,

    // Maroc (pour la langue Arabe)
    ar: `
        <svg viewBox="0 0 900 600" aria-hidden="true">
            <rect width="900" height="600" fill="#c1272d"/>
            <path d="M450,195 L480,287 L577,287 L498,344 L528,436 L450,379 L372,436 L402,344 L323,287 L420,287 Z" fill="none" stroke="#006233" stroke-width="14" stroke-linejoin="round"/>
        </svg>
    `
};


/* =========================================================
   URL DE BASE
   ========================================================= */

const I18N_BASE_URL = (() => {

    const script = document.currentScript;

    if (
        script &&
        script.src
    ) {
        return script.src.replace(
            /i18n\.js(\?.*)?$/,
            ''
        );
    }

    return 'js/';
})();


/* =========================================================
   UTILITAIRE : RÉCUPÉRER UNE TRADUCTION IMBRIQUÉE
   ========================================================= */

function getNestedTranslation(object, path) {

    if (!object || !path) {
        return null;
    }

    return path
        .split('.')
        .reduce(
            (accumulator, key) => accumulator?.[key],
            object
        ) ?? null;
}


/* =========================================================
   FETCH JSON
   ========================================================= */

function fetchJson(url) {

    return fetch(url, { cache: 'default' })
        .then(response => {

            if (!response.ok) {
                throw new Error(`HTTP ${response.status} for ${url}`);
            }

            return response.json();
        });
}


/* =========================================================
   ANALYSE DU DOM : DÉTECTER LES SECTIONS NÉCESSAIRES
   ========================================================= */

function collectI18nSections() {

    const sections = new Set();

    function addKey(key) {

        if (!key) return;

        const section = key.trim().split('.')[0];

        if (section) {
            sections.add(section);
        }
    }

    /* data-i18n */
    document.querySelectorAll('[data-i18n]').forEach(element => {
        addKey(element.getAttribute('data-i18n'));
    });

    /* data-i18n-placeholder */
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        addKey(element.getAttribute('data-i18n-placeholder'));
    });

    /* data-i18n-attr */
    document.querySelectorAll('[data-i18n-attr]').forEach(element => {

        const rules = element.getAttribute('data-i18n-attr') || '';

        rules.split(',').forEach(rule => {
            const parts = rule.split(':');
            const key = parts.slice(1).join(':').trim();
            addKey(key);
        });
    });

    return sections;
}


/* =========================================================
   MISE À JOUR DU DOM
   ========================================================= */

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


/* =========================================================
   SYNCHRONISER LE SÉLECTEUR DE LANGUE (SANS TOUCHER AU HTML)
   ========================================================= */

function syncLanguageSwitcherUI(lang) {

    /* -----------------------------------------------------
       1. Label du texte
       ----------------------------------------------------- */

    const langLabel = document.getElementById('current-lang-label');

    if (langLabel) {
        langLabel.textContent = lang.toUpperCase();
    }


    /* -----------------------------------------------------
       2. Drapeau sur le bouton principal
       ----------------------------------------------------- */

    const langButton = document.getElementById('lang-menu-button');

    if (langButton && I18N_FLAG_SVGS[lang]) {

        let flagWrapper = langButton.querySelector('.lang-flag');

        if (!flagWrapper) {
            flagWrapper = document.createElement('span');
            flagWrapper.className = 'lang-flag';
            langButton.insertBefore(flagWrapper, langButton.firstChild);
        }

        flagWrapper.innerHTML = I18N_FLAG_SVGS[lang];
    }


    /* -----------------------------------------------------
       3. Fermer le menu déroulant
       ----------------------------------------------------- */

    const langDropdown = document.getElementById('lang-menu-dropdown');

    if (langDropdown) {
        langDropdown.classList.add('hidden');
    }
}


/* =========================================================
   CHARGEMENT LAZY + CACHE
   ========================================================= */

async function ensureLangData(lang, sections) {

    const base = `${I18N_BASE_URL}translations/${lang}/`;

    const dict = allTranslations[lang] || (allTranslations[lang] = {});
    const tasks = pendingTasks[lang] || (pendingTasks[lang] = {});

    const loadFile = (name, fileName, required = false) => {

        const cacheKey = `${lang}:${name}`;

        if (!tasks[cacheKey]) {
            tasks[cacheKey] = fetchJson(`${base}${fileName}`).catch(error => {

                if (required) throw error;

                console.warn(`[i18n] Échec du chargement : ${fileName}`, error);
                return null;
            });
        }

        return tasks[cacheKey];
    };

    /* 1. CORE — OBLIGATOIRE */
    let coreData;

    try {
        coreData = await loadFile('core', 'core.json', true);
    } catch (error) {
        console.error(`[i18n] Impossible de charger core.json pour "${lang}".`, error);
        throw error;
    }

    if (!coreData || typeof coreData !== 'object') {
        throw new Error(`[i18n] core.json invalide pour "${lang}".`);
    }

    Object.assign(dict, coreData);

    /* 2. SECTIONS SPÉCIFIQUES */
    const missingSections = Array.from(sections || []).filter(name => !(name in dict));

    if (missingSections.length) {

        const loadedData = await Promise.all(
            missingSections.map(name =>
                loadFile(name, `${encodeURIComponent(name)}.json`, false)
            )
        );

        missingSections.forEach((name, index) => {
            const data = loadedData[index];
            if (data && typeof data === 'object') {
                dict[name] = data;
            }
        });
    }

    return dict;
}


/* =========================================================
   CHARGER UNE LANGUE
   ========================================================= */

async function loadLanguage(lang) {

    if (!SUPPORTED_LANGS.includes(lang)) {
        console.error(`[i18n] Langue non supportée : "${lang}"`);
        return;
    }

    const dropdown = document.getElementById('lang-menu-dropdown');
    if (dropdown) {
        dropdown.classList.add('hidden');
    }

    try {
        const sections = collectI18nSections();
        const dict = await ensureLangData(lang, sections);

        if (!dict || typeof dict !== 'object') {
            throw new Error(`Données de traduction invalides pour "${lang}".`);
        }

        currentLang = lang;

        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
        document.documentElement.lang = lang;

        localStorage.setItem('preferred_lang', lang);

        updateLanguageDOM(dict);
        syncLanguageSwitcherUI(lang);

        window.dispatchEvent(
            new CustomEvent('languageChanged', {
                detail: {
                    lang,
                    translations: dict
                }
            })
        );

    } catch (error) {
        console.error(`[i18n] Erreur lors du chargement de la langue "${lang}":`, error);
    }
}


/* =========================================================
   API PUBLIQUE
   ========================================================= */

window.i18n = {

    changeLanguage: loadLanguage,
    switchLanguage: loadLanguage,

    ensureSections: async function(names) {

        if (!currentLang) {
            return currentTranslations;
        }

        const dict = await ensureLangData(currentLang, names);
        currentTranslations = dict;
        return dict;
    },

    getTranslation: function(path) {
        return getNestedTranslation(currentTranslations, path);
    },

    getPhotoLabel: function(n) {

        const commonPhoto = getNestedTranslation(currentTranslations, 'common.photo');
        const placesPhoto = getNestedTranslation(currentTranslations, 'places.common.photo');
        const template = commonPhoto || placesPhoto;

        if (typeof template === 'string') {
            return template.replace('{n}', String(n));
        }

        return `Photo ${n}`;
    }
};


/* =========================================================
   ALIASES GLOBAUX
   ========================================================= */

window.changeLanguage = window.i18n.changeLanguage;
window.switchLanguage = window.i18n.switchLanguage;
window.i18nEnsureSections = window.i18n.ensureSections;
window.i18nPhotoLabel = window.i18n.getPhotoLabel;


/* =========================================================
   INITIALISATION
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    const savedLang = localStorage.getItem('preferred_lang');

    const initialLang = SUPPORTED_LANGS.includes(savedLang)
        ? savedLang
        : DEFAULT_LANG;

    loadLanguage(initialLang);

    document.addEventListener('click', event => {

        const langButton = event.target.closest('[data-lang]');

        if (!langButton) return;

        event.preventDefault();

        const selectedLang = langButton.getAttribute('data-lang');

        if (!selectedLang || !SUPPORTED_LANGS.includes(selectedLang)) {
            return;
        }

        if (selectedLang === currentLang) {
            document.getElementById('lang-menu-dropdown')?.classList.add('hidden');
            return;
        }

        loadLanguage(selectedLang);
    });
});
