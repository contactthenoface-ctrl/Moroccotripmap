/* =========================================================
   MOROCCO TRIP MAP — INTERNATIONALISATION
   =========================================================
   Structure :

   js/
   ├── i18n.js
   └── translations/
       ├── ar/
       │   ├── core.json
       │   ├── hero.json
       │   └── ...
       ├── en/
       │   ├── core.json
       │   ├── hero.json
       │   └── ...
       ├── es/
       │   ├── core.json
       │   ├── hero.json
       │   └── ...
       └── fr/
           ├── core.json
           ├── hero.json
           └── ...

   HTML :
   data-i18n="hero.title_line1"
   data-i18n="nav.destinations"
   data-i18n-placeholder="hero.search_placeholder"
   data-i18n-attr="aria-label:common.search"

   ========================================================= */

(() => {
    'use strict';

    /* =====================================================
       CONFIGURATION
       ===================================================== */

    const SUPPORTED_LANGS = ['fr', 'en', 'es', 'ar'];
    const DEFAULT_LANG = 'fr';

    const CORE_FILE = 'core.json';

    const STORAGE_KEY = 'preferredLanguage';

    /*
     * Détection automatique du dossier translations/
     * à partir de l'emplacement réel de i18n.js.
     */
    const SCRIPT_URL =
        document.currentScript?.src ||
        new URL('js/i18n.js', window.location.href).href;

    const I18N_BASE_URL =
        new URL('./translations/', SCRIPT_URL).href;


    /* =====================================================
       DRAPEAUX SVG
       ===================================================== */

    const I18N_FLAG_SVGS = {

        en: `
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 60 30"
                width="20"
                height="15"
                class="i18n-flag-svg rounded-sm shadow-sm"
                aria-hidden="true"
            >
                <clipPath id="i18n-en-s">
                    <path d="M0,0 v30 h60 v-30 z"/>
                </clipPath>

                <clipPath id="i18n-en-t">
                    <path d="M30,15 h30 v15 z v-15 h-30 z h-30 v-15 z v15 h30 z"/>
                </clipPath>

                <g clip-path="url(#i18n-en-s)">
                    <path
                        d="M0,0 v30 h60 v-30 z"
                        fill="#012169"
                    />

                    <path
                        d="M0,0 L60,30 M60,0 L0,30"
                        stroke="#fff"
                        stroke-width="6"
                    />

                    <path
                        d="M0,0 L60,30 M60,0 L0,30"
                        clip-path="url(#i18n-en-t)"
                        stroke="#C8102E"
                        stroke-width="4"
                    />

                    <path
                        d="M30,0 v30 M0,15 h60"
                        stroke="#fff"
                        stroke-width="10"
                    />

                    <path
                        d="M30,0 v30 M0,15 h60"
                        stroke="#C8102E"
                        stroke-width="6"
                    />
                </g>
            </svg>
        `,

        fr: `
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 3 2"
                width="20"
                height="15"
                class="i18n-flag-svg rounded-sm shadow-sm"
                aria-hidden="true"
            >
                <rect width="3" height="2" fill="#ED2939"/>
                <rect width="2" height="2" fill="#FFFFFF"/>
                <rect width="1" height="2" fill="#002395"/>
            </svg>
        `,

        es: `
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 750 500"
                width="20"
                height="15"
                class="i18n-flag-svg rounded-sm shadow-sm"
                aria-hidden="true"
            >
                <rect
                    width="750"
                    height="500"
                    fill="#C60B1E"
                />

                <rect
                    y="125"
                    width="750"
                    height="250"
                    fill="#FFC400"
                />
            </svg>
        `,

        ar: `
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 900 600"
                width="20"
                height="15"
                class="i18n-flag-svg rounded-sm shadow-sm"
                aria-hidden="true"
            >
                <rect
                    width="900"
                    height="600"
                    fill="#C1272D"
                />

                <polygon
                    fill="none"
                    stroke="#006233"
                    stroke-width="15"
                    points="450,170 361,441 593,273 307,273 639,441"
                />
            </svg>
        `
    };


    /* =====================================================
       CACHE
       ===================================================== */

    /*
     * allTranslations :
     *
     * {
     *   fr: {
     *      core: {...},
     *      hero: {...}
     *   },
     *   en: {...}
     * }
     */
    const allTranslations = {};

    /*
     * Évite de lancer plusieurs fetch simultanés
     * pour le même fichier.
     */
    const pendingTasks = {};


    let currentLang = DEFAULT_LANG;
    let currentTranslations = {};


    /* =====================================================
       OUTILS
       ===================================================== */

    function isSupportedLanguage(lang) {
        return SUPPORTED_LANGS.includes(lang);
    }


    function getSavedLanguage() {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);

            if (saved && isSupportedLanguage(saved)) {
                return saved;
            }
        } catch (error) {
            console.warn(
                '[i18n] Impossible de lire localStorage.',
                error
            );
        }

        return DEFAULT_LANG;
    }


    function getNestedTranslation(object, path) {

        if (!object || !path) {
            return undefined;
        }

        const parts = path.split('.');

        let value = object;

        for (const part of parts) {

            if (
                value === null ||
                value === undefined ||
                typeof value !== 'object' ||
                !(part in value)
            ) {
                return undefined;
            }

            value = value[part];
        }

        return value;
    }


    function fetchJson(url) {

        if (pendingTasks[url]) {
            return pendingTasks[url];
        }

        pendingTasks[url] = fetch(url, {
            cache: 'no-cache'
        })
            .then(response => {

                if (!response.ok) {
                    throw new Error(
                        `HTTP ${response.status} — ${url}`
                    );
                }

                return response.json();
            })
            .finally(() => {
                delete pendingTasks[url];
            });

        return pendingTasks[url];
    }


    /* =====================================================
       DÉTECTION DES SECTIONS NÉCESSAIRES
       ===================================================== */

    function collectI18nSections() {

        const sections = new Set();

        /*
         * data-i18n
         */
        document.querySelectorAll('[data-i18n]').forEach(element => {

            const key = element.getAttribute('data-i18n');

            if (!key) {
                return;
            }

            const firstPart = key.split('.')[0];

            if (firstPart) {
                sections.add(firstPart);
            }
        });


        /*
         * data-i18n-placeholder
         */
        document
            .querySelectorAll('[data-i18n-placeholder]')
            .forEach(element => {

                const key =
                    element.getAttribute('data-i18n-placeholder');

                if (!key) {
                    return;
                }

                const firstPart = key.split('.')[0];

                if (firstPart) {
                    sections.add(firstPart);
                }
            });


        /*
         * data-i18n-attr
         *
         * Exemple :
         *
         * data-i18n-attr="aria-label:common.search"
         */
        document
            .querySelectorAll('[data-i18n-attr]')
            .forEach(element => {

                const rules =
                    element.getAttribute('data-i18n-attr');

                if (!rules) {
                    return;
                }

                rules
                    .split(';')
                    .forEach(rule => {

                        const parts = rule.split(':');

                        if (parts.length < 2) {
                            return;
                        }

                        const key =
                            parts.slice(1).join(':').trim();

                        if (!key) {
                            return;
                        }

                        const firstPart = key.split('.')[0];

                        if (firstPart) {
                            sections.add(firstPart);
                        }
                    });
            });


        return [...sections];
    }


    /* =====================================================
       CHARGEMENT D'UNE SECTION
       ===================================================== */

    async function loadSection(lang, section) {

        if (!isSupportedLanguage(lang)) {
            throw new Error(
                `[i18n] Langue non supportée : ${lang}`
            );
        }

        if (!section) {
            return {};
        }


        if (!allTranslations[lang]) {
            allTranslations[lang] = {};
        }


        /*
         * Déjà chargée
         */
        if (
            Object.prototype.hasOwnProperty.call(
                allTranslations[lang],
                section
            )
        ) {
            return allTranslations[lang][section];
        }


        const url =
            `${I18N_BASE_URL}${lang}/${section}.json`;


        try {

            const data = await fetchJson(url);

            allTranslations[lang][section] = data;

            return data;

        } catch (error) {

            console.error(
                `[i18n] Impossible de charger ${lang}/${section}.json`,
                error
            );

            throw error;
        }
    }


    /* =====================================================
       CHARGEMENT DES DONNÉES D'UNE LANGUE
       ===================================================== */

    async function ensureLangData(lang, sections = []) {

        if (!isSupportedLanguage(lang)) {
            lang = DEFAULT_LANG;
        }


        if (!allTranslations[lang]) {
            allTranslations[lang] = {};
        }


        /*
         * CORE = OBLIGATOIRE
         */
        await loadSection(lang, 'core');


        /*
         * Sections nécessaires à la page
         */
        const uniqueSections = [
            ...new Set(
                sections.filter(
                    section =>
                        section &&
                        section !== 'core'
                )
            )
        ];


        if (uniqueSections.length > 0) {

            await Promise.all(
                uniqueSections.map(
                    section =>
                        loadSection(lang, section)
                )
            );
        }


        /*
         * Fusion virtuelle des fichiers.
         *
         * On ne modifie pas les fichiers JSON.
         */
        currentTranslations = {};

        for (
            const sectionName of Object.keys(
                allTranslations[lang]
            )
        ) {

            Object.assign(
                currentTranslations,
                allTranslations[lang][sectionName]
            );
        }


        return currentTranslations;
    }


    /* =====================================================
       OBTENIR UNE TRADUCTION
       ===================================================== */

    function translate(key, lang = currentLang) {

        if (!key) {
            return '';
        }


        /*
         * Exemple :
         *
         * hero.title_line1
         *
         * section = hero
         * path = title_line1
         */
        const parts = key.split('.');

        const section = parts.shift();

        const path = parts.join('.');


        const sectionData =
            allTranslations[lang]?.[section];


        if (!sectionData) {
            return undefined;
        }


        return path
            ? getNestedTranslation(sectionData, path)
            : sectionData;
    }


    /* =====================================================
       MISE À JOUR DU DOM
       ===================================================== */

    function updateLanguageDOM(lang) {

        /*
         * -----------------------------------------------
         * data-i18n
         * -----------------------------------------------
         */
        document
            .querySelectorAll('[data-i18n]')
            .forEach(element => {

                const key =
                    element.getAttribute('data-i18n');

                if (!key) {
                    return;
                }


                const value =
                    translate(key, lang);


                if (
                    value === undefined ||
                    value === null
                ) {
                    return;
                }


                /*
                 * HTML explicite
                 */
                if (
                    element.hasAttribute(
                        'data-i18n-html'
                    )
                ) {
                    element.innerHTML = String(value);

                } else {
                    element.textContent = String(value);
                }
            });


        /*
         * -----------------------------------------------
         * data-i18n-placeholder
         * -----------------------------------------------
         */
        document
            .querySelectorAll(
                '[data-i18n-placeholder]'
            )
            .forEach(element => {

                const key =
                    element.getAttribute(
                        'data-i18n-placeholder'
                    );

                if (!key) {
                    return;
                }


                const value =
                    translate(key, lang);


                if (
                    value === undefined ||
                    value === null
                ) {
                    return;
                }


                element.setAttribute(
                    'placeholder',
                    String(value)
                );
            });


        /*
         * -----------------------------------------------
         * data-i18n-attr
         *
         * Exemple :
         *
         * data-i18n-attr="
         * aria-label:common.search;
         * title:common.search
         * "
         * -----------------------------------------------
         */
        document
            .querySelectorAll('[data-i18n-attr]')
            .forEach(element => {

                const rules =
                    element.getAttribute(
                        'data-i18n-attr'
                    );

                if (!rules) {
                    return;
                }


                rules
                    .split(';')
                    .forEach(rule => {

                        const parts =
                            rule.split(':');


                        if (parts.length < 2) {
                            return;
                        }


                        const attrName =
                            parts.shift().trim();


                        const key =
                            parts.join(':').trim();


                        if (!attrName || !key) {
                            return;
                        }


                        const value =
                            translate(key, lang);


                        if (
                            value === undefined ||
                            value === null
                        ) {
                            return;
                        }


                        element.setAttribute(
                            attrName,
                            String(value)
                        );
                    });
            });


        /*
         * -----------------------------------------------
         * Direction RTL pour l'arabe
         * -----------------------------------------------
         */
        document.documentElement.lang = lang;

        document.documentElement.dir =
            lang === 'ar'
                ? 'rtl'
                : 'ltr';
    }


    /* =====================================================
       SÉLECTEUR DE LANGUE + DRAPEAUX
       ===================================================== */

    function syncLanguageSwitcherUI(lang) {

        /*
         * Code langue :
         *
         * FR
         * EN
         * ES
         * AR
         */
        const langLabel =
            document.getElementById(
                'current-lang-label'
            );


        if (langLabel) {

            langLabel.textContent =
                lang.toUpperCase();
        }


        /*
         * -----------------------------------------------
         * DRAPEAU DE LA LANGUE ACTUELLE
         *
         * Ton HTML possède déjà :
         *
         * <span id="current-flag">
         *
         * On modifie UNIQUEMENT son contenu.
         *
         * La flèche SVG du bouton reste intacte.
         * -----------------------------------------------
         */
        const currentFlag =
            document.getElementById(
                'current-flag'
            );


        if (
            currentFlag &&
            I18N_FLAG_SVGS[lang]
        ) {

            currentFlag.innerHTML =
                I18N_FLAG_SVGS[lang];
        }


        /*
         * -----------------------------------------------
         * Fermer le menu
         * -----------------------------------------------
         */
        const langDropdown =
            document.getElementById(
                'lang-menu-dropdown'
            );


        if (langDropdown) {

            langDropdown.classList.add(
                'hidden'
            );
        }


        /*
         * -----------------------------------------------
         * aria-expanded
         * -----------------------------------------------
         */
        const langButton =
            document.getElementById(
                'lang-menu-button'
            );


        if (langButton) {

            langButton.setAttribute(
                'aria-expanded',
                'false'
            );
        }
    }


    /* =====================================================
       CHANGEMENT DE LANGUE
       ===================================================== */

    async function loadLanguage(
        requestedLang,
        options = {}
    ) {

        let lang = requestedLang;


        if (!isSupportedLanguage(lang)) {
            lang = DEFAULT_LANG;
        }


        /*
         * Sections nécessaires à la page
         */
        const sections =
            options.sections ||
            collectI18nSections();


        try {

            /*
             * Charger les traductions
             */
            await ensureLangData(
                lang,
                sections
            );


            /*
             * Langue actuelle
             */
            currentLang = lang;


            /*
             * Sauvegarder
             */
            try {

                localStorage.setItem(
                    STORAGE_KEY,
                    lang
                );

            } catch (error) {

                console.warn(
                    '[i18n] Impossible de sauvegarder la langue.',
                    error
                );
            }


            /*
             * Mettre à jour HTML
             */
            updateLanguageDOM(lang);


            /*
             * Mettre à jour bouton + drapeau
             */
            syncLanguageSwitcherUI(lang);


            /*
             * Événement personnalisé
             *
             * Permet aux autres scripts du site
             * de réagir au changement de langue.
             */
            window.dispatchEvent(
                new CustomEvent(
                    'languageChanged',
                    {
                        detail: {
                            lang,
                            translations:
                                currentTranslations
                        }
                    }
                )
            );


            return currentTranslations;


        } catch (error) {

            console.error(
                `[i18n] Erreur lors du chargement de la langue "${lang}".`,
                error
            );


            /*
             * Si la langue demandée échoue,
             * on tente le français si ce n'est pas déjà
             * la langue demandée.
             */
            if (
                lang !== DEFAULT_LANG &&
                !options._fallbackAttempt
            ) {

                console.warn(
                    `[i18n] Retour automatique vers ${DEFAULT_LANG}.`
                );


                return loadLanguage(
                    DEFAULT_LANG,
                    {
                        ...options,
                        _fallbackAttempt: true
                    }
                );
            }


            throw error;
        }
    }


    /* =====================================================
       API PUBLIQUE
       ===================================================== */

    window.i18n = {

        /*
         * Langue actuelle
         */
        get currentLang() {
            return currentLang;
        },


        /*
         * Traduction
         */
        t(key, lang = currentLang) {
            return translate(key, lang);
        },


        /*
         * Changer de langue
         */
        changeLanguage(lang, options = {}) {
            return loadLanguage(
                lang,
                options
            );
        },


        /*
         * Charger des sections supplémentaires
         */
        ensureSections(
            sections,
            lang = currentLang
        ) {

            const list =
                Array.isArray(sections)
                    ? sections
                    : [sections];


            return ensureLangData(
                lang,
                list
            ).then(() => {

                /*
                 * Une fois les nouvelles sections
                 * chargées, on réapplique les traductions.
                 */
                updateLanguageDOM(lang);

                syncLanguageSwitcherUI(lang);

                return currentTranslations;
            });
        },


        /*
         * Accès aux traductions chargées
         */
        get translations() {
            return currentTranslations;
        },


        /*
         * Langues disponibles
         */
        get supportedLanguages() {
            return [...SUPPORTED_LANGS];
        }
    };


    /* =====================================================
       COMPATIBILITÉ AVEC L'ANCIEN CODE DU SITE
       ===================================================== */

    /*
     * Certains scripts/pages peuvent utiliser :
     *
     * changeLanguage('fr')
     */
    window.changeLanguage = function(lang) {

        return loadLanguage(lang);
    };


    /*
     * Certains boutons peuvent utiliser :
     *
     * switchLanguage('fr')
     */
    window.switchLanguage = function(lang) {

        return loadLanguage(lang);
    };


    /*
     * Alias pour charger des sections.
     */
    window.i18nEnsureSections =
        function(sections, lang) {

            return window.i18n.ensureSections(
                sections,
                lang
            );
        };


    /*
     * Alias éventuel utilisé par certains scripts
     * pour les labels de photos.
     */
    window.i18nPhotoLabel =
        function(key, lang = currentLang) {

            return translate(key, lang);
        };


    /* =====================================================
       INITIALISATION
       ===================================================== */

    async function initializeI18n() {

        const savedLang =
            getSavedLanguage();


        const sections =
            collectI18nSections();


        try {

            await loadLanguage(
                savedLang,
                {
                    sections
                }
            );

        } catch (error) {

            console.error(
                '[i18n] Échec de l’initialisation.',
                error
            );
        }
    }


    /* =====================================================
       DOM READY
       ===================================================== */

    if (
        document.readyState ===
        'loading'
    ) {

        document.addEventListener(
            'DOMContentLoaded',
            initializeI18n,
            {
                once: true
            }
        );

    } else {

        initializeI18n();
    }


    /* =====================================================
   GESTION DU MENU DE LANGUE
   ===================================================== */

