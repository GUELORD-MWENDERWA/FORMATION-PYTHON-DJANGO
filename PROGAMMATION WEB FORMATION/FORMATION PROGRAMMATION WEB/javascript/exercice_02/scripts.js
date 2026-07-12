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
