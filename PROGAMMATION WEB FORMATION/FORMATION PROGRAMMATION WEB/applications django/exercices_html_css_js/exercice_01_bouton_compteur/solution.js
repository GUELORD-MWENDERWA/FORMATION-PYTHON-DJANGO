const v = document.getElementById("value");
let n = 0;
document.getElementById("inc").onclick = () => (v.textContent = ++n);
document.getElementById("dec").onclick = () => (v.textContent = --n);
