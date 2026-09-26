#!/usr/bin/env python3
"""Cele 9 surse există, sunt actele corecte și nu sunt mai vechi decât pachetul PDF (august 2026).
Rulare: python3 test_surse.py"""
import pathlib, re, sys, datetime
LEG = pathlib.Path(__file__).resolve().parent.parent.parent / "legislatie"
# fișier → (regex pe titlul din antetul §SURSA§, consolidarea minimă — cea din PDF-urile din august 2026)
ASTEPTAT = {
 "01_Legea_98-2016_achizitii_publice.txt":         (r"^LEGE\s+98\s+19/05/2016", "17.11.2024"),
 "02_HG_395-2016_act_de_aprobare.txt":             (r"^HG\s+395\s+02/06/2016", "25.02.2026"),
 "03_Norme_HG_395-2016_achizitii_publice.txt":     (r"^NORMA\b.*02/06/2016", "25.02.2026"),
 "04_OUG_98-2017_control_ex_ante.txt":             (r"^ORD DE URGENTA\s+98\s+14/12/2017", "30.08.2021"),
 "05_HG_419-2018_norme_control_ex_ante.txt":       (r"^HOTARARE\s+419\s+08/06/2018", "29.12.2023"),
 "06_Legea_101-2016_remedii_si_cai_de_atac.txt":   (r"^LEGE\s+101\s+19/05/2016", "06.04.2023"),
 "07_Ordinul_MFP_1792-2002_act_de_aprobare.txt":   (r"^ORDIN\s+1792\s+24/12/2002", "28.12.2022"),
 "08_Norme_ALOP_1792-2002.txt":                    (r"^NORMA\b.*24/12/2002", "28.12.2022"),
 "09_Legea_500-2002_finantele_publice.txt":        (r"^LEGE\s+500\s+11/07/2002", "05.10.2023"),
}
def data(s): return datetime.datetime.strptime(s, "%d.%m.%Y").date()
erori = []
for fis, (rx, minim) in ASTEPTAT.items():
    p = LEG / fis
    if not p.is_file():
        erori.append("%s: lipsește" % fis); continue
    antet = p.read_text(encoding="utf-8").split("\n", 1)[0]
    m = re.match(r"^§SURSA§ \S+ \| (.*) \| consolidarea din ([\d.]+) \| descărcat", antet)
    if not m:
        erori.append("%s: antet §SURSA§ invalid: %s" % (fis, antet[:120])); continue
    if not re.search(rx, m.group(1), re.I):
        erori.append("%s: alt act — titlul portalului e „%s”" % (fis, m.group(1)))
    if data(m.group(2)) < data(minim):
        erori.append("%s: consolidarea %s e mai veche decât cea din PDF (%s)" % (fis, m.group(2), minim))
    print("%-48s %s | consolidarea din %s" % (fis, m.group(1)[:50], m.group(2)))
print("\n".join(erori) if erori else "OK: 9/9 surse")
sys.exit(1 if erori else 0)
