#!/usr/bin/env python3
"""Utilitar de scriere: construiește tools/tematica/NN.json dintr-un dict Python (citit din stdin, JSON) și
completează automat lista `intrebari` cu intrebari_tema. Utilizare: python3 scrie_tema.py < tema.json"""
import json, subprocess, sys, os
DIR = os.path.dirname(os.path.abspath(__file__))
d = json.load(sys.stdin)
ids = subprocess.run([sys.executable, os.path.join(DIR, "intrebari_tema.py"), str(d["nr"])], capture_output=True, text=True).stdout.strip()
d["intrebari"] = [x.strip() for x in ids.split(",") if x.strip()]
json.dump(d, open(os.path.join(DIR, "tematica", "%02d.json" % d["nr"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("tema %d scrisă: %d secțiuni, %d temeiuri, %d capcane, %d întrebări legate" % (
    d["nr"], len(d["sectiuni"]), sum(len(s["temei"]) for s in d["sectiuni"]), len(d["capcane"]), len(d["intrebari"])))
