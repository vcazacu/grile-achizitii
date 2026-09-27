# Grile — Achiziții Publice

Aplicație de tip quiz pentru pregătirea examenului de ofițer de achiziții, construită pe
legislația în formă consolidată la zi, descărcată direct de pe portalul legislatie.just.ro.
PDF-urile pachetului de studiu din folderul părinte au rămas neatinse și nu mai sunt folosite.

Bateria are **39 de teste a câte 20 de întrebări** (780 în total, dintre care maximum 4 cu
răspunsuri multiple pe test). Scorul cel mai bun al fiecărui test se salvează local în browser
(localStorage, cheia `grile-achizitii-scoruri-v2`) și apare pe grila de teste. Tot local se mai
păstrează testul început și neterminat (`grile-achizitii-in-lucru-v1`, reluat din cardul „Continuă”),
ultimul rezultat la fiecare întrebare (`grile-achizitii-istoric-v1`, din care ies procentele pe acte
de la „De recapitulat”) și întrebările puse deoparte (`grile-achizitii-marcate-v1`). Toate se
păstrează pe id-ul întrebării, așa că supraviețuiesc regenerării lui `intrebari.js`.

În timpul unui test: <kbd>1</kbd>–<kbd>4</kbd> (sau A–D) alegi varianta, <kbd>Enter</kbd> verifici și
apoi treci mai departe. Pe ecrane late (≥ 1024 px), după verificare, articolul întreg din lege apare
în dreapta, cu alineatul citat evidențiat; pe telefon, sub butonul „Arată tot articolul”. Articolul
se citește din `legislatie/*.html`, deci doar prin adresa publicată (http), nu la deschiderea din fișier.

Tematica oficială (`Tematică ofițer achiziții.docx`, în folderul părinte) are 54 de subiecte,
grupate aici în **24 de teme** și 5 grupe, acoperite din 10 fișiere de legislație. Lista exactă
de articole cerute e în `tools/bibliografie.py` (`BIB`, `TEME`, `GRUPE`).

### Sursele legislative

Fiecare fișier din `../legislatie/*.txt` a fost descărcat cu `tools/descarca.py` și are pe prima
linie un antet `§SURSA§` cu id-ul din portal și data consolidării folosite. Notele portalului
(modificări, abrogări, praguri actualizate) sunt marcate `§NOTA§` în text și **nu** sunt folosite
ca text normativ, doar ca istoric în explicații. Fișierele sunt numerotate ca PDF-urile pachetului.

| Fișier | Act normativ | Id portal | Consolidarea folosită |
|---|---|---:|---|
| 01 | Legea nr. 98/2016 — achizițiile publice | 178667 | 17.11.2024 |
| 02 | H.G. nr. 395/2016 — actul de aprobare | 179009 | 25.02.2026 |
| 03 | Normele metodologice (anexa la H.G. nr. 395/2016) | 307053 | 25.02.2026 |
| 04 | O.U.G. nr. 98/2017 — controlul ex ante | 195762 | 30.08.2021 |
| 05 | H.G. nr. 419/2018 — actul de aprobare | 201548 | 29.12.2023 |
| 06 | Normele metodologice ale O.U.G. nr. 98/2017 (anexa nr. 1 la H.G. nr. 419/2018) | 269779 | 29.12.2023 |
| 07 | Legea nr. 101/2016 — remedii și căi de atac | 178680 | 06.04.2023 |
| 08 | Ordinul M.F.P. nr. 1.792/2002 — actul de aprobare | 41403 | 28.12.2022 |
| 09 | Normele metodologice ALOP (anexa la Ordinul nr. 1.792/2002) | 262742 | 28.12.2022 |
| 10 | Legea nr. 500/2002 — finanțele publice | 37954 | 05.10.2023 |

Pragurile valorice din art. 7 și art. 19 ale Legii 98/2016 sunt, în forma consolidată, deja cele
aplicabile de la 1 ianuarie 2026. Observațiile despre structura fiecărui act și deciziile luate pe
text (unități formale scoase din bibliografie, marcaje) sunt în `tools/SURSE.md`.

## Cum o folosești

Deschide `index.html` cu dublu-click — merge în orice browser, pe telefon, tabletă sau
calculator, **complet offline**, fără server și fără instalare. O singură limită la deschiderea
direct din fișier: chenarul unei trimiteri către **alt act** nu poate încărca textul acelui act
(browserul blochează citirea altor fișiere locale); linkul „mergi la text” din chenar merge.
Prin adresa publicată (mai jos), chenarele merg și offline.

Pe telefon: folosește adresa publicată (mai jos) și „Adaugă la ecranul principal”, sau copiază
folderul `quiz-app` și deschide `index.html` din aplicația de fișiere.

