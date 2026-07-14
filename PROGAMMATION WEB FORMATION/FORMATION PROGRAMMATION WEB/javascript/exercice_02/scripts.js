/*
function calculate() {
  let produit = prompt("Nom du produit");

  let prix = parseInt(prompt("Prix du produit"));

  let quantite = parseInt(prompt("Quantité"));

  let total = prix * quantite;

  document.getElementById("result").innerHTML = `
  Produit : ${produit}
   <br>
   Total : ${total}$
   `;
}
*/

function calculate() {
  let produit = [];
  let prix = [];
  let quantite = [];
  let total = [];

  for (let i = 0; i < 3; i++) {
    produit[i] = prompt("Nom du produit");
    prix[i] = parseInt(prompt("Prix du produit"));
    quantite[i] = parseInt(prompt("Quantité"));
    total[i] = prix[i] * quantite[i];
  }

  for (let i = 0; i < 3; i++) {
    document.getElementById("result").innerHTML += `
    Produit : ${produit[i]}
    <br>
    Total : ${total[i]}$
    <br>
    `;
  }
}
