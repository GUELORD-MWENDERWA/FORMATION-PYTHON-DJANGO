// La barre d'outils (filtre / vue liste-grille) n'existe que sur la
// page produits.html : on verifie sa presence avant de brancher les
// evenements pour ne pas casser le script sur les autres pages.
var jsFilter = document.querySelector(".jsFilter");
if (jsFilter) {
  jsFilter.addEventListener("click", function () {
    document.querySelector(".filter-menu").classList.toggle("active");
  });
}

var gridButton = document.querySelector(".grid");
if (gridButton) {
  gridButton.addEventListener("click", function () {
    document.querySelector(".list").classList.remove("active");
    gridButton.classList.add("active");
    document.querySelector(".products-area-wrapper").classList.add("gridView");
    document
      .querySelector(".products-area-wrapper")
      .classList.remove("tableView");
  });
}

var listButton = document.querySelector(".list");
if (listButton) {
  listButton.addEventListener("click", function () {
    listButton.classList.add("active");
    document.querySelector(".grid").classList.remove("active");
    document.querySelector(".products-area-wrapper").classList.remove("gridView");
    document.querySelector(".products-area-wrapper").classList.add("tableView");
  });
}

// Le bouton de theme, lui, est present sur toutes les pages de contenu.
var modeSwitch = document.querySelector(".mode-switch");
if (modeSwitch) {
  modeSwitch.addEventListener("click", function () {
    document.documentElement.classList.toggle("light");
    modeSwitch.classList.toggle("active");
  });
}

// Tiroir de navigation mobile : en dessous de 1024px le menu lateral
// est masque par defaut (voir style.css). Le bouton hamburger de
// base.html reste toujours visible en haut de chaque page pour
// pouvoir naviguer ailleurs sans jamais rester bloque, meme tout en
// bas d'une page qui defile. Se ferme au clic sur le fond assombri,
// sur la croix, avec la touche Echap, ou des qu'un lien est choisi.
var menuToggle = document.querySelector(".menu-toggle");
var sidebar = document.querySelector(".sidebar");
var sidebarOverlay = document.querySelector(".sidebar-overlay");
var sidebarClose = document.querySelector(".sidebar-close");

function openSidebar() {
  if (!sidebar) return;
  sidebar.classList.add("open");
  if (sidebarOverlay) sidebarOverlay.classList.add("open");
  if (menuToggle) menuToggle.setAttribute("aria-expanded", "true");
}

function closeSidebar() {
  if (!sidebar) return;
  sidebar.classList.remove("open");
  if (sidebarOverlay) sidebarOverlay.classList.remove("open");
  if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
}

if (menuToggle && sidebar) {
  menuToggle.addEventListener("click", function () {
    if (sidebar.classList.contains("open")) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });
}
if (sidebarOverlay) {
  sidebarOverlay.addEventListener("click", closeSidebar);
}
if (sidebarClose) {
  sidebarClose.addEventListener("click", closeSidebar);
}
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeSidebar();
  }
});
if (sidebar) {
  var sidebarLinks = sidebar.querySelectorAll(".sidebar-list-item a");
  for (var i = 0; i < sidebarLinks.length; i++) {
    sidebarLinks[i].addEventListener("click", closeSidebar);
  }
}