#!/usr/bin/env python3
"""Nicio unealtă nu trebuie să mai conțină date sau căi ale proiectului RU.
Rulare: python3 test_fara_ru.py"""
import pathlib, re, sys
DIR = pathlib.Path(__file__).resolve().parent
INTERZISE = re.compile(r"Examen-Resurse-Umane|grile-ru|Legea_80-1995|Legea_1-1998|Codul_muncii|"
                       r"Legea_223-2015|Legea_360-2023|Legea_153-2017|OUG_111-2010|HG_52-2011|HG_1867-2005|"
                       r"Resurse Umane|🪖|cadru militar|Legii nr\. 80/1995|L80-\d|L223-\d|Legea 80/1995|Legii 153/2017")
gasite = []
for f in sorted(DIR.glob("*.py")) + sorted(DIR.glob("*.sh")):
    if f.name == "test_fara_ru.py":
        continue
    for i, l in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if INTERZISE.search(l):
            gasite.append("%s:%d: %s" % (f.name, i, l.strip()[:100]))
print("\n".join(gasite) if gasite else "OK: nicio urmă RU")
sys.exit(1 if gasite else 0)
