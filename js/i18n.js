// ============================================================
// I18N — Système de traduction multilingue
// ============================================================
//
// Structure attendue :
//
// js/
// ├── i18n.js
// └── translations/
//     ├── ar/
//     │   ├── _core.json
//     │   ├── home.json
//     │   ├── services.json
//     │   └── ...
//     ├── en/
//     │   ├── _core.json
//     │   └── ...
//     ├── es/
//     │   ├── _core.json
//     │   └── ...
//     └── fr/
//         ├── _core.json
//         └── ...
//
// Les anciens fichiers :
// translations/fr.json
// translations/en.json
// translations/es.json
// translations/ar.json
//
// ne sont plus utilisés.
// ============================================================


// ============================================================
// VARIABLES GLOBALES
// ============================================================

// Traductions actuellement utilisées
let currentTranslations = {};

// Cache des traductions par langue
// Chaque fichier JSON chargé est conservé en mémoire
// pour éviter de le recharger inutilement.
let allTranslations = {};


// ============================================================
// DRAPEAUX
// ============================================================

const I18N_FLAG_SVGS = {

    en: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="20" height="15" class="rounded-sm shadow-sm"><clipPath id="s"><path d="M0,0 v30 h60 v-30 z"/></clipPath><clipPath id="t"><path d="M30,15 h30 v15 z v-15 h-30 z h-30 v-15 z v15 h30 z"/></clipPath><g clip-path="url(#s)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>',

    fr: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3 2" width="20" height="15" class="rounded-sm shadow-sm"><rect width="3" height="2" fill="#ED2939"/><rect width="2" height="2" fill="#fff"/><rect width="1" height="2" fill="#002395"/></svg>',

    es: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 500" width="20" height="15" class="rounded-sm shadow-sm"><rect width="750" height="500" fill="#c60b1e"/><rect y="125" width="750" height="250" fill="#ffc400"/></svg>',

    ar: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="20" height="15" class="rounded-sm shadow-sm"><rect width="900" height="600" fill="#c1272d"/><polygon fill="none" stroke="#006233" stroke-width="15" points="450,170 361,441 593,273 307,273 639,441"/></svg>'

};


// ============================================================
// RÉCUPÉRER UNE TRADUCTION IMBRIQUÉE
// Exemple :
//
// getNestedTranslation(data, "home.hero.title")
//
// retourne :
// data.home.hero.title
// ============================================================

function getNestedTranslation(obj, path) {

    if (!obj || !path) {
        return null;
    }

    return path
        .split('.')
        .reduce((prev, curr) => {
            return prev != null ? prev[curr] : null;
        }, obj);
}


// ============================================================
// APPLIQUER LES TRADUCTIONS À LA PAGE
// ============================================================

function updateLanguage(langData) {

    currentTranslations = langData || {};


    // --------------------------------------------------------
    // data-i18n
    // --------------------------------------------------------

    document.querySelectorAll('[data-i18n]').forEach(element => {

        const key = element.getAttribute('data-i18n');

        const translation = getNestedTranslation(
            langData,
            key
        );

        if (
            translation !== null &&
            translation !== undefined
        ) {
            element.textContent = translation;
        }

    });


    // --------------------------------------------------------
    // data-i18n-placeholder
    // --------------------------------------------------------

    document
        .querySelectorAll('[data-i18n-placeholder]')
        .forEach(element => {

            const key =
                element.getAttribute(
                    'data-i18n-placeholder'
                );

            const translation =
                getNestedTranslation(
                    langData,
                    key
                );

            if (
                translation !== null &&
                translation !== undefined
            ) {
                element.placeholder = translation;
            }

        });


    // --------------------------------------------------------
    // data-i18n-attr
    //
    // Exemple :
    // data-i18n-attr="title:common.title"
    // --------------------------------------------------------

    document
        .querySelectorAll('[data-i18n-attr]')
        .forEach(element => {

            const rule =
                element.getAttribute(
                    'data-i18n-attr'
                );

            const parts =
                rule.split(':');

            const attrName =
                parts[0]?.trim();

            const key =
                parts.slice(1).join(':').trim();

            if (!attrName || !key) {
                return;
            }

            const translation =
                getNestedTranslation(
                    langData,
                    key
                );

            if (
                translation !== null &&
                translation !== undefined
            ) {

                element.setAttribute(
                    attrName,
                    translation
                );

            }

        });

}


