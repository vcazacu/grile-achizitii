#!/usr/bin/env python3
"""Conversia unică a băncii vechi (ancorată în PDF-uri) în nou/<prefix>-migrat.json,
pe noile surse la zi. Id-urile se păstrează; câmpul `test` se elimină (îl atribuie
asambleaza.py). PDF-urile 01–10 corespund 1:1 fișierelor .txt 01–10 (SURSE.md).
Utilizare: python3 migreaza.py [../intrebari.js]"""
import copy, json, os, re, sys
import bibliografie as b
from valideaza import incarca

DIR = os.path.dirname(os.path.abspath(__file__))
HARTA = {
 "01_Legea_98-2016_achizitii_publice.pdf": b.K98,
 "02_HG_395-2016_act_normativ.pdf": b.K395C,
 "03_Norme_metodologice_HG_395-2016.pdf": b.K395,
 "04_OUG_98-2017_control_ex_ante.pdf": b.KOUG,
 "05_HG_419-2018_act_normativ.pdf": b.K419C,
 "06_Norme_metodologice_HG_419-2018.pdf": b.K419,
 "07_Legea_101-2016_remedii_si_cai_de_atac.pdf": b.K101,
 "08_Ordinul_MFP_1792-2002_ALOP.pdf": b.KORD,
 "09_Norme_metodologice_ALOP_1792-2002.pdf": b.KALOP,
 "10_Legea_500-2002_finantele_publice.pdf": b.K500,
}

def converteste(q):
    vechi = q["sursa"]
    fisier = HARTA[vechi["fisier"]]          # KeyError = PDF necunoscut, intenționat
    nq = copy.deepcopy(q)
    nq.pop("test", None)
    s = nq["sursa"]
    s["fisier"] = fisier
    s.pop("anexa", None)
    s["articol"] = re.sub(r"^Norme ALOP,\s*", "", vechi["articol"])
    return nq, {"fisier_pdf": vechi["fisier"], "articol_vechi": vechi["articol"]}

def main(argv):
    sursa = argv[0] if argv else os.path.join(DIR, "..", "intrebari.js")
    pe_prefix, harta = {}, {}
    for q in incarca(sursa):
        nq, h = converteste(q)
        pe_prefix.setdefault(q["id"].split("-")[0], []).append(nq)
        harta[q["id"]] = h
    os.makedirs(os.path.join(DIR, "nou"), exist_ok=True)
    for pref, lista in pe_prefix.items():
        with open(os.path.join(DIR, "nou", "%s-migrat.json" % pref), "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=1)
    with open(os.path.join(DIR, "nou", "_harta-migrare.json"), "w", encoding="utf-8") as f:
        json.dump(harta, f, ensure_ascii=False, indent=1)
    print("migrate: %d întrebări în %d fișiere" % (len(harta), len(pe_prefix)))

if __name__ == "__main__":
    main(sys.argv[1:])
