#!/usr/bin/env python3
"""Construiește paginile de citit ale legislației (quiz-app/legislatie/*.html) din
fișierele-sursă ../../legislatie/*.txt, în același stil ca tematica.

Utilizare: python3 legislatie_build.py        (construiește toate actele din ACTE + index)

Fișierele .txt NU se modifică: sunt sursa de adevăr pentru toate uneltele. Parsarea e
deterministă, pe marcajele deja existente în text:
  §SURSA§ …            metadate (portal, consolidare)      ## Capitolul I / Secţiunea / Titlul / §n.
  Articolul N          articol (N poate fi 9^1)            (n)  alineat      x)  literă
  A. / B. / A^1.       grupuri de litere                   – …  liniuțe
  §NOTA§ …             notele portalului (modificări, abrogări, decizii) — strânse pe articol
  §ANEXA§ Anexa nr. X  anexă (numerotare proprie a articolelor)
Implicit paginile arată doar articolele cerute în bibliografie (bibliografie.py); un
comutator descoperă toată legea. Scrie și lista fișierelor în sw.js între marcajele
/* LEGISLATIE-START */ … /* LEGISLATIE-END */.
"""
import collections, html, os, re, sys
from bibliografie import BIB, RESTRICTII, tematica as bib_tematica
import bibliografie as b
from trimiteri import marcheaza
import unitati
import carcasa

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "..", "legislatie")
LEG = os.path.join(DIR, "..", "..", "legislatie")

# (fișier-sursă, slug, denumire scurtă, anexe redate — None = toate)
ACTE = [
 (b.K98, "01-legea-98-2016-achizitii-publice", "Legea nr. 98/2016 privind achizițiile publice",
  ["Anexa nr. 1", "Anexa nr. 2"]),                  # ambele anexe sunt referite din articole din tematică (art. 3, 7, 12, 35, 111, 144)
 (b.K395C, "02-hg-395-2016-act-de-aprobare", "H.G. nr. 395/2016 (actul de aprobare a Normelor metodologice)", []),
 (b.K395, "03-norme-hg-395-2016-achizitii-publice",
  "Normele metodologice de aplicare a Legii nr. 98/2016 (anexa la H.G. nr. 395/2016)", None),
 (b.KOUG, "04-oug-98-2017-control-ex-ante", "O.U.G. nr. 98/2017 privind funcția de control ex ante", None),
 (b.K419C, "05-hg-419-2018-act-de-aprobare", "H.G. nr. 419/2018 (actul de aprobare a Normelor controlului ex ante)", []),
 (b.K419, "06-norme-hg-419-2018-control-ex-ante",
  "Normele metodologice de aplicare a O.U.G. nr. 98/2017 (anexa nr. 1 la H.G. nr. 419/2018)", None),
 (b.K101, "07-legea-101-2016-remedii-si-cai-de-atac", "Legea nr. 101/2016 privind remediile și căile de atac", None),
 (b.KORD, "08-ordinul-1792-2002-act-de-aprobare", "Ordinul M.F.P. nr. 1.792/2002 (actul de aprobare a Normelor ALOP)", []),
 (b.KALOP, "09-norme-alop-1792-2002", "Normele metodologice ALOP (anexa la Ordinul M.F.P. nr. 1.792/2002)", None),
 (b.K500, "10-legea-500-2002-finantele-publice", "Legea nr. 500/2002 privind finanțele publice", None),
]

# Etapa 2: trimiteri către alt act din cele 9. Cum numește textul actul (regex la începutul
# frazei de după „din/al/potrivit”) → (fișier-țintă, anexă). Se încearcă în ordine.
SCURT = {b.K98: "Legea 98/2016", b.K395C: "HG 395/2016", b.K395: "Normele HG 395/2016", b.KOUG: "OUG 98/2017",
         b.K419C: "HG 419/2018", b.K419: "Normele HG 419/2018", b.K101: "Legea 101/2016", b.KORD: "Ordinul 1792/2002",
         b.KALOP: "Normele ALOP", b.K500: "Legea 500/2002"}
