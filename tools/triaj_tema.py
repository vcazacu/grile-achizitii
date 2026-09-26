#!/usr/bin/env python3
"""Afirmațiile unei teme cu p(contrazice) ≥ prag (implicit 0,50) — banda de triaj manual din CALIBRARE-typesafe.md.
Utilizare: python3 triaj_tema.py 07 [--prag 0.5]"""
import json, pathlib, sys
nr = sys.argv[1]; prag = float(sys.argv[sys.argv.index("--prag") + 1]) if "--prag" in sys.argv else 0.5
D = pathlib.Path(__file__).resolve().parent / "tematica"
n = 0
for bloc in json.loads((D / ("%s-ts.json" % nr)).read_text(encoding="utf-8")):
    for a in bloc.get("afirmatii", {}).values():
        p = a["probabilitati"]["contrazice"]
        if p >= prag:
            n += 1; print("%.2f | %s | %s" % (p, bloc["loc"][:60], a["text"]))
print("triaj tema %s: %d afirmații cu p(contrazice) ≥ %.2f" % (nr, n, prag))
