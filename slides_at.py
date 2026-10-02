# -*- coding: utf-8 -*-
"""Erzeugt das Ergebnis-Deck Oesterreich als HTML und rendert es zu PDF.

Aufruf:  python3 slides_at.py          # HTML schreiben
         python3 slides_at.py --pdf    # zusaetzlich mit Chromium zu PDF rendern

Alle Zahlen stammen aus NEOH_AT_analyse.csv und ERGEBNISSE_AT_funnel.csv und
werden hier neu berechnet, nicht abgeschrieben. Die Funnel-Stufen werden
hierarchisch gebildet wie in Stufe 1 (Betracht und Kauf nur unter Kennern),
damit Deck und Ergebnisdokumente dieselben Werte zeigen.

Farben nach der validierten Standardpalette: Akzent #2a78d6, Zweitserie
#eb6834, Flaechen und Schrift aus den dokumentierten Chrome-Rollen. Das Deck
ist fuer Druck und PDF gedacht und daher nur im hellen Modus ausgelegt.
"""
import csv, io, json, math, re, subprocess, sys, collections
import numpy as np

# Die Markenvarianten der Spontannennungen werden aus Stufe 4 uebernommen,
# damit beide Auswertungen dieselbe Zuordnung verwenden.
from analyse_segmente_text_at import marken_im_text

ASSETS = 'assets'
DATEN = 'NEOH_AT_analyse.csv'
FUNNEL = 'ERGEBNISSE_AT_funnel.csv'
BEKANNT = 'ERGEBNISSE_AT_bekanntheit.csv'
AUS_HTML = 'SLIDES_AT.html'
AUS_PDF = 'SLIDES_AT.pdf'
NEOH, KEINE = '13', '99'

# Standardpalette (validiert gegen die Flaeche, siehe dataviz-Richtlinie).
# Liegt assets/marke.json vor, werden Akzent, Flaeche, Schriftfarbe und die
# ordinale Rampe daraus abgeleitet - siehe marke_laden() weiter unten.
AKZENT = '#2a78d6'
ZWEIT = '#eb6834'
GUT = '#0ca30c'
INK = '#0b0b0b'
INK2 = '#52514e'
MUTED = '#898781'
GRID = '#e1e0d9'
BASE = '#c3c2b7'
FLAECHE = '#fdfdfc'
SCHRIFT = '"Helvetica Neue",Helvetica,Arial,sans-serif'
# Ordinale Rampe fuer die Funnel-Stufen (eine Hue, monoton, validiert)
ST_KAUF, ST_ERW, ST_KENNT, ST_FREMD = '#184f95', '#2a78d6', '#86b6ef', '#e9e8e3'


def _hex(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hexs(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(c)))) for c in rgb)


def _lum(h):
    def k(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (k(c) for c in _hex(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a, b):
    la, lb = _lum(a), _lum(b)
    hell, dunkel = max(la, lb), min(la, lb)
    return (hell + 0.05) / (dunkel + 0.05)


def auf(farbe, hell='#ffffff', dunkel='#0b0b0b'):
    """Lesbare Schriftfarbe auf einer Flaeche - gewaehlt, nicht geraten."""
    return hell if kontrast(farbe, hell) >= kontrast(farbe, dunkel) else dunkel


def _mische(a, b, t):
    ra, rb = _hex(a), _hex(b)
    return _hexs([ra[i] + (rb[i] - ra[i]) * t for i in range(3)])


def marke_laden():
    """Markenfarben aus assets/marke.json uebernehmen, falls vorhanden.

    Erwartet werden die Schluessel akzent (Pflicht), zweit, flaeche, ink und
    schrift. Die ordinale Funnel-Rampe wird aus dem Akzent abgeleitet, damit
    sie eine Hue behaelt und monoton bleibt - eine beliebige Markenpalette
    erfuellt diese Bedingung nicht von selbst.
    """
    global AKZENT, ZWEIT, INK, INK2, MUTED, GRID, BASE, FLAECHE, SCHRIFT
    global ST_KAUF, ST_ERW, ST_KENNT, ST_FREMD
    import json, os
    pfad = os.path.join(ASSETS, 'marke.json')
    if not os.path.exists(pfad):
        return None
    m = json.load(io.open(pfad, encoding='utf-8'))
    AKZENT = m['akzent']
    ZWEIT = m.get('zweit', ZWEIT)
    FLAECHE = m.get('flaeche', FLAECHE)
    INK = m.get('ink', INK)
    SCHRIFT = m.get('schrift', SCHRIFT)
    INK2 = _mische(INK, FLAECHE, 0.34)
    MUTED = _mische(INK, FLAECHE, 0.58)
    GRID = _mische(INK, FLAECHE, 0.88)
    BASE = _mische(INK, FLAECHE, 0.76)
    ST_ERW = AKZENT
    ST_KAUF = _mische(AKZENT, '#000000', 0.34)
    ST_KENNT = _mische(AKZENT, FLAECHE, 0.55)
    ST_FREMD = _mische(INK, FLAECHE, 0.91)
    warn = []
    if kontrast(AKZENT, FLAECHE) < 3.0:
        warn.append('Akzent %s erreicht gegen die Flaeche nur %.2f:1 (Ziel 3:1). '
                    'Balken bleiben erkennbar, Text im Akzent nicht - die Folien '
                    'setzen Text deshalb in INK.' % (AKZENT, kontrast(AKZENT, FLAECHE)))
    if kontrast(ST_KENNT, FLAECHE) < 2.0:
        warn.append('Hellste Funnel-Stufe %s liegt bei %.2f:1 gegen die Flaeche '
                    '(Ziel 2:1 fuer ordinale Rampen).' % (ST_KENNT, kontrast(ST_KENNT, FLAECHE)))
    return warn


# Spaltenbreiten in Pixeln. Die SVG-viewBox wird exakt darauf gesetzt, damit
# Schriftgroessen 1:1 gerendert werden und nicht mitskalieren.
W_FULL, W_WIDE, W_HALF, W_NARROW = 1136, 784, 547, 310
H_CHART = 404          # Zielhoehe der Diagrammflaeche


def asset(*namen):
    """Erste vorhandene Datei aus assets/ als data-URI, sonst None.

    Logo und Produktbilder sind optional: Liegen sie nicht im Ordner, rendert
    das Deck ohne sie. Eingebettet wird als data-URI, damit das PDF
    eigenstaendig bleibt.
    """
    import base64, os, mimetypes
    for n in namen:
        for endung in ('.svg', '.png', '.jpg', '.jpeg', '.webp'):
            pfad = os.path.join(ASSETS, n + endung)
            if os.path.exists(pfad):
                typ = mimetypes.guess_type(pfad)[0] or 'application/octet-stream'
                roh = io.open(pfad, 'rb').read()
                return 'data:%s;base64,%s' % (typ, base64.b64encode(roh).decode())
    return None


def produktbilder(maximal=3):
    import glob, os
    gefunden = []
    for n in range(1, maximal + 1):
        u = asset('produkt-%d' % n, 'produkt%d' % n)
        if u:
            gefunden.append(u)
    return gefunden


def de(v, dec=1):
    """Zahl in deutscher Schreibweise, fuer jeden sichtbaren Text."""
    return ('%.*f' % (dec, v)).replace('.', ',')


def z(x):
    return float(x) if str(x).strip() else np.nan


def laden():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    # Hierarchische Bereinigung wie in Stufe 1
    marken = sorted({k.split('_', 1)[1] for k in d[0] if k.startswith('bekanntheit_')},
                    key=lambda c: int(c))
    for r in d:
        for c in marken:
            if r['bekanntheit_%s' % c] != '1':
                for stufe in ('betracht', 'kauf_3monate'):
                    r['%s_%s' % (stufe, c)] = '0'
        r['neoh_betracht'] = r['betracht_%s' % NEOH]
        r['neoh_kauf'] = r['kauf_3monate_%s' % NEOH]
    return d


def anteil(d, w, bed):
    m = np.array([bool(bed(r)) for r in d], dtype=bool)
    return 100 * float(w[m].sum() / w.sum()) if w.sum() else 0.0


# ---------------------------------------------------------------- SVG-Teile
def bar_h(werte, breite=W_HALF, hoehe=H_CHART, maxwert=None, einheit=' %',
          dec=1, hervor=None, farbe=None, lb=None):
    """Liegende Balken, 1:1 in Pixeln. werte: Liste (label, wert)."""
    maxwert = maxwert or max(w for _, w in werte) * 1.14
    lb = lb or min(190, int(breite * 0.27))
    zeile = min(44, max(20, hoehe / len(werte)))
    bh = min(18, zeile * 0.46)
    fs = 13.5 if zeile >= 30 else 12
    plot = breite - lb - 58
    s = ['<svg viewBox="0 0 %d %.0f" width="%d" height="%.0f" role="img">'
         % (breite, zeile * len(werte) + 6, breite, zeile * len(werte) + 6)]
    for i, (lab, v) in enumerate(werte):
        y = i * zeile + 3
        akt = (lab == hervor)
        f = farbe or (AKZENT if akt else '#ccd2d6')
        bw = max(2.0, plot * v / maxwert)
        s.append('<text x="%.0f" y="%.1f" text-anchor="end" font-size="%.1f" '
                 'fill="%s" font-weight="%d">%s</text>'
                 % (lb - 12, y + zeile / 2 + fs * 0.35, fs, INK if akt else INK2,
                    620 if akt else 400, lab))
        s.append('<rect x="%d" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s"/>'
                 % (lb, y + (zeile - bh) / 2, bw, bh, f))
        s.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" font-weight="%d">%s%s</text>'
                 % (lb + bw + 8, y + zeile / 2 + fs * 0.35, fs - 0.5,
                    INK if akt else MUTED, 620 if akt else 400, de(v, dec), einheit))
    s.append('</svg>')
    return ''.join(s)


def funnel_stapel(reihen, breite=W_WIDE, hoehe=H_CHART, hervor=None):
    """100-Prozent-Stapel je Marke: gekauft / erwogen / kennt / kennt nicht.

    reihen: (marke, bekannt, gekauft, erwogen_ohne_kauf) in Prozent der
    Gesamtstichprobe. Kaeufer ohne vorherige Erwaegung sind im Kaufblock
    enthalten, der Erwaegungsblock zaehlt nur die, die nicht gekauft haben.
    So wird der Funnel zwischen Marken vergleichbar, statt drei Balken je
    Marke nebeneinanderzustellen.
    """
    lb, rb = 150, 16
    sp = breite - lb - rb
    zeile = min(38, (hoehe - 26) / len(reihen))
    bh = min(21, zeile * 0.62)
    h = zeile * len(reihen) + 30
    s = ['<svg viewBox="0 0 %d %.0f" width="%d" height="%.0f" role="img">'
         % (breite, h, breite, h)]
    for i, (m, bek, kauf, bet_ohne) in enumerate(reihen):
        y = i * zeile + 6
        akt = (m == hervor)
        segmente = [(kauf, ST_KAUF), (bet_ohne, ST_ERW),
                    (bek - kauf - bet_ohne, ST_KENNT), (100 - bek, ST_FREMD)]
        x = lb
        s.append('<text x="%d" y="%.1f" text-anchor="end" font-size="13" fill="%s" '
                 'font-weight="%d">%s</text>'
                 % (lb - 12, y + bh / 2 + 4.5, INK if akt else INK2, 650 if akt else 400, m))
        for v, farbe in segmente:
            bw = sp * max(0.0, v) / 100
            if bw > 0.6:
                s.append('<rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" rx="3" '
                         'fill="%s" stroke="%s" stroke-width="2"/>'
                         % (x, y, bw, bh, farbe, FLAECHE))
            x += bw
        # Direktbeschriftung nur fuer Kauf und Erwaegung, wenn Platz ist
        if sp * kauf / 100 > 30:
            s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#ffffff" '
                     'font-weight="650" text-anchor="middle">%s</text>'
                     % (lb + sp * kauf / 200, y + bh / 2 + 4, de(kauf, 0)))
        s.append('<text x="%.1f" y="%.1f" font-size="12" fill="%s" font-weight="%d">%s&#8201;%%</text>'
                 % (lb + sp * bek / 100 + 8, y + bh / 2 + 4.3, INK if akt else MUTED,
                    650 if akt else 400, de(bek, 0)))
    s.append('</svg>')
    return ''.join(s)


