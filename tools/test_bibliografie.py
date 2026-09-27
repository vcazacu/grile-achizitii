#!/usr/bin/env python3
"""Semantica intervalelor din BIB/TEME. Rulare: python3 test_bibliografie.py"""
import sys
from bibliografie import articole_cerute
EX = ["preambul", "1", "2", "2^1", "3", "221", "222", "222^1", "222^2", "223", "I", "IV", "V", "pct. 1", "pct. 2", "pct. 5"]
CAZURI = [
 ("1-3", ["1", "2", "2^1", "3"]),
 ("221-222", ["221", "222", "222^1", "222^2"]),          # limita fără indice include indicii
 ("221-222^1", ["221", "222", "222^1"]),                  # limita cu indice e exactă
 ("*", EX),
 ("preambul, pct. 1-2", ["preambul", "pct. 1", "pct. 2"]),
 ("I, V", ["I", "V"]),
]
esec = 0
for spec, astept in CAZURI:
    r = articole_cerute(spec, EX)
    if r != astept:
        esec += 1; print("EȘEC %r → %r, așteptat %r" % (spec, r, astept))
# O unitate din mai multe teme se leagă de tema cu intervalul cel mai specific pe acel act:
# art. 7 L98 e și în tema 1 („1-8"), și în tema 13 („7", Achiziția directă) → tema 13.
import bibliografie as _b
for (k, a, astept) in [(_b.K98, "7", 13), (_b.K98, "6", 1), (_b.K98, "8", 1)]:
    r = _b.tema_articol(k, a)
    if r != astept:
        esec += 1; print("EȘEC tema_articol(%s, %s) → %r, așteptat %r" % (k, a, r, astept))
print("OK: %d cazuri" % len(CAZURI) if not esec else "%d eșecuri" % esec)
sys.exit(1 if esec else 0)
