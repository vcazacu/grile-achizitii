#!/usr/bin/env python3
"""Selectează pentru verificarea adversarială: întrebările noi (id-uri absente din harta
de migrare), cele modificate „fond”/„nota” în coada de reparat, toate cele „multiplu”,
cele cu explicația rescrisă la repararea referirilor poziționale și cele din adv-extra.txt.
Scrie verificari/adv-lot-NN.json (loturi de 30). Utilizare: python3 adversarial.py"""
import glob, json, os
from valideaza import incarca
DIR = os.path.dirname(os.path.abspath(__file__))
banca = incarca(os.path.join(DIR, "..", "intrebari.js"))
harta = json.load(open(os.path.join(DIR, "nou", "_harta-migrare.json"), encoding="utf-8"))
fond = {v["id"] for f in glob.glob(os.path.join(DIR, "coada", "verdict-*.json"))
        for v in json.load(open(f, encoding="utf-8")) if v["clasa"] in ("fond", "nota")}
def lista(nume):
    p = os.path.join(DIR, nume)
    return {l.strip() for l in open(p, encoding="utf-8") if l.strip()} if os.path.exists(p) else set()
rescrise, extra = lista("coada/pozitionale-reparate.txt"), lista("adv-extra.txt")
motiv = lambda q: [m for m, ok in (("nou", q["id"] not in harta), ("fond", q["id"] in fond), ("multiplu", q["tip"] == "multiplu"),
                                     ("rescrisă", q["id"] in rescrise), ("extra", q["id"] in extra)) if ok]
sel = [q for q in banca if motiv(q)]
os.makedirs(os.path.join(DIR, "verificari"), exist_ok=True)
for f in glob.glob(os.path.join(DIR, "verificari", "adv-lot-*.json")): os.remove(f)
for i in range(0, len(sel), 30):
    json.dump(sel[i:i + 30], open(os.path.join(DIR, "verificari", "adv-lot-%02d.json" % (i // 30 + 1)), "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(m for q in sel for m in motiv(q))
print("selectate: %d (%s) în %d loturi" % (len(sel), ", ".join("%s %d" % kv for kv in c.items()), (len(sel) + 29) // 30))
