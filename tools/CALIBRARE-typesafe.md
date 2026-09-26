# Calibrarea porții semantice (TypeSafe) — banca de achiziții

Rulat pe 27.09.2026, `typesafe-sdk` 0.7.0, `check_semantic.py` copiat din proiectul RU (praguri neschimbate:
`noul` 0.70, judecata comparativă pe cheile `unic`, frază cu frază pe explicații).

## Pozitivi de control (mutante)

`mutante.py`: 12 întrebări `unic` din 8 acte diferite, cu cheia mutată deliberat pe un distractor.

| | rezultat |
|---|---|
| mutante prinse (REVIZUIT) | **12 / 12** |
| încrederea judecății comparative | 1,00 la toate 12 |
| tokens | 155.836 |

Pragurile moștenite de la RU se separă curat și pe acest corpus, pentru clasa de erori „cheie mutată pe un distractor”.
Limita rămâne cea de la RU (J3): o cheie *subtil* greșită nu a fost testată.

## Banca întreagă (780 de întrebări, după verificarea adversarială)

| | |
|---|---|
| OK | 491 |
| INCERT (listă de triaj) | 288 |
| REVIZUIT | 1 |
| tokens | 8.310.224 |

**REVIZUIT — N395A-059: defect real (sursă), cheie corectă.** Citatul era art. 35 alin. (1) din Normele H.G. 395 (definiția
garanției de participare), iar răspunsul era plafonul de 1%, care în forma la zi stă în art. 154 alin. (2) din Legea 98/2016.
Varianta corectă conținea și istoric („abrogate în anul 2023”). Reancorată pe art. 154 alin. (2); art. 35 a rămas fără
întrebare, deci s-a scris N395-N601 pe art. 35 alin. (1) (OK la poartă). Capcana textului consolidat: sub art. 35 alin. (3)
abrogat, portalul mai afișează literele orfane a)–b), cu „1%” la lit. a).

**INCERT — motive** (o întrebare poate avea mai multe): încredere mică pe o variantă (165), frază din explicație
neverificabilă din temeiul citat (163), situație ambiguă în enunț (12), frază „contrazisă” (10), cheia „nesusținută” (9),
afirmație absolută (8), distractor „apărabil” (2).

**Triaj:** semnalele tari (frază contrazisă, cheie nesusținută, distractor apărabil) — 22 de semnale pe 19 întrebări — au
fost date unui verificator independent, pe textul legii: **22/22 alarme false**. Cauza, ca la RU: articolul care susține
afirmația nu era în starea modelului (cheia e în alt articol decât `sursa.articol`, sau explicația compară două acte).
Verificatorul a găsit în schimb 2 defecte reale nesemnalate de poartă (L98A-035: „distractorul d)”; N395C-002: afirmație
fără temei despre trecerea la ofertantul următor) — reparate, iar detectorul pozițional extins la „distractorul X)”.

După repararea lor, scanarea băncii a mai găsit: 5 referiri „distractorul X)” și 4 trimiteri la articole din acte din afara
corpusului (art. 56 O.U.G. 34/2006, art. 6 și 51 din Directiva 2014/24/UE, Legea 273/2006) — toate reparate și rerulate prin
poartă (11 întrebări: 5 OK, 6 INCERT — aceleași alarme false confirmate de triaj, 0 REVIZUIT).

## Ce spune și ce nu spune această rulare

- Poarta nu a găsit nicio cheie greșită în bancă; verificarea adversarială (340 de întrebări) nu a găsit nici ea.
- Cele 288 INCERT **nu** sunt verificate una câte una în lege; doar cele 19 cu semnal tare au fost. Restul sunt, după tiparul
  RU și după triaj, în mare parte explicații care trimit la alte articole decât cel citat.
- Întrebările `multiplu` (117) nu au semnal de încredere pentru cheie (limita J1 de la RU); toate au trecut prin verificarea
  adversarială.
