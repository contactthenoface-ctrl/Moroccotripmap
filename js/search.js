// --- Données globales du site (Villes, Hôtels, Riads, Restaurants, Activités) ---
const searchData = [
    // --- 1. VILLES / DESTINATIONS ---
    { name: "Marrakech", arabicName: "مراكش", type: "Ville", url: "marrakech.html", tags: ["marrakech", "medina", "palaces", "desert", "imperial", "riad", "مراكش", "مدينة"] },
    { name: "Chefchaouen", arabicName: "شفشاون", type: "Ville", url: "chefchaouen.html", tags: ["chefchaouen", "blue pearl", "rif", "mountains", "bleu", "شفشاون", "المدينة الزرقاء"] },
    { name: "Fes", arabicName: "فاس", type: "Ville", url: "fes.html", tags: ["fes", "fès", "medina", "cultural", "spiritual", "فاس"] },
    { name: "Casablanca", arabicName: "الدار البيضاء", type: "Ville", url: "casablanca.html", tags: ["casablanca", "economic", "largest city", "mosque", "الدار البيضاء", "كازا"] },
    { name: "Essaouira", arabicName: "الصويرة", type: "Ville", url: "essaouira.html", tags: ["essaouira", "coast", "windy", "seafood", "beach", "الصويرة"] },
    { name: "Agadir", arabicName: "أكادير", type: "Ville", url: "agadir.html", tags: ["agadir", "beach", "resort", "sun", "ocean", "أكادير"] },
    { name: "Tangier", arabicName: "طنجة", type: "Ville", url: "tanger.html", tags: ["tangier", "tanger", "strait", "gateway", "north", "طنجة"] },
    { name: "Ouarzazate", arabicName: "ورزازات", type: "Ville", url: "ouarzazate.html", tags: ["ouarzazate", "desert", "kasbah", "cinematic", "sahara", "ورزازات"] },
    { name: "Rabat", arabicName: "الرباط", type: "Ville", url: "rabat.html", tags: ["rabat", "capital", "imperial", "gardens", "الرباط"] },
    { name: "Meknes", arabicName: "مكناس", type: "Ville", url: "meknes.html", tags: ["meknes", "imperial", "gates", "roman", "volubilis", "مكناس"] },
    { name: "Tetouan", arabicName: "تطوان", type: "Ville", url: "tetouan.html", tags: ["tetouan", "mediterranean", "andalusian", "rif", "تطوان"] },
    { name: "Ifrane", arabicName: "إفران", type: "Ville", url: "ifrane.html", tags: ["ifrane", "atlas", "alpine", "snow", "cedar", "إفران"] },
    { name: "El Jadida", arabicName: "الجديدة", type: "Ville", url: "el-jadida.html", tags: ["el jadida", "jadida", "portuguese", "fort", "الجديدة"] },
    { name: "Taroudant", arabicName: "تارودانت", type: "Ville", url: "taroudant.html", tags: ["taroudant", "souss", "ramparts", "souks", "تارودانت"] },
    { name: "Dakhla", arabicName: "الداخلة", type: "Ville", url: "dakhla.html", tags: ["dakhla", "lagoon", "kitesurf", "south", "sahara", "الداخلة"] },
    { name: "Al Hoceima", arabicName: "الحسيمة", type: "Ville", url: "al-hoceima.html", tags: ["al hoceima", "hoceima", "turquoise", "mediterranean", "beach", "الحسيمة"] },
    { name: "Nador", arabicName: "الناظور", type: "Ville", url: "nador.html", tags: ["nador", "mar chica", "lagoon", "mediterranean", "الناظور"] },
    { name: "Zagora", arabicName: "زاكورة", type: "Ville", url: "zagora.html", tags: ["zagora", "draa valley", "palm", "desert", "زاكورة"] },
    { name: "Safi", arabicName: "آسفي", type: "Ville", url: "safi.html", tags: ["safi", "pottery", "coast", "fortress", "آسفي"] },
    { name: "Laayoune", arabicName: "العيون", type: "Ville", url: "laayoune.html", tags: ["laayoune", "sahara", "atlantic", "sahrawi", "العيون"] },
    { name: "Merzouga", arabicName: "مرزوكة", type: "Ville", url: "merzouga.html", tags: ["merzouga", "desert", "dunes", "sahara", "erg chebbi", "camp", "مرزوكة"] },
    { name: "Azilal", arabicName: "أزيلال", type: "Ville", url: "azilal.html", tags: ["azilal", "ouzoud", "waterfalls", "atlas", "أزيلال"] },
    { name: "Tinghir", arabicName: "تنغير", type: "Ville", url: "tinghir.html", tags: ["tinghir", "todra", "gorge", "canyon", "oasis", "تنغير"] },
    { name: "Oujda", arabicName: "وجدة", type: "Ville", url: "oujda.html", tags: ["oujda", "saidia", "east", "mediterranean", "وجدة", "السعيدية"] },
    { name: "Asilah", arabicName: "أصيلة", type: "Ville", url: "asilah.html", tags: ["asilah", "white medina", "murals", "atlantic", "أصيلة"] },
    { name: "Erfoud", arabicName: "أرفود", type: "Ville", url: "erfoud.html", tags: ["erfoud", "fossils", "dates", "merzouga gateway", "أرفود"] },

    // --- 2. LIEUX PHARES & MONUMENTS ---
    { name: "Koutoubia Mosque", arabicName: "جامع الكتبية", type: "Monument", url: "places/marrakech-places/koutoubia.html", tags: ["koutoubia", "mosque", "minaret", "marrakech", "كتبية"] },
    { name: "Ben Youssef Madrasa", arabicName: "مدرسة بن يوسف", type: "Monument", url: "places/marrakech-places/medersa-ben-youssef.html", tags: ["ben youssef", "madrasa", "islamic", "marrakech", "مدرسة بن يوسف"] },
    { name: "Bahia Palace", arabicName: "قصر الباهية", type: "Monument", url: "places/marrakech-places/palais-bahia.html", tags: ["bahia", "palace", "marrakech", "architecture", "الباهية"] },
    { name: "El Badi Palace", arabicName: "قصر البديع", type: "Monument", url: "places/marrakech-places/palais-el-badi.html", tags: ["el badi", "ruins", "marrakech", "البديع"] },
    { name: "Saadian Tombs", arabicName: "القبور السعدية", type: "Monument", url: "places/marrakech-places/tombeaux-saadiens.html", tags: ["saadian", "tombs", "mausoleum", "marrakech", "القبور السعدية"] },
    { name: "Jardin Majorelle", arabicName: "حديقة ماجوريل", type: "Jardin", url: "places/marrakech-places/jardin-majorelle.html", tags: ["majorelle", "garden", "ysl", "marrakech", "ماجوريل"] },
    { name: "Jemaa el-Fnaa", arabicName: "جامع الفنا", type: "Place", url: "places/marrakech-places/jemaa-el-fnaa.html", tags: ["jemaa el fnaa", "square", "marrakech", "souks", "جامع الفنا"] },
    { name: "Dar El Bacha Museum", arabicName: "دار الباشا", type: "Musée", url: "places/marrakech-places/el-bacha-museum.html", tags: ["dar el bacha", "coffee", "museum", "marrakech", "دار الباشا"] },

    // --- 3. HÔTELS, RIADS & SÉJOURS ---
    { name: "Royal Mansour Marrakech", arabicName: "رويال منصور", type: "Riad & Hôtel", url: "marrakech.html", tags: ["royal mansour", "luxury", "riad", "hotel", "marrakech", "رويال منصور"] },
    { name: "La Mamounia", arabicName: "المامونية", type: "Hôtel de Luxe", url: "marrakech.html", tags: ["la mamounia", "hotel", "palace", "marrakech", "المامونية"] },
    { name: "Riad Yasmine", arabicName: "رياض ياسمين", type: "Riad", url: "marrakech.html", tags: ["riad yasmine", "pool", "riad", "marrakech", "رياض ياسمين"] },
    { name: "Dar Ahlam Ouarzazate", arabicName: "دار أحلام", type: "Hôtel de Charme", url: "ouarzazate.html", tags: ["dar ahlam", "ouarzazate", "hotel", "oasis", "دار أحلام"] },
    { name: "L'Heure Bleue Essaouira", arabicName: "الساعة الزرقاء", type: "Riad", url: "essaouira.html", tags: ["heure bleue", "essaouira", "hotel", "riad"] },

    // --- 4. GASTRONOMIE & RESTAURANTS ---
    { name: "Nomad Marrakech", arabicName: "نوماد", type: "Restaurant", url: "marrakech.html", tags: ["nomad", "restaurant", "rooftop", "marrakech", "نوماد"] },
    { name: "Le Jardin Marrakech", arabicName: "لجاردان", type: "Restaurant", url: "marrakech.html", tags: ["le jardin", "restaurant", "marrakech", "cafe"] },
    { name: "Café Clock Fes & Marrakech", arabicName: "كافيه كلوك", type: "Café Culturel", url: "fes.html", tags: ["cafe clock", "camel burger", "fes", "marrakech", "كافيه كلوك"] }
];

