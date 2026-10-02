# -*- coding: utf-8 -*-
"""Stufe 4 der Auswertung: Segmente und offene Angaben, Oesterreich.

Aufruf:  python3 analyse_segmente_text_at.py

Drei Teile:

  A  Ist zucker eine Schwelle oder ein Gradient? Modellvergleich auf beiden
     Toren des Funnels.
  B  spontan: ungestuetzte Bekanntheit und Top of Mind. Die Antworten werden
     regelbasiert gegen eine Markenliste mit Schreibvarianten abgeglichen.
  C  beschreibung: thematische Codierung, ebenfalls regelbasiert.

Zur Methode der Textauswertung: Die Codierung erfolgt ueber Stichwortregeln,
die im Skript stehen und damit nachvollziehbar sind. Das ist kein
Sprachmodell und keine manuelle Inhaltsanalyse. Die Trefferquote wird
ausgewiesen, nicht behauptet; nicht zugeordnete Texte werden gezaehlt und
beispielhaft gezeigt, damit sichtbar bleibt, was die Regeln verfehlen.

Schreibt ERGEBNISSE_AT_segmente_text.txt.
"""
import csv, io, re, math, collections
import numpy as np
import statsmodels.api as sm

DATEN = 'NEOH_AT_analyse.csv'
AUS_TXT = 'ERGEBNISSE_AT_segmente_text.txt'

# Markenvarianten fuer die ungestuetzte Bekanntheit. Die Reihenfolge zaehlt
# nicht, die Spezifitaet schon: laengere Muster werden zuerst geprueft, damit
# "kinder bueno" nicht als "kinder" verbucht wird.
MARKEN = [
    ('Kinder Bueno', r'kinder\s*bueno|(?<!kinder\s)bueno'),
    ('Kinder', r'kinder'),
    ('Mars', r'\bmars\b'),
    ('Milka', r'milka'),
    ('Twix', r'\btwix\b'),
    ('Snickers', r'sn[iy]ck?ers?'),
    ('Bounty', r'bount[yi]'),
    ('Duplo', r'duplo'),
    ('Balisto', r'balisto'),
    ('Lindt', r'lindt'),
    ('Corny', r'corny'),
    ('KitKat', r'kit\s*kat'),
    ('Lion', r'\blion\b'),
    ('Nussini', r'nussini|nusini'),
    ('Suchard', r'suchard'),
    ('Knoppers', r'knopp?ers'),
    ('Milky Way', r'milk[yi]\s*way'),
    ('NEOH', r'\bneoh\b'),
    ('Ritter Sport', r'ritter'),
    ('Manner', r'manner'),
    ('Zotter', r'zotter'),
    ('Nuts', r'\bnuts\b'),
    ('Ferrero', r'ferrero'),
    ('Nestle', r'nestl[ée]'),
    ('Ovomaltine', r'ovomaltine'),
    ('Merci', r'\bmerci\b'),
    ('Bahlsen', r'bahlsen'),
    ('Pick Up!', r'pick\s*up'),
    ('Hanuta', r'hanuta'),
    ('More Nutrition', r'\bmore\b'),
    ('Barebells', r'barebells'),
    ('Bensdorp', r'bensdorp'),
    ('ESN', r'\besn\b'),
    ('Hej', r'\bhej\b'),
    ('AHEAD', r'\bahead\b'),
    ('BE-KIND', r'be[\s-]*kind'),
    ('Nicks', r'\bnicks\b'),
    ('Nucao', r'nucao'),
    ('Foodspring', r'foodspring'),
    ('Dragee Keksi', r'dragee|keksi'),
]

# Im gestuetzten Markenraster abgefragte Marken (Codebuch, Abschnitt 1)
IM_RASTER = {'Balisto', 'BE-KIND', 'Bounty', 'Corny', 'Dragee Keksi', 'Hanuta',
             'Kinder', 'Kinder Bueno', 'Knoppers', 'Manner', 'Mars', 'Milka',
             'NEOH', 'Nicks', 'Nucao', 'Pick Up!', 'Snickers', 'AHEAD',
             'More Nutrition', 'Foodspring'}

THEMEN = [
    ('Zucker / zuckerfrei', r'zucker|sugar'),
    ('Kennt es nicht / nie probiert', r'nie (gegessen|probiert|gekauft|gehört|gesehen)|noch nicht|'
                                      r'kenn\w*\b[^.]{0,14}\bnicht|kenne? ich (zu )?wenig|'
                                      r'(weiss?|weiß) (zu )?wenig|zu wenig|keine ahnung|unbekannt|'
                                      r'sagt mir nichts|keine erfahrung|gar nicht'),
    ('Geschmack positiv', r'lecker|schmeckt gut|gut(er|e)? geschmack|köstlich|süss|süß|'
                          r'geschmacklich (sehr )?gut|yummy|schmeckt mir'),
    ('Geschmack negativ', r'ekelhaft|schmeckt nicht|grauslich|\bfad\b|künstlich|chemisch|komisch|'
                          r'seltsam|eigenartig|gewöhnungsbedürftig|bitter'),
    ('Gesund / Ernährung', r'ges[uü]nd|kalorien|\bfit\b|di[aä]t|abnehmen|ernährung|low\s*carb|keto|leichter'),
    ('Protein / Eiweiss', r'protein|eiweiss|eiweiß'),
    ('Innovativ / anders', r'innovativ|neu(artig)?|anders|alternativ|modern|trend'),
    ('Preis / teuer', r'teuer|preis|kostet|günstig|billig'),
    ('Verpackung / Optik', r'verpackung|packaging|design|bunt|optik|aussehen'),
    ('Knusprig / Textur', r'knusp|crunch|knack|textur|konsistenz'),
    ('Oesterreichisch / regional', r'österreich|austria|regional|heimisch'),
]


zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def num(r, v):
    return float(r[v]) if r[v].strip() else np.nan


def marken_im_text(t):
    """Liefert die erkannten Marken in der Reihenfolge ihres Auftretens."""
    low = t.lower()
    treffer = []
    for name, muster in MARKEN:
        for m in re.finditer(muster, low):
            treffer.append((m.start(), name))
            break
    # Ueberlappung aufloesen: Kinder Bueno schlaegt Kinder am selben Ort
    treffer.sort()
    gesehen, out = set(), []
    for _, name in treffer:
        if name not in gesehen:
            gesehen.add(name)
            out.append(name)
    if 'Kinder Bueno' in out and 'Kinder' in out:
        low_b = re.sub(r'kinder\s*bueno', '', low)
        if not re.search(r'kinder', low_b):
            out.remove('Kinder')
    return out


def logit_fit(X, y):
    return sm.Logit(y, sm.add_constant(X, has_constant='add')).fit(disp=0)


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    kenner = [r for r in d if r['neoh_bekannt'] == '1']
    n = len(d)

    sag('SEGMENTE UND OFFENE ANGABEN - OESTERREICH')
    sag('=' * 78)
    sag('Basis: %d Faelle, davon %d NEOH-Kenner' % (n, len(kenner)))
    sag('')

    # ===================================================================
    sag('A. IST ZUCKER EINE SCHWELLE ODER EIN GRADIENT?')
    sag('-' * 78)
    sag('Stufe 1 zeigte einen Sprung zwischen den Stufen 3 und 4, Stufe 2 einen')
    sag('monotonen Zusammenhang mit der Bewertung. Der Modellvergleich prueft,')
    sag('welche Form die Daten besser tragen - je Tor getrennt.')
    sag('')
    for titel, basis, ziel in [('Tor 1: Erwaegung (Basis Kenner)', kenner, 'neoh_betracht'),
                               ('Bekanntheit (Basis alle)', d, 'neoh_bekannt')]:
        z = np.array([num(r, 'zucker') for r in basis])
        y = np.array([1.0 if r[ziel] == '1' else 0.0 for r in basis])
        ok = ~np.isnan(z)
        z, y = z[ok], y[ok]
        modelle = [
            ('stetig (linear)', z.reshape(-1, 1)),
            ('dichotom (>= 4)', (z >= 4).astype(float).reshape(-1, 1)),
            ('fuenf Stufen (Dummies)', np.column_stack([(z == k).astype(float) for k in (2, 3, 4, 5)])),
        ]
        sag('%s, n = %d' % (titel, len(z)))
        sag('%-26s %10s %10s %10s' % ('Modell', 'LogLik', 'AIC', 'Pseudo-R2'))
        basiswert = None
        for name, X in modelle:
            m = logit_fit(X, y)
            if basiswert is None:
                basiswert = m.aic
            sag('%-26s %10.2f %10.2f %10.3f' % (name, m.llf, m.aic, m.prsquared))
        sag('')

    # ===================================================================
    sag('B. UNGESTUETZTE BEKANNTHEIT (spontan)')
    sag('-' * 78)
    texte = [(r, r['spontan'].strip()) for r in d if r['spontan'].strip()]
    sag('Antworten: %d von %d (%.1f %%)' % (len(texte), n, 100 * len(texte) / n))
    erkannt = [(r, marken_im_text(t)) for r, t in texte]
    ohne = [t for (r, t), (_, m) in zip(texte, erkannt) if not m]
    sag('Mindestens eine Marke erkannt: %d (%.1f %% der Antworten)' % (
        len(texte) - len(ohne), 100 * (len(texte) - len(ohne)) / len(texte)))
    sag('Keine Marke erkannt: %d' % len(ohne))
    sag('   Beispiele: %s' % ' | '.join(t[:28] for t in ohne[:6]))
    sag('')

    nennungen = collections.Counter()
    tom = collections.Counter()
    for r, m in erkannt:
        for name in m:
            nennungen[name] += 1
        if m:
            tom[m[0]] += 1
    sag('%-18s %8s %8s   %8s %8s   %s' % ('Marke', 'ungest.', 'Anteil', 'Top of M', 'Anteil', 'im Raster?'))
    for name, c in nennungen.most_common(18):
        sag('%-18s %8d %7.1f %%   %8d %7.1f %%   %s' % (
            name, c, 100 * c / len(texte), tom[name], 100 * tom[name] / len(texte),
            'ja' if name in IM_RASTER else 'NEIN'))
    sag('')

    neoh_u = nennungen['NEOH']
    sag('NEOH ungestuetzt: %d Nennungen = %.1f %% der Antwortenden,' % (neoh_u, 100 * neoh_u / len(texte)))
    sag('gegenueber 53,3 % gestuetzter Bekanntheit (Stufe 1).')
    gest = [r for r, m in erkannt if r['neoh_bekannt'] == '1']
    neoh_u_k = sum(1 for r, m in erkannt if 'NEOH' in m and r['neoh_bekannt'] == '1')
    sag('Unter den %d Kennern nennen %d NEOH spontan: %.1f %%.' % (
        len(gest), neoh_u_k, 100 * neoh_u_k / len(gest)))
    sag('')
    fehlen = [(nm, c) for nm, c in nennungen.most_common() if nm not in IM_RASTER]
    sag('Nicht im gestuetzten Raster, aber spontan genannt:')
    for nm, c in fehlen[:10]:
        sag('   %-18s %4d  %5.1f %%' % (nm, c, 100 * c / len(texte)))
    sag('')

    # ===================================================================
    sag('C. WIE BESCHREIBEN KENNER DIE MARKE (beschreibung)')
    sag('-' * 78)
    bt = [(r, r['beschreibung'].strip()) for r in kenner if len(r['beschreibung'].strip()) > 1]
    sag('Auswertbare Texte: %d von %d Kennern (%.1f %%)' % (
        len(bt), len(kenner), 100 * len(bt) / len(kenner)))
    sag('Median %d Zeichen - das traegt eine Themenstruktur, keine tiefe' % (
        int(np.median([len(t) for _, t in bt]))))
    sag('Inhaltsanalyse.')
    sag('')
    zuord = collections.Counter()
    pro_text = []
    # Rein kategoriale Beschreibungen ("eine Schokoriegelmarke") sind selbst
    # ein Befund: Markenkenntnis auf Kategorieniveau. Der Code greift nur,
    # wenn keine inhaltliche Regel zugetroffen hat.
    NUR_KATEGORIE = re.compile(
        r'^(ein(e|en|er)?\s+)?(gute[rn]?\s+)?(schoko(laden?)?riegel|riegel|snack\w*|'
        r'süßigkeit\w*|suessigkeit\w*|schokolade|marke)[\s\w]{0,12}$')
    for r, t in bt:
        low = t.lower()
        treffer = [nm for nm, mu in THEMEN if re.search(mu, low)]
        if not treffer and NUR_KATEGORIE.match(low.strip(' .!')):
            treffer = ['Nur Kategorie ("ein Schokoriegel")']
        pro_text.append((r, t, treffer))
        for nm in treffer:
            zuord[nm] += 1
    keine = [(r, t) for r, t, tr in pro_text if not tr]
    sag('%-34s %5s %8s' % ('Thema', 'n', 'Anteil'))
    for nm, c in zuord.most_common():
        sag('%-34s %5d %7.1f %%' % (nm, c, 100 * c / len(bt)))
    sag('%-34s %5d %7.1f %%' % ('(keinem Thema zugeordnet)', len(keine), 100 * len(keine) / len(bt)))
    sag('')
    sag('Nicht zugeordnete Beispiele: %s' % ' | '.join(t[:30] for _, t in keine[:6]))
    sag('')

    # Das inhaltlich wichtigste Thema: wer kann die Marke gar nicht beschreiben
    unkenntnis = np.array([any(nm == 'Kennt es nicht / nie probiert' for nm in tr)
                           for _, _, tr in pro_text])
    sag('Der aufschlussreichste Code ist "Kennt es nicht / nie probiert":')
    sag('%d von %d Kennern (%.1f %%) koennen die Marke, die sie im Raster' % (
        unkenntnis.sum(), len(bt), 100 * unkenntnis.mean()))
    sag('angekreuzt haben, inhaltlich nicht beschreiben.')
    sag('')
    erw = np.array([r['neoh_betracht'] == '1' for r, _, _ in pro_text])
    sag('   davon erwaegen NEOH: %.1f %%' % (100 * erw[unkenntnis].mean()))
    sag('   von den uebrigen:    %.1f %%' % (100 * erw[~unkenntnis].mean()))
    sag('')
    zuck_code = np.array([any(nm == 'Zucker / zuckerfrei' for nm in tr) for _, _, tr in pro_text])
    sag('Wer Zucker als Merkmal nennt (n = %d), erwaegt zu %.1f %%;' % (
        zuck_code.sum(), 100 * erw[zuck_code].mean()))
    sag('wer es nicht nennt (n = %d), zu %.1f %%.' % ((~zuck_code).sum(), 100 * erw[~zuck_code].mean()))
    sag('')
    sag('Das ist der Relevanzbefund aus Stufe 1 in den eigenen Worten der')
    sag('Befragten: Wer das Produktversprechen benennen kann, erwaegt die')
    sag('Marke; wer nur den Namen kennt, nicht.')
    sag('')

    sag('Geschrieben: %s' % AUS_TXT)
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
