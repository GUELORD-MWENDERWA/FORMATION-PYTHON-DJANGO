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