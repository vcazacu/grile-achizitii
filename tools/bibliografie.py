"""Bibliografia oficială a examenului: pentru fiecare fișier-sursă, intervalele de
articole cerute (exact ca în „Tematică ofițer achiziții.docx"). Este singura
sursă de adevăr pentru „ce intră în tematică" — o folosesc clasifica.py,
check_articol.py și asambleaza.py.

Cheia = numele fișierului .txt din ../../legislatie/ (+ „#<anexa>" când
articolele sunt din anexă, care are numerotare proprie).
Valoarea = (numele anexei sau "", șirul de intervale).
Notație: „9^1" = art. 9 indice 1 (așa apare și în text: „Articolul 9^1").
"""

# Restricții pe alineate/litere din bibliografie (restul articolului NU e în tematică):
# Chei = fișierul .txt din ../../legislatie/ (+ „#<anexa>" când unitățile sunt dintr-o anexă).
# Pe portal, toate cele trei seturi de norme sunt documente separate de actele de aprobare (SURSE.md).
K98   = "01_Legea_98-2016_achizitii_publice.txt"
K395C = "02_HG_395-2016_act_de_aprobare.txt"
K395  = "03_Norme_HG_395-2016_achizitii_publice.txt"
KOUG  = "04_OUG_98-2017_control_ex_ante.txt"
K419C = "05_HG_419-2018_act_de_aprobare.txt"
K419  = "06_Norme_HG_419-2018_control_ex_ante.txt"
K101  = "07_Legea_101-2016_remedii_si_cai_de_atac.txt"
KORD  = "08_Ordinul_MFP_1792-2002_act_de_aprobare.txt"
KALOP = "09_Norme_ALOP_1792-2002.txt"
K500  = "10_Legea_500-2002_finantele_publice.txt"

BIB = {
 K98:   ("", "1-222"),
 K395C: ("", "*"),
 K395:  ("", "1-166"),
 KOUG:  ("", "1-25"),
 K419C: ("", "I, V"),                         # aprobarea normelor ex ante + modificarea Normelor H.G. 395 (SURSE.md, obs. b)
 K419:  ("", "*"),
 K101:  ("", "1-36^1"),
 KORD:  ("", "*"),
 KALOP: ("", "preambul, pct. 1-4"),           # „fără elementele de contabilitate”: pct. 5 exclus
 K500:  ("", "1-37, 52, 62-70"),
}
RESTRICTII = {}

GRUPE = [
 "Legea nr. 98/2016 cu modificările și completările ulterioare și HG nr. 395/2016",
 "OUG nr. 98/2017 și HG nr. 419/2018",
 "Legea nr. 101/2016",
 "Ordinul 1792/2002",
 "Legea 500/2002",
]

def _t(nr, slug, grupa, subiecte, articole):
    return {"nr": nr, "slug": slug, "grupa": grupa, "subiecte": subiecte,
            "titlu": ". ".join(subiecte), "articole": articole}

