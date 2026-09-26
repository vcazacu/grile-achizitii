#!/usr/bin/env python3
"""Detectorul de referiri la poziția variantelor. Rulare: python3 test_pozitionale.py"""
import sys
from check_semantic import referiri_pozitionale as rp
DA = [
 "Varianta b) este greșită, deoarece termenul e de 10 zile.",
 "Distractorul din varianta D confundă garanția de participare.",
 "Prima definește angajamentul legal, iar a treia definește angajamentul bugetar.",
 "Varianta A) reproduce art. 7.",
 "răspunsul C) e cel corect",
 "Variantele A și C sunt corecte.",
 "Varianta a patra contrazice art. 12.",
 "primele trei variante sunt corecte",
 "formularea variantei a doua e incompletă",
 "capcana primei variante este termenul",
 "ca în cea de-a treia variantă",
 "variantele a), c) și d) sunt corecte",
 "Varianta de la indicele 2 este falsă.",
 "iar cea de la indicele 3 este definiția ordonanțării",
 "varianta cu indexul 1 confundă fazele",
 "Valoarea reziduală (distractorul d)) se adaugă în alt caz",
 "distractorii b) și c) inversează regula",
]
NU = [
 "Varianta a fost introdusă prin Legea nr. 208/2022.",
 "Termenul curge din a treia zi lucrătoare.",
 "A doua etapă a procedurii începe cu invitația.",
 "Varianta cu termenul de 10 zile e greșită.",
 "potrivit lit. a) și b) din art. 7",
 "Ultima teză a alin. (2) prevede excepția.",
 "prima perioadă curge de la publicare, iar a doua de la transmiterea invitației",
 "indicele prețurilor de consum publicat de INS",
 "potrivit lit. d) din art. 7, distractorul din litera b) a alin. (2)",
]
esec = [("ratat", t) for t in DA if not rp({"explicatie": t})] + [("fals", t, rp({"explicatie": t})) for t in NU if rp({"explicatie": t})]
for e in esec: print("EȘEC", *e)
print("OK: %d cazuri" % (len(DA) + len(NU)) if not esec else "%d eșecuri" % len(esec)); sys.exit(1 if esec else 0)
