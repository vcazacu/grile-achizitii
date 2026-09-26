/* Service worker — face aplicația disponibilă offline după prima deschidere.
   La fiecare modificare a întrebărilor, schimbă VERSIUNE ca să se reîmprospăteze cache-ul. */
const VERSIUNE = "grile-achizitii-v6";
const FISIERE = [
  "./",
  "./index.html",
  "./style.css",
  "./app.js",
  "./intrebari.js",
  "./manifest.json",
  "./icon-192.png",
  "./icon-512.png",
  "./apple-touch-icon.png",
  /* TEMATICA-START */
  "./tematica/index.html",
  "./tematica/01-principii-autoritati-contractante-domeniu.html",
  "./tematica/02-exceptari-achizitii-mixte-situatii-speciale.html",
  "./tematica/03-achizitii-centralizate-si-comune-ocazionale.html",
  "./tematica/04-reguli-generale-de-participare.html",
  "./tematica/05-modalitati-si-proceduri-de-atribuire.html",
  "./tematica/06-estimarea-valorii-si-alegerea-modalitatii.html",
  "./tematica/07-etapele-consultarea-pietei-loturi.html",
  /* TEMATICA-END */
  /* LEGISLATIE-START */
  "./legislatie/index.html",
  "./legislatie/01-legea-98-2016-achizitii-publice.html",
  "./legislatie/02-hg-395-2016-act-de-aprobare.html",
  "./legislatie/03-norme-hg-395-2016-achizitii-publice.html",
  "./legislatie/04-oug-98-2017-control-ex-ante.html",
  "./legislatie/05-hg-419-2018-act-de-aprobare.html",
  "./legislatie/06-norme-hg-419-2018-control-ex-ante.html",
  "./legislatie/07-legea-101-2016-remedii-si-cai-de-atac.html",
  "./legislatie/08-ordinul-1792-2002-act-de-aprobare.html",
  "./legislatie/09-norme-alop-1792-2002.html",
  "./legislatie/10-legea-500-2002-finantele-publice.html",
  /* LEGISLATIE-END */
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(VERSIUNE)
      .then(function (c) { return c.addAll(FISIERE); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys()
      .then(function (chei) {
        return Promise.all(chei.filter(function (k) { return k !== VERSIUNE; })
                               .map(function (k) { return caches.delete(k); }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then(function (raspuns) {
      if (raspuns) return raspuns;
      return fetch(e.request).then(function (net) {
        // memorează și resursele cerute ulterior, ca să reziste offline
        var copie = net.clone();
        caches.open(VERSIUNE).then(function (c) { c.put(e.request, copie); });
        return net;
      }).catch(function () {
        return caches.match("./index.html");
      });
    })
  );
});