ALIASURI = [
 (r"Legea nr\.\s*98/2016\b", b.K98, ""),
 (r"Legea nr\.\s*101/2016\b", b.K101, ""),
 (r"Legea nr\.\s*500/2002\b", b.K500, ""),
 (r"Ordonanța de urgență a Guvernului nr\.\s*98/2017\b|O\.\s*U\.\s*G\.\s*nr\.\s*98/2017\b", b.KOUG, ""),
 (r"Hotărârea Guvernului nr\.\s*395/2016\b|H\.\s*G\.\s*nr\.\s*395/2016\b", b.K395C, ""),
 (r"Hotărârea Guvernului nr\.\s*419/2018\b|H\.\s*G\.\s*nr\.\s*419/2018\b", b.K419C, ""),
]
# denumiri prescurtate valabile doar într-un anumit act (Normele spun „ordonanța de urgență” pentru OUG 111/2010)
# „din Lege” (cu L mare) = Legea 98/2016 în Normele H.G. 395 și în actul de aprobare; „ordonanța de urgență” = O.U.G. 98/2017
# în Normele H.G. 419. „Lege\b” se potrivește cu diferențiere de majuscule, ca „lege” (orice lege) să nu fie legată.
ALIASURI_LOCALE = {
 b.K395: [(r"Lege\b", b.K98, "")],
 b.K395C: [(r"Lege\b", b.K98, "")],
 b.K419: [(r"ordonan[țt](?:a|ei) de urgen[țt]ă\b(?!\s+a Guvernului nr\.)", b.KOUG, "")],
}
_SENSIBILE = {r"Lege\b"}

def act_numit(fraza, fisier_curent):
    """(fișierul-țintă, anexa) al actului numit la începutul frazei de după o trimitere, sau None."""
    for rx, f, anexa in ALIASURI_LOCALE.get(fisier_curent, []) + ALIASURI:
        if re.match(rx, fraza, 0 if rx in _SENSIBILE else re.I):
            return (f, anexa)
    return None
INDEX = {}      # (fișier, anexă) → indexeaza(...), umplut de main() înainte de redare

def fabrica_extern(fisier_curent):
    """rez_extern(fraza) pentru trimiteri.marcheaza: actul numit după trimitere → (rezolvator, pagina)."""
    slug_de = {f: s for f, s, _, _ in ACTE}
    def rez_extern(fraza):
        t = act_numit(fraza, fisier_curent)
        if t:
            f, anexa = t
            idx = INDEX.get((f, anexa))
            if not idx: return None
            baza, prefix = rezolvator(idx), SCURT[f] + (" " + anexa if anexa else "") + ", "
            def r(fel, art, alin, lit, grup, _b=baza, _p=prefix):
                t = _b(fel, art, alin, lit, grup); return (t[0], _p + t[1]) if t else None
            return r, ("" if f == fisier_curent else slug_de[f] + ".html")
        return None
    return rez_extern

_ART = unitati.RX_ARTICOL
_ALIN = re.compile(r"^\((\d+(?:\^\d+)?)\)\s*(.*)$")
_LIT = re.compile(r"^([a-zșț](?:\^\d+)?)\)\s*(.*)$")
_GRUP = re.compile(r"^([A-ZȘȚ](?:\^\d+)?)\.\s+(.*)$")
_LINIUTA = re.compile(r"^[-–]\s+(.*)$")
_TITLU_SECT = re.compile(r"^## (Titlul|Capitolul|Sec[țţ]iunea|§\d+\.)\s*(.*)$")
_NIVEL = {"Titlul": 1, "Capitolul": 2, "Secțiunea": 3, "Secţiunea": 3}
_TABEL = re.compile(r"^Tabelul nr\.\s*\d+")
_ABROGAT = re.compile(r"^\s*(\(\d+\)\s*)?Abrogat")
_RIGLA = re.compile(r"^[─-╿_\-—\s]{5,}$")   # rigle și chenare desenate (─ ┌ ┴ ┘ …), fără text

def _structurala(l):
    return bool(_ART.match(l) or _ALIN.match(l) or _LIT.match(l) or _GRUP.match(l)
                or l.startswith("## ") or l.startswith("§"))

