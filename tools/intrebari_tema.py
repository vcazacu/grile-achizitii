#!/usr/bin/env python3
"""Id-urile întrebărilor din bancă legate de o temă (după unitatea din sursa.articol).
Utilizare: python3 intrebari_tema.py 7"""
import os, sys
import bibliografie as b
from normalizare import eticheta_articol, cheie_bib
from valideaza import incarca
nr = int(sys.argv[1])
banca = incarca(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "intrebari.js"))
ids = [q["id"] for q in banca if b.tema_articol(cheie_bib(q["sursa"]), eticheta_articol(q["sursa"]["articol"])) == nr]
print(", ".join(ids)); print("(%d întrebări)" % len(ids), file=sys.stderr)
