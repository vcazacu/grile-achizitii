#!/usr/bin/env python3
"""Aplică verdictele din coada de reparat peste nou/*-migrat.json.
Utilizare: python3 aplica_coada.py coada/verdict-*.json"""
import glob, json, os, sys
DIR = os.path.dirname(os.path.abspath(__file__))
CLASE = {"forma", "fond", "nota", "eliminare"}

def aplica(intrebari, verdicte):
    ids = {q["id"] for q in intrebari}
    pe_id = {}
    for v in verdicte:
        if v["clasa"] not in CLASE: raise ValueError("%s: clasă necunoscută %r" % (v["id"], v["clasa"]))
        if v["id"] not in ids: raise ValueError("%s: id inexistent în bancă" % v["id"])
        if v["clasa"] != "eliminare" and (v.get("intrebare") or {}).get("id") != v["id"]:
            raise ValueError("%s: întrebarea reparată are alt id" % v["id"])
        pe_id[v["id"]] = v
    ram, elim = [], []
    for q in intrebari:
        v = pe_id.get(q["id"])
        if v is None: ram.append(q)
        elif v["clasa"] == "eliminare": elim.append(q)
        else: ram.append(v["intrebare"])
    return ram, elim

def main(argv):
    verdicte = [v for f in argv for v in json.load(open(f, encoding="utf-8"))]
    aplicate, toate_elim = set(), []
    for f in sorted(glob.glob(os.path.join(DIR, "nou", "*-migrat.json"))):
        lista = json.load(open(f, encoding="utf-8"))
        ids = {q["id"] for q in lista}
        ale_lui = [v for v in verdicte if v["id"] in ids]
        ram, elim = aplica(lista, ale_lui)
        json.dump(ram, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        toate_elim += elim; aplicate |= {v["id"] for v in ale_lui}
    orfane = [v["id"] for v in verdicte if v["id"] not in aplicate]
    if orfane:
        raise SystemExit("verdicte fără întrebare în nou/*-migrat.json: %s" % ", ".join(orfane))
    cale = os.path.join(DIR, "nou", "_eliminate.json")
    vechi = json.load(open(cale, encoding="utf-8")) if os.path.exists(cale) else []
    json.dump(vechi + toate_elim, open(cale, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("verdicte aplicate: %d; eliminate: %d" % (len(verdicte), len(toate_elim)))

if __name__ == "__main__":
    main(sys.argv[1:])
