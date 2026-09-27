#!/usr/bin/env python3
"""Verificarea temeiurilor din tematică: citatul trebuie să stea în unitatea declarată, eticheta
trebuie recunoscută, iar `tematica_build.py --verifica` nu scrie nimic.  python3 test_tematica_build.py"""
import os, subprocess, sys, glob
DIR = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, DIR)
from tematica_build import verifica_temei
L = "Legea nr. 98/2016 privind achizițiile publice"; F = "01_Legea_98-2016_achizitii_publice.txt"
esec = []
cit = "Valoarea estimată a achiziției se determină înainte de inițierea procedurii de atribuire"
ok, msg = verifica_temei({"act": L, "articol": "art. 12", "citat": cit, "fisier": F})
if not ok: esec.append("citat corect respins: " + msg)
ok, msg = verifica_temei({"act": L, "articol": "art. 11", "citat": cit, "fisier": F})
if ok: esec.append("citat din art. 12 acceptat sub eticheta art. 11")
ok, msg = verifica_temei({"act": L, "articol": "articolul doisprezece", "citat": cit, "fisier": F})
if ok: esec.append("etichetă nerecunoscută acceptată")
# --verifica: cod 0 pe conținutul actual și nicio scriere
pagini = glob.glob(os.path.join(DIR, "..", "tematica", "*.html")) + [os.path.join(DIR, "..", "sw.js")]
inainte = {p: os.path.getmtime(p) for p in pagini}
r = subprocess.run([sys.executable, os.path.join(DIR, "tematica_build.py"), "--verifica"], capture_output=True, text=True)
if r.returncode != 0: esec.append("--verifica: cod %d: %s" % (r.returncode, (r.stdout + r.stderr)[-300:]))
if any(os.path.getmtime(p) != t for p, t in inainte.items()): esec.append("--verifica a scris fișiere")
for m in esec: print("EȘEC", m)
print("OK: verificarea temeiurilor" if not esec else "%d eșecuri" % len(esec)); sys.exit(1 if esec else 0)
