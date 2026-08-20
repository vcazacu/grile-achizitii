# Grile — Achiziții Publice

Aplicație de tip quiz pentru pregătirea examenului, construită pe legislația în
formă consolidată din PDF-urile pachetului de studiu (legislatie.just.ro).

Bateria are **30 de teste a câte 20 de întrebări** (600 în total, dintre care
maximum 4 cu răspunsuri multiple pe test). Scorul cel mai bun al fiecărui test
se salvează local în browser (localStorage) și apare pe grila de teste.

## Cum o folosești

Deschide `index.html` cu dublu-click — merge în orice browser, pe telefon,
tabletă sau calculator, **complet offline**, fără server și fără instalare.

Pe telefon: copiază folderul `quiz-app` (AirDrop / e-mail / cloud), deschide
`index.html` din aplicația de fișiere, apoi „Adaugă la ecranul principal”
din meniul browserului dacă vrei acces rapid.

## Cum adaugi întrebări

Toate întrebările stau în **`intrebari.js`** — un singur fișier de date, separat
de aplicație. Copiază un obiect existent și completează câmpurile:

| Câmp | Ce conține |
|---|---|
| `id` | identificator unic scurt, ex. `"L98-loturi"` |
| `tip` | `"unic"` (un răspuns corect din 4) sau `"multiplu"` (mai multe corecte) |
| `intrebare` | textul întrebării |
| `variante` | lista variantelor (exact 4 la tip `"unic"`) |
| `corecte` | indecșii variantelor corecte, numărați de la 0 |
| `explicatie` | explicația detaliată afișată după răspuns |
| `sursa` | `{ act, articol, citat, fisier }` — temeiul legal exact, cu citat din PDF |
| `status` | `"ok"` sau `"de verificat"` (dacă textul legal e ambiguu/contradictoriu) |
| `test` | numărul testului din care face parte întrebarea (1–30) |

Reguli pe test, verificate automat: fiecare test are exact 20 de întrebări și
cel mult 4 de tip `"multiplu"`.

**Validare automată:** la fiecare deschidere, aplicația verifică structura
tuturor întrebărilor. Dacă ai greșit ceva (index inexistent, câmp lipsă,
id duplicat etc.), pe ecranul principal apare un banner roșu cu lista exactă
a problemelor, iar testul nu pornește până nu le corectezi.

**Reguli de calitate** (cele folosite la întrebările existente):
- distractorii să fie plauzibili — ideal valori/termene reale din aceeași lege, dar cu alt rol;
- explicația să spună și *de ce* distractorii sunt greșiți;
- citatul din `sursa.citat` să fie textul exact din PDF, nu parafrazare;
- dacă un articol e abrogat, ambiguu sau contrazis de altul, marchează `status: "de verificat"`.

## Fișiere

- `index.html` — pagina aplicației (deschide-o pe aceasta)
- `app.js` — logica quiz-ului (nu trebuie atinsă când adaugi întrebări)
- `style.css` — stilurile (design inspirat din shadcn/ui, temă light/dark automată)
- `intrebari.js` — **banca de întrebări** (aici lucrezi)

## Publicare și actualizare

Aplicația e publicată pe GitHub Pages, din depozitul `vcazacu/grile-achizitii`:

**https://vcazacu.github.io/grile-achizitii/**

Pe telefon sau tabletă: deschide adresa în browser, lasă pagina să se încarce
complet, apoi „Adaugă la ecranul principal”. Service worker-ul (`sw.js`) salvează
local toate fișierele, așa că de la a doua deschidere aplicația funcționează
**complet fără internet** — verificat pe iPad cu modul avion.

### Când modifici întrebările

Trebuie schimbate **două** fișiere, nu doar unul:

1. `intrebari.js` — întrebările propriu-zise;
2. `sw.js` — incrementează `VERSIUNE` (`grile-achizitii-v1` → `v2` etc.).

Fără al doilea pas, dispozitivele care au deja aplicația salvată rămân cu
versiunea veche în memorie, pentru că service worker-ul servește din cache
înaintea rețelei.

Apoi:

```bash
git add -A && git commit -m "Actualizare întrebări" && git push
```

GitHub Pages republică automat în 1–2 minute.

## Acoperirea materiei

Cele 600 de întrebări sunt distribuite pe acte proporțional cu ponderea lor în
tematica de examen:

| Act normativ | Întrebări |
|---|---:|
| Legea nr. 98/2016 – achizițiile publice | 204 |
| Norme metodologice (anexa la H.G. nr. 395/2016) | 119 |
| Legea nr. 101/2016 – remedii și căi de atac | 82 |
| Legea nr. 500/2002 – finanțele publice | 71 |
| O.U.G. nr. 98/2017 – controlul ex ante | 45 |
| Norme metodologice ALOP (Ordinul M.F.P. nr. 1.792/2002) | 36 |
| Norme metodologice de aplicare a O.U.G. nr. 98/2017 | 28 |
| H.G. nr. 419/2018 | 8 |
| Ordinul M.F.P. nr. 1.792/2002 – actul de aprobare | 4 |
| H.G. nr. 395/2016 – actul de aprobare | 3 |

Fiecare test conține întrebări din 6–7 acte diferite, în proporții apropiate de
cele din tabel — deci orice test luat la întâmplare e reprezentativ pentru
examen, nu concentrat pe un singur act.

## Cum au fost verificate întrebările

Fiecare întrebare a trecut două verificări automate contra textului extras din
PDF-urile din folderul părinte (cu `pdftotext -layout`):

1. **Citatul apare verbatim în sursă.** Textul din `sursa.citat` este căutat în
   PDF-ul indicat, după normalizarea despărțirilor la capăt de rând și a
   diacriticelor. Fragmentele sărite se marchează cu `[...]`.
2. **Articolul declarat corespunde locului real al citatului.** Se identifică
   titlul de articol care precedă efectiv citatul în lege și se compară cu
   `sursa.articol` — asta prinde atribuirile greșite (de exemplu un citat din
   normele sectoriale prezentat ca fiind din cele clasice).

3. **Verificare semantică adversarială** — 600/600. Fiecare întrebare a fost dată
   unui verificator independent (care nu a scris-o), cu sarcina explicită de a
   *dobori* cheia: să caute excepții în articolele vecine, distractori care ar
   putea fi și ei corecți, și afirmații false în explicații. Rezultat: 583 curate,
   14 semnalate ca discutabile, 3 cu erori. Toate cele 17 au fost corectate —
   în niciun caz cheia de răspuns nu era greșită; problemele erau în explicații
   (afirmații secundare inexacte) și în trei enunțuri.

În plus, aplicația a fost parcursă automat pe toate cele 30 de teste, verificând
că fiecare întrebare se afișează corect și că răspunsurile marcate corecte produc
scor 100%.

O singură întrebare este marcată **„de verificat"** (L98C-033, testul 22): art. 153
alin. (4) din Legea nr. 98/2016 se contrazice cu alin. (1) lit. a) al aceluiași
articol, din cauza unei transpuneri defectuoase a Directivei 2014/24/UE.
Explicația detaliază contradicția în loc să o ascundă.

Notele de modificare din formele consolidate („la 13-07-2020, Articolul X a fost
modificat de...") nu sunt folosite ca text normativ, ci doar ca istoric în
explicații. Articolele abrogate nu apar ca drept în vigoare — dar câteva
întrebări testează chiar faptul abrogării, fiindcă e o capcană frecventă
(de exemplu notificarea prealabilă din Legea 101/2016, eliminată în 2018).
