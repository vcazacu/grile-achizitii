#!/usr/bin/env python3
"""Teste pentru unitati.py. Rulare: python3 test_unitati.py"""
import re, sys
import unitati as u

PCT = re.compile(r"^(\d+)\.\s+[A-ZĂÂÎȘȚ]")
CAZURI = [
 # (funcție, argumente, rezultat așteptat)
 (u.eticheta_titlu, ("Articolul 113^1", None), "113^1"),
 (u.eticheta_titlu, ("Articolul IV", None), "IV"),
 (u.eticheta_titlu, ("Articolul 5 din lege", None), None),
 (u.eticheta_titlu, ("3. Ordonanțarea cheltuielilor", PCT), "pct. 3"),
 (u.eticheta_titlu, ("3. Ordonanțarea cheltuielilor", None), None),        # în afara zonelor de puncte
 (u.eticheta, ("art. 20^1 alin. (2) lit. b)",), "20^1"),
 (u.eticheta, ("art. V pct. 35 (art. 37 alin. (3) din normele aprobate prin H.G. nr. 395/2016)",), "V"),
 (u.eticheta, ("art. I",), "I"),
 (u.eticheta, ("pct. 1 (angajarea cheltuielilor)",), "pct. 1"),
 (u.eticheta, ("Norme ALOP, pct. 4 (plata cheltuielilor)",), "pct. 4"),
 (u.eticheta, ("formula introductivă (preambul)",), "preambul"),
 (u.eticheta, ("Norme ALOP, preambul",), "preambul"),
 (u.eticheta, ("nota la actul normativ — art. IV alin. (1) din H.G. nr. 336/2023",), None),   # notă: nu e unitate
 (u.eticheta, ("art. Legea",), None),
 (u.ancora, ("20^1",), "art-20-1"),
 (u.ancora, ("IV",), "art-IV"),
 (u.ancora, ("pct. 3",), "pct-3"),
 (u.ancora, ("preambul",), "preambul"),
 (u.ancora, ("7", "Anexa nr. 1"), "anexa-anexa-nr-1-art-7"),
]
ORDINE = ["preambul", "1", "2", "2^1", "9", "10", "IV", "V", "VIII"]
esec = 0
for f, args, astept in CAZURI:
    r = f(*args)
    if r != astept:
        esec += 1; print("EȘEC %s%r → %r, așteptat %r" % (f.__name__, args, r, astept))
if sorted(reversed(ORDINE), key=u.cheie) != ORDINE:
    esec += 1; print("EȘEC ordinea: %r" % sorted(ORDINE, key=u.cheie))
if u.cheie("I") <= u.cheie("3") or u.cheie("pct. 1") <= u.cheie("IV"):
    esec += 1; print("EȘEC: tipurile de unități nu sunt separate (un interval arab ar prinde art. I)")
if u.cheie("pct. 2") >= u.cheie("pct. 10"):
    esec += 1; print("EȘEC ordinea punctelor")
linii = ["HOTĂRÂRE", "Având în vedere …", "Articolul 1", "(1) text", "Articolul 2", "text"]
z = u.unitati_zona(linii, None)
if [e for e, _ in z if e] != ["preambul", "1", "2"] or z[1] != (None, "HOTĂRÂRE"):
    esec += 1; print("EȘEC unitati_zona: %r" % z)
import pathlib
LEG = pathlib.Path(__file__).resolve().parent.parent.parent / "legislatie"
if (LEG / "05_HG_419-2018_norme_control_ex_ante.txt").is_file():
    import normalizare, bibliografie
    corp = normalizare.linii_zona("05_HG_419-2018_norme_control_ex_ante.txt", "")
    romane = [e for e, _ in corp if e and re.match(r"^[IVX]+$", e)]
    if romane != ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]:
        esec += 1; print("EȘEC: corpul H.G. 419 — articolele romane recunoscute: %r" % romane)
    for cheie_bib in u.ZONE_PUNCTE:
        fis, _, anexa = cheie_bib.partition("#")
        pct = [e for e, _ in normalizare.linii_zona(fis, anexa) if e and e.startswith("pct. ")]
        if pct != ["pct. 1", "pct. 2", "pct. 3", "pct. 4", "pct. 5"]:
            esec += 1; print("EȘEC: punctele din %s: %r" % (cheie_bib, pct))
        arts = bibliografie.articole_din_text(str(LEG / fis), anexa)
        if sorted(arts, key=u.cheie)[:6] != ["preambul", "pct. 1", "pct. 2", "pct. 3", "pct. 4", "pct. 5"]:
            esec += 1; print("EȘEC: articole_din_text pe %s: %r" % (cheie_bib, sorted(arts, key=u.cheie)[:8]))
    if normalizare.eticheta_articol("art. V pct. 24 (art. 26 din normele)") != "V":
        esec += 1; print("EȘEC: normalizare.eticheta_articol nu trece prin unitati")
    import check_citat
    corpus = check_citat.corpus_zona("08_Norme_ALOP_1792-2002.txt", "", {})
    if "3. ordonanțarea cheltuielilor" not in corpus:
        esec += 1; print("EȘEC: titlul punctului 3 ALOP nu e citabil")
    print("regresie pe texte reale: rulată")
print("OK: %d cazuri" % (len(CAZURI) + 4) if not esec else "%d eșecuri" % esec)
sys.exit(1 if esec else 0)
