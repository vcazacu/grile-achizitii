#!/usr/bin/env python3
"""Unitățile de text ale actelor: articole (arabe, cu indice, romane), puncte de nivel 1
(Normele ALOP) și preambulul. Singurul loc în care se recunosc titlurile de unitate și
etichetele din `sursa.articol` — toate uneltele trec prin el, ca o etichetă să nu fie
înțeleasă diferit de două unelte."""
import re

PREAMBUL = "preambul"
_NR = r"(\d+(?:\^\d+)?|[IVXLC]+(?:\^\d+)?)"
RX_ARTICOL = re.compile(r"^Articolul " + _NR + r"$")
# cheie_bib → regex pentru titlul unui punct de nivel 1 (grupul 1 = numărul).
# Normele ALOP n-au „Articolul N”: 5 puncte „N. Titlu” în corpul documentului (SURSE.md, obs. c).
ZONE_PUNCTE = {"08_Norme_ALOP_1792-2002.txt": re.compile(r"^(\d+)\.\s+[A-ZĂÂÎȘȚ]")}
_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def _roman(s):
    total = 0
    for i, ch in enumerate(s):
        v = _ROMAN[ch]
        total += -v if i + 1 < len(s) and _ROMAN[s[i + 1]] > v else v
    return total


def eticheta_titlu(linie, zona_puncte=None):
    m = RX_ARTICOL.match(linie)
    if m:
        return m.group(1)
    if zona_puncte is not None:
        m = zona_puncte.match(linie)
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


def unitati_zona(linii, zona_puncte=None):
    rez = [(PREAMBUL, "")]
    for l in linii:
        rez.append((eticheta_titlu(l, zona_puncte), l))
    return rez
