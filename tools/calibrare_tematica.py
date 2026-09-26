#!/usr/bin/env python3
"""Separarea pragului „contrazice”: afirmațiile plantate vs. cele corecte ale aceleiași teme.
Plantatele se recunosc după fragmentele din <nr>-plantat-lista.json (început al textului nou).
Utilizare: python3 calibrare_tematica.py 01"""
import json, pathlib, sys
D = pathlib.Path(__file__).resolve().parent / "tematica"
nr = sys.argv[1]
fragmente = [f.lower() for f in json.loads((D / ("%s-plantat-lista.json" % nr)).read_text(encoding="utf-8"))]
def p_contrazice(fisier):
    out = {}
    for bloc in json.loads((D / fisier).read_text(encoding="utf-8")):
        for a in bloc.get("afirmatii", {}).values():
            out[a["text"]] = a["probabilitati"]["contrazice"]
    return out
pl = p_contrazice("%s-plantat-ts.json" % nr)
co = p_contrazice("%s-ts.json" % nr)
gasite = {}
for f in fragmente:
    for t, p in pl.items():
        if f in t.lower(): gasite[f] = max(p, gasite.get(f, 0))
p_pl = sorted(gasite.values())
p_co = sorted(co.values())
for f in fragmente: print("  %-62s %s" % (f[:62], "%.2f" % gasite[f] if f in gasite else "NEGĂSIT"))
print("plantate găsite: %d/%d; p(contrazice) min=%.2f" % (len(p_pl), len(fragmente), p_pl[0] if p_pl else -1))
print("corecte: %d afirmații; p(contrazice) max=%.2f" % (len(p_co), p_co[-1] if p_co else -1))
if p_pl and p_co and p_pl[0] > p_co[-1]:
    print("SEPARARE CURATĂ: orice prag în (%.2f, %.2f] funcționează; 0.90 %s" % (
        p_co[-1], p_pl[0], "e în interval" if p_co[-1] < 0.90 <= p_pl[0] else "NU e în interval"))
else:
    print("NESEPARABIL: pragul nu poate prinde toate plantatele fără alarme false")