// --- Logique de recherche globale ---
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const resultsContainer = document.getElementById('searchResults');
    const cityCards = document.querySelectorAll('.city-card');

    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const input = e.target.value.toLowerCase().trim();
            resultsContainer.innerHTML = '';
            
            if (input.length < 1) {
                resultsContainer.style.display = 'none';
                cityCards.forEach(card => card.style.display = 'block');
                return;
            }

            const filtered = searchData.filter(item => 
                item.name.toLowerCase().includes(input) || 
                (item.arabicName && item.arabicName.includes(input)) ||
                item.tags.some(tag => tag.toLowerCase().includes(input))
            );

            if (filtered.length > 0) {
                filtered.forEach(item => {
                    const link = document.createElement('a');
                    link.href = item.url;
                    link.className = "block px-4 py-3 hover:bg-creme hover:text-vert transition border-b border-gray-100 last:border-none flex justify-between items-center";
                    
                    const typeBadge = item.type ? `<span class="text-[10px] font-bold bg-sable/20 text-sable px-2 py-0.5 rounded uppercase">${item.type}</span>` : '';
                    
                    link.innerHTML = `
                        <div>
                            <span class="font-semibold text-vert">${item.name}</span>
                            ${item.arabicName ? `<span class="text-xs text-gray-400 ml-2">(${item.arabicName})</span>` : ''}
                        </div>
                        <div class="flex items-center gap-2">
                            ${typeBadge}
                            <span class="text-xs text-gray-400">🔗</span>
                        </div>
                    `;
                    resultsContainer.appendChild(link);
                });
                resultsContainer.style.display = 'block';
            } else {
                resultsContainer.style.display = 'none';
            }

            if (cityCards.length > 0) {
                cityCards.forEach(card => {
                    const cardText = card.innerText.toLowerCase();
                    const isMatch = filtered.some(item => cardText.includes(item.name.toLowerCase())) || cardText.includes(input);
                    
                    if (isMatch) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
        });
    }

    document.addEventListener('click', function(e) {
        if (searchInput && resultsContainer && !searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.style.display = 'none';
        }
    });
});
