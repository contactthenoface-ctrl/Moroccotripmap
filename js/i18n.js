/* =========================================================
   MOROCCO TRIP MAP — I18N ENGINE (DELEGATION & MULTI-MATCH)
   ========================================================= */

const SUPPORTED_LANGS = ['fr', 'en', 'es', 'ar'];
const DEFAULT_LANG = 'fr';

const allTranslations = {};
const pendingTasks = {};

let currentLang = null;
let currentTranslations = {};

/* DRAPEAUX SVG */
const I18N_FLAG_SVGS = {
    fr: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3 2" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="3" height="2" fill="#ED2939"/><rect width="2" height="2" fill="#fff"/><rect width="1" height="2" fill="#002395"/></svg>`,
    en: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="60" height="30" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#C8102E" stroke-width="2"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></svg>`,
    es: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 500" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="750" height="500" fill="#c60b1e"/><rect y="125" width="750" height="250" fill="#ffc400"/></svg>`,
    ar: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="20" height="15" class="rounded-sm shadow-sm flex-shrink-0" aria-hidden="true"><rect width="900" height="600" fill="#c1272d"/><polygon fill="none" stroke="#006233" stroke-width="15" points="450,170 361,441 593,273 307,273 639,441"/></svg>`
};

/* CHEMIN ABSOLU */
const I18N_BASE_URL = (() => {
    const scripts = document.getElementsByTagName('script');
    for (let i = 0; i < scripts.length; i++) {
        const src = scripts[i].src;
        if (src && src.includes('i18n.js')) {
            return src.replace(/i18n\.js(\?.*)?$/, '');
        }
    }
    return '/js/';
})();

function getNestedTranslation(object, path) {
    if (!object || !path) return null;
    return path.split('.').reduce((acc, key) => acc?.[key], object) ?? null;
}

async function fetchJson(url) {
    try {
        const res = await fetch(url, { cache: 'default' });
        return res.ok ? await res.json() : null;
    } catch (e) {
        return null;
    }
}

function collectI18nSections() {
    const sections = new Set();
    const addKey = (key) => key && sections.add(key.trim().split('.')[0]);

    document.querySelectorAll('[data-i18n]').forEach(el => addKey(el.getAttribute('data-i18n')));
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => addKey(el.getAttribute('data-i18n-placeholder')));
    document.querySelectorAll('[data-i18n-attr]').forEach(el => {
        (el.getAttribute('data-i18n-attr') || '').split(',').forEach(r => addKey(r.split(':').slice(1).join(':').trim()));
    });

    return sections;
}

function updateLanguageDOM(langData) {
    currentTranslations = langData || {};

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const val = getNestedTranslation(langData, el.getAttribute('data-i18n'));
        if (val !== null && val !== undefined) el.textContent = val;
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const val = getNestedTranslation(langData, el.getAttribute('data-i18n-placeholder'));
        if (val !== null && val !== undefined) el.placeholder = val;
    });

    document.querySelectorAll('[data-i18n-attr]').forEach(el => {
        (el.getAttribute('data-i18n-attr') || '').split(',').forEach(rule => {
            const [attrName, ...keyParts] = rule.split(':');
            const val = getNestedTranslation(langData, keyParts.join(':').trim());
            if (attrName && val !== null && val !== undefined) el.setAttribute(attrName.trim(), val);
        });
    });
}

function syncLanguageSwitcherUI(lang) {
    const activeLang = lang || currentLang || DEFAULT_LANG;
    
    // Recherche par ID principal ou par conteneur parent
    const langBtn = document.getElementById('lang-menu-button') || document.querySelector('#lang-menu-container button');

    if (langBtn) {
        const flagSvg = I18N_FLAG_SVGS[activeLang] || I18N_FLAG_SVGS[DEFAULT_LANG];
        langBtn.innerHTML = `
            ${flagSvg}
            <span id="current-lang-label">${activeLang.toUpperCase()}</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        `;
    }
}

async function ensureLangData(lang, sections) {
    const base = `${I18N_BASE_URL}translations/${lang}/`;
    const dict = allTranslations[lang] || (allTranslations[lang] = {});
    const tasks = pendingTasks[lang] || (pendingTasks[lang] = {});

    const loadFile = (name, fileName) => {
        const cacheKey = `${lang}:${name}`;
        if (!tasks[cacheKey]) tasks[cacheKey] = fetchJson(`${base}${fileName}`);
        return tasks[cacheKey];
    };

    let coreData = await loadFile('core', 'core.json');
    if (coreData && typeof coreData === 'object') Object.assign(dict, coreData);

    const missing = Array.from(sections || []).filter(name => !(name in dict));
    if (missing.length) {
        const loaded = await Promise.all(missing.map(name => loadFile(name, `${encodeURIComponent(name)}.json`)));
        missing.forEach((name, idx) => {
            if (loaded[idx] && typeof loaded[idx] === 'object') dict[name] = loaded[idx];
        });
    }

    return dict;
}

window.switchLanguage = window.changeLanguage = async function(lang) {
    if (!SUPPORTED_LANGS.includes(lang)) return;

    currentLang = lang;
    localStorage.setItem('preferred_lang', lang);

    syncLanguageSwitcherUI(lang);

    // Recherche tolérante du menu déroulant
    const dropdown = document.getElementById('lang-menu-dropdown') || document.querySelector('#lang-menu-container > div');
    if (dropdown) dropdown.classList.add('hidden');

    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;

    try {
        const sections = collectI18nSections();
        const dict = await ensureLangData(lang, sections);
        updateLanguageDOM(dict);
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang, translations: dict } }));
    } catch (e) {
        console.error(`[i18n] Error loading "${lang}":`, e);
    }
};

window.i18n = {
    changeLanguage: window.switchLanguage,
    switchLanguage: window.switchLanguage,
    ensureSections: async (names) => currentLang ? ensureLangData(currentLang, names) : currentTranslations,
    getTranslation: (path) => getNestedTranslation(currentTranslations, path)
};

/* GESTION ÉVÉNEMENTIELLE UNIVERSELLE */
function setupEvents() {
    document.addEventListener('click', (e) => {
        const langBtn = e.target.closest('#lang-menu-button') || e.target.closest('#lang-menu-container button');
        const dropdown = document.getElementById('lang-menu-dropdown') || document.querySelector('#lang-menu-container > div');

        if (langBtn && dropdown) {
            e.stopPropagation();
            dropdown.classList.toggle('hidden');
            return;
        }

        if (dropdown && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
}

function initI18n() {
    const saved = localStorage.getItem('preferred_lang');
    const initialLang = SUPPORTED_LANGS.includes(saved) ? saved : DEFAULT_LANG;
    
    setupEvents();
    window.switchLanguage(initialLang);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initI18n);
} else {
    initI18n();
}