def pyramide(stufen, breite=W_WIDE, hoehe=H_CHART, vergleich=None):
    """Markenpyramide: jede Stufe ist Teilmenge der darunterliegenden.

    stufen: (label, prozent, n, zusatz) von unten nach oben.
    vergleich: optionale Medianwerte der Uebergaenge, als Referenz rechts.
    """
    basis = breite * 0.48
    mitte = breite * 0.43
    zh = (hoehe - 34) / len(stufen)
    farben = [ST_KENNT, _mische(ST_KENNT, ST_ERW, 0.5), ST_ERW, ST_KAUF]
    maxv = stufen[0][1]
    s = ['<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
         % (breite, hoehe, breite, hoehe)]
    for i, (lab, v, nn, zusatz) in enumerate(stufen):
        y = hoehe - 20 - (i + 1) * zh
        b_u = basis * (stufen[i][1] / maxv) ** 0.45
        b_o = basis * (stufen[i + 1][1] / maxv) ** 0.45 if i + 1 < len(stufen) else b_u * 0.42
        s.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" '
                 'stroke="%s" stroke-width="2"/>'
                 % (mitte - b_u / 2, y + zh, mitte + b_u / 2, y + zh,
                    mitte + b_o / 2, y, mitte - b_o / 2, y, farben[i % len(farben)], FLAECHE))
        hell = i >= 2
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" '
                 'font-weight="650" fill="%s">%s&#8201;%%</text>'
                 % (mitte, y + zh / 2 + 7, 24 if zh > 54 else 19,
                    '#ffffff' if hell else INK, de(v)))
        s.append('<text x="%.1f" y="%.1f" font-size="14" font-weight="620" fill="%s">%s</text>'
                 % (mitte + basis / 2 + 26, y + zh / 2 - 2, INK, lab))
        s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="%s">%s</text>'
                 % (mitte + basis / 2 + 26, y + zh / 2 + 15, MUTED, zusatz))
        if i + 1 < len(stufen):
            rate = 100 * stufen[i + 1][1] / v
            ref = ''
            if vergleich and i < len(vergleich):
                ref = '  (Median %s&#8201;%%)' % de(vergleich[i], 0)
            s.append('<text x="6" y="%.1f" font-size="13" font-weight="620" '
                     'fill="%s">%s&#8201;%% weiter%s</text>'
                     % (y + 5, INK2, de(rate, 0), ref))
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="1" stroke-dasharray="3 3"/>'
                     % (142, y, mitte - b_o / 2 - 8, y, GRID))
    s.append('</svg>')
    return ''.join(s)


def funnel_trichter(stufen, breite=W_WIDE, hoehe=H_CHART):
    """Verjuengender Trichter mit den Abfluessen an jeder Stufe."""
    lb, rb = 40, 40
    sp = breite - lb - rb
    seg = sp / len(stufen)
    mitte = hoehe / 2 - 16
    maxh = hoehe * 0.52
    farben = [ST_KAUF, ST_ERW, ST_KENNT][::-1]
    s = ['<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
         % (breite, hoehe, breite, hoehe)]
    hoehen = [maxh * v / stufen[0][1] for _, v, _ in stufen]
    for i, (lab, v, sub) in enumerate(stufen):
        x0, x1 = lb + i * seg, lb + (i + 1) * seg
        h0 = hoehen[i]
        h1 = hoehen[i + 1] if i + 1 < len(hoehen) else h0 * 0.97
        s.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s"/>'
                 % (x0, mitte - h0 / 2, x1, mitte - h1 / 2,
                    x1, mitte + h1 / 2, x0, mitte + h0 / 2, farben[i]))
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="26" '
                 'font-weight="650" fill="#ffffff">%s&#8201;%%</text>'
                 % ((x0 + x1) / 2, mitte + 9, de(v)))
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="13.5" '
                 'font-weight="620" fill="%s">%s</text>'
                 % ((x0 + x1) / 2, mitte + maxh / 2 + 36, INK, lab))
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11.5" '
                 'fill="%s">%s</text>' % ((x0 + x1) / 2, mitte + maxh / 2 + 54, MUTED, sub))
        if i + 1 < len(stufen):
            verlust = v - stufen[i + 1][1]
            s.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="1.5" '
                     'stroke-dasharray="3 3"/>'
                     % (x1, mitte + h1 / 2 + 2, x1, mitte + maxh / 2 + 62, BASE))
            s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11.5" '
                     'fill="%s">&#8722;%s&#8201;Pp.</text>'
                     % (x1, mitte + maxh / 2 + 78, MUTED, de(verlust)))
            s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="13" '
                     'font-weight="620" fill="%s">%s&#8201;%% weiter</text>'
                     % (x1, mitte - maxh / 2 - 14, INK2, de(100 * stufen[i + 1][1] / v, 0)))
    s.append('</svg>')
    return ''.join(s)


def funnel_svg(stufen, breite=W_WIDE, hoehe=H_CHART):
    """Drei Stufen mit Uebergangsraten dazwischen, 1:1 in Pixeln."""
    lu = 86
    bw = (breite - 2 * lu - 12) / 3
    plot = hoehe - 86
    s = ['<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
         % (breite, hoehe, breite, hoehe),
         '<defs><marker id="pf" markerWidth="7" markerHeight="7" refX="6" refY="3.5" '
         'orient="auto"><path d="M0 0 L7 3.5 L0 7 z" fill="%s"/></marker></defs>' % BASE]
    maxv = stufen[0][1]
    for i, (lab, v, sub) in enumerate(stufen):
        x = i * (bw + lu) + 6
        h = max(34.0, plot * v / maxv)
        y = plot - h + 14
        s.append('<rect x="%.0f" y="%.1f" width="%.0f" height="%.1f" rx="6" fill="%s" '
                 'opacity="%.2f"/>' % (x, y, bw, h, AKZENT, 1 - i * 0.22))
        gross = h > 70
        s.append('<text x="%.0f" y="%.1f" font-size="38" font-weight="650" fill="%s">%s&#8201;%%</text>'
                 % (x + 16, y + 52 if gross else y - 13, '#ffffff' if gross else INK, de(v)))
        s.append('<text x="%.0f" y="%d" font-size="15" font-weight="620" fill="%s">%s</text>'
                 % (x, plot + 46, INK, lab))
        s.append('<text x="%.0f" y="%d" font-size="12.5" fill="%s">%s</text>'
                 % (x, plot + 66, MUTED, sub))
        if i < len(stufen) - 1:
            nx = x + bw
            my = plot / 2 + 14
            s.append('<path d="M%.0f %.0f L%.0f %.0f" stroke="%s" stroke-width="2" '
                     'marker-end="url(#pf)"/>' % (nx + 12, my, nx + lu - 14, my, BASE))
            s.append('<text x="%.0f" y="%.0f" font-size="14" text-anchor="middle" '
                     'font-weight="620" fill="%s">%s&#8201;%%</text>'
                     % (nx + lu / 2, my - 13, INK2, de(100 * stufen[i + 1][1] / v, 0)))
    s.append('</svg>')
    return ''.join(s)


