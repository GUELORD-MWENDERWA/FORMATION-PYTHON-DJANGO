document.addEventListener("DOMContentLoaded", () => {
  
  // ==========================================
  // 1. CARROUSEL DE FOND (HERO) AVEC PAUSE
  // ==========================================
  const hero = document.querySelector(".hero");
  const toggleBtn = document.getElementById("carousel-toggle");
  
  // Liste d'images issues de vos rubriques (Web, Électronique, Informatique, Automatisation)
  const images = [
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1600&q=80"
  ];
  
  let currentIndex = 0;
  let carouselInterval;
  let isPlaying = true;

  function changeBg() {
    currentIndex = (currentIndex + 1) % images.length;
    hero.style.backgroundImage = `url('${images[currentIndex]}')`;
  }

  function startCarousel() {
    carouselInterval = setInterval(changeBg, 5000); // Change toutes les 5 secondes
  }

  function stopCarousel() {
    clearInterval(carouselInterval);
  }

  if (toggleBtn && hero) {
    // Initialise la première image
    hero.style.transition = "background-image 0.8s ease-in-out";
    startCarousel();

    toggleBtn.addEventListener("click", () => {
      if (isPlaying) {
        stopCarousel();
        toggleBtn.textContent = "▶ Continuer";
        toggleBtn.classList.add("paused");
      } else {
        startCarousel();
        toggleBtn.textContent = "⏸ Pause";
        toggleBtn.classList.remove("paused");
      }
      isPlaying = !isPlaying;
    });
  }

  // ==========================================
  // 2. SURVOL DU BOUTON SERVICES (NAVBAR)
  // ==========================================
  // Recherche le lien "Services" dans la navigation
  const navLinks = document.querySelectorAll(".nav-links a");
  let servicesNavLink = null;
  
  navLinks.forEach(link => {
    if (link.textContent.trim().toLowerCase() === "services") {
      servicesNavLink = link;
    }
  });

  if (servicesNavLink) {
    servicesNavLink.addEventListener("mouseenter", () => {
      const servicesSection = document.querySelector(".services-section");
      if (servicesSection) {
        servicesSection.scrollIntoView({ behavior: "smooth", block: "center" });
        // Petit effet de flash visuel pour attirer l'attention
        servicesSection.style.outline = "2px solid #007bff";
        setTimeout(() => servicesSection.style.outline = "none", 1000);
      }
    });
  }

  // ==========================================
  // 3. ANIMATION DES CARTES AU DEFILEMENT (SCROLL)
  // ==========================================
  const cards = document.querySelectorAll(".service-card");
  
  const appearanceOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  };

  const appearanceObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
        observer.unobserve(entry.target); // Anime une seule fois
      }
    });
  }, appearanceOptions);

  cards.forEach(card => {
    // Style initial avant animation
    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";
    card.style.transition = "all 0.6s ease-out";
    appearanceObserver.observe(card);
  });

  // ==========================================
  // 4. ANIMATION DU FORMULAIRE DE CONTACT
  // ==========================================
  const form = document.querySelector(".appointment-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault(); // Empêche le rechargement de la page
      
      const submitBtn = form.querySelector(".submit-btn");
      const originalText = submitBtn.textContent;
      
      submitBtn.textContent = "Envoi en cours...";
      submitBtn.disabled = true;

      // Simulation d'envoi de formulaire réussi
      setTimeout(() => {
        submitBtn.textContent = "✓ Message Envoyé !";
        submitBtn.style.backgroundColor = "#28a745";
        form.reset();

        setTimeout(() => {
          submitBtn.textContent = originalText;
          submitBtn.style.backgroundColor = "";
          submitBtn.disabled = false;
        }, 3000);
      }, 1500);
    });
  }
});