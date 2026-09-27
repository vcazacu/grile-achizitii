# Probleme găsite și cum au fost rezolvate

Lucrare din 27.09.2026: aplicația de grile pentru achiziții a primit aceleași funcții ca aplicația
de Resurse Umane (surse la zi de pe legislatie.just.ro, secțiunile Tematica și Legislația, lanțul de
unelte și porțile de verificare). Punctul de plecare: o bancă de 600 de întrebări scrise pe PDF-uri,
verificată atunci pe trei straturi. Documentul adună ce a ieșit la iveală la mutarea pe textul la zi,
inclusiv alarmele false și limitele, fiindcă ele spun cât valorează fiecare verificare.

Cifrele brute ale porții semantice: [`tools/CALIBRARE-typesafe.md`](tools/CALIBRARE-typesafe.md).
Verificarea adversarială: [`../raport-adversarial.txt`](../raport-adversarial.txt).

**Rezumat:** 780 de întrebări (600 migrate, 2 eliminate, 182 noi), 0 chei greșite găsite de
verificarea adversarială sau de poarta semantică; 3 defecte de fond reale în banca veche (reparate);
24 de pagini de sinteză cu 1081 de afirmații judecate, 0 contrazise, după ce porțile au prins 3 erori
reale în conținut proaspăt scris; 10 pagini de legislație cu trimiteri apăsabile, inclusiv 93 din
Normele H.G. 395 către Lege, care la început lipseau din cauza unui bug.

---

## A. Sursele

### A1. Actele de pe portal nu corespund PDF-urilor unu la unu — **rezolvat**

Pachetul de studiu avea normele în același PDF cu actul de aprobare. Pe portal, Normele H.G. 395
(id 307053), Normele O.U.G. 98/2017 (269779) și Normele ALOP (206786, consolidat 262742) sunt documente
separate; actele de aprobare doar trimit la ele. Soluția: 10 fișiere `.txt`, numerotate exact ca
PDF-urile (01–10), fiecare cu antetul `§SURSA§`. Testele de surse au fost adaptate la titlurile reale
ale portalului („HG 395”, „ORD DE URGENTA 98”, „NORMA (A)”).

### A2. Actul H.G. 419 citează articole arabe în interiorul articolelor romane — **rezolvat**

Art. IV–VI din H.G. 419/2018 modifică alte acte și conțin textual „Articolul 26 se modifică…”.
Parserul le lua drept articole ale actului. `unitati.py` marchează corpul actului `DOAR_ROMANE`
(test roșu, apoi verde).

### A3. Articole romane care se ciocneau cu cele arabe în intervale — **rezolvat**

`cheie()` sortează acum pe categorii (preambul, arabe, romane, puncte ALOP), așa că „I” nu mai
intră într-un interval „1-20”.

### A4. Trei unități formale scoase din bibliografie — **decizie**

Norme 419 art. 21 („anexele fac parte integrantă”), preambulul și art. 3 (publicarea) din Ordinul
1.792: verificatorii au respins ca triviale întrebările pe ele. Consemnat în `tools/SURSE.md`.

## B. Banca migrată pe textul la zi

### B1. Defecte de fond reale în banca publicată anterior — **reparat**

Coada de reparat (19 întrebări) a găsit o întrebare a cărei cheie nu mai corespundea legii:
**OUGB-007** trimitea la Norme art. 46, abrogat; obligația de notificare trimestrială a achizițiilor
directe e acum în Legea 98/2016, art. 7 alin. (8). Alte două întrebări (N395A-003, N395A-006) se
sprijineau pe reguli care există doar în notele portalului și au fost eliminate. Poarta semantică a
mai găsit **N395A-059**: citat reancorat, pentru că plafonul de 1% al garanției de participare stă
acum în Legea 98/2016, art. 154 alin. (2), nu în Norme.

### B2. Explicații care trimiteau la poziția variantei — **reparat**

Banca veche nu amesteca variantele, așa că explicații ca „varianta a doua” sau „indicele 2” erau
corecte. După amestecarea deterministă, au devenit greșite. Detectorul pozițional a fost extins de
patru ori, de fiecare dată cu test întâi: litere („varianta D”), genitive („variantei a doua”),
„iar a treia”, „indicele N”, „distractorul b)”. Au fost reparate 75 de explicații la migrare, apoi
22 de explicații ALOP cu „indicele N”, care contraziceau cheia după amestecare, plus 5 „distractorul X)”.