def parseaza(cale, anexe_redate=None):
    """Întoarce {sursa, titlu:[…], meta:{}, corp:[blocuri], anexe:[{nume, titlu, blocuri}]}.
    Bloc = {"tip":"sect", nivel, eticheta, titlu} | {"tip":"art", nr, titlu, continut:[(tip, text)], note:[…]}
         | {"tip":"text", text}."""
    linii = [l.rstrip() for l in open(cale, encoding="utf-8").read().split("\n")]
    linii = [l[:-2] if l.endswith(" +") else l for l in linii]       # artefact al portalului
    # riglele orizontale ale tabelelor („──────”, anexa VI la Legea 153) sunt un singur „cuvânt”
    # de 70+ caractere fără punct de rupere: lățesc pagina peste ecran și tableta o micșorează
    linii = ["" if _RIGLA.match(l) else l for l in linii]
    doc = {"sursa": "", "titlu": [], "meta": {}, "corp": [], "anexe": []}
    blocuri, art, in_preambul, anexa_activa = doc["corp"], None, True, True
    fisier = os.path.basename(cale); zona_puncte = unitati.ZONE_SPECIALE.get(fisier)
    i = 0
    while i < len(linii):
        l = linii[i]; i += 1
        if not l: continue
        if l.startswith("§SURSA§"):
            doc["sursa"] = l[len("§SURSA§"):].strip(); continue
        if l.startswith("§ANEXA§"):
            nume = l[len("§ANEXA§"):].strip()
            anexa_activa = anexe_redate is None or nume in anexe_redate
            if not anexa_activa: doc.setdefault("anexe_omise", []).append(nume)
            art, in_preambul = None, False
            zona_puncte = unitati.ZONE_SPECIALE.get(fisier + "#" + nume)
            if anexa_activa:
                titlu = ""
                if i < len(linii) and linii[i] and not _structurala(linii[i]):
                    titlu = linii[i]; i += 1
                doc["anexe"].append({"nume": nume, "titlu": titlu, "blocuri": []})
                blocuri = doc["anexe"][-1]["blocuri"]
            continue
        if not anexa_activa: continue
        if l.startswith("§NOTA§"):
            nota = l[len("§NOTA§"):].strip()
            if art: art["note"].append(nota)
            elif blocuri: blocuri.append({"tip": "nota", "text": nota})
            continue
        if l.startswith("## "):
            if l in ("## EMITENT", "## Publicat în"):
                if i < len(linii): doc["meta"][l[3:]] = linii[i]; i += 1
                continue
            m = _TITLU_SECT.match(l)
            fel = m.group(1) if m else l[3:]
            nivel = _NIVEL.get(fel, 4 if fel.startswith("§") else 2)
            titlu = ""
            if i < len(linii) and linii[i] and not _structurala(linii[i]):
                titlu = linii[i]; i += 1
            blocuri.append({"tip": "sect", "nivel": nivel, "eticheta": l[3:], "titlu": titlu})
            art, in_preambul = None, False
            continue
        e = unitati.eticheta_titlu(l, zona_puncte)
        if e:
            art = {"tip": "art", "nr": e, "titlu": "", "continut": [], "note": [], "zona": zona_puncte}
            blocuri.append(art); in_preambul = False
            if e.startswith("pct. "):            # punctele au titlul pe același rând: „3. Ordonanțarea …”
                art["titlu"] = re.sub(r"^\d+\.\s*", "", l); continue
            # titlu marginal: rând scurt, fără punctuație finală, care nu e text normativ
            if i < len(linii) and linii[i] and not _structurala(linii[i]) \
               and len(linii[i]) <= 90 and not linii[i].endswith((".", ";", ":", ",")):
                art["titlu"] = linii[i]; i += 1
            continue
        if in_preambul:
            doc["titlu"].append(l); continue
        tinta = art["continut"] if art else None
        if tinta is None:
            blocuri.append({"tip": "text", "text": l}); continue
        if _TABEL.match(l):
            rows = [l]
            while i < len(linii) and linii[i] and not _structurala(linii[i]) and not _TABEL.match(linii[i]):
                rows.append(linii[i]); i += 1
            tinta.append(("tabel", rows)); continue
        m = _ALIN.match(l)
        if m: tinta.append(("alin", (m.group(1), m.group(2)))); continue
        m = _GRUP.match(l)
        if m: tinta.append(("grup", l)); continue
        m = _LIT.match(l)
        if m: tinta.append(("lit", (m.group(1), m.group(2)))); continue
        m = _LINIUTA.match(l)
        if m: tinta.append(("liniuta", m.group(1))); continue
        tinta.append(("text", l))
    for bl in [doc["corp"]] + [ax["blocuri"] for ax in doc["anexe"]]:
        for b in bl:
            if b["tip"] == "art": _aplatizeaza_citat(b)
    return doc

# Articolele romane de modificare (H.G. 419, art. II–VI) citează textul pe care îl modifică:
# „(3) Strategia de contractare …”, „a) etapa de planificare”. Acele rânduri nu sunt alineatele sau
# literele articolului, deci se redau ca text simplu — fără id-uri și fără să devină ținte de trimiteri.
_MODIFICARE = re.compile(r"se modifică|se completează|se introduc|va avea următorul cuprins|vor avea următorul cuprins")

def _aplatizeaza_citat(art):
    if art.pop("zona", None) != unitati.DOAR_ROMANE: return
    if not any(t == "text" and _MODIFICARE.search(v) for t, v in art["continut"]): return
    plat = []
    for t, v in art["continut"]:
        if t == "alin": plat.append(("text", "(%s) %s" % v))
        elif t == "lit": plat.append(("text", "%s) %s" % v))
        elif t == "grup": plat.append(("text", v))
        else: plat.append((t, v))
    art["continut"] = plat