// ============================================================
// METTRE À JOUR L'INTERFACE DU SÉLECTEUR DE LANGUE
// ============================================================

function syncLanguageSwitcherUI(lang) {

    // --------------------------------------------------------
    // Texte de la langue actuelle
    // --------------------------------------------------------

    const langLabel =
        document.getElementById(
            'current-lang-label'
        );

    if (langLabel) {

        langLabel.textContent =
            lang.toUpperCase();

    }


    // --------------------------------------------------------
    // Drapeau
    // --------------------------------------------------------

    const langButton =
        document.getElementById(
            'lang-menu-button'
        );

    if (
        langButton &&
        I18N_FLAG_SVGS[lang]
    ) {

        const svgElement =
            langButton.querySelector('svg');

        if (svgElement) {

            svgElement.outerHTML =
                I18N_FLAG_SVGS[lang];

        }

    }


    // --------------------------------------------------------
    // Fermer le menu
    // --------------------------------------------------------

    const langDropdown =
        document.getElementById(
            'lang-menu-dropdown'
        );

    if (langDropdown) {

        langDropdown.classList.add(
            'hidden'
        );

    }

}


// ============================================================
// DÉTERMINER LE DOSSIER DU SCRIPT
// ============================================================
//
// Permet de fonctionner depuis :
//
// /
// /places/ville-places/
//
// etc.
//
// Si i18n.js se trouve dans /js/,
// I18N_BASE_URL devient automatiquement /js/.
//
// ============================================================

const I18N_BASE_URL = (function () {

    const current =
        document.currentScript;

    if (
        current &&
        current.src
    ) {

        return current.src.replace(
            /i18n\.js(\?.*)?$/,
            ''
        );

    }

    return 'js/';

})();


// ============================================================
// LANGUE ACTIVE
// ============================================================

let currentLang = null;


// ============================================================
// MÉTADONNÉES DE CHARGEMENT
// ============================================================
//
// Exemple :
//
// i18nMeta.fr = {
//     full: false,
//     tasks: {
//         _core: Promise,
//         home: Promise
//     }
// }
//
// ============================================================

const i18nMeta = {};


// ============================================================
// DÉTECTER LES SECTIONS UTILISÉES PAR LA PAGE
// ============================================================
//
// Exemple :
//
// data-i18n="home.hero.title"
//                  ↓
// section = "home"
//
// Le système chargera donc :
//
// translations/fr/home.json
//
// ============================================================

function collectI18nSections() {

    const sections =
        new Set();


    const add = (key) => {

        if (!key) {
            return;
        }

        const name =
            key
                .trim()
                .split('.')[0];

        if (name) {
            sections.add(name);
        }

    };


    // data-i18n

    document
        .querySelectorAll('[data-i18n]')
        .forEach(element => {

            add(
                element.getAttribute(
                    'data-i18n'
                )
            );

        });


    // data-i18n-placeholder

    document
        .querySelectorAll(
            '[data-i18n-placeholder]'
        )
        .forEach(element => {

            add(
                element.getAttribute(
                    'data-i18n-placeholder'
                )
            );

        });


    // data-i18n-attr

    document
        .querySelectorAll(
            '[data-i18n-attr]'
        )
        .forEach(element => {

            const parts =
                (
                    element.getAttribute(
                        'data-i18n-attr'
                    ) || ''
                ).split(':');

            if (parts.length > 1) {

                add(
                    parts
                        .slice(1)
                        .join(':')
                );

            }

        });


    return sections;

}


// ============================================================
// CHARGER UN FICHIER JSON
// ============================================================

function i18nFetchJson(url) {

    return fetch(url)
        .then(response => {

            if (!response.ok) {

                throw new Error(
                    'HTTP ' +
                    response.status +
                    ' for ' +
                    url
                );

            }

            return response.json();

        });

}