# Intervalele provin din harta tematicii din 00_Ghid_tematica_si_stadiul_legislatiei.pdf (§3–4),
# confirmate pe textul la zi (diferențele: SURSE.md).
TEME = [
 _t(1, "principii-autoritati-contractante-domeniu", 0,
    ["Principiile achizițiilor publice", "Autorități contractante", "Domeniu de aplicare"],
    {K98: "1-8", K395C: "*", K395: "1-7", K419C: "V"}),
 _t(2, "exceptari-achizitii-mixte-situatii-speciale", 0,
    ["Exceptări", "Achiziții mixte", "Situații speciale"], {K98: "26-39"}),
 _t(3, "achizitii-centralizate-si-comune-ocazionale", 0,
    ["Activități de achiziție centralizare și achiziții comune ocazionale"], {K98: "40-48"}),
 _t(4, "reguli-generale-de-participare", 0,
    ["Reguli generale de participare și desfășurare a procedurilor de atribuire"], {K98: "49-67", K395: "47-53"}),
 _t(5, "modalitati-si-proceduri-de-atribuire", 0,
    ["Modalități de atribuire", "Procedurile de atribuire"], {K98: "68-113", K395: "58-106"}),
 _t(6, "estimarea-valorii-si-alegerea-modalitatii", 0,
    ["Estimarea valorii achiziției publice și alegerea modalității de atribuire"], {K98: "9-25", K395: "15-17"}),
 _t(7, "etapele-consultarea-pietei-loturi", 0,
    ["Organizarea și desfășurarea procedurii de atribuire", "Etapele procesului de achiziție publică",
     "Consultarea pieței", "Împărțirea pe loturi"], {K98: "139-141", K395: "8-11, 18-19"}),
 _t(8, "publicitate-si-transparenta", 0,
    ["Reguli de publicitate și transparență"], {K98: "142-153", K395: "54-57"}),
 _t(9, "documentatia-oferte-alternative-duae", 0,
    ["Documentația de atribuire", "Oferte alternative", "Documentul unic de achiziție European"],
    {K98: "154-162, 193-202", K395: "20-28"}),
 _t(10, "criterii-de-calificare-si-selectie", 0,
    ["Criterii de calificare și selecție"], {K98: "163-186", K395: "29-31"}),
 _t(11, "criterii-de-atribuire", 0, ["Criterii de atribuire"], {K98: "187-192", K395: "32-34"}),
 _t(12, "garantii-de-participare-si-buna-executie", 0,
    ["Stabilirea garanțiilor de participare și de bună execuție"], {K395: "35-42"}),
 _t(13, "achizitia-directa", 0, ["Achiziția directă"], {K98: "7", K395: "43-46"}),
 _t(14, "instrumente-si-tehnici-specifice", 0,
    ["Derularea procedurilor de atribuire",
     "Instrumente și tehnici specifice de atribuire a contractelor de achiziție publică",
     "Instrumente și tehnici specifice de atribuire a contractelor de achiziție publică, acordul cadru, licitația electronică",
     "Cataloage electronice"], {K98: "114-138, 203-206", K395: "107-125"}),
 _t(15, "comisia-de-evaluare-verificare-si-evaluare", 0,
    ["Comisia de evaluare și modul de lucru al acesteia", "Procesul de verificare și evaluare"], {K395: "126-141"}),
 _t(16, "atribuirea-finalizarea-informarea-dosarul", 0,
    ["Atribuirea contractelor de achiziție publică și încheierea acordurilor-cadru",
     "Finalizarea procedurii de atribuire", "Informarea candidaților / ofertanților",
     "Dosarul achiziției și raportul procedurii de atribuire"], {K98: "207-217", K395: "142-149"}),
 _t(17, "executarea-subcontractarea-modificarea-contractului", 0,
    ["Executarea contractului de achiziție publică / acordului-cadru", "Subcontractarea",
     "Modificarea contractului de achiziție publică / acordului cadru",
     "Finalizarea contractului de achiziție publică"], {K98: "218-222", K395: "150-166"}),
 _t(18, "programul-anual-al-achizitiilor-publice", 0,
    ["Programul anual al achizițiilor publice"], {K395: "12-14"}),
 _t(19, "controlul-ex-ante", 1,
    ["Activitatea de control ex ante", "Metodologia de selecție", "Inițierea controlului ex ante",
     "Desfășurarea activității de control", "Avizul conform al ANAP", "Procedura de conciliere",
     "Controlul ex ante al procedurilor de negociere", "Controlul ex ante al modificărilor contractului"],
    {KOUG: "1-25", K419C: "I", K419: "*"}),
 _t(20, "remedii-contestatii-termen-efecte-solutionare", 2,
    ["Remedii și căi de atac în atribuirea contractelor de achiziție publică",
     "Contestațiile formulate pe cale administrativ-jurisdicțională",
     "Termenul de contestare, efectele, elementele și soluționarea contestațiilor"], {K101: "1-25"}),
 _t(21, "solutii-de-pronuntare-cai-de-atac", 2,
    ["Soluții de pronunțare, căi de atac"], {K101: "26-36^1"}),
 _t(22, "fazele-cheltuielilor-publice", 3,
    ["Fazele pe care le parcurg cheltuielile din fondurile publice și definirea acestora"],
    {KORD: "*", KALOP: "preambul, pct. 1-4"}),
 _t(23, "venituri-si-cheltuieli", 4, ["Venituri și cheltuieli"], {K500: "1-15, 26-30, 62-70"}),
 _t(24, "ordonatorii-de-credite-aprobarea-bugetului", 4,
    ["Rolul și responsabilitatea ordonatorilor de credite", "Aprobarea bugetului de stat"],
    {K500: "16-25, 31-37, 52"}),
]

import re

import unitati
cheie = unitati.cheie

def articole_din_text(fisier, anexa=""):
    """{eticheta_unitate: [linii normative]} pentru corpul actului (anexa="") sau pentru anexa dată.
    Unitățile vin din unitati.py (articole arabe/romane, puncte, preambul)."""
    import os
    lines = open(fisier, encoding="utf-8").read().split("\n")
    zona_puncte = unitati.ZONE_SPECIALE.get(os.path.basename(fisier) + ("#" + anexa if anexa else ""))
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
    """Extinde „1-3, 5, 9^1-11, preambul, pct. 1-4, I, V, *" în lista de etichete.
    „*" = toate unitățile existente. O limită superioară fără indice include și
    indicii ei („1-222" cuprinde 222^1, 222^2). Capetele inexistente rămân în listă,
    ca tematica() să le raporteze drept lipsă."""
    if spec.strip() == "*":
        return list(existente)
    want = []
    for part in [p.strip() for p in spec.split(",") if p.strip()]:
        m = re.match(r"^(pct\.\s*)?(\S+?)-(\S+)$", part)
        if m and part != "preambul":
            pref = "pct. " if m.group(1) else ""
            a, b = pref + m.group(2), pref + m.group(3)
            ka, kb = cheie(a), cheie(b)
            if "^" not in b:
                kb = (kb[0], kb[1], 10 ** 6)
            want += [x for x in existente if ka <= cheie(x) <= kb]
            for e in (a, b):
                if e not in existente: want.append(e)
        else:
            want.append(re.sub(r"^pct\.\s*", "pct. ", part))
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


def articole_tema(nr):
    """{cheie_bib: [unitățile existente și cerute ale temei]}."""
    tem = tematica()
    t = next(x for x in TEME if x["nr"] == nr)
    out = {}
    for k, spec in t["articole"].items():
        cerute = tem[k][2]
        out[k] = [a for a in articole_cerute(spec, sorted(tem[k][5], key=cheie)) if a in cerute]
    return out

_CACHE_TEME = {}
def tema_articol(cheie_bib, eticheta):
    """Prima temă (în ordinea TEME) care conține unitatea; None dacă niciuna."""
    if not _CACHE_TEME:
        for t in TEME:
            for k, arts in articole_tema(t["nr"]).items():
                for a in arts: _CACHE_TEME.setdefault((k, a), t["nr"])
    return _CACHE_TEME.get((cheie_bib, eticheta))
