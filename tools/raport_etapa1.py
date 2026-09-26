#!/usr/bin/env python3
"""Raportul etapei 1: câte întrebări migrate trec pe textul la zi și de ce pică celelalte.
Utilizare: python3 raport_etapa1.py > ../../raport-etapa1.txt"""
import collections, glob, json, os
import check_citat, check_articol
from normalizare import fragmente_citat, eticheta_articol

DIR = os.path.dirname(os.path.abspath(__file__))
cc, ca = {}, {}
motive, pe_act, cazuri = collections.Counter(), collections.Counter(), []
total = 0
for f in sorted(glob.glob(os.path.join(DIR, "nou", "*-migrat.json"))):
    for q in json.load(open(f, encoding="utf-8")):
        total += 1
        s = q["sursa"]; k = s["fisier"] + ("#" + s["anexa"] if s.get("anexa") else "")
        er = check_citat.verifica_intrebare(q, cc)
        declarat = eticheta_articol(s["articol"])
        if declarat is None:
            er.append("etichetă nerecunoscută: „%s”" % s["articol"])
        elif not er:
            corpus = check_articol.corpus_cu_santinele(s["fisier"], s.get("anexa", ""), ca)
            e = check_articol.potriveste_articol(corpus, fragmente_citat(s["citat"]), declarat)
            if e: er.append("articol: " + e)
            ok, e2, _ = check_articol.verifica_tematica(s, declarat)
            if e2: er.append("tematică: " + e2)
        if er:
            cheie_motiv = "citat" if "fragmentul" in er[0] else er[0].split(":")[0]
            motive[cheie_motiv] += 1; pe_act[k] += 1
            cazuri.append("%s | %s | %s" % (q["id"], s["articol"], er[0].replace("\n", " ")[:220]))
print("TOTAL migrate: %d | trec: %d | în coada de reparat: %d" % (total, total - len(cazuri), len(cazuri)))
print("\nPe motiv:"); [print("  %-40s %d" % m) for m in motive.most_common()]
print("\nPe act:"); [print("  %-70s %d" % a) for a in pe_act.most_common()]
print("\nCazuri:"); [print("  " + c) for c in cazuri]
