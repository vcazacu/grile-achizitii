#!/usr/bin/env python3
"""12 întrebări „unic” din bancă, câte una din acte diferite unde e posibil, cu cheia mutată
deliberat pe un distractor. Poarta TREBUIE să le semnaleze pe toate (REVIZUIT).
Utilizare: python3 mutante.py → nou/_mutante.json"""
import json, os, random
from valideaza import incarca, grup
DIR = os.path.dirname(os.path.abspath(__file__))
banca = [q for q in incarca(os.path.join(DIR, "..", "intrebari.js")) if q["tip"] == "unic"]
rng = random.Random("mutante-achizitii")
rng.shuffle(banca)
ales, vazute = [], set()
for q in banca + banca:
    if len(ales) == 12: break
    if q["id"] + "-MUT" in {x["id"] for x in ales}: continue
    if grup(q) in vazute and len(vazute) < 8: continue
    vazute.add(grup(q))
    m = dict(q); gresit = [i for i in range(4) if i not in q["corecte"]]
    m["corecte"] = [rng.choice(gresit)]; m["id"] = q["id"] + "-MUT"
    ales.append(m)
json.dump(ales, open(os.path.join(DIR, "nou", "_mutante.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("mutante: %d din %d acte" % (len(ales), len({grup(q) for q in ales})))