// ============================================================
// CHARGER LES DONNÉES D'UNE LANGUE
// ============================================================
//
// Charge uniquement :
//
// translations/{lang}/_core.json
//
// puis les sections nécessaires :
//
// translations/{lang}/{section}.json
//
// IMPORTANT :
// Aucun fallback vers :
//
// translations/fr.json
// translations/en.json
// translations/es.json
// translations/ar.json
//
// ============================================================

async function ensureLangData(
    lang,
    sections
) {

    const base =
        I18N_BASE_URL +
        'translations/';


    // --------------------------------------------------------
    // Vérification de la langue
    // --------------------------------------------------------

    const supportedLanguages = [
        'fr',
        'en',
        'es',
        'ar'
    ];

    if (
        !supportedLanguages.includes(lang)
    ) {

        throw new Error(
            'Langue non supportée : ' +
            lang
        );

    }


    // --------------------------------------------------------
    // Cache
    // --------------------------------------------------------

    const dict =
        allTranslations[lang] ||
        (
            allTranslations[lang] = {}
        );


    const meta =
        i18nMeta[lang] ||
        (
            i18nMeta[lang] = {
                full: false,
                tasks: {}
            }
        );


    // Si tout est déjà chargé

    if (meta.full) {

        return dict;

    }


    // --------------------------------------------------------
    // Éviter les doubles requêtes
    // --------------------------------------------------------

    const once = (
        name,
        url,
        apply
    ) => {

        if (!meta.tasks[name]) {

            meta.tasks[name] =
                i18nFetchJson(url)
                    .then(apply);

        }

        return meta.tasks[name];

    };


    // --------------------------------------------------------
    // 1. Charger _core.json
    // --------------------------------------------------------

    await once(
        '_core',
        base +
        lang +
        '/_core.json',
        data => {

            if (
                data &&
                typeof data === 'object'
            ) {

                Object.assign(
                    dict,
                    data
                );

            }

        }
    );


    // --------------------------------------------------------
    // 2. Charger les sections nécessaires
    // --------------------------------------------------------

    const missing =
        Array.from(
            sections || []
        ).filter(
            name =>
                !(name in dict)
        );


    await Promise.all(

        missing.map(name => {

            return once(

                name,

                base +
                lang +
                '/' +
                encodeURIComponent(name) +
                '.json',

                data => {

                    dict[name] =
                        data;

                }

            ).catch(error => {

                console.warn(
                    'Section de traduction introuvable : ' +
                    name +
                    ' (' +
                    lang +
                    ')',
                    error
                );

            });

        })

    );


    return dict;

}


// ============================================================
// CHARGER DES SECTIONS SUPPLÉMENTAIRES DEPUIS DU JS
// ============================================================
//
// Exemple :
//
// await i18nEnsureSections([
//     'hero',
//     'cities'
// ]);
//
// ============================================================

window.i18nEnsureSections =
    async function (names) {

        if (!currentLang) {

            return currentTranslations;

        }


        const dict =
            await ensureLangData(
                currentLang,
                names
            );


        currentTranslations =
            dict;


        return dict;

    };


// ============================================================
// CHANGER DE LANGUE
// ============================================================

