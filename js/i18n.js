/* =========================================================
   MOROCCO TRIP MAP — I18N ENGINE
   =========================================================

   Structure :

   js/
   ├── i18n.js
   └── translations/
       ├── fr/
       │   ├── core.json
       │   ├── hero.json
       │   └── ...
       │
       ├── en/
       │   ├── core.json
       │   ├── hero.json
       │   └── ...
       │
       ├── es/
       │   ├── core.json
       │   ├── hero.json
       │   └── ...
       │
       └── ar/
           ├── core.json
           ├── hero.json
           └── ...

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
   DRAPEAUX SVG
   ========================================================= */

const I18N_FLAG_SVGS = {

    fr: `
        <svg
            class="i18n-flag-svg"
            viewBox="0 0 24 16"
            aria-hidden="true"
            focusable="false"
        >
            <rect
                width="8"
                height="16"
                fill="#0055A4"
            />

            <rect
                width="8"
                height="16"
                x="8"
                fill="#FFFFFF"
            />

            <rect
                width="8"
                height="16"
                x="16"
                fill="#EF4135"
            />
        </svg>
    `,

    en: `
        <svg
            class="i18n-flag-svg"
            viewBox="0 0 24 16"
            aria-hidden="true"
            focusable="false"
        >
            <rect
                width="24"
                height="16"
                fill="#012169"
            />

            <path
                d="M0 0L24 16M24 0L0 16"
                stroke="#FFFFFF"
                stroke-width="3"
            />

            <path
                d="M0 0L24 16M24 0L0 16"
                stroke="#C8102E"
                stroke-width="1.5"
            />

            <path
                d="M12 0V16M0 8H24"
                stroke="#FFFFFF"
                stroke-width="5"
            />

            <path
                d="M12 0V16M0 8H24"
                stroke="#C8102E"
                stroke-width="3"
            />
        </svg>
    `,

    es: `
        <svg
            class="i18n-flag-svg"
            viewBox="0 0 24 16"
            aria-hidden="true"
            focusable="false"
        >
            <rect
                width="24"
                height="16"
                fill="#AA151B"
            />

            <rect
                width="24"
                height="8"
                y="4"
                fill="#F1BF00"
            />
        </svg>
    `,

    ar: `
        <svg
            class="i18n-flag-svg"
            viewBox="0 0 24 16"
            aria-hidden="true"
            focusable="false"
        >
            <rect
                width="24"
                height="16"
                fill="#006233"
            />

            <path
                d="
                    M12 3.5
                    l1.05 3.24
                    h3.4
                    l-2.75 2
                    l1.05 3.24
                    l-2.75-2
                    l-2.75 2
                    l1.05-3.24
                    l-2.75-2
                    h3.4z
                "
                fill="none"
                stroke="#C1272D"
                stroke-width="0.9"
            />
        </svg>
    `
};


/* =========================================================
   URL DE BASE
   ========================================================= */