## Cum adaugi întrebări

**`intrebari.js` este generat** de `tools/asambleaza.py` din `tools/nou/*.json` (neversionate) —
nu se editează direct.

1. Întrebările noi se scriu în `tools/nou/<prefix>-<n>.json`, după schema din `tools/SPEC.md`:
   `id`, `tip` (`"unic"` sau `"multiplu"`), `intrebare`, `variante`, `corecte`, `explicatie`,
   `sursa` (`act`, `articol`, `citat`, `fisier`), `status` (`"ok"` sau `"de verificat"`). Câmpul
   `test` **nu** se completează manual — îl atribuie asamblarea.
2. `python3 tools/asambleaza.py --scrie` validează, aplică cotele pe act (`COTE`), selectează
   uniform pe articole, intercalează proporțional pe cele 39 de teste (max. 4 „multiplu”/test) și
   **amestecă variantele determinist** (`random.Random("grile-achizitii:" + id)`, per întrebare —
   aplicația însăși nu amestecă variantele), apoi scrie `../intrebari.js`.
3. `bash tools/verifica_tot.sh` rulează toate verificările automate (vezi mai jos).
4. Incrementează `VERSIUNE` în `sw.js`.

Explicațiile nu au voie să trimită la poziția unei variante („varianta a doua”, „indicele 2”,
„distractorul b)”), pentru că asamblarea le amestecă. Detectorul din
`check_semantic.py --doar-pozitionale` le respinge.

**Validare în aplicație:** la fiecare deschidere, `app.js` verifică structura tuturor întrebărilor
(exact 20 pe test, cel mult 4 „multiplu”, câmpuri complete). Dacă ceva e greșit, pe ecranul
principal apare un banner roșu cu problemele exacte, iar testul nu pornește.

## Tematica — sinteze pe teme

Secțiunea **Tematica** (`tematica/index.html`, link în antet) are câte o pagină de sinteză pentru
fiecare dintre cele 24 de teme, grupate după cele 5 capitole ale tematicii oficiale. Fiecare pagină
are un rezumat, secțiuni cu reguli, termene și excepții, fiecare cu **temeiul legal citat verbatim**
din forma consolidată, o listă de capcane de examen și întrebările din bancă legate de temă.
Fiecare pagină arată și data consolidării folosite.

Conținutul unei teme stă în `tools/tematica/NN.json`. `tools/tematica_build.py` verifică fiecare
citat contra `../legislatie/*.txt`, generează paginile și indexul și actualizează lista din `sw.js`.
Fiecare temă a trecut prin trei porți înainte de publicare:

1. **Citatele** — fiecare temei apare verbatim, în întregime, în unitatea declarată de eticheta lui
   (aceeași regulă ca `check_articol.py` la întrebări); o etichetă nerecunoscută e eroare. Dacă un
   singur citat nu trece, `tematica_build.py` nu scrie nimic.
2. **Auditul determinist** (`tools/audit_tematica.py`, cod de ieșire 1 la orice problemă) — orice cifră
   și orice articol din paragrafe apar în citatele secțiunii; din rezumat și din capcane, în citatele
   temei; orice id de întrebare există.
3. **Poarta semantică** (`tools/check_tematica.py`, TypeSafe) — fiecare frază e judecată contra
   articolelor citate în secțiunea ei; pragul automat „contrazice” e 0,90, iar orice frază cu
   p ≥ 0,50 se verifică manual în lege (`tools/triaj_tema.py`, `tools/poarta_tema.sh NN`).

Primele două porți rulează și în `verifica_tot.sh`, pe toate temele, fără să scrie fișiere
(`tematica_build.py --verifica`); poarta semantică rulează doar la cerere, fiindcă folosește API-ul.

O întrebare se leagă de tema care conține articolul ei; dacă articolul e în mai multe teme (doar
art. 7 din Legea 98/2016), câștigă tema cu intervalul cel mai specific (tema 13, Achiziția directă).

## Legislația — textele de lege, de citit

Secțiunea **Legislația** (`legislatie/index.html`) redă cele 10 fișiere în text integral
consolidat, formatat pentru telefon: cuprins, câte un bloc pe articol (cu ancoră `#art-N`,
`#art-113-1` pentru art. 113^1; la Normele ALOP `#pct-N`; preambulul are `#preambul`; caseta „Sari”
acceptă „113^1”, „v”, „pct. 3” sau „preambul”), alineate și
litere indentate, iar notele portalului strânse sub fiecare articol. Implicit se văd doar unitățile
cerute în bibliografie; comutatorul „Arată toată legea” descoperă restul. Anexele nr. 1 și nr. 2
ale Legii 98/2016 sunt redate. Anexele actelor de aprobare (H.G. 395, H.G. 419, Ordinul 1.792) nu se
redau acolo: normele din ele au pagini proprii (fișierele 03, 06, 09), iar celelalte nu sunt în bibliografie.

