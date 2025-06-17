
// ArtisanFind - Script principal
document.addEventListener('DOMContentLoaded', function() {
  // Données d'exemple d'artisans
  const artisans = [
    {
      id: 1,
      name: "Jean Dupont",
      job: "Plombier",
      rating: 4.8,
      reviewCount: 127,
      distance: "1.2 km",
      price: "50-80€/h",
      image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
      verified: true,
      available: true,
      specialties: ["Urgence", "Rénovation", "Installation"],
      phone: "06 12 34 56 78",
      description: "Plombier expérimenté avec 15 ans d'expérience. Interventions rapides et soignées.",
      location: "Paris 11ème",
      experience: "15 ans"
    },
    {
      id: 2,
      name: "Marie Martin",
      job: "Électricien",
      rating: 4.9,
      reviewCount: 89,
      distance: "2.1 km",
      price: "45-70€/h",
      image: "https://images.unsplash.com/photo-1494790108755-2616b332c108?w=150&h=150&fit=crop&crop=face",
      verified: true,
      available: false,
      specialties: ["Domotique", "Rénovation", "Tableau électrique"],
      phone: "06 98 76 54 32",
      description: "Électricienne certifiée, spécialisée dans les installations modernes et la domotique.",
      location: "Paris 12ème",
      experience: "12 ans"
    },
    {
      id: 3,
      name: "Pierre Lefebvre",
      job: "Menuisier",
      rating: 4.7,
      reviewCount: 156,
      distance: "3.5 km",
      price: "40-65€/h",
      image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
      verified: true,
      available: true,
      specialties: ["Sur mesure", "Restauration", "Agencement"],
      phone: "06 45 67 89 12",
      description: "Menuisier artisan passionné, créateur de meubles sur mesure et spécialiste en restauration.",
      location: "Vincennes",
      experience: "20 ans"
    },
    {
      id: 4,
      name: "Sophie Durand",
      job: "Peintre",
      rating: 4.6,
      reviewCount: 93,
      distance: "4.2 km",
      price: "35-55€/h",
      image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
      verified: true,
      available: true,
      specialties: ["Décoration", "Façade", "Enduits"],
      phone: "06 78 90 12 34",
      description: "Peintre décoratrice avec un œil artistique, spécialisée dans les finitions haut de gamme.",
      location: "Saint-Mandé",
      experience: "8 ans"
    },
    {
      id: 5,
      name: "Laurent Rousseau",
      job: "Chauffagiste",
      rating: 4.5,
      reviewCount: 76,
      distance: "5.1 km",
      price: "55-85€/h",
      image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&h=150&fit=crop&crop=face",
      verified: true,
      available: true,
      specialties: ["Pompe à chaleur", "Chaudière", "Climatisation"],
      phone: "06 23 45 67 89",
      description: "Chauffagiste expert en énergies renouvelables et systèmes de chauffage modernes.",
      location: "Montreuil",
      experience: "18 ans"
    },
    {
      id: 6,
      name: "Isabelle Moreau",
      job: "Serrurier",
      rating: 4.4,
      reviewCount: 112,
      distance: "2.8 km",
      price: "60-90€/h",
      image: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face",
      verified: true,
      available: true,
      specialties: ["Urgence", "Blindage", "Serrure connectée"],
      phone: "06 34 56 78 90",
      description: "Serrurier disponible 24h/24 pour toutes urgences et installations de sécurité.",
      location: "Paris 20ème",
      experience: "10 ans"
    }
  ];

  // Éléments DOM
  const jobSelect = document.getElementById('job-select');
  const locationInput = document.getElementById('location-input');
  const keywordInput = document.getElementById('keyword-input');
  const searchButton = document.getElementById('search-button');
  const artisansContainer = document.getElementById('artisans-container');
  const sortSelect = document.getElementById('sort-select');
  const artisanCountElement = document.getElementById('artisan-count');
  const noResultsElement = document.getElementById('no-results');
  const filterButton = document.getElementById('filter-button');

  // État de l'application
  let currentSearchQuery = '';
  let currentSelectedJob = '';
  let currentLocation = '';
  let currentSort = 'rating';
  let filteredArtisans = [...artisans];

  // Initialisation
  renderArtisans(artisans);
  updateArtisanCount(artisans.length);
  
  // Écouteurs d'événements
  searchButton.addEventListener('click', handleSearch);
  sortSelect.addEventListener('change', handleSort);
  filterButton.addEventListener('click', toggleFilters);
  
  // Recherche en temps réel
  keywordInput.addEventListener('input', debounce(handleLiveSearch, 300));
  jobSelect.addEventListener('change', handleLiveSearch);
  locationInput.addEventListener('input', debounce(handleLiveSearch, 500));

  // Gestion de la recherche
  function handleSearch() {
    currentSearchQuery = keywordInput.value.toLowerCase().trim();
    currentSelectedJob = jobSelect.value;
    currentLocation = locationInput.value.trim();

    console.log('Recherche:', { currentSearchQuery, currentSelectedJob, currentLocation });

    const filtered = filterArtisans(artisans);
    filteredArtisans = filtered;
    renderArtisans(filtered);
    updateArtisanCount(filtered.length);
    
    // Effet visuel de recherche
    searchButton.classList.add('animate-pulse');
    setTimeout(() => {
      searchButton.classList.remove('animate-pulse');
    }, 1000);
  }

  // Recherche en temps réel
  function handleLiveSearch() {
    currentSearchQuery = keywordInput.value.toLowerCase().trim();
    currentSelectedJob = jobSelect.value;
    currentLocation = locationInput.value.trim();

    const filtered = filterArtisans(artisans);
    filteredArtisans = filtered;
    renderArtisans(filtered);
    updateArtisanCount(filtered.length);
  }

  // Gestion du tri
  function handleSort() {
    currentSort = sortSelect.value;
    console.log('Tri par:', currentSort);
    
    const sorted = sortArtisans(filteredArtisans, currentSort);
    renderArtisans(sorted);
  }

  // Filtrage des artisans
  function filterArtisans(artisansList) {
    return artisansList.filter(artisan => {
      // Filtre par métier
      if (currentSelectedJob && artisan.job !== currentSelectedJob) {
        return false;
      }
      
      // Filtre par mots-clés
      if (currentSearchQuery) {
        const searchTerms = currentSearchQuery.split(' ').filter(term => term.length > 0);
        const searchableText = [
          artisan.name,
          artisan.job,
          artisan.description,
          artisan.location,
          ...artisan.specialties
        ].join(' ').toLowerCase();
        
        const matchesSearch = searchTerms.every(term => 
          searchableText.includes(term)
        );
        
        if (!matchesSearch) return false;
      }
      
      // Filtre par localisation (simulation)
      if (currentLocation) {
        const locationMatch = artisan.location.toLowerCase().includes(currentLocation.toLowerCase());
        if (!locationMatch) return false;
      }
      
      return true;
    });
  }

  // Tri des artisans
  function sortArtisans(artisansList, sortBy) {
    const sortedList = [...artisansList];
    
    switch (sortBy) {
      case 'rating':
        return sortedList.sort((a, b) => b.rating - a.rating);
      case 'distance':
        return sortedList.sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance));
      case 'price':
        return sortedList.sort((a, b) => parseInt(a.price) - parseInt(b.price));
      case 'reviews':
        return sortedList.sort((a, b) => b.reviewCount - a.reviewCount);
      default:
        return sortedList;
    }
  }

  // Rendu des artisans
  function renderArtisans(artisansList) {
    artisansContainer.innerHTML = '';
    
    if (artisansList.length === 0) {
      noResultsElement.classList.remove('hidden');
      noResultsElement.classList.add('fade-in');
    } else {
      noResultsElement.classList.add('hidden');
      
      artisansList.forEach((artisan, index) => {
        const artisanCard = createArtisanCard(artisan);
        artisanCard.style.animationDelay = `${index * 100}ms`;
        artisanCard.classList.add('fade-in');
        artisansContainer.appendChild(artisanCard);
      });
    }
  }

  // Création d'une carte d'artisan
  function createArtisanCard(artisan) {
    const card = document.createElement('div');
    card.className = 'artisan-card';
    
    const stars = renderStars(artisan.rating);
    
    const specialtiesBadges = artisan.specialties.slice(0, 2).map(specialty =>
      `<span class="badge">${specialty}</span>`
    ).join('');
    
    const moreBadge = artisan.specialties.length > 2 ? 
      `<span class="badge gray">+${artisan.specialties.length - 2}</span>` : '';

    card.innerHTML = `
      <div class="p-6">
        <div class="flex items-start space-x-4 mb-4">
          <div class="relative">
            <img
              src="${artisan.image}"
              alt="${artisan.name}"
              class="w-16 h-16 rounded-full object-cover"
              loading="lazy"
            />
            ${artisan.verified ? '<span class="icon-check-circle" title="Artisan vérifié"></span>' : ''}
          </div>
          
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-gray-900 truncate">
              ${artisan.name}
            </h3>
            <p class="text-blue-600 font-medium">${artisan.job}</p>
            <p class="text-sm text-gray-500">${artisan.location}</p>
            
            <div class="flex items-center space-x-2 mt-1">
              <div class="flex items-center">
                ${stars}
              </div>
              <span class="text-sm text-gray-600">
                ${artisan.rating} (${artisan.reviewCount} avis)
              </span>
            </div>
          </div>
        </div>

        <p class="text-gray-600 text-sm mb-4 line-clamp-2">
          ${artisan.description}
        </p>

        <div class="flex flex-wrap gap-1 mb-4">
          ${specialtiesBadges}
          ${moreBadge}
        </div>

        <div class="space-y-2 mb-4">
          <div class="flex items-center justify-between text-sm">
            <div class="flex items-center text-gray-600">
              <span class="icon-map-pin mr-1"></span>
              ${artisan.distance}
            </div>
            <div class="flex items-center text-gray-600">
              <span class="icon-clock"></span>
              ${artisan.available ? 
                '<span class="status-available">Disponible</span>' : 
                '<span class="status-busy">Occupé</span>'
              }
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500">${artisan.experience} d'expérience</span>
            <span class="text-lg font-semibold text-gray-900">${artisan.price}</span>
          </div>
        </div>

        <div class="flex space-x-2">
          <button 
            class="btn btn-outline flex-1"
            onclick="callArtisan('${artisan.phone}', '${artisan.name}')"
            title="Appeler ${artisan.name}"
          >
            <span class="icon-phone mr-1"></span>
            Appeler
          </button>
          <button 
            class="btn btn-primary flex-1"
            onclick="contactArtisan(${artisan.id}, '${artisan.name}')"
            title="Envoyer un message à ${artisan.name}"
          >
            Contacter
          </button>
        </div>
      </div>
    `;
    
    return card;
  }

  // Rendu des étoiles
  function renderStars(rating) {
    let starsHTML = '';
    for (let i = 0; i < 5; i++) {
      if (i < Math.floor(rating)) {
        starsHTML += '<span class="icon-star filled" title="' + rating + ' étoiles"></span>';
      } else if (i < rating) {
        starsHTML += '<span class="icon-star filled" style="opacity: 0.5" title="' + rating + ' étoiles"></span>';
      } else {
        starsHTML += '<span class="icon-star empty" title="' + rating + ' étoiles"></span>';
      }
    }
    return starsHTML;
  }

  // Mise à jour du compteur d'artisans
  function updateArtisanCount(count) {
    const locationText = currentLocation ? ` près de ${currentLocation}` : '';
    artisanCountElement.textContent = `${count} artisan${count > 1 ? 's' : ''} trouvé${count > 1 ? 's' : ''}${locationText}`;
  }

  // Gestion des filtres (fonctionnalité future)
  function toggleFilters() {
    alert('Fonctionnalité de filtres avancés à venir !');
    console.log('Toggle filters clicked');
  }

  // Fonction utilitaire de debounce
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Fonctions globales pour les boutons
  window.callArtisan = function(phone, name) {
    if (confirm(`Appeler ${name} au ${phone} ?`)) {
      window.location.href = `tel:${phone}`;
    }
  };

  window.contactArtisan = function(id, name) {
    alert(`Fonctionnalité de contact pour ${name} à venir !`);
    console.log('Contact artisan:', id, name);
  };

  // Gestion des erreurs d'images
  document.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
      e.target.src = 'https://via.placeholder.com/150x150/e5e7eb/9ca3af?text=Photo';
      e.target.alt = 'Photo non disponible';
    }
  }, true);

  // Analytics et suivi (simulation)
  function trackEvent(action, category, label) {
    console.log('Analytics:', { action, category, label });
  }

  // Suivi des interactions
  searchButton.addEventListener('click', () => {
    trackEvent('search', 'user_interaction', 'search_button');
  });

  sortSelect.addEventListener('change', () => {
    trackEvent('sort', 'user_interaction', sortSelect.value);
  });

  console.log('ArtisanFind initialisé avec succès !');
});