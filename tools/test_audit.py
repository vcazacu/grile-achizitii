#!/usr/bin/env python3
"""Rulare: python3 test_audit.py"""
import sys
from audit_tematica import numere
CAZURI = [
 ("pragul este de 27.334.460 lei", {"27334460"}),
 ("aceeași valoare scrisă 27 334 460 lei", {"27334460"}),
 ("pragul este de 26 960 556 lei", {"26960556"}),
 ("garanția de participare nu poate depăși 2% din valoarea estimată", {"2"}),
 ("un termen de 10 zile, respectiv 5 zile", {"10", "5"}),
 ("art. 28–30 din Legea 98/2016", set()),
 ("cota de 2,5% din valoare", {"2.5"}),
]
esec = 0
for text, astept in CAZURI:
    r = numere(text)
    if r != astept: esec += 1; print("EȘEC %r → %r, așteptat %r" % (text, r, astept))

# Rezumatul și capcanele: cifrele și articolele lor trebuie să apară în citatele temei.
import json, tempfile, pathlib, io, contextlib
import audit_tematica as au
T = lambda a, c: {"act": "Legea nr. 98/2016 privind achizițiile publice", "articol": a, "citat": c, "fisier": "01_Legea_98-2016_achizitii_publice.txt"}
tema = {"nr": 99, "titlu": "Test", "rezumat": "Termenul e de 35 de zile, dar și 99 de zile.", "capcane": ["Garanția: 7%; art. 999 nu există în temei."],
        "sectiuni": [{"titlu": "S1", "paragrafe": ["Cel puțin 35 de zile."], "temei": [T("art. 74 alin. (1)", "este de cel puțin 35 de zile")]}],
        "intrebari": []}
_, probleme, _ = au.audit_dict(tema, set())
gasite = {(p[0], p[1], p[3]) for p in probleme}
for astept in [("CIFRĂ", "rezumat", "99"), ("CIFRĂ", "capcane", "7"), ("ART.", "capcane", "art. 999")]:
    if astept not in gasite: esec += 1; print("EȘEC audit: lipsește %r din %r" % (astept, sorted(gasite)))
if ("CIFRĂ", "rezumat", "35") in gasite: esec += 1; print("EȘEC audit: 35 e în citat, nu trebuia semnalat")
# codul de ieșire: 1 când auditul găsește probleme, 0 pe o temă curată
with tempfile.TemporaryDirectory() as tmp:
    vechi = au.DIR; au.DIR = pathlib.Path(tmp)
    (au.DIR / "99.json").write_text(json.dumps(tema, ensure_ascii=False), encoding="utf-8")
    curata = dict(tema, rezumat="Termenul e de 35 de zile.", capcane=[])
    (au.DIR / "98.json").write_text(json.dumps(curata, ensure_ascii=False), encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()):
        c99, c98 = au.main(["99"]), au.main(["98"])
    au.DIR = vechi
if c99 != 1: esec += 1; print("EȘEC audit: cod de ieșire %r pe o temă cu probleme, așteptat 1" % c99)
if c98 != 0: esec += 1; print("EȘEC audit: cod de ieșire %r pe o temă curată, așteptat 0" % c98)
print("OK: %d cazuri + auditul rezumatului/capcanelor și codul de ieșire" % len(CAZURI) if not esec else "%d eșecuri" % esec); sys.exit(1 if esec else 0)