async function loadLanguage(lang) {

    // --------------------------------------------------------
    // Fermer immédiatement le menu
    // --------------------------------------------------------
    //
    // Même si le réseau met quelques secondes à charger
    // les fichiers JSON, le menu ne reste pas bloqué.
    //

    const langDropdown =
        document.getElementById(
            'lang-menu-dropdown'
        );

    if (langDropdown) {

        langDropdown.classList.add(
            'hidden'
        );

    }


    try {

        // ----------------------------------------------------
        // Charger les traductions
        // ----------------------------------------------------

        const sections =
            collectI18nSections();

        const dict =
            await ensureLangData(
                lang,
                sections
            );


        // ----------------------------------------------------
        // Vérification
        // ----------------------------------------------------

        if (
            !dict ||
            typeof dict !== 'object'
        ) {

            console.error(
                'Langue "' +
                lang +
                '" introuvable ou fichier invalide.'
            );

            return;

        }


        // ----------------------------------------------------
        // Définir la langue active
        // ----------------------------------------------------

        currentLang =
            lang;


        // ----------------------------------------------------
        // Direction du texte
        // ----------------------------------------------------

        document.documentElement.dir =
            lang === 'ar'
                ? 'rtl'
                : 'ltr';


        // ----------------------------------------------------
        // Attribut lang
        // ----------------------------------------------------

        document.documentElement.lang =
            lang;


        // ----------------------------------------------------
        // Sauvegarder la préférence
        // ----------------------------------------------------

        localStorage.setItem(
            'preferred_lang',
            lang
        );


        // ----------------------------------------------------
        // Appliquer les traductions
        // ----------------------------------------------------

        updateLanguage(
            dict
        );


        // ----------------------------------------------------
        // Mettre à jour le sélecteur
        // ----------------------------------------------------

        syncLanguageSwitcherUI(
            lang
        );


    } catch (error) {

        console.error(
            'Erreur de chargement de la langue ' +
            lang +
            ':',
            error
        );

    }

}


// ============================================================
// FONCTIONS PUBLIQUES
// ============================================================

function changeLanguage(lang) {

    loadLanguage(lang);

}


function switchLanguage(lang) {

    loadLanguage(lang);

}


// Rendre disponibles globalement

window.changeLanguage =
    changeLanguage;

window.switchLanguage =
    switchLanguage;


// ============================================================
// INITIALISATION
// ============================================================

document.addEventListener(
    'DOMContentLoaded',
    () => {

        // ----------------------------------------------------
        // Langue sauvegardée
        // ----------------------------------------------------

        const savedLang =
            localStorage.getItem(
                'preferred_lang'
            ) || 'fr';


        // ----------------------------------------------------
        // Charger la langue
        // ----------------------------------------------------

        loadLanguage(
            savedLang
        );


        // ----------------------------------------------------
        // Boutons de langues
        // ----------------------------------------------------

        document
            .querySelectorAll(
                '[data-lang]'
            )
            .forEach(button => {

                button.addEventListener(
                    'click',
                    event => {

                        event.preventDefault();
                        event.stopPropagation();


                        const selectedLang =
                            button.getAttribute(
                                'data-lang'
                            );


                        if (
                            selectedLang
                        ) {

                            loadLanguage(
                                selectedLang
                            );

                        }

                    }
                );

            });

    }
);


// ============================================================
// LABEL "PHOTO"
// ============================================================
//
// Utilisé par du JavaScript externe.
//
// Exemple :
//
// i18nPhotoLabel(3)
//
// ============================================================

window.i18nPhotoLabel =
    function (n) {

        let tpl = null;


        try {

            tpl =
                (
                    currentTranslations
                        .common &&
                    currentTranslations
                        .common
                        .photo
                ) ||

                (
                    currentTranslations
                        .places &&
                    currentTranslations
                        .places
                        .common &&
                    currentTranslations
                        .places
                        .common
                        .photo
                ) ||

                null;

        } catch (e) {

            tpl = null;

        }


        if (
            tpl &&
            typeof tpl === 'string'
        ) {

            return tpl.replace(
                '{n}',
                String(n)
            );

        }


        return 'Photo ' + n;

    };


// ============================================================
// FIN I18N
// ============================================================

Après avoir remplacé le fichier :

1. Enregistre "js/i18n.js".
2. Vérifie que tu as bien "js/translations/fr/_core.json", "ar/_core.json", "en/_core.json", "es/_core.json".
3. Vérifie que les sections demandées par chaque page existent dans les dossiers correspondants.
4. Fais un hard refresh du site ("Ctrl + F5" sur PC) ou vide le cache du navigateur sur mobile.
5. Teste FR → EN → ES → AR.

Avec cette version, "fr.json", "en.json", "es.json" et "ar.json" ne sont plus nécessaires du tout.