document.addEventListener('click', function (event) {

    const langButton = event.target.closest('#lang-menu-button');

    /*
     * OUVERTURE / FERMETURE DU MENU
     */
    if (langButton) {

        event.preventDefault();
        event.stopPropagation();

        const dropdown =
            document.getElementById('lang-menu-dropdown');

        if (!dropdown) {
            return;
        }

        const isCurrentlyHidden =
            dropdown.classList.contains('hidden');

        dropdown.classList.toggle('hidden');

        langButton.setAttribute(
            'aria-expanded',
            isCurrentlyHidden ? 'true' : 'false'
        );

        return;
    }


    /*
     * CLIC SUR UNE LANGUE
     *
     * Compatible avec :
     *
     * onclick="switchLanguage('en')"
     * onclick="switchLanguage('fr')"
     * onclick="switchLanguage('es')"
     * onclick="switchLanguage('ar')"
     */
    const languageButton =
        event.target.closest(
            '#lang-menu-dropdown button'
        );

    if (languageButton) {

        const onclickValue =
            languageButton.getAttribute('onclick');

        if (onclickValue) {

            const match =
                onclickValue.match(
                    /switchLanguage\s*\(\s*['"]([^'"]+)['"]\s*\)/
                );

            if (match && match[1]) {

                event.preventDefault();
                event.stopPropagation();

                window.switchLanguage(match[1]);

                return;
            }
        }
    }


    /*
     * CLIC À L'EXTÉRIEUR DU MENU
     */
    const container =
        document.getElementById(
            'lang-menu-container'
        );

    if (
        container &&
        !container.contains(event.target)
    ) {

        const dropdown =
            document.getElementById(
                'lang-menu-dropdown'
            );

        const button =
            document.getElementById(
                'lang-menu-button'
            );

        if (dropdown) {
            dropdown.classList.add('hidden');
        }

        if (button) {
            button.setAttribute(
                'aria-expanded',
                'false'
            );
        }
    }

});