### B3. Numărul de teste — **decizie a utilizatorului**

La 600 de întrebări nu încăpea câte o întrebare pe fiecare unitate cerută de bibliografie. Utilizatorul
a ales „mai multe teste”: 39 × 20 = 780, cu acoperire completă.

### B4. Explicația L98C-035 folosea lectura inversă a art. 154 alin. (3) — **reparat**

Textul spune: „Cu excepția contractelor de servicii de proiectare și a contractelor de lucrări, a căror
valoare estimată este mai mică decât […] art. 7 alin. (1), precum și în cazul […] negocierii fără
publicare […], autoritatea contractantă are dreptul de a nu solicita […] garanția de bună execuție.”
Explicația din bancă îl citea ca pe o listă de cazuri în care se poate renunța la garanție pentru
proiectare și lucrări. Lectura adoptată: renunțarea e permisă sub praguri, **cu excepția** proiectării
și lucrărilor, plus la negocierea fără publicare. E coerentă cu riscul, iar Norme art. 39 alin. (2),
care detalia regula, e abrogat. Cheia nu s-a schimbat. Ambiguitatea e semnalată pe pagina temei 9.
Eroarea a ieșit la lumină când poarta semantică a marcat prima formulare a temei 9 (0,55).

## C. Verificarea adversarială și poarta semantică pe bancă

- **Adversarial:** 340 de întrebări, 12 loturi. 248 OK, 92 suspecte, 0 chei greșite. 110 corectate.
  A doua trecere a găsit **5 inexactități introduse chiar de reparații**, corectate după verificarea
  în lege. Lecția: o reparație e și ea un text nou, care trebuie verificat.
- **TypeSafe:** 12/12 chei mutate prinse. Pe bancă: 491 OK, 288 incerte, 1 revizuită (B1). Cele 22 de
  semnale tari au fost toate **alarme false**, cu aceeași cauză ca la RU: articolul care susține
  afirmația nu era cel citat (cheia în alt articol, explicații care compară două acte). Verificatorul
  care le-a triat a găsit însă 2 defecte reale nesemnalate de poartă: L98A-035 și N395C-002.

## D. Legislația

### D1. „din Lege” în Normele H.G. 395 lega spre articolele Normelor — **reparat**

Gramatica trimiterilor recunoștea „din Legea …”, dar nu „din Lege”, forma folosită peste tot în
Normele H.G. 395. Trimiterile „art. 7 alin. (5) din Lege” duceau la art. 7 din Norme. După reparația
din `trimiteri._EXTERN`, trimiterile din Norme către Lege au crescut **de la 1 la 93**. În Norme,
„Lege” cu majusculă se recunoaște doar local (`ALIASURI_LOCALE`), ca să nu prindă alte acte.

### D2. Resturi din RU în pagini — **reparat**

Textele copiate din unelte („grile de salarizare”, „Cele nouă acte”, antetul RU) au fost scoase, iar
`test_fara_ru.py` blochează orice revenire.

### D3. Textul citat din H.G. 419 devenea alineate și ținte de trimiteri — **reparat** (revizuirea finală)

Art. II–VI din H.G. 419/2018 modifică alte acte și citează textul modificat („(3) Strategia de
contractare …”, „a) etapa de planificare”). Regula `DOAR_ROMANE` oprea doar „Articolul 26” citat, nu și
rândurile „(N)” și „x)”: ele deveneau alineatele art. IV–V, cu **24 de id-uri duplicate** și **49 de
trimiteri** care duceau la textul greșit (un „alin. (1)” din Normele modificate deschidea „art. V alin.
(1)”). Acum articolele romane care conțin formule de modificare își redau conținutul ca text simplu
(art. VII și VIII, cu alineate și litere proprii, rămân structurate). `test_legislatie.py` verifică
id-uri unice și trimiteri spre ținte existente pe toate cele 10 pagini, iar build-ul se oprește la
id-uri duplicate.

