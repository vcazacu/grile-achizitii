#!/usr/bin/env python3
"""Audit determinist al paginilor de sinteză, complementar poarții semantice.

Poarta semantică judecă fondul, dar o afirmație despre un articol absent din temeiuri
iese doar „neverificabilă". Aici se verifică trasabilitatea: fiecare cifră și fiecare
trimitere la articol dintr-un paragraf trebuie să apară în citatele aceleiași secțiunii; din rezumat și
din capcane, în citatele temei. Cod de ieșire 1 la orice problemă. Ce nu se regăsește se verifică manual
în lege. Se verifică și că id-urile de întrebări există în bancă.

    python3 audit_tematica.py 02 03 04
"""
import json, re, sys
from pathlib import Path
from normalizare import incarca_intrebari, normalizeaza

DIR = Path(__file__).resolve().parent / "tematica"
# separatorul de mii („27.334.460”, „26 960 556”) ține numărul întreg; „80/1995” nu e cifră de audit
_NUM = re.compile(r"(?<![\w^/])(\d{1,3}(?:[. ]\d{3})+(?:,\d+)?(?![\d])|\d+(?:[.,]\d+)?)(?:\s*%)?(?![\w^/])")
# trimiterile la unități („art. 28–30”, „alin. (1)-(4)”, „pct. 1–4”) nu sunt cifre de audit;
# intervalele de valori („5–10 zile”) sunt
_UNIT = r"\(?\d+(?:\^\d+)?\)?"
_REF = re.compile(r"\b(?:(?i:art)|alin|pct)\.\s*" + _UNIT + r"(?:\s*[–-]\s*" + _UNIT + r")?")
_ART = re.compile(r"\b(?i:art)\.\s*(\d+(?:\^\d+)?|[IVXLC]+(?:\^\d+)?)(?![\w^])")
_ALIN = re.compile(r"alin\.\s*\(?(\d+(?:\^\d+)?)\)?", re.I)

def numere(text, cu_trimiteri=False):
    """Cifrele de audit din text; trimiterile la unități se scot, dacă nu se cer explicit (etichetele temeiurilor)."""
    out = set()
    for m in _NUM.finditer(text if cu_trimiteri else _REF.sub(" ", text)):
        g = m.group(1)
        if re.match(r"^\d{1,3}(?:[. ]\d{3})+", g):          # separator de mii → forma canonică, fără separatori
            g = re.sub(r"[. ]", "", g)
        out.add(g.replace(",", "."))
    return out

def _verifica_text(probleme, loc, ip, par, num_citate, arts_temei):
    # cifre care nu apar nici în citate, nici în etichetele articolelor
    for n in numere(par) - num_citate:
        # ignoră numerele care sunt doar numere de articol/alineat/literă menționate
        if re.search(r"(?:art\.|alin\.|lit\.|pct\.|nr\.|anexa|anexele|capitol|tabelul)\s*(?:\(|nr\.\s*)?%s\b" % re.escape(n), par, re.I):
            continue
        probleme.append(("CIFRĂ", loc, ip, n, par[:160]))
    # articole numite, dar absente din temeiuri
    for a in {m.group(1) for m in _ART.finditer(par)} - arts_temei:
        probleme.append(("ART.", loc, ip, "art. " + a, par[:120]))

def _trasabile(temeiuri):
    """(numere, articole) trasabile dintr-o listă de temeiuri: citatele, etichetele și trimiterile din citate."""
    citate = " ".join(t["citat"] for t in temeiuri)
    # un articol e trasabil dacă e temei SAU dacă legea însăși îl numește în textul citat
    # (trimitere internă, ex. „cei prevăzuți la art. 36 alin. 1 lit. a)")
    arts = {m.group(1) for t in temeiuri for m in _ART.finditer(t["articol"])} | {m.group(1) for m in _ART.finditer(citate)}
    return numere(citate) | numere(" ".join(t["articol"] for t in temeiuri), cu_trimiteri=True), arts

def audit_dict(d, banca_ids):
    """Paragrafele se raportează la citatele secțiunii lor; rezumatul și capcanele, la toate citatele temei."""
    probleme = []
    for s in d["sectiuni"]:
        num, arts = _trasabile(s["temei"])
        for ip, par in enumerate(s["paragrafe"]):
            _verifica_text(probleme, s["titlu"][:45], ip + 1, par, num, arts)
    num_tot, arts_tot = _trasabile([t for s in d["sectiuni"] for t in s["temei"]])
    _verifica_text(probleme, "rezumat", 1, d.get("rezumat", ""), num_tot, arts_tot)
    for ic, c in enumerate(d.get("capcane") or []):
        _verifica_text(probleme, "capcane", ic + 1, c, num_tot, arts_tot)
    lipsa = [i for i in d.get("intrebari") or [] if i not in banca_ids]
    return d["titlu"], probleme, lipsa

def audit(nr, banca_ids):
    return audit_dict(json.loads((DIR / f"{nr}.json").read_text(encoding="utf-8")), banca_ids)

def main(argv):
    banca = {q["id"] for q in incarca_intrebari(Path(__file__).resolve().parent.parent / "intrebari.js")}
    cod = False
    for nr in argv:
        titlu, probleme, lipsa = audit(nr, banca)
        cif = [p for p in probleme if p[0] == "CIFRĂ"]; art = [p for p in probleme if p[0] == "ART."]
        print("=== tema %s — %s: %d cifre netrasabile, %d articole fără temei, %d id-uri lipsă ===" % (nr, titlu[:50], len(cif), len(art), len(lipsa)))
        for tip, sec, ip, ce, ctx in probleme:
            print("  %-6s %-45s ¶%d  %-14s %s" % (tip, sec, ip, ce, ctx.replace("\n", " ")[:110]))
        if lipsa: print("  ID-URI LIPSĂ:", lipsa)
        print()
        cod = cod or bool(probleme or lipsa)
    return 1 if cod else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