**Trimiterile din text sunt apăsabile** (`tools/trimiteri.py`, gramatică deterministă testată în
`tools/test_trimiteri.py`): la apăsare se deschide sub paragraf un chenar cu textul țintei, care
merge offline. Trimiterile către alt act din bibliografie („art. 7 alin. (5) din Lege” în Normele
H.G. 395, „din ordonanța de urgență” în Normele H.G. 419) trimit la pagina actului respectiv
(`ALIASURI`, `ALIASURI_LOCALE` în `tools/legislatie_build.py`). La ultimul build:

| Fișier | Trimiteri legate | dintre care către alt act |
|---|---:|---:|
| 01 Legea 98/2016 | 986 | 0 |
| 03 Normele H.G. 395 | 372 | 93 |
| 04 O.U.G. 98/2017 | 115 | 10 |
| 06 Normele O.U.G. 98 | 180 | 42 |
| 07 Legea 101/2016 | 159 | 4 |
| 10 Legea 500/2002 | 212 | 0 |

Rămân text simplu trimiterile către acte din afara bibliografiei (Legea 99/2016, 100/2016, O.U.G.
34/2006 etc.) și cele către ținte inexistente. `../legislatie/*.txt` **nu se modifică** — sunt
sursa de adevăr pentru toate uneltele.

## Fișiere

- `index.html`, `app.js`, `style.css` — aplicația (nu se ating când adaugi întrebări)
- `intrebari.js` — **banca de întrebări** (generată)
- `sw.js` — service worker (offline + versiunea cache-ului; listele `TEMATICA` și `LEGISLATIE` sunt generate)
- `tematica/`, `legislatie/` — paginile generate
- `tools/` — lanțul de generare și verificare (Python standard, fără dependențe, cu excepția porții semantice):
  - `descarca.py` — formele consolidate de pe legislatie.just.ro în `../legislatie/`
  - `unitati.py` — etichetele unităților (articole arabe, cu indice, romane; puncte ALOP; preambul)
  - `bibliografie.py` — tematica → unități cerute (`BIB`), temele și grupele (`TEME`, `GRUPE`)
  - `migreaza.py`, `coada.py`, `aplica_coada.py` — migrarea băncii vechi pe textul la zi și coada de reparat
  - `asambleaza.py` — `nou/*.json` → `intrebari.js` (cote, teste, amestecare)
  - `valideaza.py` — schema, unicitate, texte nedublate
  - `check_citat.py` — citatul apare verbatim în sursă (după normalizare)
  - `check_articol.py` — articolul declarat = locul real al citatului + în bibliografie
  - `acoperire.py` — fiecare unitate cerută are cel puțin o întrebare
  - `check_semantic.py` — referirile poziționale (determinist) și poarta semantică TypeSafe pe bancă
  - `adversarial.py`, `mutante.py` — loturile verificării adversariale; cheile mutate de calibrare
  - `tematica_build.py`, `audit_tematica.py`, `check_tematica.py`, `triaj_tema.py`, `poarta_tema.sh`,
    `text_tema.py`, `scrie_tema.py`, `intrebari_tema.py` — paginile de tematică și porțile lor
  - `legislatie_build.py`, `trimiteri.py` — paginile de legislație
  - `verifica_sw.py` — lista cache-ului offline = fișierele reale
  - `verifica_tot.sh` — toate verificările deterministe într-un pas (banca, acoperirea, cache-ul offline,
    temele fără scrieri, paginile de legislație: id-uri unice și trimiteri spre ținte existente); cu `--semantic` adaugă poarta
    TypeSafe (cere `TYPESAFE_API_KEY` și mediul `tools/.venv-ts` cu `typesafe-sdk` 0.7.0)
  - `test_*.py` — testele uneltelor (stdlib, `python3 test_<nume>.py`)
  - `SPEC.md` (contractul schemei), `SURSE.md` (sursele), `CALIBRARE-typesafe.md` (cifrele porții semantice)
  - `nou/` — întrebările brute înainte de asamblare (neversionate)

## Publicare și actualizare

Aplicația e publicată pe GitHub Pages, din depozitul `vcazacu/grile-achizitii`:

**https://vcazacu.github.io/grile-achizitii/**

Pe telefon sau tabletă: deschide adresa în browser, lasă pagina să se încarce complet, apoi
„Adaugă la ecranul principal”. Service worker-ul salvează local aplicația, toate paginile de
tematică și de legislație, așa că de la a doua deschidere totul funcționează **fără internet**.

