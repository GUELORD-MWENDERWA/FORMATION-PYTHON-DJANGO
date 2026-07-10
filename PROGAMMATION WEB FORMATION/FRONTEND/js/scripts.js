//declaration etl'affectation
let premier_nombre = 0;
let deuxieme_nombre = 0;
let somme = 0;

/*
//lire les deux nombres entrer au clavier par l'utilisateur
premier_nombre = prompt("Entrer le premier nombre");
deuxieme_nombre = prompt("Entrer le deuxieme nombre");

//convetir les données entrée par l'utilisateur en entier
premier_nombre = parseInt(premier_nombre);
deuxieme_nombre = parseInt(deuxieme_nombre);
*/

premier_nombre = parseInt(prompt("Entrer le premier nombre"));
deuxieme_nombre = parseInt(prompt("Entrer le deuxieme nombre"));
//traitement
somme = premier_nombre + deuxieme_nombre;
//affichage
alert(
  "La somme  de " + premier_nombre + " et " + deuxieme_nombre + " est " + somme,
); // la fonction alert permet à afficher un message a l'utilisateur
