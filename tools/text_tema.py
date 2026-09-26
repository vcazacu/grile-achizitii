#!/usr/bin/env python3
"""Textul normativ (fără §NOTA§) al unităților unei teme, pe fișier și unitate — pentru scrierea sintezei.
Utilizare: python3 text_tema.py 5 [--max N]   (N = caractere maxime pe unitate, implicit fără limită)"""
import os, sys
import bibliografie as b
nr = int(sys.argv[1]); mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 0
LEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "legislatie")
tem = b.tematica()
for k, arts in b.articole_tema(nr).items():
    fis, anexa = k.split("#")[0], ""
    print("#### %s" % k)
    toate = tem[k][5]
    for a in arts:
        t = " ".join(toate.get(a, []))
        if mx and len(t) > mx: t = t[:mx] + " […]"
        print("[%s] %s" % (a, t))
