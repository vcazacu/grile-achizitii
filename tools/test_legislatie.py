#!/usr/bin/env python3
"""Paginile de legislație: id-uri unice și fără trimiteri interne către text citat.

La H.G. 419/2018 (actul de aprobare), art. II–VI modifică alte acte și citează textul modificat
(„(3) Strategia de contractare …”, „a) etapa de planificare”). Acele rânduri nu sunt alineatele
sau literele articolului roman: nu primesc id-uri și nu devin ținte de trimiteri. Art. VII are
alineate proprii, iar art. VIII litere proprii — acestea rămân structurate.
Utilizare: python3 test_legislatie.py"""
import os, re, sys
from collections import Counter
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import legislatie_build as lb

esec = []
def verifica(cond, mesaj):
    if not cond: esec.append(mesaj)

# 1) parsarea: articolele de modificare nu au alineate/litere proprii; VII și VIII da
doc = lb.parseaza(os.path.join(lb.LEG, "05_HG_419-2018_act_de_aprobare.txt"), [])
art = {b["nr"]: b for b in doc["corp"] if b["tip"] == "art"}
for nr in ("II", "III", "IV", "V", "VI"):
    tipuri = {t for t, _ in art[nr]["continut"]}
    verifica(not tipuri & {"alin", "lit", "grup"}, "art. %s (de modificare) are structură proprie: %s" % (nr, sorted(tipuri)))
verifica([v[0] for t, v in art["VII"]["continut"] if t == "alin"] == ["1", "2"], "art. VII și-a pierdut alineatele (1)–(2)")
verifica([v[0] for t, v in art["VIII"]["continut"] if t == "lit"][:2] == ["a", "b"], "art. VIII și-a pierdut literele")

# 2) paginile generate: niciun id duplicat, nicio trimitere spre un id inexistent
paginile = {}
docs = {f: lb.parseaza(os.path.join(lb.LEG, f), ar) for f, _, _, ar in lb.ACTE}
for f, d in docs.items():
    lb.INDEX[(f, "")] = lb.indexeaza(d["corp"], "")
    for ax in d["anexe"]: lb.INDEX[(f, ax["nume"])] = lb.indexeaza(ax["blocuri"], ax["nume"])
bib = lb.bib_tematica()
for f, slug, den, ar in lb.ACTE:
    h = lb.pagina(f, slug, den, ar, bib, docs[f])[0]
    ids = re.findall(r'\bid="([^"]+)"', h)
    dubluri = [i for i, n in Counter(ids).items() if n > 1]
    verifica(not dubluri, "%s: id-uri duplicate: %s" % (f, dubluri[:5]))
    paginile[slug] = set(ids)
for f, slug, den, ar in lb.ACTE:
    h = lb.pagina(f, slug, den, ar, bib, docs[f])[0]
    for pag, tinta in re.findall(r'<a class="trm" href="([^"#]*)#([^"]+)"', h):
        tinta_pag = pag[:-5] if pag.endswith(".html") else slug
        verifica(tinta in paginile.get(tinta_pag, set()), "%s: trimitere spre ținta inexistentă %s#%s" % (f, pag, tinta))

# 3) pagina H.G. 419: nicio trimitere internă (textul citat nu se leagă de art. II–VI)
h05 = lb.pagina(*[a for a in lb.ACTE if a[0].startswith("05_")][0][:3], [], bib, docs["05_HG_419-2018_act_de_aprobare.txt"])[0]
interne = re.findall(r'<a class="trm" href="#(art-[IVX]+[^"]*)"', h05)
verifica(not interne, "H.G. 419: %d trimiteri interne în text citat, ex. %s" % (len(interne), interne[:3]))

for m in esec: print("EȘEC", m)
print("OK: pagini de legislație" if not esec else "%d eșecuri" % len(esec))
sys.exit(1 if esec else 0)
