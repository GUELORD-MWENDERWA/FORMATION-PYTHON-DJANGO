let compteur = 0;

function increment() {
  compteur++;
  document.getElementById("result").innerText = compteur;
  document.getElementById("result").style.color = "green";
}

function decrement() {
  compteur--;
  document.getElementById("result").innerText = compteur;
  document.getElementById("result").style.color = "red";
}

function reset() {
  compteur = 0;
  document.getElementById("result").innerText = compteur;
  document.getElementById("result").style.color = "black";
}

document.getElementById("increment").addEventListener("click", increment);
document.getElementById("decrement").addEventListener("click", decrement);
document.getElementById("reset").addEventListener("click", reset);
