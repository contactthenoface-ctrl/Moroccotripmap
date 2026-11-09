with open("tanger.html", "r", encoding="utf-8") as f:
    html = f.read()

# On cherche où commence l ancienne section d hébergement ou les filtres pour les remplacer proprement
start_marker = '<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">'
end_marker = '<!-- Where to Eat Section'

# Nouveau contenu propre pour les hébergements et la bannière Booking
new_section = '''<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            
            <!-- Section Header -->
            <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
                <div>
                    <span class="text-xs font-bold text-sable uppercase tracking-wider" data-i18n="tanger_page.stays.badge">Selection &amp; Advice</span>
                    <h2 class="text-3xl font-bold text-vert mt-1" data-i18n="tanger_page.stays.title">Where to stay in Tangier? Our Favorites</h2>
                </div>
                <p class="text-sm text-sombre/70 max-w-md" data-i18n="tanger_page.stays.subtitle">
                    Charming kasbah riads, strait-view hotels, and modern beachside stays: explore our top recommended addresses.
                </p>
            </div>

            <!-- Featured Highlights Grid (4 Handpicked Stays) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                
                <!-- Pick 1 -->
                <div class="bg-white rounded-2xl overflow-hidden border border-sable/10 shadow-sm hover:shadow-xl transition duration-300 flex flex-col group">
                    <div class="relative h-48 overflow-hidden">
                        <img src="images/tanger/hotel-skala-view.webp" alt="Hotel Skala Kasbah View" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
                        <span class="absolute top-3 left-3 bg-vert text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider" data-i18n="tanger_page.stays.card1.badge">
                            ★ Strait View Riad
                        </span>
                    </div>
                    <div class="p-5 flex flex-col flex-grow">
                        <h3 class="text-lg font-bold text-sombre" data-i18n="tanger_page.stays.card1.name">Hotel Skala Kasbah View</h3>
                        <p class="text-xs text-sombre/70 mt-2 flex-grow" data-i18n="tanger_page.stays.card1.desc">
                            Perched at the top of the historic Kasbah, offering breathtaking panoramas over the Strait of Gibraltar and the Spanish coast.
                        </p>
                        <div class="mt-4 pt-3 border-t border-sable/10 flex items-center justify-between">
                            <span class="text-xs font-bold text-vert" data-i18n="tanger_page.stays.card1.location">The Kasbah</span>
                            <a href="https://www.booking.com/searchresults.html?ss=Kasbah+Tangier" target="_blank" rel="noopener sponsored" class="text-xs font-bold text-sable hover:underline" data-i18n="tanger_page.stays.book">
                                Book →
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Pick 2 -->
                <div class="bg-white rounded-2xl overflow-hidden border border-sable/10 shadow-sm hover:shadow-xl transition duration-300 flex flex-col group">
                    <div class="relative h-48 overflow-hidden">
                        <img src="images/tanger/hotel-dar-medina.webp" alt="Dar Medina Tangier" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
                        <span class="absolute top-3 left-3 bg-sable text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider" data-i18n="tanger_page.stays.card2.badge">
                            ★ Authentic Riad
                        </span>
                    </div>
                    <div class="p-5 flex flex-col flex-grow">
                        <h3 class="text-lg font-bold text-sombre" data-i18n="tanger_page.stays.card2.name">Dar Medina Tangier</h3>
                        <p class="text-xs text-sombre/70 mt-2 flex-grow" data-i18n="tanger_page.stays.card2.desc">
                            A peaceful sanctuary in the white medina streets, featuring a lush patio courtyard and a panoramic rooftop terrace.
                        </p>
                        <div class="mt-4 pt-3 border-t border-sable/10 flex items-center justify-between">
                            <span class="text-xs font-bold text-vert" data-i18n="tanger_page.stays.card2.location">Medina</span>
                            <a href="https://www.booking.com/searchresults.html?ss=Dar+Medina+Tangier" target="_blank" rel="noopener sponsored" class="text-xs font-bold text-sable hover:underline" data-i18n="tanger_page.stays.book">
                                Book →
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Pick 3 -->
                <div class="bg-white rounded-2xl overflow-hidden border border-sable/10 shadow-sm hover:shadow-xl transition duration-300 flex flex-col group">
                    <div class="relative h-48 overflow-hidden">
                        <img src="images/tanger/hotel-atlas-bay.webp" alt="Hotel Atlas Bay Tangier" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
                        <span class="absolute top-3 left-3 bg-vert text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider" data-i18n="tanger_page.stays.card3.badge">
                            ★ Boutique Gem
                        </span>
                    </div>
                    <div class="p-5 flex flex-col flex-grow">
                        <h3 class="text-lg font-bold text-sombre" data-i18n="tanger_page.stays.card3.name">Hotel Atlas Bay Tangier</h3>
                        <p class="text-xs text-sombre/70 mt-2 flex-grow" data-i18n="tanger_page.stays.card3.desc">
                            Combines classic elegance with history, ideally located just steps away from the Grand Socco square and historic cafés.
                        </p>
                        <div class="mt-4 pt-3 border-t border-sable/10 flex items-center justify-between">
                            <span class="text-xs font-bold text-vert" data-i18n="tanger_page.stays.card3.location">Grand Socco</span>
                            <a href="https://www.booking.com/searchresults.html?ss=Grand+Socco+Tangier" target="_blank" rel="noopener sponsored" class="text-xs font-bold text-sable hover:underline" data-i18n="tanger_page.stays.book">
                                Book →
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Pick 4 -->
                <div class="bg-white rounded-2xl overflow-hidden border border-sable/10 shadow-sm hover:shadow-xl transition duration-300 flex flex-col group">
                    <div class="relative h-48 overflow-hidden">
                        <img src="images/tanger/hotel-corniche.webp" alt="Hotel Corniche Tangier" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
                        <span class="absolute top-3 left-3 bg-sombre text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider" data-i18n="tanger_page.stays.card4.badge">
                            ★ Beachfront Hotel
                        </span>
                    </div>
                    <div class="p-5 flex flex-col flex-grow">
                        <h3 class="text-lg font-bold text-sombre" data-i18n="tanger_page.stays.card4.name">Hotel Corniche Tangier</h3>
                        <p class="text-xs text-sombre/70 mt-2 flex-grow" data-i18n="tanger_page.stays.card4.desc">
                            Located right on Tangier Beach promenade, perfect for sea views, sand walks, and easy access to nightlife.
                        </p>
                        <div class="mt-4 pt-3 border-t border-sable/10 flex items-center justify-between">
                            <span class="text-xs font-bold text-vert" data-i18n="tanger_page.stays.card4.location">Corniche / Beach</span>
                            <a href="https://www.booking.com/searchresults.html?ss=Corniche+Tangier" target="_blank" rel="noopener sponsored" class="text-xs font-bold text-sable hover:underline" data-i18n="tanger_page.stays.book">
                                Book →
                            </a>
                        </div>
                    </div>
                </div>

            </div>

            <!-- BOOKING REDIRECTION BANNER -->
            <div class="bg-gradient-to-br from-vert to-[#0e3823] text-creme rounded-3xl p-8 sm:p-10 shadow-lg relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-6">
                
                <div class="max-w-xl text-start z-10">
                    <span class="text-xs font-bold text-sable uppercase tracking-wider" data-i18n="tanger_page.booking_banner.badge">
                        Over 150+ Accommodations
                    </span>
                    <h3 class="text-2xl sm:text-3xl font-extrabold text-white mt-1 leading-tight" data-i18n="tanger_page.booking_banner.title">
                        Explore All Places to Stay in Tangier
                    </h3>
                    <p class="text-creme/80 mt-2 text-sm leading-relaxed" data-i18n="tanger_page.booking_banner.desc">
                        Compare real-time rates, read verified guest reviews, and discover more riads, apartments, and hotels on Booking.com.
                    </p>
                </div>

                <div class="w-full md:w-auto shrink-0 z-10 text-center">
                    <a href="https://www.booking.com/city/ma/tangier.html" 
                       target="_blank" 
                       rel="noopener sponsored" 
                       class="inline-flex items-center justify-center gap-3 w-full sm:w-auto bg-sable hover:bg-[#b08a52] text-sombre font-bold text-base px-7 py-3.5 rounded-2xl shadow-md transition duration-200 transform hover:-translate-y-0.5">
                       <span data-i18n="tanger_page.booking_banner.btn">View All Hotels on Booking.com</span>
                       <svg class="w-4 h-4 rtl:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                       </svg>
                    </a>
                    <p class="text-[11px] text-creme/60 mt-2" data-i18n="tanger_page.booking_banner.guarantee">✓ Best price guaranteed &amp; secure booking</p>
                </div>

                <div class="absolute -right-12 -bottom-12 w-56 h-56 bg-sable/10 rounded-full blur-2xl pointer-events-none"></div>
            </div>
        </section>

        <!-- Where to Eat Section'''

# Remplacement de l ancienne section dans le fichier
parts = html.split('<!-- ==========================================')
if len(parts) > 2:
    # On reconstruit en gardant le début et en insérant la nouvelle section avant les restaurants
    new_html = parts[0] + '<!-- ==========================================\n             ACCOMMODATION HYBRID SECTION: FEATURED PICKS + BOOKING BANNER\n             ========================================== -->\n        ' + new_section + '\n\n <!-- Where to Eat Section' + parts[2].split('<!-- Where to Eat Section')[1]
    with open("tanger.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Succès : tanger.html mis à jour !")
else:
    print("Erreur de repérage des balises dans tanger.html")