# ---------------------------------------------------------------- HTML


JS = """
(function(){
  var K='leg-toata', cb=document.getElementById('leg-tot'); if(!cb) return;
  function aplica(){ document.body.classList.toggle('doar-bib', !cb.checked);
    try{ localStorage.setItem(K, cb.checked?'1':'0'); }catch(e){} }
  try{ cb.checked = localStorage.getItem(K)==='1'; }catch(e){}
  cb.addEventListener('change', aplica); aplica();
  function tinta(){ var h=location.hash; if(!h) return; var el=document.getElementById(h.slice(1)); if(!el) return;
    var a=el.closest('.leg-art'); if(!cb.checked && ((a && !a.classList.contains('bib')) || el.closest('.leg-sect:not(.are-bib), .leg-anexa:not(.are-bib)'))){ cb.checked=true; aplica(); }
    el.scrollIntoView(); }
  window.addEventListener('hashchange', tinta); tinta();
  var f=document.getElementById('leg-sari'); if(f) f.addEventListener('submit', function(e){ e.preventDefault();
    var brut=f.querySelector('input').value.trim(); if(!brut) return;
    /* „113^1”, „113-1”, „v” (roman), „pct. 3” sau „3” pe pagina cu puncte (ALOP), „preambul” */
    var v=brut.replace(/^(art|pct)\\.?\\s*/i,'').replace(/\\s+/g,'').replace('^','-');
    var cand=/^pre/i.test(brut) ? ['preambul'] : ['art-'+v, 'art-'+v.toUpperCase(), 'pct-'+v];
    var id=cand.filter(function(c){ return document.getElementById(c); })[0];
    if(!id){ f.querySelector('input').setCustomValidity('Nu există '+brut+' pe această pagină'); f.reportValidity();
      setTimeout(function(){ f.querySelector('input').setCustomValidity(''); },1500); return; }
    location.hash='#'+id; });

  /* Trimiteri: la apăsare, sub paragraf se deschide un chenar cu textul țintei, copiat din pagină. */
  function urmatoarele(el, oprire, accepta){ var out=[el], s=el.nextElementSibling;
    while(s && !oprire(s)){ if(accepta(s)) out.push(s); s=s.nextElementSibling; } return out; }
  function extrage(el){
    if(el.classList.contains('leg-art')) return Array.prototype.filter.call(el.children, function(c){ return c.tagName!=='H4' && !c.classList.contains('leg-note'); });
    if(el.classList.contains('alin')) return urmatoarele(el, function(s){ return s.classList.contains('alin') || s.tagName==='DETAILS'; }, function(s){ return s.tagName==='P' || s.classList.contains('grup'); });
    if(el.classList.contains('grup')) return urmatoarele(el, function(s){ return s.classList.contains('alin') || s.classList.contains('grup') || s.tagName==='DETAILS'; }, function(s){ return s.tagName==='P'; });
    return urmatoarele(el, function(s){ return !s.classList.contains('liniuta') && !s.classList.contains('trm-box'); }, function(s){ return s.classList.contains('liniuta'); });
  }
  function curata(n, pag){ var c=n.cloneNode(true); if(c.removeAttribute) c.removeAttribute('id');
    c.querySelectorAll('[id]').forEach(function(x){ x.removeAttribute('id'); });
    c.querySelectorAll('.trm-box').forEach(function(x){ x.remove(); });
    if(pag) c.querySelectorAll('a.trm').forEach(function(x){   /* textul vine din altă pagină: trimiterile lui interne rămân ale acelei pagini */
      x.dataset.t=x.dataset.t.split(' ').map(function(t){ return t.indexOf('#')<0 ? pag+'#'+t : t; }).join(' ');
      if(x.getAttribute('href').charAt(0)==='#') x.setAttribute('href', pag+x.getAttribute('href')); });
    return c; }
  /* Ținta poate fi în altă pagină („07-….html#art-8”): pagina se ia cu fetch (e în cache-ul offline) și se parsează o singură dată. */
  var docs={};
  function iaDoc(pag, cb){ if(!pag) return cb(document); if(docs[pag]) return cb(docs[pag]);
    fetch(pag).then(function(r){ return r.text(); }).then(function(t){ docs[pag]=new DOMParser().parseFromString(t,'text/html'); cb(docs[pag]); })
      .catch(function(){ cb(null); }); }
  document.addEventListener('click', function(ev){
    var a=ev.target.closest('a.trm'); if(!a) return; ev.preventDefault();
    var bloc=a.closest('p, .grup, .leg-titlu'); if(!bloc) return;
    var existent=bloc.nextElementSibling;
    if(existent && existent.classList.contains('trm-box') && existent.dataset.de===a.dataset.t){ existent.remove(); a.classList.remove('deschis'); return; }
    var box=document.createElement('div'); box.className='trm-box'; box.dataset.de=a.dataset.t;
    var ids=a.dataset.t.split(' '), et=a.dataset.e.split('|');
    ids.forEach(function(ref, i){ var p=ref.split('#'), pag=p.length>1?p[0]:'', id=p[p.length-1];
      var cont=document.createElement('div'); box.appendChild(cont);
      var h=document.createElement('div'); h.className='trm-h';
      h.innerHTML='<b></b><a href="'+pag+'#'+id+'">mergi la text ↗</a>'+(i===0?'<button type="button" aria-label="Închide">×</button>':'');
      h.querySelector('b').textContent=et[i]||id; cont.appendChild(h);
      iaDoc(pag, function(doc){ var el=doc && doc.getElementById(id);
        if(!el){ var e=document.createElement('p');
          e.textContent = doc ? 'Textul nu a fost găsit.' : (location.protocol==='file:'
            ? 'Deschisă direct din fișier, pagina nu poate încărca textul altui act în chenar (browserul blochează). Folosește „mergi la text” sau adresa publicată a aplicației.'
            : 'Pagina actului nu a putut fi încărcată. Folosește „mergi la text”.');
          cont.appendChild(e); return; }
        extrage(el).forEach(function(n){ cont.appendChild(curata(n, pag)); }); }); });
    box.addEventListener('click', function(e){ if(e.target.tagName==='BUTTON'){ box.remove(); a.classList.remove('deschis'); } });
    bloc.insertAdjacentElement('afterend', box); a.classList.add('deschis');
  });
})();
"""

