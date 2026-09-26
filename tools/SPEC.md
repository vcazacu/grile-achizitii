# SPEC — întrebări pentru examenul de ofițer achiziții publice

Contractul dintre coordonator și agenții care scriu sau repară întrebări. Un agent primește: un act (fișier
`.txt` din `Examen-Achizitii/legislatie/`), lista unităților de acoperit (articole / puncte), numărul de
întrebări cerut, cota de întrebări „multiplu" și un fișier de ieșire `tools/nou/<PREFIX>-N<lot>.json`.
Scrie **incremental** (după fiecare 5 întrebări rescrie fișierul complet), ca să nu se piardă nimic dacă
sesiunea se oprește.

## 1. Sursa de adevăr

- Se folosește **exclusiv** textul din `legislatie/<fisier>.txt` (forma consolidată la zi de pe
  legislatie.just.ro, descărcată cu `tools/descarca.py`; lista și datele în `tools/SURSE.md`). Nimic din
  memorie despre lege: dacă memoria și textul diferă, textul are dreptate. Dacă textul nu spune ceva,
  întrebarea nu se pune. **Pragurile valorice** (art. 7 din Legea 98/2016 etc.) se iau numai din textul la zi.
- Liniile `§NOTA§` sunt istoricul modificărilor și notele portalului — **nu sunt text normativ**. Nu se
  citează din ele. Pot apărea doar în explicație („alineatul a fost introdus prin Legea nr. 208/2022"), fără
  să schimbe ce e în vigoare.
- Liniile `## ...` sunt titluri de capitol/secțiune. `§ANEXA§ ...` marchează o anexă (formulare, liste).
- O unitate al cărei text e „Abrogat." nu produce întrebări despre conținutul ei; cel mult o întrebare-capcană
  despre faptul abrogării, sprijinită pe un text normativ în vigoare (de ex. Legea 101/2016: notificarea
  prealabilă, art. 6–7, abrogată — adresarea directă la CNSC/instanță, art. 4 alin. (1)).
- Actele de aprobare și normele sunt fișiere separate: `02` (H.G. 395) / `03` (Normele H.G. 395),
  `05` (H.G. 419, articole I–VIII) / `06` (Normele O.U.G. 98/2017), `08` (Ordinul 1.792) / `09` (Normele ALOP,
  structurate pe puncte 1–5, fără „Articolul N").

## 2. Ce se acoperă (tematica oficială → unități)

Tabelul e generat din `bibliografie.TEME` (sursa procesabilă; nu se editează aici). Unitățile abrogate apar
în listă, dar nu primesc întrebări despre conținut.

| # | Temă (subiectele din docx) | Fișier | Unități din tematică |
|---|---|---|---|
| 1 | Principiile achizițiilor publice. Autorități contractante. Domeniu de aplicare | 01 | 1, 2, 3, 4, 5, 6, 7, 8 |
| 1 | Principiile achizițiilor publice. Autorități contractante. Domeniu de aplicare | 02 | preambul, 1, 2 |
| 1 | Principiile achizițiilor publice. Autorități contractante. Domeniu de aplicare | 03 | 1, 2, 3, 4, 5, 6, 7 |
| 1 | Principiile achizițiilor publice. Autorități contractante. Domeniu de aplicare | 05 | V |
| 2 | Exceptări. Achiziții mixte. Situații speciale | 01 | 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39 |
| 3 | Activități de achiziție centralizare și achiziții comune ocazionale | 01 | 40, 41, 42, 43, 44, 45, 46, 47, 48 |
| 4 | Reguli generale de participare și desfășurare a procedurilor de atribuire | 01 | 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67 |
| 4 | Reguli generale de participare și desfășurare a procedurilor de atribuire | 03 | 47, 48, 49, 50, 51, 52, 53 |
| 5 | Modalități de atribuire. Procedurile de atribuire | 01 | 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 113^1 |
| 5 | Modalități de atribuire. Procedurile de atribuire | 03 | 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106 |
| 6 | Estimarea valorii achiziției publice și alegerea modalității de atribuire | 01 | 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 |
| 6 | Estimarea valorii achiziției publice și alegerea modalității de atribuire | 03 | 15, 16, 17 |
| 7 | Organizarea și desfășurarea procedurii de atribuire. Etapele procesului de achiz | 01 | 139, 140, 141 |
| 7 | Organizarea și desfășurarea procedurii de atribuire. Etapele procesului de achiz | 03 | 8, 9, 10, 11, 18, 19 |
| 8 | Reguli de publicitate și transparență | 01 | 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153 |
| 8 | Reguli de publicitate și transparență | 03 | 54, 55, 56, 57 |
| 9 | Documentația de atribuire. Oferte alternative. Documentul unic de achiziție Euro | 01 | 154, 154^1, 154^2, 155, 156, 157, 158, 159, 160, 161, 162, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202 |
| 9 | Documentația de atribuire. Oferte alternative. Documentul unic de achiziție Euro | 03 | 20, 21, 22, 23, 24, 25, 26, 27, 28 |
| 10 | Criterii de calificare și selecție | 01 | 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186 |
| 10 | Criterii de calificare și selecție | 03 | 29, 30, 31 |
| 11 | Criterii de atribuire | 01 | 187, 188, 189, 190, 191, 192 |
| 11 | Criterii de atribuire | 03 | 32, 33, 34 |
| 12 | Stabilirea garanțiilor de participare și de bună execuție | 03 | 35, 36, 37, 38, 39, 40, 41, 42 |
| 13 | Achiziția directă | 01 | 7 |
| 13 | Achiziția directă | 03 | 43, 44, 45, 46 |
| 14 | Derularea procedurilor de atribuire. Instrumente și tehnici specifice de atribui | 01 | 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 203, 204, 205, 206 |
| 14 | Derularea procedurilor de atribuire. Instrumente și tehnici specifice de atribui | 03 | 107, 108, 109, 110, 111, 112, 113, 113^1, 113^2, 113^3, 113^4, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125 |
| 15 | Comisia de evaluare și modul de lucru al acesteia. Procesul de verificare și eva | 03 | 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141 |
| 16 | Atribuirea contractelor de achiziție publică și încheierea acordurilor-cadru. Fi | 01 | 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217 |
| 16 | Atribuirea contractelor de achiziție publică și încheierea acordurilor-cadru. Fi | 03 | 142, 143, 144, 145, 146, 147, 148, 149 |
| 17 | Executarea contractului de achiziție publică / acordului-cadru. Subcontractarea. | 01 | 218, 219, 220, 221, 222, 222^1, 222^2 |
| 17 | Executarea contractului de achiziție publică / acordului-cadru. Subcontractarea. | 03 | 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 165^1, 166 |
| 18 | Programul anual al achizițiilor publice | 03 | 12, 13, 14 |
| 19 | Activitatea de control ex ante. Metodologia de selecție. Inițierea controlului e | 04 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 |
| 19 | Activitatea de control ex ante. Metodologia de selecție. Inițierea controlului e | 05 | I |
| 19 | Activitatea de control ex ante. Metodologia de selecție. Inițierea controlului e | 06 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 |
| 20 | Remedii și căi de atac în atribuirea contractelor de achiziție publică. Contesta | 07 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 |
| 21 | Soluții de pronunțare, căi de atac | 07 | 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 36^1 |
| 22 | Fazele pe care le parcurg cheltuielile din fondurile publice și definirea acesto | 08 | preambul, 1, 1^1, 2, 3 |
| 22 | Fazele pe care le parcurg cheltuielile din fondurile publice și definirea acesto | 09 | preambul, pct. 1, pct. 2, pct. 3, pct. 4 |
| 23 | Venituri și cheltuieli | 10 | 1, 2, 3, 4, 5, 6, 7, 7^1, 8, 9, 10, 11, 12, 13, 14, 14^1, 15, 26, 27, 28, 28^1, 28^2, 28^3, 28^4, 28^5, 29, 30, 30^1, 30^2, 30^3, 30^4, 30^5, 62, 63, 64, 65, 66, 67, 68, 69, 70 |
| 24 | Rolul și responsabilitatea ordonatorilor de credite. Aprobarea bugetului de stat | 10 | 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 31, 31^1, 32, 33, 34, 35, 35^1, 36, 37, 52 |

## 3. Schema unei întrebări (JSON, într-un array)

```json
{
  "id": "L98-N0101",
  "tip": "unic",
  "intrebare": "Potrivit Legii nr. 98/2016, ...?",
  "variante": ["...", "...", "...", "..."],
  "corecte": [2],
  "explicatie": "De ce e corect + de ce fiecare distractor e greșit, cu articolul de unde vine valoarea lui.",
  "sursa": {
    "act": "Legea nr. 98/2016 privind achizițiile publice",
    "articol": "art. 7 alin. (1) lit. a)",
    "citat": "fragment verbatim [...] alt fragment verbatim",
    "fisier": "01_Legea_98-2016_achizitii_publice.txt"
  },
  "status": "ok"
}
```

- `id`: `<PREFIX>-N<lot><nn>` (N = întrebare nouă; nu se ciocnește cu id-urile migrate `L98A-001` etc.).
  Prefixe: `L98`, `HG395`, `N395`, `OUG98`, `HG419`, `N419`, `L101`, `ORD1792`, `ALOP`, `L500`.
- `tip`: `"unic"` (exact 4 variante, exact 1 corectă) sau `"multiplu"` (4 variante, 2–3 corecte).
  Câmpul `test` NU se completează — îl pune `asambleaza.py`.
- `sursa.act` — exact una dintre valorile (cele din banca existentă):
  - `Legea nr. 98/2016 privind achizițiile publice`
  - `H.G. nr. 395/2016`
  - `Normele metodologice de aplicare a Legii nr. 98/2016 (anexa la H.G. nr. 395/2016)`
  - `O.U.G. nr. 98/2017 privind funcția de control ex ante`
  - `H.G. nr. 419/2018`
  - `Normele metodologice de aplicare a O.U.G. nr. 98/2017 (anexa nr. 1 la H.G. nr. 419/2018)`
  - `Legea nr. 101/2016 privind remediile și căile de atac`
  - `Ordinul M.F.P. nr. 1.792/2002 (ALOP)`
  - `Normele metodologice ALOP (anexa la Ordinul M.F.P. nr. 1.792/2002)`
  - `Legea nr. 500/2002 privind finanțele publice`
- `sursa.fisier`: numele fișierului `.txt` (fără cale). Fără `sursa.anexa` (normele sunt fișiere proprii).
- `sursa.articol`: forma recunoscută de `unitati.eticheta` — `art. 7 alin. (5)`, `art. 113^1`,
  `art. V pct. 24 (...)` (H.G. 419, cifre romane), `pct. 3 (ordonanțarea cheltuielilor)` (Normele ALOP),
  `preambul`. Se scrie unitatea **în care se află citatul**.
- `sursa.citat`: text **verbatim** din `.txt` (copiat, nu rescris), maximum ~600 de caractere; fragmentele
  sărite se marchează cu ` [...] `; **toate fragmentele din aceeași unitate** (celelalte articole se numesc în
  explicație). Fără citate din `§NOTA§`. Atenție la spațiile după „/" din text („ofertelor/ofertanților").
- `status`: `"ok"`; `"de verificat"` doar dacă textul e ambiguu/contradictoriu, iar explicația descrie
  problema în loc să inventeze un răspuns.

## 4. Reguli de calitate (verificate de un agent adversarial, care NU a scris întrebarea)

1. **Un singur răspuns corect** la `unic`: niciun distractor nu poate fi apărat ca fiind și el corect, nici
   printr-o excepție din alt alineat/articol vecin. Caută explicit excepțiile înainte de a scrie cheia.
2. **Distractori plauzibili**: valori, termene, procente, praguri, organe, proceduri reale din **aceeași lege**
   sau din actul „pereche" (Legea 98/2016 vs. Normele H.G. 395; O.U.G. 98/2017 vs. Normele ei; Legea 500/2002 vs.
   Normele ALOP), dar cu alt rol. Nu distractori absurzi.