def dot_vergleich(zeilen, breite=W_HALF, hoehe=H_CHART, vmin=-15, vmax=85, hervor=None):
    """Punktvergleich zweier Werte je Zeile, mit Verbindungslinie."""
    lb, rb = 150, 26
    sp = breite - lb - rb
    zeile = min(60, (hoehe - 36) / len(zeilen))
    h = zeile * len(zeilen) + 34
    sx = lambda v: lb + sp * (v - vmin) / (vmax - vmin)
    s = ['<svg viewBox="0 0 %d %.0f" width="%d" height="%.0f" role="img">' % (breite, h, breite, h)]
    for g in range(0, int(vmax) + 1, 20):
        s.append('<line x1="%.1f" y1="8" x2="%.1f" y2="%.0f" stroke="%s" stroke-width="1"/>'
                 % (sx(g), sx(g), h - 22, GRID))
        s.append('<text x="%.1f" y="%.0f" font-size="11.5" text-anchor="middle" fill="%s">%d</text>'
                 % (sx(g), h - 6, MUTED, g))
    for i, (lab, a_, b_) in enumerate(zeilen):
        y = 22 + i * zeile
        akt = (lab == hervor)
        if akt:
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="#eef4fc"/>'
                     % (8, y - zeile / 2 + 3, breite - 16, zeile - 6))
        s.append('<text x="%d" y="%.1f" text-anchor="end" font-size="13.5" fill="%s" '
                 'font-weight="%d">%s</text>'
                 % (lb - 14, y + 5, INK if akt else INK2, 650 if akt else 400, lab))
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/>'
                 % (sx(a_), y, sx(b_), y, BASE))
        for v, f in ((a_, ZWEIT), (b_, AKZENT)):
            s.append('<circle cx="%.1f" cy="%.1f" r="6.5" fill="%s" stroke="%s" stroke-width="2"/>'
                     % (sx(v), y, f, FLAECHE))
    s.append('</svg>')
    return ''.join(s)


def gruppen_bar(stufen, gruppen, breite=W_WIDE, hoehe=H_CHART):
    """Gruppierte Balken: je Stufe zwei Gruppen. gruppen: [(name, farbe, [werte])]."""
    lb, tb = 36, 44
    sp = (breite - lb - 20) / len(stufen)
    maxv = max(max(g[2]) for g in gruppen) * 1.2
    plot = hoehe - tb - 44
    bw = min(78, sp / (len(gruppen) + 1.1))
    s = ['<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
         % (breite, hoehe, breite, hoehe)]
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
             % (lb, tb + plot, breite - 20, tb + plot, BASE))
    for i, stufe in enumerate(stufen):
        mitte = lb + sp * i + sp / 2
        for j, (nm, farbe, werte) in enumerate(gruppen):
            v = werte[i]
            h = max(3.0, plot * v / maxv)
            x = mitte - (len(gruppen) * bw + 8) / 2 + j * (bw + 8)
            y = tb + plot - h
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s"/>'
                     % (x, y, bw, h, farbe))
            s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="16" '
                     'font-weight="650" fill="%s">%s&#8201;%%</text>'
                     % (x + bw / 2, y - 9, INK, de(v, 0)))
        s.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="14" '
                 'font-weight="600" fill="%s">%s</text>' % (mitte, tb + plot + 26, INK2, stufe))
    s.append('</svg>')
    return ''.join(s)


# ---------------------------------------------------------------- Deck
NR = None          # Platzhalter: folie() vergibt die Nummer in Aufrufreihenfolge
_zaehler = [1]


def folie(nr, kicker, titel, inhalt, fuss=''):
    """Eine Folie. Die Nummer wird fortlaufend vergeben, nicht uebergeben -
    beim Einschieben einer Folie verrutscht sonst der ganze Rest."""
    _zaehler[0] += 1
    nr = _zaehler[0]
    return """<section class="s">
  <header><span class="kick">%s</span></header>
  <h2>%s</h2>
  %s
  <footer><span>%s</span><span class="nr">%d</span></footer>
</section>""" % (kicker, titel, inhalt, fuss, nr)