SUBSOL = ("Textele sunt formele consolidate la zi de pe legislatie.just.ro, redate fără modificări; "
          "notele portalului sunt strânse sub fiecare articol.")

def ancora(nr, anexa=""):
    return unitati.ancora(nr, anexa)

def _ph(cls, inner, nr=None, idd=None):
    """Paragraf cu conținut deja redat în HTML (textul trece prin txt()/marcheaza)."""
    n = '<span class="nr">%s</span>' % html.escape(nr) if nr else ""
    return '<p class="%s"%s>%s%s</p>' % (cls, ' id="%s"' % idd if idd else "", n, inner)

def indexeaza(blocuri, anexa):
    """Id-urile alineatelor, grupurilor și literelor fiecărui articol din zonă, pentru ancore și
    pentru rezolvarea trimiterilor. d["ids"][k] = id-ul elementului k din continut (sau None)."""
    idx = {}
    for b in blocuri:
        if b["tip"] != "art": continue
        e = ancora(b["nr"], anexa)
        d = {"id": e, "alin": {}, "lit": {}, "grup": {}, "ids": []}
        alin = grup = None
        for tip, v in b["continut"]:
            idd = None
            if tip == "alin":
                alin, grup = v[0], None
                idd = "%s-al-%s" % (e, alin.replace("^", "-"))
                d["alin"][alin] = {"id": idd, "lit": {}, "grup": {}}
            elif tip == "grup":
                grup = _GRUP.match(v).group(1)
                tinta = d["alin"][alin] if alin else d
                idd = "%s-g%s" % (tinta["id"], grup.replace("^", "-"))
                tinta["grup"].setdefault(grup, {"id": idd, "lit": {}})
            elif tip == "lit":
                tinta = d["alin"][alin] if alin else d
                baza = tinta["grup"][grup] if grup else tinta
                idd = "%s-lit-%s" % (baza["id"], v[0].replace("^", "-"))
                if idd in d["ids"]: idd += "-%d" % (d["ids"].count(idd) + 1)   # literă repetată fără grup
                if grup: baza["lit"][v[0]] = idd
                tinta["lit"].setdefault(v[0], []).append(idd)
            d["ids"].append(idd)
        idx[b["nr"]] = d
    return idx

def rezolvator(idx):
    """rez(fel, art, alin, lit, grup) → (id, etichetă) sau None, pentru trimiteri.marcheaza."""
    def rez(fel, art, alin, lit, grup):
        d = idx.get(art)
        if not d: return None
        et = "art. %s" % art
        if fel == "art": return d["id"], et
        if alin is not None:
            al = d["alin"].get(alin)
            if not al: return None
            et += " alin. (%s)" % alin
            if fel == "alin": return al["id"], et
            tinta = al
        else:
            if fel == "alin": return None
            tinta = d
        if grup:
            g = tinta["grup"].get(grup)
            lid = g["lit"].get(lit) if g else None
            return (lid, "%s %s. lit. %s)" % (et, grup, lit)) if lid else None
        ids = tinta["lit"].get(lit, [])
        return (ids[0], "%s lit. %s)" % (et, lit)) if len(ids) == 1 else None    # ambiguu (mai multe grupuri) → nelegat
    return rez