### Când modifici ceva

1. `python3 tools/asambleaza.py --scrie` (dacă ai schimbat întrebări), `python3 tools/tematica_build.py`
   (teme), `python3 tools/legislatie_build.py` (legislație);
2. `bash tools/verifica_tot.sh` — toate verificările automate trebuie să treacă;
3. incrementează `VERSIUNE` în `sw.js`.

Fără al treilea pas, dispozitivele care au deja aplicația rămân cu versiunea veche, pentru că
service worker-ul servește din cache înaintea rețelei. Apoi:

```bash
git add -A && git commit -m "Actualizare" && git push
```

GitHub Pages republică automat în 1–2 minute.

## Acoperirea materiei

Cele 780 de întrebări sunt distribuite pe acte conform cotelor din `tools/asambleaza.py` (`COTE`):

| Act normativ | Întrebări |
|---|---:|
| Legea nr. 98/2016 — achizițiile publice | 303 |
| Normele metodologice (anexa la H.G. nr. 395/2016) | 194 |
| Legea nr. 500/2002 — finanțele publice | 84 |
| Legea nr. 101/2016 — remedii și căi de atac | 68 |
| O.U.G. nr. 98/2017 — controlul ex ante | 45 |
| Normele metodologice ale O.U.G. nr. 98/2017 | 39 |
| Normele metodologice ALOP | 37 |
| Ordinul M.F.P. nr. 1.792/2002 — actul de aprobare | 4 |
| H.G. nr. 395/2016 — actul de aprobare | 3 |
| H.G. nr. 419/2018 — actul de aprobare | 3 |

Din cele 780: 117 sunt de tip `"multiplu"` (59 cu 2 răspunsuri corecte, 58 cu 3 — echilibrate, ca
strategia „alege mereu 3” să nu câștige) și 663 de tip `"unic"`; toate au `status: "ok"`.
Fiecare unitate cerută de bibliografie are cel puțin o întrebare (`tools/acoperire.py`:
„ACOPERIRE COMPLETĂ” pe toate cele 10 fișiere). De aici vine și numărul de teste: la 600 de
întrebări nu încăpea câte o întrebare pe fiecare unitate cerută, iar decizia a fost să crească
bateria la 39 de teste.

## Cum au fost verificate întrebările

Banca pleacă de la cele 600 de întrebări ale versiunii anterioare, scrise pe PDF-uri, migrate pe
textul la zi, plus 182 de întrebări noi pentru unitățile neacoperite.

1. **Straturile deterministe** (`verifica_tot.sh`): schema, citatul verbatim, articolul declarat,
   referirile poziționale, distribuția pe teste, acoperirea, trasabilitatea temelor față de docx,
   lista cache-ului offline. Toate trec.
2. **Coada de reparat a migrării**: 19 întrebări pe care textul la zi le contrazicea sau le lăsa
   fără temei — 15 corecturi de formă, 1 de fond (OUGB-007: obligația citată trecuse din Normele
   abrogate în Legea 98/2016, art. 7 alin. (8)), 1 notă, 2 eliminări (reguli existente doar în
   note ale portalului). Fiecare decizie „fond” a fost verificată în lege (`tools/coada/`).
3. **Verificarea adversarială** (`../raport-adversarial.txt`): 340 de întrebări (toate cele noi,
   toate cele „multiplu”, cele cu explicația rescrisă), în 12 loturi de verificatori independenți,
   cu sarcina de a dobori cheia. Prima trecere: 248 OK, 92 suspecte, **0 chei greșite**. 110 întrebări
   corectate (explicații și enunțuri, nicio cheie schimbată), reverificate; cele 5 inexactități
   introduse chiar de reparații au fost corectate după verificarea în lege.
4. **Poarta semantică TypeSafe** (`tools/CALIBRARE-typesafe.md`): calibrată pe 12 chei mutate
   deliberat (12/12 prinse), apoi rulată pe toate cele 780: 491 OK, 288 incerte, 1 revizuită —
   un defect real de sursă (N395A-059), reparat. Cele 22 de semnale tari au fost verificate în lege:
   toate alarme false, dar verificarea a găsit alte 2 defecte reale, reparate.

În plus, aplicația a fost parcursă automat în browser pe toate cele 39 de teste
(`tools/sweep.js`): **39/39 cu scor 100%**, fără erori, iar toate cele 37 de pagini (aplicația,
indexurile, 24 de teme, 10 acte) încap pe lățimea de 375 px a unui telefon.

Ce a apărut pe parcurs, inclusiv alarmele false și limitele cunoscute, e descris în
[`PROBLEME-SI-REZOLVARI.md`](PROBLEME-SI-REZOLVARI.md).
