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
print("OK: %d cazuri" % len(CAZURI) if not esec else "%d eșecuri" % esec)
sys.exit(1 if esec else 0)