def main():
    warnungen = marke_laden()
    if warnungen is not None:
        print('Markenfarben aus %s/marke.json uebernommen.' % ASSETS)
        for hinweis in warnungen:
            print('  HINWEIS: ' + hinweis)
    d = laden()
    w = np.array([float(r['gewicht_quote']) for r in d])
    fu = {r['marke']: r for r in csv.DictReader(io.open(FUNNEL, encoding='utf-8-sig'))}
    bq = {r['marke']: r for r in csv.DictReader(io.open(BEKANNT, encoding='utf-8-sig'))}
    n = len(d)
    kenner = [r for r in d if r['neoh_bekannt'] == '1']
    wk = np.array([float(r['gewicht_quote']) for r in kenner])

    bek = anteil(d, w, lambda r: r['neoh_bekannt'] == '1')
    bet = anteil(d, w, lambda r: r['neoh_betracht'] == '1')
    kauf = anteil(d, w, lambda r: r['neoh_kauf'] == '1')

    # Kategorie
    kategorie = ['NEOH', 'More Nutrition', 'AHEAD', 'Foodspring', 'Nicks', 'BE-KIND', 'Nucao']
    kat = sorted(((m, float(fu[m]['bekanntheit'])) for m in kategorie), key=lambda t: -t[1])

    # Gesamtmarkt nach Bekanntheit
    alle = sorted(((m, float(r['bekanntheit'])) for m, r in fu.items()), key=lambda t: -t[1])

    # Konversionen, Vergleichsbasis >= 30 Kenner
    verg = [r for r in fu.values() if int(r['bekanntheit_n']) >= 30]
    k2 = sorted(((r['marke'], float(r['konv_bet_kauf'])) for r in verg), key=lambda t: -t[1])
    k1 = sorted(((r['marke'], float(r['konv_bek_bet'])) for r in verg), key=lambda t: -t[1])
    med_k1 = float(np.median([v for _, v in k1]))
    med_k2 = float(np.median([v for _, v in k2]))
    rang_k2 = [m for m, _ in k2].index('NEOH') + 1
    rang_k1 = [m for m, _ in k1].index('NEOH') + 1

    # Segment
    seg = np.array([bool(r['zucker'].strip()) and int(r['zucker']) >= 4 for r in d], dtype=bool)
    seg_anteil = 100 * float(seg.mean())
    dseg = [r for r, m in zip(d, seg) if m]
    dnon = [r for r, m in zip(d, seg) if not m]
    wseg, wnon = w[seg], w[~seg]
    seg_bet = anteil(dseg, wseg, lambda r: r['neoh_betracht'] == '1')
    non_bet = anteil(dnon, wnon, lambda r: r['neoh_betracht'] == '1')
    seg_bek = anteil(dseg, wseg, lambda r: r['neoh_bekannt'] == '1')
    non_bek = anteil(dnon, wnon, lambda r: r['neoh_bekannt'] == '1')

    # Slider
    SL = [('qualität_1', 'Qualität'), ('emotion_1', 'Emotionale Bindung'),
          ('zufriedenheit_1', 'Zufriedenheit'), ('wom_1', 'Weiterempfehlung'),
          ('plv_1', 'Preis-Leistung')]
    slider = []
    for v, lab in SL:
        x = np.array([z(r[v]) for r in kenner])
        slider.append((lab, float(np.nanmean(x)), int((~np.isnan(x)).sum())))

    # Erwaeger gegen Nicht-Erwaeger
    erw = np.array([r['neoh_betracht'] == '1' for r in kenner], dtype=bool)
    vergleich = []
    for v, lab in SL[:4] + [SL[4]]:
        x = np.array([z(r[v]) for r in kenner])
        vergleich.append((lab, float(np.nanmean(x[~erw])), float(np.nanmean(x[erw]))))

    # H1
    h1lab = {1: 'Zu teuer', 2: 'Nicht im bevorzugten Geschäft', 3: 'Sehe ich nie im Regal',
             4: 'Begrenzte Geschmacksauswahl', 5: 'Packungsgröße fehlt', 6: 'Nie im Angebot',
             7: 'Haushalt bevorzugt sie nicht', 8: 'Weiß nicht genug darüber', 9: 'Sonstiges'}
    h1 = [r for r in kenner if r['H1_1'] != '']
    h1z = sorted(((h1lab[i], 100 * sum(1 for r in h1 if r['H1_%d' % i] == '1') / len(h1))
                  for i in range(1, 10)), key=lambda t: -t[1])

    # Ungestuetzt: dieselbe Zuordnung wie in Stufe 4
    sp = [r['spontan'] for r in d if r['spontan'].strip()]
    sp_n = len(sp)
    ung = collections.Counter()
    for t in sp:
        for nm in marken_im_text(t):
            ung[nm] += 1
    neoh_u = ung['NEOH']
    neoh_uk = sum(1 for r in kenner if 'NEOH' in marken_im_text(r['spontan']))
    # Gegenueberstellung gestuetzt/ungestuetzt fuer die bekanntesten Marken
    paar = [(m, 100 * ung.get(m, 0) / sp_n, float(fu[m]['bekanntheit']))
            for m, _ in alle[:8] if m in fu]
    paar.append(('NEOH', 100 * ung.get('NEOH', 0) / sp_n, float(fu['NEOH']['bekanntheit'])))
    paar = sorted(paar, key=lambda t: -t[2])

    css = """
*{box-sizing:border-box;margin:0;padding:0}
@page{size:1280px 720px;margin:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{background:%(plane)s;font-family:%(font)s;color:%(ink)s}
.s{width:1280px;height:720px;background:%(fl)s;padding:56px 72px 44px;position:relative;
   page-break-after:always;break-after:page;display:flex;flex-direction:column;margin:0 auto 22px}
.s:last-child{page-break-after:auto}
.kick{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:%(muted)s;font-weight:600}
h2{font-size:33px;line-height:1.16;font-weight:650;margin:10px 0 20px;max-width:62ch;letter-spacing:-.011em}
h2 em{font-style:normal;color:%(ak)s}
.body{flex:1;display:flex;gap:42px;min-height:0;align-items:stretch}
.body.mid{align-items:center}
svg{display:block}
.col{flex:1;min-width:0}
.col.narrow{flex:0 0 310px}
p{font-size:15.5px;line-height:1.56;color:%(ink2)s;margin-bottom:13px;max-width:52ch}
p strong{color:%(ink)s;font-weight:620}
ul{list-style:none;margin:4px 0 0}
ul.big li{font-size:16.5px;line-height:1.56;margin-bottom:21px;padding-left:22px}
ul.big li:before{top:9px;width:8px;height:8px}
li{font-size:15px;line-height:1.5;color:%(ink2)s;margin-bottom:12px;padding-left:19px;position:relative}
li:before{content:"";position:absolute;left:0;top:8px;width:7px;height:7px;border-radius:50%%;background:%(ak)s}
li strong{color:%(ink)s;font-weight:620}
footer{position:absolute;left:72px;right:72px;bottom:26px;display:flex;justify-content:space-between;
  font-size:11px;color:%(muted)s;border-top:1px solid %(grid)s;padding-top:9px}
.hero{display:flex;gap:34px;margin-bottom:20px}
.stat{flex:1}
.stat .v{font-size:50px;font-weight:650;letter-spacing:-.025em;line-height:1;color:%(ak)s}
.stat .v.n{color:%(ink)s}
.stat .l{font-size:13px;color:%(ink2)s;margin-top:9px;line-height:1.4}
.note{font-size:12.5px;color:%(muted)s;line-height:1.5;margin-top:12px}
.lead{font-size:19px;line-height:1.5;color:%(ink)s;font-weight:500;max-width:56ch}
.tag{display:inline-block;font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:4px;
  background:#e8f0fb;color:#1c5cab;margin-bottom:14px}
.tag.g{background:#e6f5e6;color:#0a7a0a}
table{width:100%%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;font-weight:600;color:%(muted)s;font-size:11.5px;text-transform:uppercase;
   letter-spacing:.07em;padding:0 10px 7px 0;border-bottom:1px solid %(grid)s}
td{padding:7px 10px 7px 0;color:%(ink2)s;border-bottom:1px solid %(grid)s}
td.n{text-align:right;font-variant-numeric:tabular-nums}
tr.hi td{color:%(ink)s;font-weight:620}
.legend{display:flex;gap:18px;font-size:12px;color:%(ink2)s;margin-top:8px}
.legend i{display:inline-block;width:9px;height:9px;border-radius:50%%;margin-right:6px}
.title{justify-content:center}
.title h1{font-size:54px;font-weight:650;letter-spacing:-.025em;line-height:1.08;max-width:19ch}
.title .sub{font-size:19px;color:%(ink2)s;margin-top:22px;max-width:46ch;line-height:1.5}
.title .meta{position:absolute;bottom:56px;left:72px;font-size:13px;color:%(muted)s;line-height:1.7}
.title .logo{position:absolute;top:56px;left:72px;height:42px;width:auto;object-fit:contain}
.title .produkte{position:absolute;right:72px;bottom:56px;display:flex;gap:18px;align-items:flex-end}
.title .produkte img{height:300px;width:auto;object-fit:contain}
.s .mark{position:absolute;top:50px;right:72px;height:22px;width:auto;opacity:.75}
.strip{margin-top:auto;border-top:1px solid %(grid)s;padding-top:14px;display:flex;gap:40px}
.strip div{flex:1;font-size:13.5px;line-height:1.5;color:%(ink2)s}
.strip b{display:block;color:%(ink)s;font-weight:620;margin-bottom:3px;font-size:14px}
.col{display:flex;flex-direction:column;align-items:stretch}
.tag{align-self:flex-start}
.rule{height:4px;width:62px;background:%(ak)s;border-radius:2px;margin-bottom:26px}
""" % dict(ink=INK, ink2=INK2, muted=MUTED, grid=GRID, ak=AKZENT, fl=FLAECHE,
            font=SCHRIFT, plane=_mische(INK, FLAECHE, 0.84))

    F = []

    # 1 Titel
    logo = asset('neoh-logo', 'logo', 'neoh')
    bilder = produktbilder()
    F.append("""<section class="s title">
  %s<div class="rule"></div>
  <h1>NEOH im österreichischen Riegelmarkt</h1>
  <div class="sub">Markenstudie September 2026 — Bekanntheit, Markenbild und
  Kaufverhalten im Wettbewerbsvergleich</div>
  <div class="meta">Online-Befragung, quotiert nach Alter und Geschlecht, n = %s<br>
  WU Wien · Dr. Arne Floh · Oktober 2026</div>
  %s
</section>""" % ('<img class="logo" src="%s" alt="NEOH">' % logo if logo else '',
                 n,
                 ('<div class="produkte">' +
                  ''.join('<img src="%s" alt="">' % b for b in bilder) + '</div>')
                 if bilder else ''))

    # 2 Kernaussagen
    F.append(folie(NR, 'Das Wichtigste', 'Eine junge Marke, die ihre Kategorie <em>bereits gewonnen hat</em>',
        """<div class="body"><div class="col">
        <div class="hero">
          <div class="stat"><div class="v">%s&nbsp;%%</div><div class="l">der Österreicherinnen und
            Österreicher kennen NEOH</div></div>
          <div class="stat"><div class="v">%s&times;</div><div class="l">so bekannt wie der nächste
            zuckerreduzierte Wettbewerber</div></div>
          <div class="stat"><div class="v">%s&nbsp;%%</div><div class="l">der Erwäger kaufen auch —
            Rang&nbsp;%d von 18 Marken</div></div>
        </div>
        <p>Nach weniger als zehn Jahren am Markt steht NEOH in der Bekanntheit vor jedem
        anderen Anbieter zuckerreduzierter Riegel — und zwar nicht knapp. <strong>Wer die
        Marke in Erwägung zieht, kauft sie auch</strong>, häufiger als bei Mars, Snickers
        oder Bounty.</p>
        <p>Das Wachstumspotenzial liegt damit nicht in mehr Reichweite, sondern in der
        Verankerung: Die Marke muss im Entscheidungsmoment präsent sein und ihr
        Versprechen erkennbar machen.</p>
        <div class="strip">
          <div><b>Salienz</b>Bekannt, aber im Entscheidungsmoment selten präsent</div>
          <div><b>Relevanz</b>Das Versprechen erreicht bisher vor allem Zuckerbewusste</div>
          <div><b>Verfügbarkeit</b>Preis und fehlende Aktionen bremsen kaufbereite Erwäger</div>
        </div>
        </div><div class="col narrow">
        <div class="tag g">Kategorie zuckerreduziert</div>%s
        <div class="note">Gestützte Bekanntheit, gewichtet. Basis n = %d.</div>
        </div></div>""" % (de(bek, 0), de(kat[0][1] / kat[1][1]), de(float(fu['NEOH']['konv_bet_kauf']), 0),
                           rang_k2, bar_h(kat, breite=W_NARROW, hoehe=230, lb=108,
                                          hervor='NEOH'), n),
        'NEOH Markenstudie Österreich 2026'))

    # 3 Methode
    F.append(folie(NR, 'Anlage', 'Methode und Stichprobe',
        """<div class="body"><div class="col">
        <table><tbody>
        <tr><td>Zielgruppe</td><td class="n">Österreich, 18 Jahre und älter</td></tr>
        <tr><td>Erhebung</td><td class="n">Online-Panel, 25.–30. September 2026</td></tr>
        <tr><td>Realisierte Interviews</td><td class="n">596</td></tr>
        <tr><td>Nach Qualitätsprüfung</td><td class="n">%d</td></tr>
        <tr><td>Bearbeitungsdauer (Median)</td><td class="n">3,2 Minuten</td></tr>
        <tr class="hi"><td>Gewichtung</td><td class="n">Alter × Geschlecht, Designeffekt 1,08</td></tr>
        </tbody></table>
        <p class="note">Ausgeschlossen wurden 29 Fälle (4,9 %%): nicht bestandene
        Aufmerksamkeitsprüfung, Bearbeitungszeit unter einem Drittel des Medians und ein
        Fall unter 18 Jahren. Die Markenreihenfolge war in allen Rastern randomisiert.</p>
        </div><div class="col">
        <div class="tag">Funnel-Logik</div>
        <p>Je Marke wurden drei Stufen erhoben: <strong>gestützte Bekanntheit</strong>,
        <strong>Erwägung beim nächsten Kauf</strong> und <strong>Kauf in den letzten drei
        Monaten</strong>. Erwägung und Kauf zählen nur unter den Kennern der jeweiligen
        Marke.</p>
        <p>Weil alle 20 Marken im selben Raster abgefragt wurden, sind die Übergangsraten
        direkt vergleichbar — NEOH wird am tatsächlichen Wettbewerb gemessen, nicht an
        einem Branchenrichtwert.</p>
        </div></div>""" % n,
        'Feldbericht: FELDBERICHT_AT.md'))

    # 4 Kategorie
    F.append(folie(NR, 'Position', 'In der eigenen Kategorie ist NEOH <em>Marktführer in der Bekanntheit</em>',
        """<div class="body mid"><div class="col">%s
        <div class="note">Gestützte Bekanntheit, gewichtet, n = %d.</div>
        </div><div class="col narrow">
        <p class="lead">Fast doppelt so bekannt wie der nächste Anbieter.</p>
        <p>More Nutrition, AHEAD, Foodspring und Nicks liegen alle unter 30 %%. Für ein
        österreichisches Unternehmen, das vor weniger als zehn Jahren gestartet ist, ist
        das eine ungewöhnlich starke Position.</p>
        <p>Im Gesamtmarkt steht NEOH auf <strong>Rang 13 von 20</strong> — hinter den
        Konzernmarken, aber vor dem gesamten eigenen Wettbewerbsfeld.</p>
        </div></div>""" % (bar_h(kat, breite=W_WIDE, hoehe=H_CHART, hervor='NEOH'), n),
        'Stufe 1 — Funnel im Wettbewerbsvergleich'))

    # 5 Gesamtmarkt
    F.append(folie(NR, 'Gesamtmarkt', 'Im Vergleich mit den Konzernmarken',
        """<div class="body mid"><div class="col">%s</div>
        <div class="col narrow"><div class="tag">Lesehilfe</div>
        <p>Die Spitze besetzen Marken mit jahrzehntelanger Fernsehpräsenz und
        flächendeckender Distribution. Der Abstand dorthin ist kein Qualitätsurteil,
        sondern eine Frage von Zeit und Mediabudget.</p>
        <p>Entscheidend für die Bewertung ist deshalb nicht die Höhe der Bekanntheit,
        sondern <strong>was NEOH daraus macht</strong> — dazu die nächste Folie.</p>
        </div></div>""" % bar_h([(m, v) for m, v in alle[:14]], breite=W_WIDE, hoehe=H_CHART + 36,
                     hervor='NEOH'),
        'Gestützte Bekanntheit, gewichtet'))

    # 6 Konversion Staerke
    F.append(folie(NR, 'Stärke', 'Wer NEOH erwägt, <em>kauft es auch</em>',
        """<div class="body mid"><div class="col">%s
        <div class="note">Anteil der Erwäger, die in den letzten drei Monaten gekauft haben.
        Nur Marken mit mindestens 30 Kennern.</div>
        </div><div class="col narrow">
        <div class="hero"><div class="stat"><div class="v">%s&nbsp;%%</div>
        <div class="l">Erwäger-zu-Käufer bei NEOH<br>Median aller Marken: %s&nbsp;%%</div></div></div>
        <p>NEOH liegt auf <strong>Rang %d von 18</strong> — vor Mars, Snickers, Bounty,
        Knoppers und Balisto.</p>
        <p>Das ist der belastbarste Hinweis auf Produktstärke in dieser Studie: Sobald
        die Marke in der Auswahl ist, setzt sie sich gegen etablierte Konkurrenz durch.</p>
        </div></div>""" % (bar_h(k2[:12], breite=W_WIDE, hoehe=H_CHART + 24, dec=0, hervor='NEOH'),
                           de(float(fu['NEOH']['konv_bet_kauf']), 0), de(med_k2, 0), rang_k2),
        'Stufe 1 — Übergangsrate Betracht → Kauf'))

    # 7 Markenpyramide
    def stufe(bed):
        m = np.array([bool(bed(r)) for r in d], dtype=bool)
        return 100 * float(w[m].sum() / w.sum()), int(m.sum())
    p_bek = stufe(lambda r: r['neoh_bekannt'] == '1')
    p_bet = stufe(lambda r: r['neoh_bekannt'] == '1' and r['neoh_betracht'] == '1')
    p_kauf = stufe(lambda r: r['neoh_bekannt'] == '1' and r['neoh_betracht'] == '1'
                   and r['neoh_kauf'] == '1')
    p_pro = stufe(lambda r: r['neoh_bekannt'] == '1' and r['neoh_betracht'] == '1'
                  and r['neoh_kauf'] == '1' and r['empfehlung'].strip()
                  and float(r['empfehlung']) >= 9)
    # Medianuebergaenge aller Marken mit mindestens 30 Kennern
    uebergaenge = [[], [], []]
    for m_, r_ in fu.items():
        c = r_['code']
        if int(r_['bekanntheit_n']) < 30:
            continue
        bk = np.array([x['bekanntheit_%s' % c] == '1' for x in d], dtype=bool)
        bt = bk & np.array([x['betracht_%s' % c] == '1' for x in d], dtype=bool)
        kf = bt & np.array([x['kauf_3monate_%s' % c] == '1' for x in d], dtype=bool)
        a_, b_, c_ = (w[bk].sum(), w[bt].sum(), w[kf].sum())
        if a_ > 0:
            uebergaenge[0].append(100 * b_ / a_)
        if b_ > 0:
            uebergaenge[1].append(100 * c_ / b_)
    med_u = [float(np.median(x)) if x else float('nan') for x in uebergaenge[:2]]

    F.append(folie(NR, 'Markenpyramide', 'Von der Bekanntheit bis zur <em>aktiven Empfehlung</em>',
        """<div class="body mid"><div class="col">%s</div>
        <div class="col narrow">
        <p>Jede Stufe ist eine <strong>Teilmenge der darunterliegenden</strong>: Wer
        empfiehlt, hat gekauft; wer gekauft hat, zieht die Marke in Betracht; wer sie in
        Betracht zieht, kennt sie.</p>
        <p>Der Engpass liegt sichtbar auf der ersten Stufe: %s&nbsp;%% statt %s&nbsp;%% im
        Median. Darüber arbeitet die Pyramide <strong>über dem Marktdurchschnitt</strong> —
        von den Erwägern kaufen %s&nbsp;%%, Median %s&nbsp;%%.</p>
        <p class="note">Zehn Befragte haben NEOH gekauft, würden es beim nächsten Mal aber
        nicht in Betracht ziehen. Sie zählen in der Pyramide nicht mit, im Funnel der
        vorigen Folie (8,2&nbsp;%%) schon.</p>
        </div></div>""" % (
            pyramide([('kennt die Marke', p_bek[0], p_bek[1], 'gestützte Bekanntheit, n = %d' % p_bek[1]),
                      ('zieht sie in Betracht', p_bet[0], p_bet[1], 'beim nächsten Kauf, n = %d' % p_bet[1]),
                      ('hat gekauft', p_kauf[0], p_kauf[1], 'letzte drei Monate, n = %d' % p_kauf[1]),
                      ('empfiehlt aktiv', p_pro[0], p_pro[1], 'Empfehlung 9–10, n = %d' % p_pro[1])],
                     breite=W_WIDE, hoehe=390, vergleich=med_u),
            de(100 * p_bet[0] / p_bek[0], 0), de(med_u[0], 0),
            de(100 * p_kauf[0] / p_bet[0], 0), de(med_u[1], 0)),
        'Stufe 1 und 2 — Markenpyramide NEOH'))

    # 7b Trichter
    F.append(folie(NR, 'Hebel', 'Derselbe Weg als Trichter, mit den Abflüssen',
        """<div class="body mid"><div class="col">%s
        <div class="note">Gewichtete Anteile der Gesamtstichprobe. Oben die Übergangsrate,
        unten der Abfluss in Prozentpunkten. Hier zählen alle Käufer, auch die ohne
        Erwägung.</div></div>
        <div class="col narrow">
        <p>Von den Kennern nehmen <strong>%s %%</strong> NEOH in die engere Auswahl; über
        alle Marken sind es im Median %s %%.</p>
        <p>Das ist die eine Stufe mit sichtbarem Spielraum — und zugleich die am besten
        adressierbare, weil die Marke die Menschen bereits erreicht hat.</p>
        <p class="note">Rechnerisch: Jeder Prozentpunkt mehr auf dieser Stufe bringt bei
        gleicher Kaufquote rund 0,5 Prozentpunkte zusätzliche Käufer in der
        Gesamtbevölkerung.</p>
        </div></div>""" % (funnel_trichter([('Kennen NEOH', bek, 'gestützte Bekanntheit'),
                                            ('Ziehen in Betracht', bet, 'beim nächsten Kauf'),
                                            ('Haben gekauft', kauf, 'letzte drei Monate')],
                                           breite=W_WIDE, hoehe=330),
                           de(float(fu['NEOH']['konv_bek_bet']), 0), de(med_k1, 0)),
        'Stufe 1 — NEOH-Funnel'))

    # 7b Funnel im Markenvergleich
    # Segmente aus den Falldaten: Kaeufer ohne vorherige Erwaegung gibt es
    # (bis zu 8 Prozentpunkte), die Differenz zweier Randanteile waere falsch.
    code = {}
    for e in csv.DictReader(io.open(FUNNEL, encoding='utf-8-sig')):
        code[e['marke']] = e['code']
    stapel = []
    for m, _ in list(alle[:9]) + [('NEOH', 0)]:
        c = code[m]
        kaufm = np.array([r['kauf_3monate_%s' % c] == '1' for r in d], dtype=bool)
        betm = np.array([r['betracht_%s' % c] == '1' for r in d], dtype=bool)
        bekm = np.array([r['bekanntheit_%s' % c] == '1' for r in d], dtype=bool)
        p_kauf = 100 * w[kaufm].sum() / w.sum()
        p_bet_ohne = 100 * w[betm & ~kaufm].sum() / w.sum()
        p_bek = 100 * w[bekm].sum() / w.sum()
        stapel.append((m, p_bek, p_kauf, p_bet_ohne))
    stapel = sorted(set(stapel), key=lambda t: -t[1])
    F.append(folie(NR, 'Vergleich', 'Derselbe Funnel, <em>über alle Marken gelesen</em>',
        """<div class="body mid"><div class="col">%s
        <div class="legend">
          <span><i style="background:%s"></i>gekauft</span>
          <span><i style="background:%s"></i>erwogen, nicht gekauft</span>
          <span><i style="background:%s"></i>kennt, erwägt nicht</span>
          <span><i style="background:%s"></i>kennt die Marke nicht</span></div>
        <div class="note">Jeder Balken ist die gesamte Bevölkerung (100 %%). Der Wert am
        Ende ist die gestützte Bekanntheit.</div>
        </div><div class="col narrow">
        <p>NEOHs bekannter Anteil ist der kürzeste im Feld — das ist die kleinere Basis.
        Entscheidend ist aber die Aufteilung innerhalb: <strong>Bei NEOH ist der helle
        Block, der die Marke kennt und nicht erwägt, proportional am größten.</strong>
        Genau dort liegt Tor 1.</p>
        <p>Umgekehrt ist der Weg vom Erwägen zum Kauf der kürzeste im Feld: Die Hälfte
        der Erwäger kauft auch — bei Bounty, Snickers und Knoppers rund 40 %%.</p>
        </div></div>""" % (funnel_stapel(stapel, breite=W_WIDE, hoehe=376, hervor='NEOH'),
                           ST_KAUF, ST_ERW, ST_KENNT, ST_FREMD),
        'Stufe 1 — Funnel im Wettbewerbsvergleich'))

    # 8 Salienz
    F.append(folie(NR, 'Salienz', 'Bekannt heißt noch nicht <em>präsent</em>',
        """<div class="body"><div class="col">%s
        <div class="legend"><span><i style="background:%s"></i>ungestützt genannt</span>
        <span><i style="background:%s"></i>gestützt bekannt</span></div>
        <div class="note">Ungestützt: Anteil, der die Marke bei der Frage nach
        Riegelmarken von sich aus nennt (n = %d). Die acht bekanntesten Marken und NEOH.</div>
        </div><div class="col narrow">
        <div class="hero"><div class="stat"><div class="v">%s&nbsp;%%</div>
        <div class="l">der %d Kenner nennen NEOH auch spontan</div></div></div>
        <p>Die gestützte Zahl misst <strong>Wiedererkennung</strong>, die ungestützte
        <strong>Erinnerung</strong>. Bei den großen Marken liegen beide näher beieinander.</p>
        <p>Wer NEOH überhaupt erinnert, nennt es zur Hälfte zuerst — bei denen sitzt die
        Marke fest. Die Frage ist, ob die kleine Zahl an der Verankerung liegt oder an
        der Basis.</p>
        <p class="note">45,6&nbsp;%% der Kenner hatten den letzten Markenkontakt im
        Supermarkt — mit Abstand der wichtigste Kontaktpunkt.</p>
        </div></div>""" % (dot_vergleich(paar, breite=W_WIDE, hoehe=376, vmin=0, vmax=100, hervor='NEOH'),
                           ZWEIT, AKZENT, sp_n, de(100 * neoh_uk / len(kenner), 0), len(kenner)),
        'Stufe 4 — Spontannennungen, n = %d' % sp_n))

    # 10 Demografie
    ALTER_ORD = ['18 bis 29 Jahre', '30 bis 39 Jahre', '40 bis 49 Jahre',
                 '50 bis 59 Jahre', '60 Jahre und älter']
    alterswerte = []
    for a_ in ALTER_ORD:
        m = np.array([r['alter_txt'] == a_ for r in d], dtype=bool)
        bk = m & np.array([r['neoh_bekannt'] == '1' for r in d], dtype=bool)
        alterswerte.append((a_.replace(' Jahre', '').replace(' und älter', '+'),
                            100 * w[bk].sum() / w[m].sum()))
    geschl = []
    for g in ['Weiblich', 'Männlich']:
        m = np.array([r['geschlecht_txt'] == g for r in d], dtype=bool)
        bk = m & np.array([r['neoh_bekannt'] == '1' for r in d], dtype=bool)
        geschl.append((g, 100 * w[bk].sum() / w[m].sum()))
    F.append(folie(NR, 'Zielgruppe', 'Jünger und weiblich — <em>und sonst nichts</em>',
        """<div class="body mid"><div class="col">%s
        <div class="note">Gestützte Bekanntheit nach Altersgruppe, gewichtet.</div>
        %s
        <div class="note">Nach Geschlecht. Die Erinnerungsquote ist in beiden Gruppen
        gleich (7,9 gegen 8,7&nbsp;%%) — Frauen kennen die Marke häufiger, aber nicht
        fester.</div>
        </div><div class="col narrow">
        <div class="hero"><div class="stat"><div class="v">3,3&times;</div>
        <div class="l">höhere Chance, dass eine Frau NEOH kennt — bei gleichem Alter,
        gleicher Bildung, gleichem Einkommen</div></div></div>
        <p>Von fünf geprüften Merkmalen tragen <strong>zwei</strong>. Zehn Jahre mehr
        Lebensalter senken die Chance um 35&nbsp;%%, Frauen kennen die Marke mit
        3,3-facher Chance.</p>
        <p><strong>Bildung, Einkommen und Region tragen nichts</strong> (alle p &gt; 0,05).
        NEOH ist keine Akademiker- und keine Einkommensmarke — die Bekanntheit verteilt
        sich quer durch alle Schichten.</p>
        <p class="note">Das vereinfacht die Zielgruppendefinition: Alter und Geschlecht
        genügen, Regionalschnitte trägt die Stichprobe ohnehin nicht.</p>
        </div></div>""" % (
            bar_h(alterswerte, breite=W_WIDE, hoehe=200, maxwert=78, farbe=AKZENT),
            bar_h(geschl, breite=W_WIDE, hoehe=86, maxwert=78, farbe=AKZENT)),
        'Vertiefung Bekanntheit — Demografie'))

    # 11 Altersgefaelle im Markenvergleich
    jung = np.array([r['alter'] == '2' for r in d], dtype=bool)
    alt6 = np.array([r['alter'] == '6' for r in d], dtype=bool)
    gef = []
    for m_, r_ in fu.items():
        c = r_['code']
        if int(r_['bekanntheit_n']) < 30:
            continue
        bk = np.array([x['bekanntheit_%s' % c] == '1' for x in d], dtype=bool)
        gef.append((m_, 100 * w[jung & bk].sum() / w[jung].sum()
                    - 100 * w[alt6 & bk].sum() / w[alt6].sum()))
    gef.sort(key=lambda t: -t[1])
    gef_rang = [m_ for m_, _ in gef].index('NEOH') + 1
    gef_med = float(np.median([v for _, v in gef]))
    F.append(folie(NR, 'Kohorte', 'Das Altersprofil <em>der eigenen Kategorie</em>',
        """<div class="body mid"><div class="col">%s
        <div class="note">Differenz der gestützten Bekanntheit zwischen 18–29 und 60+, in
        Prozentpunkten. Nur Marken mit mindestens 30 Kennern.</div>
        </div><div class="col narrow">
        <div class="hero"><div class="stat"><div class="v">Rang&nbsp;%d</div>
        <div class="l">von %d Marken, Median %s Prozentpunkte</div></div></div>
        <p>Die Gesellschaft ist aufschlussreich: More Nutrition, Corny und Pick&nbsp;Up! —
        die funktionalen und modernen Snackmarken. Die klassische Schokolade ist
        altersneutral bekannt (Milka 1,6, Manner 1,0, Mars 2,5).</p>
        <p>NEOH hat damit <strong>das Altersprofil seiner Kategorie, nicht das eines
        Nachzüglers</strong>. Marken wachsen über Kohorten, und die Marke besetzt die
        richtige.</p>
        <p class="note">Die Kehrseite: 60+ ist die größte Altersgruppe des Landes und die,
        in der NEOH am schwächsten steht.</p>
        </div></div>""" % (
            bar_h([(m_, v) for m_, v in gef if v > 0][:13], breite=W_WIDE, hoehe=H_CHART,
                  dec=0, einheit=' Pp.', hervor='NEOH'),
            gef_rang, len(gef), de(gef_med)),
        'Vertiefung Bekanntheit — Altersgefälle im Markenvergleich'))

    # 10 Erinnerungsquote
    eq = sorted(((m, float(r['erinnerungsquote'])) for m, r in bq.items()), key=lambda t: -t[1])
    eq_med = float(np.median([v for _, v in eq]))
    eq_rang = [m for m, _ in eq].index('NEOH') + 1
    F.append(folie(NR, 'Verankerung', 'Pro Einheit Bekanntheit <em>besser verankert</em> als die meisten',
        """<div class="body mid"><div class="col">%s
        <div class="note">Erinnerungsquote = ungestützte Nennung geteilt durch gestützte
        Bekanntheit. Median aller Marken: %s&nbsp;%%.</div>
        </div><div class="col narrow">
        <div class="hero"><div class="stat"><div class="v">Rang&nbsp;%d</div>
        <div class="l">von %d Marken in der Erinnerungsquote</div></div></div>
        <p>Die niedrige ungestützte Zahl ist <strong>kein Verankerungsproblem</strong>,
        sondern eine Folge der kleineren Basis. NEOH holt aus seiner Bekanntheit mehr
        heraus als Knoppers, Manner, Pick&nbsp;Up! oder Hanuta — Marken mit 70 bis
        90&nbsp;%% gestützter Bekanntheit.</p>
        <p>Dragee Keksi ist der Gegenfall: 80&nbsp;%% kennen die Marke,
        <strong>niemand</strong> nennt sie spontan.</p>
        <p class="note">Und wer NEOH erinnert, nennt es zu 48&nbsp;%% zuerst — auf dem
        Niveau von Mars (49&nbsp;%%).</p>
        </div></div>""" % (bar_h([(m, v) for m, v in eq if v > 0][:14], breite=W_WIDE,
                                 hoehe=H_CHART, hervor='NEOH'),
                           de(eq_med), eq_rang, len(eq)),
        'Vertiefung Bekanntheit — Erinnerungsquote'))

    # 11 Erinnerung als eigener Hebel
    F.append(folie(NR, 'Wirkung', 'Erinnerung wirkt <em>eigenständig</em>, nicht nur über Sympathie',
        """<div class="body"><div class="col">
        <div class="hero">
          <div class="stat"><div class="v">62,5&nbsp;%</div><div class="l">der Kenner, die NEOH
            spontan erinnern, ziehen es in Betracht</div></div>
          <div class="stat"><div class="v n">22,4&nbsp;%</div><div class="l">der Kenner, die es
            nur wiedererkennen</div></div>
          <div class="stat"><div class="v">7,1&times;</div><div class="l">höhere Chance auf
            Erwägung — auch bei gleichem Markenurteil</div></div>
        </div>
        <p>Der naheliegende Einwand wäre: Wer die Marke mag, erinnert sie auch. Die Daten
        widerlegen das. Nimmt man das Markenurteil ins Modell, <strong>bleibt der Effekt
        der Erinnerung bestehen</strong> (p = 0,0007), und das Modell wird messbar besser.</p>
        <p>Umgekehrt bewerten Erinnerer die Marke <strong>nicht signifikant besser</strong>
        als reine Wiedererkenner. Erinnerung ist keine Folge der Zuneigung, sondern eine
        eigene Größe.</p>
        <div class="strip">
          <div><b>Für die Steuerung</b>Die ungestützte Bekanntheit als Leitindikator führen,
          nicht die gestützte</div>
          <div><b>Einschränkung</b>24 Erinnerer in der Stichprobe — der Effekt ist groß,
          die Schätzung unsicher</div>
          <div><b>Kausalität</b>Querschnitt: Wer erwägt, erinnert womöglich deshalb. Das
          deutsche Sample klärt es</div>
        </div>
        </div><div class="col narrow">
        <div class="tag">Modellvergleich</div>
        <table><tbody>
        <tr><td>nur Markenurteil</td><td class="n">AIC 246,4</td></tr>
        <tr class="hi"><td>+ Erinnerung</td><td class="n">AIC 236,0</td></tr>
        </tbody></table>
        <p class="note">Logistische Regression auf die Erwägung, Basis 260 Kenner mit
        gültigem Markenurteil. Odds für Erinnerung 7,14 (SE 0,58), p = 0,0007.</p>
        </div></div>""",
        'Vertiefung Bekanntheit — Erinnerung und Erwägung'))

    # 9 Markenbild
    F.append(folie(NR, 'Markenbild', 'Die Qualität wird <em>klar honoriert</em>',
        """<div class="body mid"><div class="col">%s
        <div class="note">Skala −100 bis +100, nur Kenner mit Urteil, ungewichtet.</div>
        </div><div class="col narrow">
        <p>Qualität und emotionale Bindung liegen deutlich im positiven Bereich. Das
        Preis-Leistungs-Urteil ist <strong>neutral, nicht negativ</strong> — das
        Konfidenzintervall schließt die Null ein.</p>
        <p>NEOH wird also als gutes Produkt zu einem angemessenen Preis gesehen. Der
        Abstand zwischen beiden Werten beschreibt die Positionierung einer Premiummarke,
        keine Preisablehnung.</p>
        </div></div>""" % bar_h([(l, v) for l, v, _ in slider], breite=W_WIDE, hoehe=H_CHART,
                                maxwert=60, dec=0, einheit='', farbe=AKZENT),
        'Stufe 2 — Brand Health, n = %d Kenner' % len(kenner)))

    # 10 Was Erwaegung treibt
    F.append(folie(NR, 'Treiber', 'Erwägung entsteht aus dem Markenurteil — <em>nicht aus dem Preis</em>',
        """<div class="body mid"><div class="col">%s
        <div class="legend"><span><i style="background:%s"></i>Kenner ohne Erwägung</span>
        <span><i style="background:%s"></i>Erwäger</span></div>
        <div class="note">Mittelwerte je Gruppe. Qualität, Bindung und Zufriedenheit
        unterscheiden sich um rund 40 Punkte (p &lt; 0,001), das Preisurteil nicht
        signifikant.</div>
        </div><div class="col narrow">
        <p>Wer NEOH nicht erwägt, hält es <strong>nicht für zu teuer</strong> — er hat
        schlicht kein ausgeprägtes Markenurteil.</p>
        <p>Was dieses Urteil erzeugt, sind zwei Dinge: ob das Produkt zum eigenen Bedarf
        passt und ob es persönlich bedeutsam ist. Zusammen erklären sie über
        <strong>90 %%</strong> der erklärbaren Varianz. Demografie trägt nichts bei.</p>
        </div></div>""" % (dot_vergleich(vergleich, breite=W_WIDE), ZWEIT, AKZENT),
        'Stufe 2 und 3 — Markenurteil entlang des Funnels'))

    # 11 Segment
    seg_chart = gruppen_bar(
        ['Kennen NEOH', 'Ziehen in Betracht', 'Haben gekauft'],
        [('Zuckerreduktion wichtig (Stufe 4–5)', AKZENT,
          [seg_bek, seg_bet, anteil(dseg, wseg, lambda r: r['neoh_kauf'] == '1')]),
         ('weniger wichtig (Stufe 1–3)', '#ccd2d6',
          [non_bek, non_bet, anteil(dnon, wnon, lambda r: r['neoh_kauf'] == '1')])],
        breite=W_WIDE, hoehe=330)
    F.append(folie(NR, 'Segment', 'Zuckerreduktion ist der Zugang — und sie betrifft <em>die Mehrheit</em>',
        """<div class="body"><div class="col">%s
        <div class="legend"><span><i style="background:%s"></i>Zuckerreduktion wichtig (Stufe 4–5)</span>
        <span><i style="background:#ccd2d6"></i>weniger wichtig (Stufe 1–3)</span></div>
        <div class="note">Gewichtete Anteile der jeweiligen Teilgruppe.</div>
        </div><div class="col narrow">
        <div class="hero"><div class="stat"><div class="v">%s&nbsp;%%</div>
        <div class="l">der Erwachsenen ist Zuckerreduktion wichtig</div></div></div>
        <p>Das relevante Segment ist <strong>kein Nischenpublikum</strong>, sondern die
        Mehrheit der Bevölkerung.</p>
        <p>Die Bekanntheit ist in beiden Gruppen ähnlich — NEOH erreicht also längst beide.
        Angesprochen fühlt sich bisher nur eine davon.</p>
        <p>Der Zusammenhang ist eine <strong>Schwelle, kein Verlauf</strong>: Ab Stufe 4
        springt die Erwägung sprunghaft an.</p>
        </div></div>""" % (
            gruppen_bar(['Kennen NEOH', 'Ziehen in Betracht', 'Haben gekauft'],
                        [('seg', AKZENT, [seg_bek, seg_bet,
                                          anteil(dseg, wseg, lambda r: r['neoh_kauf'] == '1')]),
                         ('non', '#ccd2d6', [non_bek, non_bet,
                                             anteil(dnon, wnon, lambda r: r['neoh_kauf'] == '1')])],
                        breite=W_WIDE, hoehe=376),
            AKZENT, de(seg_anteil, 0)),
        'Stufe 4 — Segmentanalyse'))

    # 12 Barrieren
    F.append(folie(NR, 'Barrieren', 'Beim Kauf entscheiden Preis <em>und Verfügbarkeit</em>',
        """<div class="body mid"><div class="col">%s
        <div class="note">Mehrfachnennung, Basis: %d Erwäger ohne Kauf in den letzten drei
        Monaten. Kleine Fallzahl — die Rangfolge der ersten beiden Nennungen ist deutlich,
        alles darunter nicht belastbar.</div>
        </div><div class="col narrow">
        <p>An dieser Stelle — und nur hier — wirkt der Preis. Er entscheidet nicht, ob NEOH
        auf die Liste kommt, sondern ob es vom Regal in den Korb wandert.</p>
        <p><strong>Ein Viertel nennt fehlende Aktionen</strong>, ein weiteres Siebtel
        Verfügbarkeit. Das sind Handels- und Promotionsfragen, operativ adressierbar und
        ohne Eingriff in die Positionierung.</p>
        </div></div>""" % (bar_h(h1z[:7], breite=W_WIDE, hoehe=H_CHART, dec=0, lb=252, farbe=AKZENT), len(h1)),
        'Stufe 3 — Selbstauskunft der Erwäger'))

    # 13 Empfehlungen
    F.append(folie(NR, 'Ableitung', 'Vier Hebel, in der Reihenfolge ihrer Wirkung',
        """<div class="body"><div class="col">
        <ul class="big">
        <li><strong>Reichweite zahlt sich hier aus.</strong> NEOH verwandelt Bekanntheit
        überdurchschnittlich gut in Erinnerung (Rang 7 von 18). Jeder Punkt zusätzliche
        gestützte Bekanntheit trägt deshalb weiter als bei den meisten Wettbewerbern —
        anders als bei Marken, die bekannt sind und trotzdem niemandem einfallen.</li>
        <li><strong>Präsenz im Entscheidungsmoment.</strong> Erinnerung erhöht die Chance
        auf Erwägung um das Siebenfache, unabhängig vom Markenurteil. Regalpräsenz,
        Zweitplatzierung und wiederkehrende Anlässe wirken genau darauf. Als
        Leitindikator gehört die ungestützte Bekanntheit ins Reporting, nicht die
        gestützte.</li>
        <li><strong>Das Versprechen erkennbar machen.</strong> Wer benennen kann, wofür
        NEOH steht, erwägt die Marke zu %s %% — wer es nicht kann, zu %s %%. Zucker ist
        das einzige im Markenbild verankerte Merkmal; ein zweites Merkmal zu etablieren
        erweitert die Zielgruppe über das Zuckersegment hinaus.</li>
        <li><strong>Aktionen und Distribution.</strong> Ein Viertel der kaufbereiten
        Erwäger scheitert an fehlenden Angeboten oder Verfügbarkeit. Das ist der am
        schnellsten realisierbare Zuwachs.</li>
        </ul>
        <div class="strip">
          <div><b>Kurzfristig</b>Aktionen und Regalpräsenz — wirkt auf Tor 2, wo NEOH
          ohnehin stark ist</div>
          <div><b>Mittelfristig</b>Ein zweites Markenmerkmal neben Zucker — öffnet Tor 1
          über das Zuckersegment hinaus</div>
          <div><b>Messbar in Welle 2</b>Ungestützte Bekanntheit und Erinnerungsquote als
          Leitindikatoren</div>
        </div>
        </div><div class="col narrow">
        <div class="tag g">Ausgangslage</div>
        <p class="lead">Die Studie beschreibt keine Marke in Schwierigkeiten.</p>
        <p>Sie beschreibt eine junge Marke, die ihre Kategorie angeführt hat und nun vor
        der normalen nächsten Aufgabe steht: aus Bekanntheit Gewohnheit zu machen.</p>
        <p>Die Produktseite ist dabei kein Problem — die Kaufkonversion der Erwäger liegt
        über der von Mars und Snickers.</p>
        </div></div>""" % (de(41.8, 0), de(22.1, 0)),
        'Ableitung aus den Stufen 1 bis 4'))

    # 14 Vorbehalte
    F.append(folie(NR, 'Einordnung', 'Was diese Zahlen tragen — und was nicht',
        """<div class="body"><div class="col">
        <ul class="big">
        <li><strong>Gewichtung.</strong> Die Werte sind auf den vereinbarten Quotenplan
        gewichtet, nicht auf die amtliche Altersverteilung. Da die Bekanntheit mit dem
        Alter fällt, liegt die bevölkerungsbezogene Bekanntheit eher bei 49 bis 53 %%.
        Die Übergangsraten sind davon nicht betroffen.</li>
        <li><strong>Markenurteile.</strong> Wer kein Urteil abgab, bewertet die übrigen
        Merkmale schlechter. Die berichteten Mittelwerte beschreiben daher eher die obere
        Grenze.</li>
        <li><strong>Kleine Teilgruppen.</strong> Die Kaufbarrieren beruhen auf %d Fällen,
        der Vergleich von Erwägern und Käufern auf unter 50. Beides ist im deutschen
        Sample mit n ≈ 1.000 belastbar zu prüfen.</li>
        <li><strong>Kausalität.</strong> Alle Treiberrechnungen sind Varianzzerlegungen
        einer Querschnittserhebung. Sie zeigen, was zusammenhängt, nicht was wirkt.</li>
        </ul>
        </div><div class="col narrow">
        <div class="tag">Nächster Schritt</div>
        <p>Das deutsche Feld mit n ≈ 1.000 erlaubt den Ländervergleich und belastbare
        Aussagen zu den hier noch offenen Teilgruppen.</p>
        <p class="note">Alle Auswertungen sind als Skript hinterlegt und aus den Rohdaten
        reproduzierbar.</p>
        </div></div>""" % len(h1),
        'Methodische Hinweise'))

    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<title>NEOH Markenstudie Österreich 2026</title><style>%s</style></head>'
            '<body>%s</body></html>' % (css, '\n'.join(F)))
    io.open(AUS_HTML, 'w', encoding='utf-8').write(html)
    print('Geschrieben: %s (%d Folien)' % (AUS_HTML, len(F)))

    if '--pdf' in sys.argv:
        pdf()


