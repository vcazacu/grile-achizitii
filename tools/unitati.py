#!/usr/bin/env python3
"""Unitățile de text ale actelor: articole (arabe, cu indice, romane), puncte de nivel 1
(Normele ALOP) și preambulul. Singurul loc în care se recunosc titlurile de unitate și
etichetele din `sursa.articol` — toate uneltele trec prin el, ca o etichetă să nu fie
înțeleasă diferit de două unelte."""
import re

PREAMBUL = "preambul"
_NR = r"(\d+(?:\^\d+)?|[IVXLC]+(?:\^\d+)?)"
RX_ARTICOL = re.compile(r"^Articolul " + _NR + r"$")
# Zone cu reguli speciale de unitate, cheie_bib → regulă:
#  - un regex = zona e structurată pe puncte de nivel 1 (grupul 1 = numărul). Normele ALOP n-au
#    „Articolul N”: 5 puncte „N. Titlu” în corpul documentului (SURSE.md, obs. c);
#  - DOAR_ROMANE = unitățile zonei sunt articolele romane; un „Articolul 26” arab e text citat de un
#    articol modificator („Articolul 26 se modifică și va avea următorul cuprins: Articolul 26 …”).
DOAR_ROMANE = "doar-romane"
ZONE_SPECIALE = {
 "09_Norme_ALOP_1792-2002.txt": re.compile(r"^(\d+)\.\s+[A-ZĂÂÎȘȚ]"),
 "05_HG_419-2018_act_de_aprobare.txt": DOAR_ROMANE,
}
_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def _roman(s):
    total = 0
    for i, ch in enumerate(s):
        v = _ROMAN[ch]
        total += -v if i + 1 < len(s) and _ROMAN[s[i + 1]] > v else v
    return total


def eticheta_titlu(linie, regula=None):
    """Eticheta unității dacă linia e titlu de unitate; `regula` = ZONE_SPECIALE[cheia zonei] sau None."""
    m = RX_ARTICOL.match(linie)
    if m:
        if regula == DOAR_ROMANE and m.group(1)[0].isdigit():
            return None
        return m.group(1)
    if regula is not None and regula != DOAR_ROMANE:
        m = regula.match(linie)
        if m:
            return "pct. " + m.group(1)
    return None


def eticheta(sursa_articol):
    s = (sursa_articol or "").strip()
    m = re.match(r"^(?i:art\.)\s*" + _NR + r"(?![\w^])", s)
    if m:
        return m.group(1)
    if re.match(r"^(?i:nota)\b", s):
        return None
    m = re.search(r"\bpct\.\s*(\d+)\b", s)
    if m:
        return "pct. " + m.group(1)
    if re.search(r"preambul|formula introductiv", s, re.I):
        return PREAMBUL
    return None


def cheie(e):
    """(categorie, valoare, indice). Categoria separă tipurile de unități: preambul 0,
    articole arabe 1, articole romane 2, puncte 3 — un interval nu trece dintr-un tip în altul."""
    if e == PREAMBUL:
        return (0, 0, 0)
    m = re.match(r"^pct\. (\d+)$", e)
    if m:
        return (3, int(m.group(1)), 0)
    m = re.match(r"^(\d+|[IVXLC]+)(?:\^(\d+))?$", e)
    if not m:
        return (9, 10 ** 9, 0)
    if m.group(1).isdigit():
        return (1, int(m.group(1)), int(m.group(2) or 0))
    return (2, _roman(m.group(1)), int(m.group(2) or 0))


def ancora(e, anexa=""):
    if e == PREAMBUL:
        a = PREAMBUL
    elif e.startswith("pct. "):
        a = "pct-" + e[5:]
    else:
        a = "art-" + e.replace("^", "-")
    if not anexa:
        return a
    return "anexa-%s-" % re.sub(r"[^A-Za-z0-9]+", "-", anexa).strip("-").lower() + a


def unitati_zona(linii, regula=None):
    rez = [(PREAMBUL, "")]
    for l in linii:
        rez.append((eticheta_titlu(l, regula), l))
    return rez
