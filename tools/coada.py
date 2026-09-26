#!/usr/bin/env python3
"""Construiește coada de reparat: întrebările migrate care nu trec pe textul la zi,
cu contextul din PDF-ul vechi și textul la zi al unității declarate, în loturi de 25.
Utilizare: python3 coada.py            → scrie coada/lot-NN.json și tipărește sumarul"""
import glob, json, os, re, subprocess
import check_citat, check_articol, bibliografie as b
from normalizare import fragmente_citat, eticheta_articol, normalizeaza

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(DIR, "..", ".."))
CACHE = os.path.join(DIR, ".cache-pdf")

def erori_intrebare(q, cc, ca):
    s = q["sursa"]
    er = check_citat.verifica_intrebare(q, cc)
    declarat = eticheta_articol(s["articol"])
    if declarat is None:
        er.append("etichetă nerecunoscută: „%s”" % s["articol"])
    elif not er:
        corpus = check_articol.corpus_cu_santinele(s["fisier"], s.get("anexa", ""), ca)
        e = check_articol.potriveste_articol(corpus, fragmente_citat(s["citat"]), declarat)
        if e: er.append("articol: " + e)
        _, e2, _ = check_articol.verifica_tematica(s, declarat)
        if e2: er.append("tematică: " + e2)
    return er

def text_pdf(fisier_pdf):
    os.makedirs(CACHE, exist_ok=True)
    txt = os.path.join(CACHE, fisier_pdf[:-4] + ".txt")
    if not os.path.exists(txt):
        subprocess.run(["pdftotext", "-layout", os.path.join(ROOT, fisier_pdf), txt], check=True)
    return open(txt, encoding="utf-8").read()

def context_pdf(fisier_pdf, citat, lat=800):
    brut = text_pdf(fisier_pdf)
    plat = re.sub(r"-\n\s*", "", brut)          # despărțirile la capăt de rând
    plat = re.sub(r"\s+", " ", plat)
    frag = (fragmente_citat(citat) or [""])[0][:60]
    poz = normalizeaza(plat).find(frag) if frag else -1
    if poz < 0:
        return "(fragmentul nu se găsește în PDF)"
    return plat[max(0, poz - lat): poz + len(frag) + lat]

def text_la_zi(sursa):
    e = eticheta_articol(sursa["articol"])
    arts = b.articole_din_text(os.path.join(ROOT, "legislatie", sursa["fisier"]), sursa.get("anexa", ""))
    return "\n".join(arts.get(e, [])) if e else "(etichetă nerecunoscută — vezi unitati.py)"

def main():
    harta = json.load(open(os.path.join(DIR, "nou", "_harta-migrare.json"), encoding="utf-8"))
    cc, ca, coada = {}, {}, []
    for f in sorted(glob.glob(os.path.join(DIR, "nou", "*-migrat.json"))):
        for q in json.load(open(f, encoding="utf-8")):
            er = erori_intrebare(q, cc, ca)
            if not er: continue
            h = harta[q["id"]]
            coada.append({"id": q["id"], "erori": er, "intrebare": q,
                          "sursa_veche": h,
                          "context_vechi": context_pdf(h["fisier_pdf"], q["sursa"]["citat"]),
                          "unitatea_la_zi": text_la_zi(q["sursa"])})
    os.makedirs(os.path.join(DIR, "coada"), exist_ok=True)
    for i in range(0, len(coada), 25):
        with open(os.path.join(DIR, "coada", "lot-%02d.json" % (i // 25 + 1)), "w", encoding="utf-8") as g:
            json.dump(coada[i:i + 25], g, ensure_ascii=False, indent=1)
    print("în coadă: %d întrebări, %d loturi" % (len(coada), (len(coada) + 24) // 25))

if __name__ == "__main__":
    main()
