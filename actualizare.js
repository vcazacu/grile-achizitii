/* Trecerea la versiunea nouă. sw.js servește întâi din cache, deci la prima deschidere după o actualizare
   pagina rulează încă fișierele vechi; noul service worker se instalează în fundal și preia pagina câteva
   secunde mai târziu („controllerchange”). Atunci reîncărcăm: imediat dacă nu e o întrebare pe ecran,
   altfel la cerere, ca să nu se piardă răspunsul în curs. La revenirea în aplicație (pe iPad rămâne
   deschisă în fundal) cerem o verificare a versiunii, ca actualizarea să nu aștepte o redeschidere. */
(function () {
  if (!("serviceWorker" in navigator) || location.protocol.indexOf("http") !== 0) return;
  var sw = navigator.serviceWorker;
  if (!sw.controller) return; // prima instalare: pagina tocmai a venit din rețea, e deja la zi
  var preluat = false;
  sw.addEventListener("controllerchange", function () {
    if (preluat) return;
    preluat = true;
    if (!document.querySelector(".question-text")) { location.reload(); return; }
    var bara = document.createElement("div");
    bara.className = "bara-versiune";
    bara.setAttribute("role", "status");
    bara.innerHTML = '<span>A apărut o versiune nouă a aplicației.</span>' +
      '<button type="button" class="btn btn-primary">Reîncarcă</button>';
    bara.querySelector("button").addEventListener("click", function () { location.reload(); });
    document.body.appendChild(bara);
  });
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState !== "visible") return;
    sw.getRegistration().then(function (r) { if (r) r.update(); }).catch(function () {});
  });
})();