def pdf():
    """Deck mit Chromium zu PDF rendern.

    Playwright und der Browser liegen je nach Umgebung an verschiedenen
    Stellen; das Skript probiert die ueblichen durch, statt einen Pfad
    festzuschreiben. PW_BROWSER setzt den Browser von aussen.
    """
    skript = """
const fs = require('fs');
function ladePlaywright() {
  for (const p of ['playwright', 'playwright-core', '/tmp/node_modules/playwright']) {
    try { return require(p); } catch (e) {}
  }
  throw new Error('playwright nicht gefunden - npm install playwright');
}
function browserPfad() {
  if (process.env.PW_BROWSER) return process.env.PW_BROWSER;
  const wurzeln = ['/opt/pw-browsers'];
  for (const w of wurzeln) {
    if (!fs.existsSync(w)) continue;
    for (const d of fs.readdirSync(w).filter(x => x.startsWith('chromium-')).sort().reverse()) {
      const c = `${w}/${d}/chrome-linux/chrome`;
      if (fs.existsSync(c)) return c;
    }
  }
  return null;
}
(async () => {
  const { chromium } = ladePlaywright();
  let b;
  try { b = await chromium.launch(); }
  catch (e) {
    const exe = browserPfad();
    if (!exe) throw e;
    b = await chromium.launch({ executablePath: exe });
  }
  const p = await b.newPage();
  await p.goto('file://' + process.cwd() + '/%s', { waitUntil: 'networkidle' });
  await p.pdf({ path: '%s', width: '1280px', height: '720px', printBackground: true,
                margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await b.close();
})();
""" % (AUS_HTML, AUS_PDF)
    io.open('/tmp/_render.js', 'w').write(skript)
    subprocess.run(['node', '/tmp/_render.js'], check=True)
    datum_normieren(AUS_PDF)
    print('Geschrieben: %s' % AUS_PDF)