3. **Enunț autonom**: numește actul („Potrivit Legii nr. 98/2016, ..." / „Potrivit Normelor metodologice aprobate
   prin H.G. nr. 395/2016, ..."). Legea și normele au reguli apropiate — întrebarea spune care dintre ele. Dacă
   răspunsul depinde de tipul contractului, de valoare față de praguri sau de procedură, enunțul le precizează.
4. **Explicația** (4–8 propoziții): de ce e corect răspunsul, cu articolul; de ce e greșit fiecare distractor,
   **cu articolul de unde vine valoarea lui**; capcana tipică de examen, dacă există.
5. **Fără referiri la poziția variantelor** („a doua variantă", „varianta B)", „primele trei") — variantele se
   amestecă la asamblare; se numește conținutul variantei.
6. **Fără întrebări triviale de lexic** și fără numere de Monitor Oficial, date de publicare sau istoricul
   modificărilor. Se testează norma în vigoare.
7. **Nivelul de examen**: termene, praguri, condiții cumulative (multiplu!), competențe (cine aprobă/decide),
   cuantumuri, procente (garanții), excepții, enumerări, etapele procedurii.
8. **Lecții din proiectul-model și din verificarea băncii**: ultima propoziție a explicației e tot o trimitere la
   text, nu o concluzie generală („legea nu mai prevede...", „în toate cazurile..."); distractorii care diferă de
   cheie doar printr-un sinonim sunt interziși — diferența trebuie să fie de drept; la `multiplu` se alternează
   2/4 și 3/4 corecte; termenele se scriu cu unitatea exactă din text („zile lucrătoare"/„zile"); un act din
   AFARA corpusului (Legea 99/2016, Legea 100/2016, Codul civil, Codul de procedură civilă) nu se citează cu
   articol și cifre neverificabile.

## 5. Capcane cunoscute ale materiei (de verificat în text înainte de a scrie)

- **Praguri**: art. 7 din Legea 98/2016 (pragurile europene, revizuite periodic — valorile din textul la zi) vs.
  pragurile achiziției directe (art. 7 alin. (5)); nu se folosesc valori din memorie sau din materiale de curs.
- **Notificarea achizițiilor directe** e în Legea 98/2016 art. 7 alin. (8) (trimestrial), nu în Normele H.G. 395
  (art. 46 abrogat) — capcană reală găsită în bancă.
- **Normele H.G. 395** au multe articole abrogate în forma la zi (art. 2 alin. (1), 23–25, 28, 36, 38, 40, 42–44,
  46, 93, 101, 164, 165^1): nu se scriu întrebări pe conținutul lor.
- **Garanții**: garanția de participare (max. 2%) vs. garanția de bună execuție (max. 10%) — procentele și
  regulile de restituire din textul la zi (unele reguli s-au mutat din Norme în Lege, de ex. art. 154^1).
- **Legea 101/2016**: termenele de contestare (art. 8: 10 / 7 zile, după prag) vs. termenele de soluționare
  (art. 24–25); notificarea prealabilă (art. 6–7) este abrogată.
- **O.U.G. 98/2017**: art. 8 este abrogat; termenele ANAP din control și conciliere — numai din text.
- **Normele ALOP**: fazele angajare → lichidare → ordonanțare → plată (pct. 1–4); pct. 5 (contabilitatea
  angajamentelor) NU e în tematică.
- **Legea 500/2002**: ordonatorii principali / secundari / terțiari (art. 20–22); calendarul bugetar și aprobarea
  bugetului de stat (art. 31–37).

## 6. Formatul livrării

- Fișier `tools/nou/<PREFIX>-N<lot>.json` = un array JSON valid (UTF-8, diacritice ș/ț cu virgulă). Fără
  comentarii, fără virgule finale.
- La final agentul rulează din `quiz-app/tools/`:
  `python3 valideaza.py nou/<fisier>.json && python3 check_citat.py nou/<fisier>.json && python3 check_articol.py nou/<fisier>.json && python3 check_semantic.py --doar-pozitionale nou/<fisier>.json`
  și repară tot ce nu trece **înainte** de a raporta. Raportul final conține ieșirea celor patru comenzi, verbatim.
