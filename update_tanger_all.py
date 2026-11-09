import json, os

# 1. Définition des traductions pour les 4 langues
translations = {
    "en": {
        "stays": {
            "badge": "Selection & Advice",
            "title": "Where to stay in Tangier? Our Favorites",
            "subtitle": "Charming kasbah riads, strait-view hotels, and modern beachside stays: explore our top recommended addresses.",
            "book": "Book →",
            "card1": {
                "badge": "★ Strait View Riad",
                "name": "Hotel Skala Kasbah View",
                "desc": "Perched at the top of the historic Kasbah, offering breathtaking panoramas over the Strait of Gibraltar and the Spanish coast.",
                "location": "The Kasbah"
            },
            "card2": {
                "badge": "★ Authentic Riad",
                "name": "Dar Medina Tangier",
                "desc": "A peaceful sanctuary in the white medina streets, featuring a lush patio courtyard and a panoramic rooftop terrace.",
                "location": "Medina"
            },
            "card3": {
                "badge": "★ Boutique Gem",
                "name": "Hotel Atlas Bay Tangier",
                "desc": "Combines classic elegance with history, ideally located just steps away from the Grand Socco square and historic cafés.",
                "location": "Grand Socco"
            },
            "card4": {
                "badge": "★ Beachfront Hotel",
                "name": "Hotel Corniche Tangier",
                "desc": "Located right on Tangier Beach promenade, perfect for sea views, sand walks, and easy access to nightlife.",
                "location": "Corniche / Beach"
            }
        },
        "booking_banner": {
            "badge": "Over 150+ Accommodations",
            "title": "Explore All Places to Stay in Tangier",
            "desc": "Compare real-time rates, read verified guest reviews, and discover more riads, apartments, and hotels on Booking.com.",
            "btn": "View All Hotels on Booking.com",
            "guarantee": "✓ Best price guaranteed & secure booking"
        },
        "eat": {
            "badge": "Food",
            "title": "Where to eat in Tangier",
            "subtitle": "Strait-view terraces, historic cafés and traditional medina grills.",
            "nomad": { "tag": "Seafood", "loc": "Marina", "title": "Marina tables", "desc": "Fish and seafood with harbour views." },
            "jardin": { "tag": "Café", "loc": "Beach", "title": "Beach cafés", "desc": "Casual drinks and snacks along the promenade." },
            "fassia": { "tag": "Hotel", "loc": "Corniche", "title": "Hotel restaurants", "desc": "Reliable options on the seafront strip." },
            "moha": { "tag": "Grill", "loc": "Medina", "title": "Simple grills", "desc": "Everyday Moroccan plates in the medina." },
            "bacha": { "tag": "Seafood", "loc": "Port", "title": "Port catch", "desc": "Fresh fish when the boats are in." },
            "elfenn": { "tag": "Local", "loc": "Centre", "title": "City centre", "desc": "Cafés and tagines away from the beach crowds." }
        }
    },
    "fr": {
        "stays": {
            "badge": "Sélection & Conseils",
            "title": "Où loger à Tanger ? Nos coups de cœur",
            "subtitle": "Riads de charme dans la kasbah, hôtels avec vue sur le détroit et séjours modernes en bord de mer : découvrez nos adresses recommandées.",
            "book": "Réserver →",
            "card1": {
                "badge": "★ Riad vue sur le détroit",
                "name": "Hotel Skala Kasbah View",
                "desc": "Perché au sommet de la kasbah historique, offrant des panoramas époustouflants sur le détroit de Gibraltar et la côte espagnole.",
                "location": "La Kasbah"
            },
            "card2": {
                "badge": "★ Riad authentique",
                "name": "Dar Medina Tangier",
                "desc": "Un sanctuaire paisible dans les rues blanches de la médina, doté d'une cour intérieure luxuriante et d'une terrasse panoramique.",
                "location": "Médina"
            },
            "card3": {
                "badge": "★ Bijou de charme",
                "name": "Hotel Atlas Bay Tangier",
                "desc": "Allie élégance classique et histoire, idéalement situé à quelques pas de la place du Grand Socco et des cafés historiques.",
                "location": "Grand Socco"
            },
            "card4": {
                "badge": "★ Hôtel en bord de mer",
                "name": "Hotel Corniche Tangier",
                "desc": "Situé directement sur la promenade de la plage de Tanger, idéal pour les vues sur la mer et les balades.",
                "location": "Corniche / Plage"
            }
        },
        "booking_banner": {
            "badge": "Plus de 150 hébergements",
            "title": "Explorer tous les hébergements à Tanger",
            "desc": "Comparez les tarifs en temps réel, lisez les avis vérifiés et découvrez d'autres riads, appartements et hôtels sur Booking.com.",
            "btn": "Voir tous les hôtels sur Booking.com",
            "guarantee": "✓ Meilleur prix garanti et réservation sécurisée"
        },
        "eat": {
            "badge": "Gastronomie",
            "title": "Où manger à Tanger",
            "subtitle": "Terrasses avec vue sur le détroit, cafés historiques et grills traditionnels de la médina.",
            "nomad": { "tag": "Fruits de mer", "loc": "Marina", "title": "Tables de la marina", "desc": "Poissons et fruits de mer avec vue sur le port." },
            "jardin": { "tag": "Café", "loc": "Plage", "title": "Cafés de plage", "desc": "Boissons et snacks décontractés le long de la promenade." },
            "fassia": { "tag": "Hôtel", "loc": "Corniche", "title": "Restaurants d'hôtels", "desc": "Options fiables sur le front de mer." },
            "moha": { "tag": "Grillades", "loc": "Médina", "title": "Grills simples", "desc": "Plats marocains du quotidien dans la médina." },
            "bacha": { "tag": "Fruits de mer", "loc": "Port", "title": "Pêche du port", "desc": "Poissons frais lorsque les bateaux rentrent." },
            "elfenn": { "tag": "Local", "loc": "Centre", "title": "Centre-ville", "desc": "Cafés et tajines à l'écart de la foule de la plage." }
        }
    },
    "es": {
        "stays": {
            "badge": "Selección y Consejos",
            "title": "¿Dónde alojarse en Tánger? Nuestros favoritos",
            "subtitle": "Encantadores riads en la kasbah, hoteles con vistas al estrecho y estancias modernas junto a la playa.",
            "book": "Reservar →",
            "card1": {
                "badge": "★ Riad vista al Estrecho",
                "name": "Hotel Skala Kasbah View",
                "desc": "Ubicado en lo alto de la histórica Kasbah, ofrece impresionantes vistas panorámicas sobre el Estrecho de Gibraltar.",
                "location": "La Kasbah"
            },
            "card2": {
                "badge": "★ Riad auténtico",
                "name": "Dar Medina Tangier",
                "desc": "Un refugio tranquilo en las calles de la medina blanca, con un patio interior y terraza panorámica.",
                "location": "Medina"
            },
            "card3": {
                "badge": "★ Hotel boutique",
                "name": "Hotel Atlas Bay Tangier",
                "desc": "Combina elegancia y tradición, situado a pocos pasos de la plaza del Gran Socco y cafés históricos.",
                "location": "Grand Socco"
            },
            "card4": {
                "badge": "★ Hotel en la playa",
                "name": "Hotel Corniche Tangier",
                "desc": "Situado directamente en el paseo marítimo de la playa de Tánger, ideal para disfrutar de vistas al mar.",
                "location": "Cornisa / Playa"
            }
        },
        "booking_banner": {
            "badge": "Más de 150 alojamientos",
            "title": "Explorar todos los alojamientos en Tánger",
            "desc": "Compara tarifas en tiempo real, lee opiniones de huéspedes y descubre más riads y hoteles en Booking.com.",
            "btn": "Ver todos los hoteles en Booking.com",
            "guarantee": "✓ Mejor precio garantizado y reserva segura"
        },
        "eat": {
            "badge": "Gastronomía",
            "title": "Dónde comer en Tánger",
            "subtitle": "Terrazas con vistas al Estrecho, cafés históricos y parrillas tradicionales en la medina.",
            "nomad": { "tag": "Pescado", "loc": "Marina", "title": "Mesas del puerto", "desc": "Pescado y marisco con vistas al puerto." },
            "jardin": { "tag": "Café", "loc": "Playa", "title": "Cafés de playa", "desc": "Bebidas y aperitivos a lo largo del paseo marítimo." },
            "fassia": { "tag": "Hotel", "loc": "Cornisa", "title": "Restaurantes de hotel", "desc": "Opciones fiables en la franja marítima." },
            "moha": { "tag": "Parrilla", "loc": "Medina", "title": "Parrillas sencillas", "desc": "Platos marroquíes caseros en la medina." },
            "bacha": { "tag": "Pescado", "loc": "Puerto", "title": "Pesca del puerto", "desc": "Pescado fresco cuando los barcos regresan." },
            "elfenn": { "tag": "Local", "loc": "Centro", "title": "Centro ciudad", "desc": "Cafés y tajines lejos de las aglomeraciones de la playa." }
        }
    },
    "ar": {
        "stays": {
            "badge": "اختيارات ونصائح",
            "title": "أين تقيم في طنجة؟ الأفضل لدينا",
            "subtitle": "رياضات ساحرة في القصبة، وفنادق مطلة على المضيق، وإقامات عصرية على الشاطئ.",
            "book": "احجز ←",
            "card1": {
                "badge": "★ رياض مطل على المضيق",
                "name": "Hotel Skala Kasbah View",
                "desc": "يقع في أعلى القصبة التاريخية مع إطلالات بانورامية خلابة على مضيق جبل طارق والساحل الإسباني.",
                "location": "القصبة"
            },
            "card2": {
                "badge": "★ رياض أصيل",
                "name": "Dar Medina Tangier",
                "desc": "ملاذ هادئ في شوارع المدينة العتيقة البيضاء، يضم فناء داخلي وتراس للسطح.",
                "location": "المدينة العتيقة"
            },
            "card3": {
                "badge": "★ فندق بوتيكي مميز",
                "name": "Hotel Atlas Bay Tangier",
                "desc": "يجمع بين الأناقة الكلاسيكية والتاريخ، على بعد خطوة واحدة من ساحة الكران سوكو.",
                "location": "الكران سوكو"
            },
            "card4": {
                "badge": "★ فندق على الشاطئ",
                "name": "Hotel Corniche Tangier",
                "desc": "يقع مباشرة على كورنيش شاطئ طنجة، مثالي للاستمتاع بالإطلالات البحرية.",
                "location": "الكورنيش / الشاطئ"
            }
        },
        "booking_banner": {
            "badge": "أكثر من 150 مكان إقامة",
            "title": "استكشف جميع أماكن الإقامة في طنجة",
            "desc": "قارن الأسعار الفورية، واقرأ تقييمات الضيوف، واكتشف المزيد من الرياضات والفنادق عبر Booking.com.",
            "btn": "عرض جميع الفنادق على Booking.com",
            "guarantee": "✓ ضمان أفضل الأسعار والحجز الآمن"
        },
        "eat": {
            "badge": "المطاعم",
            "title": "أين تأكل في طنجة",
            "subtitle": "شرفات مطلة على المضيق، ومقاهي تاريخية، ومشاوي تقليدية في المدينة العتيقة.",
            "nomad": { "tag": "مأكولات بحرية", "loc": "المارينا", "title": "مطاعم المارينا", "desc": "أسماك ومأكولات بحرية مع إطلالات على الميناء." },
            "jardin": { "tag": "مقهى", "loc": "الشاطئ", "title": "مقاهي الشاطئ", "desc": "مشروبات ووجبات خفيفة على طول الكورنيش." },
            "fassia": { "tag": "فندق", "loc": "الكورنيش", "title": "مطاعم الفنادق", "desc": "خيارات ممتازة على واجهة البحر." },
            "moha": { "tag": "مشاوي", "loc": "المدينة", "title": "مشاوي بسيطة", "desc": "أطباق مغربية يومية في المدينة العتيقة." },
            "bacha": { "tag": "مأكولات بحرية", "loc": "الميناء", "title": "صيد الميناء", "desc": "أسماك طازجة عندما عودة القوارب." },
            "elfenn": { "tag": "محلي", "loc": "المركز", "title": "وسط المدينة", "desc": "مقاهي وطواجن بعيداً عن زحام الشاطئ." }
        }
    }
}

# 2. Mise à jour des fichiers JSON
for lang, data in translations.items():
    json_path = f"js/translations/{lang}/tanger_page.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        content["stays"] = data["stays"]
        content["booking_banner"] = data["booking_banner"]
        content["eat"] = data["eat"]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        print(f"Mise à jour réussie : {json_path}")
    else:
        print(f"Fichier non trouvé : {json_path}")

print("Toutes les traductions ont été mises à jour avec succès !")