def datum_normieren(pfad):
    """CreationDate und ModDate auf den Stand der Eingabedaten setzen.

    Chromium schreibt die aktuelle Uhrzeit ins PDF. Dadurch unterscheiden
    sich zwei Laeufe mit identischem Inhalt in sechs Bytes, und jede
    Neuerzeugung erzeugt einen 200-KB-Diff in der Versionsverwaltung. Der
    Zeitstempel wird deshalb auf die Datei gesetzt, aus der das Deck
    stammt - damit ist das PDF reproduzierbar und der Stempel bleibt
    wahrheitsgemaess.
    """
    import os, re, time
    quellen = [DATEN, FUNNEL, BEKANNT, 'slides_at.py']
    stand = max(os.path.getmtime(q) for q in quellen if os.path.exists(q))
    stempel = time.strftime("D:%Y%m%d%H%M%S+00'00'", time.gmtime(stand))
    roh = io.open(pfad, 'rb').read()
    neu_roh = re.sub(rb"(/(?:Creation|Mod)Date )\(D:[^)]*\)",
                     lambda m: m.group(1) + b'(' + stempel.encode() + b')', roh)
    if len(neu_roh) == len(roh):
        io.open(pfad, 'wb').write(neu_roh)


if __name__ == '__main__':
    main()
