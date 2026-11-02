#!/bin/bash

declare -A GUIDES

GUIDES["agadir-food-guide.html"]="
<article class=\"max-w-4xl mx-auto px-4 py-8\">
  <header class=\"mb-8\">
    <span class=\"text-sm font-semibold text-emerald-600 uppercase tracking-wider\">Guide Gastronomique</span>
    <h1 class=\"text-3xl sm:text-4xl font-bold text-gray-900 mt-2 mb-4\">Que Manger à Agadir ? Cuisine Soussia & Grillades du Port</h1>
    <p class=\"text-lg text-gray-600\">Entre poissons frais, huile d'argan, amlou et tajines du Souss, découvrez la richesse culinaire d'Agadir.</p>
  </header>
  <section class=\"space-y-6 text-gray-700 leading-relaxed\">
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">1. Grillades de Poisson au Port</h2>
    <p>Dégustez sardines, soles et merlans ultra-frais grillés sur place avec du pain frais, de la charmoula et une salade marocaine.</p>
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">2. Amlou & Pain Tafarnout</h2>
    <p>Le petit-déjeuner soussi incontournable : Amlou (amandes, huile d'argan et miel) étalé sur du pain Tafarnout chaud.</p>
  </section>
</article>"

GUIDES["marrakech-food-guide.html"]="
<article class=\"max-w-4xl mx-auto px-4 py-8\">
  <header class=\"mb-8\">
    <span class=\"text-sm font-semibold text-emerald-600 uppercase tracking-wider\">Guide Gastronomique</span>
    <h1 class=\"text-3xl sm:text-4xl font-bold text-gray-900 mt-2 mb-4\">Les Incontournables de la Cuisine Marrakchie : Tanjia & Jemaa El-Fna</h1>
    <p class=\"text-lg text-gray-600\">Plongez au cœur de la gastronomie de la Ville Rouge, de la mythique Tanjia Marrakchia aux stand de la place Jemaa El-Fna.</p>
  </header>
  <section class=\"space-y-6 text-gray-700 leading-relaxed\">
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">1. La Tanjia Marrakchia</h2>
    <p>Le plat emblématique préparé dans une jarre en terre cuite et confit lentement dans les cendres du dornier (le four du hammam).</p>
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">2. Méchoui au Souk Ahl El-Fassi</h2>
    <p>Agneau rôti à la vapeur puis doré au four sous terre, assaisonné simplement de sel et de cumin.</p>
  </section>
</article>"

GUIDES["fes-food-guide.html"]="
<article class=\"max-w-4xl mx-auto px-4 py-8\">
  <header class=\"mb-8\">
    <span class=\"text-sm font-semibold text-emerald-600 uppercase tracking-wider\">Guide Gastronomique</span>
    <h1 class=\"text-3xl sm:text-4xl font-bold text-gray-900 mt-2 mb-4\">Gastronomie Fassie : Pastilla, Khliâ & Saveurs de la Médina</h1>
    <p class=\"text-lg text-gray-600\">Fès est la capitale spirituelle et culinaire du Maroc. Découvrez la Pastilla impériale et les traditions sucrées-salées.</p>
  </header>
  <section class=\"space-y-6 text-gray-700 leading-relaxed\">
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">1. La Pastilla Fassie au Pigeon ou Poulet</h2>
    <p>L'excellence de la cuisine fassie : du feuilleté de warka garni de viande mijotée, d'amandes grillées, saupoudré de sucre glace et de cannelle.</p>
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">2. Le Khliâ (Viande Séchée)</h2>
    <p>Spécialité incontournable de Fès, la viande confite dans de la graisse et des épices, idéale servie avec des œufs au petit-déjeuner.</p>
  </section>
</article>"

GUIDES["rabat-food-guide.html"]="
<article class=\"max-w-4xl mx-auto px-4 py-8\">
  <header class=\"mb-8\">
    <span class=\"text-sm font-semibold text-emerald-600 uppercase tracking-wider\">Guide Gastronomique</span>
    <h1 class=\"text-3xl sm:text-4xl font-bold text-gray-900 mt-2 mb-4\">Spécialités de Rabat : Couscous aux Sept Légumes & Pâtisseries Raffinées</h1>
    <p class=\"text-lg text-gray-600\">Entre cuisine royale raffinée, tajines aux fruits secs et poisson de l'estuaire du Bouregreg.</p>
  </header>
  <section class=\"space-y-6 text-gray-700 leading-relaxed\">
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">1. Couscous Rwabi (Couscous de Rabat)</h2>
    <p>Un couscous délicat parfumé au smen, aux sept légumes de saison et à la tfaya (oignons confits et raisins secs).</p>
    <h2 class=\"text-2xl font-bold text-gray-800 border-b pb-2\">2. Cornes de Gazelle de la Médina</h2>
    <p>Les pâtisseries traditionnelles de Rabat se distinguent par leur finesse, à la pâte fine garnie de pure pâte d'amande à l'eau de fleur d'oranger.</p>
  </section>
</article>"

# Injecter le contenu dans les fichiers correspondants
for file in "${!GUIDES[@]}"; do
  filepath="blog/$file"
  if [ -f "$filepath" ]; then
    echo "Mise à jour de $filepath..."
    # Remplacement simple du bloc <main> s'il existe ou insertion
    sed -i "s|<main[^>]*>.*</main>|<main class=\"py-12 bg-gray-50\">${GUIDES[$file]}</main>|s" "$filepath" 2>/dev/null || echo "Structure à adapter pour $file"
  fi
done

echo "Mise à jour terminée !"
