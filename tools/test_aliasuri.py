#!/usr/bin/env python3
"""Recunoașterea actului numit după o trimitere. Rulare: python3 test_aliasuri.py"""
import sys
import bibliografie as b
from legislatie_build import act_numit
CAZURI = [
 ("Legea nr. 98/2016, cu modificările și completările ulterioare", b.K395, (b.K98, "")),
 ("Legea nr. 99/2016 privind achizițiile sectoriale", b.K395, None),                  # act din afara bibliografiei
 ("Legea nr. 100/2016 privind concesiunile", b.K101, None),
 ("Lege, autoritatea contractantă", b.K395, (b.K98, "")),                             # „din Lege” în Normele H.G. 395
 ("Lege, autoritatea contractantă", b.K101, None),                                    # nu în afara Normelor
 ("Legea nr. 99/2016", b.K395, None),                                                 # „Lege\\b” nu prinde „Legea”
 ("lege, în condițiile", b.K395, None),                                               # „lege” cu minusculă = orice lege
 ("ordonanța de urgență, ANAP", b.K419, (b.KOUG, "")),
 ("ordonanței de urgență", b.K419, (b.KOUG, "")),
 ("ordonanța de urgență", b.K98, None),
 ("Ordonanța de urgență a Guvernului nr. 98/2017", b.K101, (b.KOUG, "")),
 ("O.U.G. nr. 98/2017", b.K98, (b.KOUG, "")),
 ("Legea nr. 101/2016", b.K98, (b.K101, "")),
 ("Legea nr. 500/2002 privind finanțele publice", b.KALOP, (b.K500, "")),
 ("Legea nr. 500/2002", b.K98, (b.K500, "")),
 ("Legea contabilității nr. 82/1991", b.KALOP, None),
 ("Hotărârea Guvernului nr. 395/2016", b.K419C, (b.K395C, "")),
]
esec = 0
for fraza, curent, astept in CAZURI:
    r = act_numit(fraza, curent)
    if r != astept:
        esec += 1; print("EȘEC %r în %s → %r, așteptat %r" % (fraza, curent, r, astept))
print("OK: %d cazuri" % len(CAZURI) if not esec else "%d eșecuri" % esec)
sys.exit(1 if esec else 0)
