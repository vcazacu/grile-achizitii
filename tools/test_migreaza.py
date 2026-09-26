#!/usr/bin/env python3
"""Rulare: python3 test_migreaza.py"""
import sys
import bibliografie as b
from migreaza import converteste

def q(fisier, articol, qid="X-001"):
    return {"id": qid, "tip": "unic", "test": 7, "intrebare": "?", "variante": ["a", "b", "c", "d"],
            "corecte": [0], "explicatie": "e", "status": "ok",
            "sursa": {"act": "A", "articol": articol, "citat": "c", "fisier": fisier}}

CAZURI = [
 ("01_Legea_98-2016_achizitii_publice.pdf", "art. 7 alin. (5)", b.K98, "art. 7 alin. (5)"),
 ("02_HG_395-2016_act_normativ.pdf", "art. 2 lit. a) și b)", b.K395C, "art. 2 lit. a) și b)"),
 ("03_Norme_metodologice_HG_395-2016.pdf", "art. 43 alin. (4)", b.K395, "art. 43 alin. (4)"),
 ("04_OUG_98-2017_control_ex_ante.pdf", "art. 9", b.KOUG, "art. 9"),
 ("05_HG_419-2018_act_normativ.pdf", "art. V pct. 24 (art. 26 din normele aprobate prin H.G. nr. 395/2016)", b.K419C, "art. V pct. 24 (art. 26 din normele aprobate prin H.G. nr. 395/2016)"),
 ("06_Norme_metodologice_HG_419-2018.pdf", "art. 5", b.K419, "art. 5"),
 ("07_Legea_101-2016_remedii_si_cai_de_atac.pdf", "art. 8 alin. (1)", b.K101, "art. 8 alin. (1)"),
 ("08_Ordinul_MFP_1792-2002_ALOP.pdf", "art. 1^1", b.KORD, "art. 1^1"),
 ("09_Norme_metodologice_ALOP_1792-2002.pdf", "Norme ALOP, pct. 3 (ordonanțarea cheltuielilor)", b.KALOP, "pct. 3 (ordonanțarea cheltuielilor)"),
 ("09_Norme_metodologice_ALOP_1792-2002.pdf", "Norme ALOP, preambul", b.KALOP, "preambul"),
 ("10_Legea_500-2002_finantele_publice.pdf", "art. 22", b.K500, "art. 22"),
]
esec = 0
for fis, art, fis_nou, art_nou in CAZURI:
    nq, harta = converteste(q(fis, art))
    s = nq["sursa"]
    if (s["fisier"], s.get("anexa", ""), s["articol"]) != (fis_nou, "", art_nou):
        esec += 1; print("EȘEC %s | %s → %r" % (fis, art, (s["fisier"], s.get("anexa", ""), s["articol"])))
    if "test" in nq or nq["id"] != "X-001" or harta != {"fisier_pdf": fis, "articol_vechi": art}:
        esec += 1; print("EȘEC câmpuri/hartă pentru %s" % fis)
try:
    converteste(q("99_necunoscut.pdf", "art. 1")); esec += 1; print("EȘEC: PDF necunoscut acceptat")
except KeyError:
    pass
print("OK: %d cazuri" % (len(CAZURI) + 1) if not esec else "%d eșecuri" % esec)
sys.exit(1 if esec else 0)
