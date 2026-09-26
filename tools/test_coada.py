#!/usr/bin/env python3
"""Rulare: python3 test_coada.py"""
import sys
from aplica_coada import aplica
Q = lambda i, t="x": {"id": i, "intrebare": t}
intr = [Q("A-1"), Q("A-2"), Q("A-3")]
verd = [{"id": "A-1", "clasa": "forma", "motiv": "m", "intrebare": Q("A-1", "reancorat")},
        {"id": "A-3", "clasa": "eliminare", "motiv": "abrogat", "intrebare": None}]
ram, elim = aplica(intr, verd)
esec = 0
if [q["id"] for q in ram] != ["A-1", "A-2"] or ram[0]["intrebare"] != "reancorat": esec += 1; print("EȘEC rămase", ram)
if [q["id"] for q in elim] != ["A-3"]: esec += 1; print("EȘEC eliminate", elim)
for rau in ({"id": "A-9", "clasa": "forma", "motiv": "m", "intrebare": Q("A-9")},      # id inexistent
            {"id": "A-2", "clasa": "fond", "motiv": "m", "intrebare": Q("A-7")},       # id schimbat
            {"id": "A-2", "clasa": "altceva", "motiv": "m", "intrebare": Q("A-2")}):    # clasă necunoscută
    try: aplica(intr, [rau]); esec += 1; print("EȘEC: acceptat", rau)
    except ValueError: pass
print("OK" if not esec else "%d eșecuri" % esec); sys.exit(1 if esec else 0)
