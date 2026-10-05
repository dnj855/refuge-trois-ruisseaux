// Refuge des Trois Ruisseaux · scripts du site

// Carrousel de l'accueil : les douze photos sont chargées d'un coup, une seule est visible
(function () {
  var carrousel = document.querySelector(".carrousel");
  if (!carrousel) return;
  var figures = carrousel.querySelectorAll("figure");
  var points = carrousel.querySelectorAll(".carrousel-points button");
  var courant = 0;

  function montrer(n) {
    figures[courant].classList.remove("actif");
    points[courant].removeAttribute("aria-current");
    courant = (n + figures.length) % figures.length;
    figures[courant].classList.add("actif");
    points[courant].setAttribute("aria-current", "true");
  }

  carrousel.querySelector(".prec").addEventListener("click", function () { montrer(courant - 1); });
  carrousel.querySelector(".suiv").addEventListener("click", function () { montrer(courant + 1); });
  points.forEach(function (point, i) {
    point.addEventListener("click", function () { montrer(i); });
  });
})();

// Fenêtre d'appel aux dons : s'ouvre 3 secondes après l'arrivée sur l'accueil.
// Pour une prise sans la fenêtre : ajouter ?fenetre=non à l'adresse.
(function () {
  var voile = document.getElementById("fenetre-don");
  if (!voile) return;
  if (new URLSearchParams(window.location.search).get("fenetre") === "non") return;

  var dernierFocus = null;

  function fermer() {
    voile.hidden = true;
    if (dernierFocus) dernierFocus.focus();
  }

  setTimeout(function () {
    dernierFocus = document.activeElement;
    voile.hidden = false;
    voile.querySelector(".fenetre h2").focus();
  }, 3000);

  voile.querySelectorAll("[data-fermer]").forEach(function (el) {
    el.addEventListener("click", function (e) { e.preventDefault(); fermer(); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !voile.hidden) fermer();
  });
})();

// Formulaire de contact : site fictif, rien n'est envoyé
(function () {
  var form = document.querySelector("form.contact");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var message = document.getElementById("message-envoi");
    message.hidden = false;
    message.focus();
  });
})();
