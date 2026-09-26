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
print("OK: %d cazuri" % len(CAZURI) if not esec else "%d eșecuri" % esec); sys.exit(1 if esec else 0)