const I18N_BASE_URL = (() => {

    const script =
        document.currentScript;

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
   UTILITAIRE :
   TRADUCTION IMBRIQUÉE
   ========================================================= */

function getNestedTranslation(
    object,
    path
) {

    if (
        !object ||
        !path
    ) {
        return null;
    }

    return path
        .split('.')
        .reduce(
            (accumulator, key) =>
                accumulator?.[key],
            object
        ) ?? null;
}


/* =========================================================
   FETCH JSON
   ========================================================= */

function fetchJson(url) {

    return fetch(
        url,
        {
            cache: 'default'
        }
    )
    .then(response => {

        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status} for ${url}`
            );
        }

        return response.json();
    });
}


/* =========================================================
   COLLECTE DES SECTIONS UTILISÉES
   ========================================================= */

function collectI18nSections() {

    const sections =
        new Set();


    function addKey(key) {

        if (!key) {
            return;
        }

        const section =
            key
                .trim()
                .split('.')[0];

        if (section) {

            sections.add(
                section
            );
        }
    }


    /* -----------------------------------------------------
       data-i18n
       ----------------------------------------------------- */

    document
        .querySelectorAll(
            '[data-i18n]'
        )
        .forEach(element => {

            addKey(
                element.getAttribute(
                    'data-i18n'
                )
            );
        });


    /* -----------------------------------------------------
       data-i18n-placeholder
       ----------------------------------------------------- */

    document
        .querySelectorAll(
            '[data-i18n-placeholder]'
        )
        .forEach(element => {

            addKey(
                element.getAttribute(
                    'data-i18n-placeholder'
                )
            );
        });


    /* -----------------------------------------------------
       data-i18n-attr
       ----------------------------------------------------- */

    document
        .querySelectorAll(
            '[data-i18n-attr]'
        )
        .forEach(element => {

            const rules =
                element.getAttribute(
                    'data-i18n-attr'
                ) || '';


            rules
                .split(',')
                .forEach(rule => {

                    const parts =
                        rule.split(':');

                    const key =
                        parts
                            .slice(1)
                            .join(':')
                            .trim();

                    addKey(key);
                });
        });


    return sections;
}


/* =========================================================
   MISE À JOUR DU DOM
   ========================================================= */

function updateLanguageDOM(
    langData
) {

    currentTranslations =
        langData || {};


    /* =====================================================
       1. TEXT CONTENT
       ===================================================== */

    document
        .querySelectorAll(
            '[data-i18n]'
        )
        .forEach(element => {

            const key =
                element.getAttribute(
                    'data-i18n'
                );


            const value =
                getNestedTranslation(
                    langData,
                    key
                );


            if (
                value !== null &&
                value !== undefined
            ) {

                element.textContent =
                    value;
            }
        });


    /* =====================================================
       2. PLACEHOLDERS
       ===================================================== */

    document
        .querySelectorAll(
            '[data-i18n-placeholder]'
        )
        .forEach(element => {

            const key =
                element.getAttribute(
                    'data-i18n-placeholder'
                );


            const value =
                getNestedTranslation(
                    langData,
                    key
                );


            if (
                value !== null &&
                value !== undefined
            ) {

                element.placeholder =
                    value;
            }
        });


    /* =====================================================
       3. ATTRIBUTS
       ===================================================== */

    document
        .querySelectorAll(
            '[data-i18n-attr]'
        )
        .forEach(element => {

            const rules =
                element.getAttribute(
                    'data-i18n-attr'
                ) || '';


            rules
                .split(',')
                .forEach(rule => {

                    const parts =
                        rule.split(':');


                    const attrName =
                        parts[0]?.trim();


                    const key =
                        parts
                            .slice(1)
                            .join(':')
                            .trim();


                    if (
                        !attrName ||
                        !key
                    ) {
                        return;
                    }


                    const value =
                        getNestedTranslation(
                            langData,
                            key
                        );


                    if (
                        value !== null &&
                        value !== undefined
                    ) {

                        element.setAttribute(
                            attrName,
                            value
                        );
                    }
                });
        });
}


/* =========================================================
   SYNCHRONISER LE SÉLECTEUR DE LANGUE
   ========================================================= */

function syncLanguageSwitcherUI(
    lang
) {

    /* =====================================================
       1. LABEL DE LANGUE
       ===================================================== */

    const langLabel =
        document.getElementById(
            'current-lang-label'
        );


    if (langLabel) {

        langLabel.textContent =
            lang.toUpperCase();
    }


    /* =====================================================
       2. DRAPEAU DU BOUTON PRINCIPAL
       ===================================================== */

    const langButton =
        document.getElementById(
            'lang-menu-button'
        );


    if (
        langButton &&
        I18N_FLAG_SVGS[lang]
    ) {

        /*
         * PRIORITÉ 1 :
         * Conteneur dédié .lang-flag
         */

        const flagContainer =
            langButton.querySelector(
                '.lang-flag'
            );


        if (flagContainer) {

            flagContainer.innerHTML =
                I18N_FLAG_SVGS[lang];

        } else {

            /*
             * PRIORITÉ 2 :
             * Un SVG déjà présent dans le bouton
             */

            const existingSvg =
                langButton.querySelector(
                    'svg'
                );


            if (existingSvg) {

                existingSvg.outerHTML =
                    I18N_FLAG_SVGS[lang];

            } else {

                /*
                 * PRIORITÉ 3 :
                 * Aucun SVG :
                 * on crée automatiquement
                 * un conteneur dédié.
                 */

                const newFlagContainer =
                    document.createElement(
                        'span'
                    );


                newFlagContainer.className =
                    'lang-flag';


                newFlagContainer.innerHTML =
                    I18N_FLAG_SVGS[lang];


                langButton.insertBefore(
                    newFlagContainer,
                    langButton.firstChild
                );
            }
        }
    }


    /* =====================================================
       3. FERMER LE DROPDOWN
       ===================================================== */

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


/* =========================================================
   CHARGEMENT LAZY + CACHE
   ========================================================= */

async function ensureLangData(
    lang,
    sections
) {

    const base =
        `${I18N_BASE_URL}translations/${lang}/`;


    /* -----------------------------------------------------
       Dictionnaire
       ----------------------------------------------------- */

    const dict =
        allTranslations[lang] ||
        (allTranslations[lang] = {});


    /* -----------------------------------------------------
       Tâches déjà lancées
       ----------------------------------------------------- */

    const tasks =
        pendingTasks[lang] ||
        (pendingTasks[lang] = {});


    /* =====================================================
       CHARGEUR DE FICHIER
       ===================================================== */

    const loadFile = (
        name,
        fileName,
        required = false
    ) => {

        const cacheKey =
            `${lang}:${name}`;


        if (!tasks[cacheKey]) {

            tasks[cacheKey] =
                fetchJson(
                    `${base}${fileName}`
                )
                .catch(error => {

                    if (required) {

                        throw error;
                    }


                    console.warn(
                        `[i18n] Échec du chargement : ${fileName}`,
                        error
                    );


                    return null;
                });
        }


        return tasks[cacheKey];
    };


    /* =====================================================
       CORE.JSON — OBLIGATOIRE
       ===================================================== */

    let coreData;


    try {

        coreData =
            await loadFile(
                'core',
                'core.json',
                true
            );

    } catch (error) {

        console.error(
            `[i18n] Impossible de charger core.json pour "${lang}".`,
            error
        );

        throw error;
    }


    if (
        !coreData ||
        typeof coreData !== 'object'
    ) {

        throw new Error(
            `[i18n] core.json invalide pour "${lang}".`
        );
    }


    Object.assign(
        dict,
        coreData
    );


    /* =====================================================
       SECTIONS SPÉCIFIQUES
       ===================================================== */

    const missingSections =
        Array
            .from(
                sections || []
            )
            .filter(
                name =>
                    !(name in dict)
            );


    if (
        missingSections.length
    ) {

        const loadedData =
            await Promise.all(
                missingSections.map(
                    name =>
                        loadFile(
                            name,
                            `${encodeURIComponent(name)}.json`,
                            false
                        )
                )
            );


        missingSections.forEach(
            (name, index) => {

                const data =
                    loadedData[index];


                if (
                    data &&
                    typeof data === 'object'
                ) {

                    dict[name] =
                        data;
                }
            }
        );
    }


    return dict;
}


/* =========================================================
   CHANGEMENT DE LANGUE
   ========================================================= */

async function loadLanguage(
    lang
) {

    /* -----------------------------------------------------
       Vérifier la langue
       ----------------------------------------------------- */

    if (
        !SUPPORTED_LANGS.includes(
            lang
        )
    ) {

        console.error(
            `[i18n] Langue non supportée : "${lang}"`
        );

        return;
    }


    /* -----------------------------------------------------
       Fermer le menu immédiatement
       ----------------------------------------------------- */

    document
        .getElementById(
            'lang-menu-dropdown'
        )
        ?.classList.add(
            'hidden'
        );


    try {

        /* -------------------------------------------------
           Détecter les sections
           ------------------------------------------------- */

        const sections =
            collectI18nSections();


        /* -------------------------------------------------
           Charger les données
           ------------------------------------------------- */

        const dict =
            await ensureLangData(
                lang,
                sections
            );


        if (
            !dict ||
            typeof dict !== 'object'
        ) {

            throw new Error(
                `Données de traduction invalides pour "${lang}".`
            );
        }


        /* -------------------------------------------------
           Langue actuelle
           ------------------------------------------------- */

        currentLang =
            lang;


        /* -------------------------------------------------
           Direction
           ------------------------------------------------- */

        document.documentElement.dir =
            lang === 'ar'
                ? 'rtl'
                : 'ltr';


        /* -------------------------------------------------
           Attribut lang
           ------------------------------------------------- */

        document.documentElement.lang =
            lang;


        /* -------------------------------------------------
           Sauvegarder
           ------------------------------------------------- */

        localStorage.setItem(
            'preferred_lang',
            lang
        );


        /* -------------------------------------------------
           Appliquer les traductions
           ------------------------------------------------- */

        updateLanguageDOM(
            dict
        );


        /* -------------------------------------------------
           Synchroniser le bouton
           ------------------------------------------------- */

        syncLanguageSwitcherUI(
            lang
        );


        /* -------------------------------------------------
           Événement global
           ------------------------------------------------- */

        window.dispatchEvent(
            new CustomEvent(
                'languageChanged',
                {
                    detail: {
                        lang,
                        translations: dict
                    }
                }
            )
        );


    } catch (error) {

        console.error(
            `[i18n] Erreur lors du chargement de la langue "${lang}":`,
            error
        );
    }
}


/* =========================================================
   API PUBLIQUE
   ========================================================= */

window.i18n = {

    /* -----------------------------------------------------
       Changement de langue
       ----------------------------------------------------- */

    changeLanguage:
        loadLanguage,

    switchLanguage:
        loadLanguage,


    /* -----------------------------------------------------
       Charger des sections supplémentaires
       ----------------------------------------------------- */

    ensureSections:
        async function(names) {

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
        },


    /* -----------------------------------------------------
       Récupérer une traduction
       ----------------------------------------------------- */

    getTranslation:
        function(path) {

            return getNestedTranslation(
                currentTranslations,
                path
            );
        },


    /* -----------------------------------------------------
       Label photo
       ----------------------------------------------------- */

    getPhotoLabel:
        function(n) {

            const commonPhoto =
                getNestedTranslation(
                    currentTranslations,
                    'common.photo'
                );


            const placesPhoto =
                getNestedTranslation(
                    currentTranslations,
                    'places.common.photo'
                );


            const template =
                commonPhoto ||
                placesPhoto;


            if (
                typeof template ===
                'string'
            ) {

                return template.replace(
                    '{n}',
                    String(n)
                );
            }


            return `Photo ${n}`;
        }
};


/* =========================================================
   ALIASES GLOBAUX
   ========================================================= */

window.changeLanguage =
    window.i18n.changeLanguage;

window.switchLanguage =
    window.i18n.switchLanguage;

window.i18nEnsureSections =
    window.i18n.ensureSections;

window.i18nPhotoLabel =
    window.i18n.getPhotoLabel;


/* =========================================================
   INITIALISATION
   ========================================================= */

document.addEventListener(
    'DOMContentLoaded',
    () => {

        /* -------------------------------------------------
           Langue sauvegardée
           ------------------------------------------------- */

        const savedLang =
            localStorage.getItem(
                'preferred_lang'
            );


        const initialLang =
            SUPPORTED_LANGS.includes(
                savedLang
            )
                ? savedLang
                : DEFAULT_LANG;


        /* -------------------------------------------------
           Charger la langue initiale
           ------------------------------------------------- */

        loadLanguage(
            initialLang
        );


        /* -------------------------------------------------
           Délégation des boutons
           ------------------------------------------------- */

        document.addEventListener(
            'click',
            event => {

                const langButton =
                    event.target.closest(
                        '[data-lang]'
                    );


                if (!langButton) {
                    return;
                }


                event.preventDefault();


                const selectedLang =
                    langButton.getAttribute(
                        'data-lang'
                    );


                if (
                    !selectedLang ||
                    !SUPPORTED_LANGS.includes(
                        selectedLang
                    )
                ) {

                    return;
                }


                /* -------------------------------------------------
                   Éviter un rechargement inutile
                   ------------------------------------------------- */

                if (
                    selectedLang ===
                    currentLang
                ) {

                    document
                        .getElementById(
                            'lang-menu-dropdown'
                        )
                        ?.classList.add(
                            'hidden'
                        );

                    return;
                }


                loadLanguage(
                    selectedLang
                );
            }
        );
    }
);


/* =========================================================
   FIN DU I18N ENGINE
   ========================================================= */