def art_html(art, anexa, cerute, restrictii, idx=None, stat=None, rez_extern=None):
    nr, e = art["nr"], ancora(art["nr"], anexa)
    in_bib = nr in cerute
    d = (idx or {}).get(nr, {"ids": [None] * len(art["continut"])})
    rez = rezolvator(idx) if idx else None
    alin = grup = None
    def txt(s):
        return marcheaza(s, (nr, alin, grup), rez, stat, rez_extern) if rez else html.escape(s)
    prim = art["continut"][0] if art["continut"] else None
    prim_text = (prim[1] if prim[0] == "text" else (prim[1][1] if prim[0] in ("alin", "lit") else "")) if prim else ""
    abrogat = not art["continut"] or bool(_ABROGAT.match(prim_text)) or (prim and prim[0] == "alin" and prim[1][0] == "1" and _ABROGAT.match(prim[1][1]) and len(art["continut"]) == 1)
    cls = "leg-art" + (" bib" if in_bib else "") + (" abrogat" if abrogat else "")
    h = ['<article class="%s" id="%s"><h4>Art. %s' % (cls, e, html.escape(nr))]
    if in_bib: h.append('<span class="badge bib">bibliografie</span>')
    if abrogat: h.append('<span class="badge abrogat">abrogat</span>')
    r = restrictii.get(nr)
    if r and in_bib: h.append('<span class="restr">în bibliografie %s</span>' % html.escape(r))
    h.append("</h4>")
    if art["titlu"]: h.append('<div class="leg-titlu">%s</div>' % html.escape(art["titlu"]))
    for k, (tip, v) in enumerate(art["continut"]):
        idd = d["ids"][k] if k < len(d["ids"]) else None
        if tip == "alin":
            alin, grup = v[0], None
            h.append(_ph("alin", txt(v[1]), "(%s)" % v[0], idd))
        elif tip == "lit": h.append(_ph("lit", txt(v[1]), "%s)" % v[0], idd))
        elif tip == "grup":
            grup = _GRUP.match(v).group(1)
            h.append('<div class="grup"%s>%s</div>' % (' id="%s"' % idd if idd else "", txt(v)))
        elif tip == "liniuta": h.append(_ph("liniuta", txt(v)))
        elif tip == "tabel": h.append('<div class="leg-tabel"><span class="t">%s</span>%s</div>' % (html.escape(v[0]), html.escape(" ".join(v[1:]))))
        else: h.append(_ph("text", txt(v)))
    if art["note"]:
        h.append('<details class="leg-note"><summary>Note (%d)</summary>%s</details>'
                 % (len(art["note"]), "".join("<p>%s</p>" % html.escape(n) for n in art["note"])))
    h.append("</article>")
    return "".join(h), in_bib

def blocuri_html(blocuri, anexa, cerute, restrictii, stat=None, rez_extern=None):
    """Redă o listă de blocuri; secțiunile se închid la următoarea secțiune de nivel ≤."""
    idx = indexeaza(blocuri, anexa)
    # 1) ce secțiune conține articole din bibliografie (până la următoarea de nivel ≤)
    are_bib = []
    for i, b in enumerate(blocuri):
        if b["tip"] != "sect": continue
        ok = False
        for c in blocuri[i + 1:]:
            if c["tip"] == "sect" and c["nivel"] <= b["nivel"]: break
            if c["tip"] == "art" and c["nr"] in cerute: ok = True; break
        are_bib.append(ok)
    # 2) HTML
    out, cuprins, deschise, n_bib, n_art, k = [], [], [], 0, 0, 0
    for b in blocuri:
        if b["tip"] == "sect":
            ok = are_bib[k]; k += 1
            while deschise and deschise[-1] >= b["nivel"]:
                out.append("</section>"); deschise.pop()
            sid = "s-%d" % k + ("-" + re.sub(r"[^A-Za-z0-9]+", "-", anexa).strip("-").lower() if anexa else "")
            out.append('<section class="leg-sect n%d%s" id="%s"><h3>%s%s</h3>'
                       % (b["nivel"], " are-bib" if ok else "", sid, html.escape(b["eticheta"]),
                          "<small>%s</small>" % html.escape(b["titlu"]) if b["titlu"] else ""))
            deschise.append(b["nivel"])
            cuprins.append((b["nivel"], sid, b["eticheta"], b["titlu"], ok))
        elif b["tip"] == "art":
            h, in_bib = art_html(b, anexa, cerute, restrictii, idx, stat, rez_extern)
            out.append(h); n_art += 1; n_bib += in_bib
        elif b["tip"] == "nota":
            out.append('<p class="leg-nota-libera">%s</p>' % html.escape(b["text"]))
        else:
            out.append('<p class="leg-text">%s</p>' % html.escape(b["text"]))
    out.extend("</section>" for _ in deschise)
    return "".join(out), cuprins, n_art, n_bib

