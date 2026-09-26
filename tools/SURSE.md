# Surse — formele consolidate descărcate de pe legislatie.just.ro

Descărcate la 27.09.2026 cu `descarca.py <id> <nume>` în `Examen-Achizitii/legislatie/` (în afara depozitului).
Datele de consolidare coincid cu cele din pachetul PDF din august 2026.

| Fișier | Id portal (ales după consolidări) | Act | Consolidare |
|---|---|---|---|
| `01_Legea_98-2016_achizitii_publice.txt` | 178667 | Legea nr. 98/2016 | 17.11.2024 |
| `02_HG_395-2016_act_de_aprobare.txt` | 179009 | H.G. nr. 395/2016 (actul de aprobare) | 25.02.2026 |
| `03_Norme_HG_395-2016_achizitii_publice.txt` | 307053 | Normele metodologice (anexa la H.G. 395/2016) | 25.02.2026 |
| `04_OUG_98-2017_control_ex_ante.txt` | 195762 | O.U.G. nr. 98/2017 | 30.08.2021 |
| `05_HG_419-2018_act_de_aprobare.txt` | 201548 | H.G. nr. 419/2018 (actul de aprobare; Anexa nr. 2 = structura ANAP) | 29.12.2023 |
| `06_Norme_HG_419-2018_control_ex_ante.txt` | 269779 | Normele de aplicare a O.U.G. 98/2017 (anexa nr. 1 la H.G. 419/2018) | 29.12.2023 |
| `07_Legea_101-2016_remedii_si_cai_de_atac.txt` | 178680 | Legea nr. 101/2016 | 06.04.2023 |
| `08_Ordinul_MFP_1792-2002_act_de_aprobare.txt` | 41403 | Ordinul M.F.P. nr. 1.792/2002 (actul de aprobare) | 28.12.2022 |
| `09_Norme_ALOP_1792-2002.txt` | 206786 → 262742 | Normele ALOP (anexa la Ordinul 1.792/2002) | 28.12.2022 |
| `10_Legea_500-2002_finantele_publice.txt` | 37954 | Legea nr. 500/2002 | 05.10.2023 |

Numerotarea 01–10 e aceeași cu a PDF-urilor din pachetul de studiu.

## Observații de structură (intrarea Task 4)

(a) **Anexele** (`§ANEXA§`): Legea 98 — „Anexa nr. 1”, „Anexa nr. 2”; H.G. 395 (act) — „Anexă” (doar titlul + link către
Norme, document separat); Normele H.G. 395 — „Anexa nr. 1”, „Anexa nr. 2” (modele/formulare); H.G. 419 — „Anexa nr. 1” (doar titlul +
link către Norme, document separat), „Anexa nr. 2” (structura ANAP); Normele H.G. 419 — „Anexa nr. 1.1”, „1.2”, „1.3”; Ordinul 1792 (act) — „Anexă” (doar titlul); Normele ALOP —
„Anexa nr. 1”, „1a)”, „1b)”, „2”, „3”, „4” (formulare).

(b) **H.G. 419/2018** are în corp „Articolul I” … „Articolul VIII” (cifre romane). Decizia pe fiecare, după regula din spec §6.1:
- art. I — aprobă Normele O.U.G. 98/2017 → ÎN
- art. II — modifică H.G. 34/2009 (organizarea MFP) → ÎN AFARĂ
- art. III — modifică H.G. 634/2015 (organizarea ANAP) → ÎN AFARĂ
- art. IV — modifică normele sectoriale (Legea 99/2016, H.G. 394/2016) → ÎN AFARĂ
- art. V — modifică Normele H.G. 395/2016 → ÎN
- art. VI — modifică normele concesiunilor (Legea 100/2016) → ÎN AFARĂ
- art. VII — încadrarea personalului ANAP → ÎN AFARĂ
- art. VIII — abrogări → ÎN AFARĂ

(c) **Normele ALOP** nu au „Articolul N”: sunt structurate în 5 puncte de nivel 1, în corpul documentului (înainte de prima
`§ANEXA§`), cu titluri exact de forma `N. Titlu`: „1. Angajarea cheltuielilor”, „2. Lichidarea cheltuielilor”,
„3. Ordonanțarea cheltuielilor”, „4. Plata cheltuielilor”, „5. Organizarea, evidenta și raportarea angajamentelor bugetare și legale”.
`grep -c -E '^[0-9]+\.\s'` pe corp = 5.

## Diferențe față de spec (decizii)

- Pe portal, **toate trei seturile de norme** (H.G. 395/2016, O.U.G. 98/2017 prin H.G. 419/2018, ALOP) sunt documente
  separate de actele de aprobare — anexa din act conține doar titlul și un link. Se descarcă în fișiere proprii (03, 06, 09),
  ca Normele H.G. 52/2011 în proiectul RU. Rezultă 10 fișiere, numerotate ca PDF-urile.
- Corpul H.G. 419/2018 conține în art. IV–VI textul articolelor modificate ale altor norme („Articolul 26 se modifică și va
  avea următorul cuprins: Articolul 26 …”). `unitati.ZONE_SPECIALE` marchează corpul ca `DOAR_ROMANE`: unitățile sunt doar
  art. I–VIII, iar articolele arabe citate rămân text în interiorul articolului modificator.
- În temele de mai jos, art. I din corpul H.G. 419 (aprobarea normelor ex ante) e la tema 19, iar art. V (modificarea Normelor
  H.G. 395) la tema 1, lângă actul de aprobare al H.G. 395.

## Diferențe față de harta din ghid

Niciuna: intervalele temelor din `bibliografie.TEME` (luate din `00_Ghid_tematica_si_stadiul_legislatiei.pdf`, §3–4) acoperă
exact unitățile din `BIB` pe textul la zi — `test_teme.py`: „OK: trasabilitate completă”. Unități abrogate în forma la zi
(rămân în BIB, fără întrebări despre conținut): Normele H.G. 395 art. 2, 23–25, 28, 36, 38, 40, 42–44, 46, 93, 101, 164,
165^1; O.U.G. 98/2017 art. 8; Legea 101/2016 art. 6, 7, 36.

## Unități formale scoase din bibliografie (27.09.2026, după verificarea adversarială)

Verificatorii au respins ca triviale (SPEC §4.6) întrebările pe unități fără conținut normativ de examen; în loc să
păstrăm întrebări slabe doar pentru acoperire, unitățile ies din `BIB`:
- Normele H.G. 419/2018, art. 21 — „anexele nr. 1.1–1.3 fac parte integrantă din prezentele norme”;
- Ordinul M.F.P. nr. 1.792/2002, preambulul (lista actelor în temeiul cărora se emite) și art. 3 (publicarea în Monitorul Oficial).
