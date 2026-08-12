const form = document.getElementById("monFormulaire");

form.addEventListener("submit", (e) => {
  e.preventDefault(); // Empêche le rechargement de la page

  const formData = new FormData(form);

  // Récupérer une valeur spécifique
  const nom = formData.get("nom");
  console.log("Nom saisi :", nom);

  // Convertir toutes les données en objet JS standard
  const dataObjet = Object.fromEntries(formData.entries());
  console.log("Toutes les données :", dataObjet);
});