def cuprins_html(intrari):
    li = []
    for nivel, sid, eticheta, titlu, ok in intrari:
        li.append('<li class="n%d%s"><a href="#%s">%s%s</a></li>'
                  % (nivel, " are-bib" if ok else "", sid, html.escape(eticheta), (" — " + html.escape(titlu)) if titlu else ""))
    return '<details class="accordion leg-cuprins"><summary><span>Cuprins</span><svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"></polyline></svg></summary><div class="accordion-body"><ul>%s</ul></div></details>' % "".join(li)

def pagina(fisier, slug, denumire, anexe_redate, bib, doc=None):
    doc = doc or parseaza(os.path.join(LEG, fisier), anexe_redate)
    cerute_corp = set(bib.get(fisier, ("", "", [], [], [], {}))[2])
    restr_corp = {a: r for (f, a), r in RESTRICTII.items() if f == fisier}
    stat, rez_extern = {}, fabrica_extern(fisier)
    corp_html, cuprins, n_art, n_bib = blocuri_html(doc["corp"], "", cerute_corp, restr_corp, stat, rez_extern)
    anexe_html = []
    for ax in doc["anexe"]:
        cheie = fisier + "#" + ax["nume"]
        cerute = set(bib[cheie][2]) if cheie in bib else set()
        restr = {a: r for (f, a), r in RESTRICTII.items() if f == cheie}
        h, cup, na, nb = blocuri_html(ax["blocuri"], ax["nume"], cerute, restr, stat, rez_extern)
        n_art += na; n_bib += nb
        aid = "anexa-" + re.sub(r"[^A-Za-z0-9]+", "-", ax["nume"]).strip("-").lower()
        anexe_html.append('<section class="leg-anexa%s" id="%s"><h3>%s%s</h3>%s</section>'
                          % (" are-bib" if nb else "", aid, html.escape(ax["nume"]),
                             "<small>%s</small>" % html.escape(ax["titlu"]) if ax["titlu"] else "", h))
        cuprins.append((1, aid, ax["nume"], ax["titlu"], bool(nb)))
        cuprins.extend((min(nivel + 1, 4), sid, et, ti, ok) for nivel, sid, et, ti, ok in cup)
    consolidare = re.search(r"consolidarea din [\d.]+", doc["sursa"])
    url = doc["sursa"].split("|")[0].strip()
    meta = " · ".join(x for x in [consolidare.group(0) if consolidare else "", "%d articole, %d cerute în bibliografie" % (n_art, n_bib)] if x)
    if url: meta = html.escape(meta) + ' · <a href="https://%s">sursa pe portal</a>' % html.escape(url)
    else: meta = html.escape(meta)
    poz = next((i for i, a in enumerate(ACTE) if a[0] == fisier), 0) + 1
    corp = [carcasa.cap("Actul %d din %d" % (poz, len(ACTE)), denumire, ("index.html", "Toate actele"), meta)]
    corp.append('<div class="leg-bar"><label class="leg-comutator"><input type="checkbox" id="leg-tot" role="switch"> Arată toată legea</label>'
                '<form id="leg-sari" class="leg-sari"><label for="leg-sari-nr">Sari la art.</label><input id="leg-sari-nr" type="text" '
                'inputmode="numeric" placeholder="nr." aria-label="numărul articolului sau al punctului"><button type="submit">Sari</button></form></div>')
    if doc["titlu"] or doc["meta"]:
        corp.append('<div class="card leg-preambul" id="%s">%s%s</div>'
                    % (unitati.ancora(unitati.PREAMBUL), "".join("<p>%s</p>" % html.escape(t) for t in doc["titlu"]),
                       "".join('<p><strong>%s:</strong> %s</p>' % (html.escape(k), html.escape(v)) for k, v in doc["meta"].items())))
    corp.append(cuprins_html(cuprins))
    corp.append(corp_html)
    corp.extend(anexe_html)
    if anexe_redate is not None and doc.get("anexe_omise"):
        corp.append('<p class="leg-omis">Anexele actului care nu sunt în bibliografie (%s) nu sunt redate aici.</p>'
                    % html.escape(", ".join(doc["anexe_omise"])))
    corp.append('<div class="actions"><a class="btn btn-outline" href="index.html">Toate actele</a><a class="btn btn-outline" href="../index.html">Înapoi la teste</a></div>')
    return carcasa.pagina(denumire, "".join(corp), "legislatie", subsol=SUBSOL, script=JS, cls="pagina-lege"), doc, n_art, n_bib, stat

