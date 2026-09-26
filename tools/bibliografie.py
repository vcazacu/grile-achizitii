"""Bibliografia oficială a examenului: pentru fiecare fișier-sursă, intervalele de
articole cerute (exact ca în „Tematică ofițer achiziții.docx"). Este singura
sursă de adevăr pentru „ce intră în tematică" — o folosesc clasifica.py,
check_articol.py și asambleaza.py.

Cheia = numele fișierului .txt din ../../legislatie/ (+ „#<anexa>" când
articolele sunt din anexă, care are numerotare proprie).
Valoarea = (numele anexei sau "", șirul de intervale).
Notație: „9^1" = art. 9 indice 1 (așa apare și în text: „Articolul 9^1").
"""
BIB = {}

# Restricții pe alineate/litere din bibliografie (restul articolului NU e în tematică):
RESTRICTII = {}

import re

import unitati
cheie = unitati.cheie

def articole_din_text(fisier, anexa=""):
    """{eticheta_unitate: [linii normative]} pentru corpul actului (anexa="") sau pentru anexa dată.
    Unitățile vin din unitati.py (articole arabe/romane, puncte, preambul)."""
    import os
    lines = open(fisier, encoding="utf-8").read().split("\n")
    zona_puncte = unitati.ZONE_PUNCTE.get(os.path.basename(fisier) + ("#" + anexa if anexa else ""))
    arts, cur, zona = {}, unitati.PREAMBUL, (anexa == "")
    for l in lines:
        if l.startswith("§ANEXA§"):
            zona = (anexa != "" and l == "§ANEXA§ " + anexa); cur = unitati.PREAMBUL if zona else None; continue
        if not zona or l.startswith("§SURSA§"): continue
        e = unitati.eticheta_titlu(l, zona_puncte)
        if e: cur = e; arts.setdefault(cur, []); continue
        if cur and l.strip() and not l.startswith("§NOTA§") and not l.startswith("## "):
            arts.setdefault(cur, []).append(l)
    return arts

def articole_cerute(spec, existente):
    """Extinde „1-3, 5, 9^1-11" în lista de etichete, folosind etichetele care există în text."""
    want = []
    for part in [p.strip() for p in spec.split(",")]:
        if "-" in part:
            a, b = part.split("-"); ka, kb = cheie(a), cheie(b)
            want += [x for x in existente if ka <= cheie(x) <= kb]
            for e in (a, b):
                if e not in existente: want.append(e)
        else:
            want.append(part)
    out, seen = [], set()
    for w in want:
        if w not in seen: seen.add(w); out.append(w)
    return out

def tematica():
    """Întoarce {cheie_bib: (fisier, anexa, [articole cerute existente], [lipsă], [abrogate])}."""
    import os
    baza = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "legislatie")
    rez = {}
    for k, (anexa, spec) in BIB.items():
        fis = os.path.join(baza, k.split("#")[0])
        arts = articole_din_text(fis, anexa)
        exist = sorted(arts, key=cheie)
        want = articole_cerute(spec, exist)
        lipsa = [w for w in want if w not in arts]
        abrog = [w for w in want if w in arts and (not arts[w] or re.match(r"^\s*(\(\d+\)\s*)?Abrogat", arts[w][0]))]
        rez[k] = (k.split("#")[0], anexa, [w for w in want if w in arts], lipsa, abrog, arts)
    return rez

if __name__ == "__main__":
    tot = 0
    for k, (fis, anexa, want, lipsa, abrog, arts) in tematica().items():
        nchar = sum(len(x) for w in want for x in arts[w])
        tot += nchar
        print("%-62s cerute=%3d lipsă=%s abrogate=%s caractere=%6d" % (k, len(want), lipsa, abrog, nchar))
    print("total caractere normative în tematică:", tot)