### D4. Linkurile spre alt act din panoul „Temei legal” nu se încărcau — **reparat** (28.09.2026, după redesign)

Panoul din aplicație copiază articolul întreg din pagina de legislație. Se rescriau doar trimiterile
interne (`#art-5`); cele spre alt act (ex. în Normele H.G. 395: `01-legea-98-2016-….html#art-216`) rămâneau
relative și porneau de la rădăcina aplicației, fără `legislatie/` — pagina nu exista. Parcurgerea tuturor
celor 780 de întrebări a găsit **166 de linkuri rupte** (spre Legea 98, O.U.G. 98, Legea 101, Legea 500).
Acum toate linkurile articolului se rezolvă față de pagina legii din care vine: 791 de linkuri, 0 rupte
(`tools/linkuri_panou.js`). Paginile statice (aplicația, 24 de teme, 10 acte, indexurile) erau corecte;
`tools/test_linkuri.py` le verifică acum pe toate în `verifica_tot.sh` (fișier existent, ancoră existentă,
id-urile din „Exersează tema” prezente în bancă). Chenarele din paginile de legislație nu au problema:
actul adus stă în același folder, iar trimiterile `#…` se rescriu deja.

## E. Tematica

Porțile (citat verbatim, audit determinist, TypeSafe cu pragul 0,90 și banda de triaj ≥ 0,50) au
prins, înainte de commit:

1. **Tema 1 (0,88):** excepția de la referatul de necesitate omitea necesitățile „care nu pot fi
   identificate în ultimul trimestru” (Norme art. 3 alin. (2)). Scorul era sub pragul de 0,90; de aici
   banda de triaj de la 0,50, aplicată la toate temele.
2. **Tema 9 (0,55):** prima formulare inversa excepția negocierii fără publicare (B4).
3. **Tema 18 (0,97, contrazis):** „pragurile *mai mici* de la art. 7 alin. (5)”. Comparația venea din
   Lege, nu din Normele citate; reformulată fără comparație.

Auditul determinist a prins 7 mențiuni de articol fără citatul lor în secțiune și un paragraf sprijinit
pe o notă a portalului (tema 13), necitabilă. Toate au fost rezolvate. La tema 5, căutarea citatului
lipsă a arătat că paragraful trimitea la art. 7 alin. (1), deși art. 113 alin. (1) trimite la alin. (2).

**Prinse la recitire, nu de porți:**
- tema 8: art. 153 alin. (4) era parafrazat („informații necerute la timp”), nu redat. Textul spune
  „nu au fost transmise în timp util”, ceea ce contrazice alin. (1) lit. a). Acum e redat exact, cu
  contradicția semnalată. Poarta nu avea cum să prindă asta: parafraza era plauzibilă și consistentă
  cu scopul normei.

**Porțile erau mai slabe decât le descria README-ul — reparat (revizuirea finală).** Citatul era căutat
în toată zona actului, nu în unitatea declarată; build-ul scria paginile chiar cu citate eșuate;
auditul ieșea mereu cu 0 și nu privea rezumatul și capcanele; `poarta_tema.sh` pierdea codurile de ieșire
prin `grep`/`tail`, iar `verifica_tot.sh` nu verifica temele deloc. Conținutul publicat era curat (toate
cele 605 citate stau în unitatea declarată), dar o editare viitoare ar fi trecut tăcut. Acum: citatul se
verifică în unitatea declarată (regula `check_articol`), o etichetă nerecunoscută e eroare, build-ul nu
scrie nimic la erori, auditul acoperă rezumatul și capcanele și iese cu 1, iar `verifica_tot.sh` rulează
ambele porți pe toate temele (testat și pe o temă stricată deliberat: ambele erori prinse).

**Alarme false verificate în lege (bandă ≥ 0,50):** 5 în versiunile finale, toate corecte. Una dintre
ele (0,50, tema 9) reflectă ambiguitatea reală a art. 154 alin. (3).

Totalul: 1081 de afirmații, 1079 susținute, 1 absență corectă, 1 neverificabilă (un sfat de studiu,
nu o afirmație de drept), **0 contrazise**.

## F. Legarea întrebărilor de teme — **decizie**

