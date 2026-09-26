#!/usr/bin/env python3
"""Trasabilitatea temelor: (1) fiecare subiect din docx aparține exact unei teme;
(2) articolele fiecărei teme sunt în BIB; (3) fiecare unitate din BIB aparține cel puțin
unei teme. Rulare: python3 test_teme.py"""
import pathlib, re, subprocess, sys
import bibliografie as b

DOCX = pathlib.Path(__file__).resolve().parent.parent.parent / "Tematică ofițer achiziții.docx"
ANTET = re.compile(r"^(Legea( nr\.)? \d+/\d{4}|OUG nr\. \d+/\d{4}|Ordinul \d+/\d{4})")

def subiecte_docx():
    text = subprocess.run(["textutil", "-convert", "txt", "-stdout", str(DOCX)],
                          capture_output=True, check=True).stdout.decode("utf-8")
    zona = text.split("\nTematica", 1)[1]
    out = []
    for linie in (l.strip() for l in zona.splitlines()):
        if not linie or ANTET.match(linie):
            continue
        for s in re.split(r"(?<=\.)\s+(?=[A-ZĂÂÎȘȚ])", linie):
            s = s.strip().rstrip(".").strip()
            if s: out.append(s)
    return out

esec = []
docx = subiecte_docx()
teme = [s for t in b.TEME for s in t["subiecte"]]
for s in docx:
    n = teme.count(s)
    if n != 1: esec.append("subiectul „%s” apare în %d teme" % (s, n))
for s in teme:
    if s not in docx: esec.append("subiectul „%s” din TEME nu există în docx" % s)
if [t["nr"] for t in b.TEME] != list(range(1, 25)): esec.append("TEME nu sunt numerotate 1..24")

tem = b.tematica()
for t in b.TEME:
    for k, spec in t["articole"].items():
        if k not in b.BIB: esec.append("tema %d: cheia %s nu e în BIB" % (t["nr"], k)); continue
        existente = sorted(tem[k][5], key=b.cheie)
        for a in b.articole_cerute(spec, existente):
            if a not in tem[k][2]: esec.append("tema %d: %s %s nu e în BIB (sau nu există)" % (t["nr"], k, a))
for k, (fis, anexa, want, lipsa, abrog, arts) in tem.items():
    for a in want:
        if b.tema_articol(k, a) is None: esec.append("%s %s: în BIB, dar în nicio temă" % (k, a))
print("docx: %d subiecte; TEME: %d subiecte în %d teme" % (len(docx), len(teme), len(b.TEME)))
print("\n".join(esec) if esec else "OK: trasabilitate completă")
sys.exit(1 if esec else 0)