def index_html(rows):
    li = "".join('<li><a class="rand-lista" href="%s.html"><span class="nr">%02d</span><span class="text"><span class="titlu">%s</span>'
                 '<span class="det">%s</span></span>%s</a></li>'
                 % (slug, i + 1, html.escape(den), html.escape(sub), carcasa.icon("dreapta", 18)) for i, (slug, den, sub) in enumerate(rows))
    corp = (carcasa.cap("%d acte · text integral consolidat" % len(ACTE), "Legislația din bibliografie",
                        meta='Legile, actele de aprobare și normele lor, în text integral consolidat. Implicit se văd doar articolele '
                             'cerute în bibliografie (marcate <span class="badge bib">bibliografie</span>); comutatorul „Arată toată legea” '
                             'descoperă și restul.')
            + '<ul class="lista">%s</ul>' % li)
    return carcasa.pagina("Legislația din bibliografie", corp, "legislatie", pe_index=True, subsol=SUBSOL)

def main():
    os.makedirs(OUT, exist_ok=True)
    bib = bib_tematica()
    rows, fisiere, erori = [], ["./legislatie/index.html"], 0
    # toate actele se parsează întâi, ca trimiterile către alt act să aibă indexul țintei
    docs = {fisier: parseaza(os.path.join(LEG, fisier), anexe_redate) for fisier, _, _, anexe_redate in ACTE}
    for fisier, doc in docs.items():
        INDEX[(fisier, "")] = indexeaza(doc["corp"], "")
        for ax in doc["anexe"]: INDEX[(fisier, ax["nume"])] = indexeaza(ax["blocuri"], ax["nume"])
    for fisier, slug, denumire, anexe_redate in ACTE:
        pag, doc, n_art, n_bib, stat = pagina(fisier, slug, denumire, anexe_redate, bib, docs[fisier])
        # asertări: fiecare articol cerut are ancoră; numărul de articole din corp = cel văzut de bibliografie.py
        for cheie, (f, anexa, cerute, _l, _a, arts) in bib.items():
            if f != fisier: continue
            for a in cerute:
                if 'id="%s"' % ancora(a, anexa) not in pag:
                    erori += 1; print("  EROARE %s: art. %s%s cerut în bibliografie, fără ancoră în pagină" % (fisier, a, " " + anexa if anexa else ""))
            if not anexa:
                n_corp = sum(1 for b in doc["corp"] if b["tip"] == "art")
                n_text = len([a for a in arts if a != unitati.PREAMBUL])     # preambulul e card separat, nu articol
                if n_corp != n_text:
                    erori += 1; print("  EROARE %s: %d articole redate, %d în articole_din_text()" % (fisier, n_corp, n_text))
        dubluri = sorted(i for i, n in collections.Counter(re.findall(r'\bid="([^"]+)"', pag)).items() if n > 1)
        if dubluri:
            erori += 1; print("  EROARE %s: %d id-uri duplicate, ex. %s" % (fisier, len(dubluri), ", ".join(dubluri[:3])))
        nume = slug + ".html"
        open(os.path.join(OUT, nume), "w", encoding="utf-8").write(pag)
        fisiere.append("./legislatie/" + nume)
        consolidare = re.search(r"consolidarea din [\d.]+", doc["sursa"])
        rows.append((slug, denumire, "%d articole cerute din %d · %s" % (n_bib, n_art, consolidare.group(0) if consolidare else "")))
        print("%-46s %4d art., %3d în bibl., trimiteri: %4d legate (%3d către alt act), %3d nelegate, %3d alt act necunoscut, %5d KB"
              % (fisier[:46], n_art, n_bib, stat.get("legate", 0), stat.get("extern_legate", 0), stat.get("nelegate", 0), stat.get("extern", 0), len(pag) // 1024))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(index_html(rows))
    sw = os.path.join(DIR, "..", "sw.js"); s = open(sw, encoding="utf-8").read()
    bloc = "/* LEGISLATIE-START */\n" + "".join('  "%s",\n' % f for f in fisiere) + "  /* LEGISLATIE-END */"
    s2 = re.sub(r"/\* LEGISLATIE-START \*/.*?/\* LEGISLATIE-END \*/", bloc, s, flags=re.S)
    if s2 != s: open(sw, "w", encoding="utf-8").write(s2); print("sw.js: %d fișiere de legislație în FISIERE" % len(fisiere))
    print("erori: %d" % erori)
    sys.exit(1 if erori else 0)

if __name__ == "__main__":
    main()