Art. 7 din Legea 98/2016 e în tema 1 („1-8”) și în tema 13 („7”, Achiziția directă). Regula „prima
temă câștigă” lăsa tema 13 cu o singură întrebare. Acum câștigă tema cu intervalul cel mai specific:
10 întrebări au trecut la tema 13 (test roșu, apoi verde).

## F2. Minorele amânate — **rezolvate** (27.09.2026, după publicare)

- **Întrebările `multiplu` erau înclinate spre 3 răspunsuri corecte** (87 din 117): „alege mereu 3” câștiga
  prea des. 29 au fost convertite la 2 corecte, transformând o variantă corectă într-una falsă după lege
  (ex.: termenul de 20 de zile în locul celor 45 de la art. 32 alin. (4) din Legea 101/2016). Acum: 59 cu 2,
  58 cu 3.
- **27 de întrebări reformulate** după propunerile opționale ale verificatorilor: enunțuri care numesc actul,
  trimiteri la articole, afirmații despre acte din afara corpusului scoase; ALOP-007 nu mai dă răspunsul la
  ALOP-002; N395B-030 („minim absolut”) și OUGB-034 („suplimentare”) formulate exact.
- **Explicația ALOP-007 completată** (3 → 5 fraze, cât cere SPEC): cine poate primi delegarea și unde apare
  persoana delegată în fazele execuției (pct. 2 „Bun de plată”, pct. 3 ordonanțarea). TypeSafe: INCERT pe fraza
  cu pct. 2–3 (în afara temeiului declarat), verificată în lege — corectă.
- **Verificare:** două verificări adversariale independente (29 de chei schimbate: 25 OK, 4 suspecte;
  27 reformulări: 24 OK, 3 suspecte; 0 greșite), toate cele 7 suspecte corectate; poarta TypeSafe pe cele
  56: 32 OK, 24 incerte, 0 revizuite; cele 6 semnale tari verificate în lege — alarme false (frazele citează
  articole din afara temeiului declarat).
- **Unelte:** auditul temelor verifică și intervalele de valori („5–10 zile”); caseta „Sari” acceptă puncte,
  preambul și romane scrise mic; chenarul explică limita la deschiderea din fișier; `SPEC.md` corectat
  (garanția de participare: max. 1%, nu 2%; art. 36 și 40 din Normele H.G. 395 sunt abrogate doar parțial).

## G. Stare finală

| | |
|---|---|
| întrebări | 780 (663 unic, 117 multiplu: 59 cu 2 corecte, 58 cu 3), 39 de teste, toate `ok` |
| acoperire | completă pe toate cele 10 fișiere |
| `verifica_tot.sh` | toate verificările trec |
| parcurgere în browser | 39/39 teste cu 100%, fără erori |
| lățime de telefon (375 px) | 37/37 pagini fără depășire |
| teme | 24/24, 1081 de afirmații, 0 contrazise |

## H. Limite cunoscute — unde să nu te bazezi pe verificare

1. **Cele 117 întrebări `multiplu` nu au semnal de încredere pentru cheie** în poarta semantică
   (judecata comparativă se aplică doar la `unic`). Toate au trecut însă prin verificarea adversarială.
2. **Cele 288 de întrebări „incerte” nu au fost citite una câte una în lege**, ci doar cele 19 cu
   semnal tare. Tiparul arată explicații care trimit la alte articole decât cel citat, nu erori.
3. **Detecția cheilor greșite e validată doar pe cazul ușor** (cheie mutată pe un distractor oarecare).
   O cheie subtil greșită nu a fost testată.
4. **Consolidările au date diferite** (de la 30.08.2021 la 25.02.2026). Sunt cele mai recente de pe
   portal la descărcare, dar o modificare publicată după aceste date nu e prinsă decât la o nouă
   descărcare (`tools/descarca.py`).
5. **Formulări ambigue ale legii** (art. 153 alin. (4) și art. 154 alin. (3) din Legea 98/2016) sunt
   semnalate, nu rezolvate: aplicația spune ce e sigur și unde textul se contrazice.
6. **Verificarea semantică nu înlocuiește citirea legii.** Fiecare verdict care a contat a fost
   confirmat în text înainte de a fi aplicat, iar corectura de la tema 8 (secțiunea E) a venit din
   recitire, nu din porți.
