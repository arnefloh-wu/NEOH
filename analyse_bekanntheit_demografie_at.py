# -*- coding: utf-8 -*-
"""Markenbekanntheit nach Demografie, Oesterreich.

Aufruf:  python3 analyse_bekanntheit_demografie_at.py

Vertieft die gestuetzte und ungestuetzte Bekanntheit von NEOH nach Alter,
Geschlecht, Region, Bildung und Einkommen - und zwar in drei Schritten, weil
die uebliche Tabelle allein in die Irre fuehrt:

  1  Bivariate Tabellen je Merkmal, mit Konfidenzintervallen und Fallzahlen
  2  Multivariates Modell: Welche Merkmale tragen, wenn man die anderen
     kontrolliert? Bildung korreliert mit Alter, Einkommen mit Bildung -
     ohne Kontrolle sieht man Scheinzusammenhaenge.
  3  Ist NEOHs Altersgefaelle ungewoehnlich? Vergleich mit allen Marken.

Regionen nach NUTS-1, nicht nach einer frei gewaehlten Ost-West-Linie:
  Ost   Wien, Niederoesterreich, Burgenland
  Sued  Steiermark, Kaernten
  West  Oberoesterreich, Salzburg, Tirol, Vorarlberg

Schreibt ERGEBNISSE_AT_bekanntheit_demografie.txt und .csv
"""
import csv, io, math, collections
import numpy as np
import statsmodels.api as sm
from scipy import stats

from analyse_segmente_text_at import marken_im_text

DATEN = 'NEOH_AT_analyse.csv'
QSF = 'NEOH_AT_Sep2026.qsf'
AUS_TXT = 'ERGEBNISSE_AT_bekanntheit_demografie.txt'
AUS_CSV = 'ERGEBNISSE_AT_bekanntheit_demografie.csv'
NEOH = '13'
MIN_ZELLE = 40          # darunter wird die Zelle als unsicher markiert

NUTS1 = {'Wien': 'Ost', 'Niederösterreich': 'Ost', 'Burgenland': 'Ost',
         'Steiermark': 'Süd', 'Kärnten': 'Süd',
         'Oberösterreich': 'West', 'Salzburg': 'West', 'Tirol': 'West',
         'Vorarlberg': 'West'}

# Bildung auf drei Stufen, weil Doktorat (n=10) und Sonstiges (n=14) allein
# nicht tragen. Die Rohkategorie bleibt im Datensatz erhalten.
BILDUNG3 = {'Pflichtschule': 'Pflichtschule/Lehre',
            'Lehre/Berufsausbildung': 'Pflichtschule/Lehre',
            'Matura/Abitur': 'Matura',
            'Bachelor': 'Hochschule', 'Master/Magister/Diplom': 'Hochschule',
            'Doktorat/PhD': 'Hochschule'}

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def wilson(p, n, z=1.96):
    if n <= 0:
        return (0.0, 0.0)
    nenner = 1 + z * z / n
    mitte = (p + z * z / (2 * n)) / nenner
    halb = z * math.sqrt(max(0.0, p * (1 - p) / n + z * z / (4 * n * n))) / nenner
    return (max(0.0, mitte - halb), min(1.0, mitte + halb))


def kennwerte(teil, gew):
    """Gestuetzt (gewichtet, mit KI auf dem effektiven n), ungestuetzt, Quote."""
    w = np.array(gew, float)
    g_m = np.array([r['neoh_bekannt'] == '1' for r in teil], dtype=bool)
    p = float(w[g_m].sum() / w.sum())
    n_eff = w.sum() ** 2 / (w ** 2).sum()
    u, o = wilson(p, n_eff)
    ung = sum(1 for r in teil if 'NEOH' in r['_sp']) / len(teil)
    return dict(n=len(teil), gest=100 * p, ku=100 * u, ko=100 * o,
                ungest=100 * ung, quote=100 * ung / p if p else 0.0)


def tabelle(d, w, var, titel, reihenfolge=None, csv_rows=None):
    stufen = sorted({r[var] for r in d if r[var].strip()})
    if reihenfolge:
        stufen = [s for s in reihenfolge if s in stufen]
    sag(titel)
    sag('   %-26s %5s %9s %17s %11s %12s'
        % ('', 'n', 'gestützt', '95-%-Intervall', 'ungestützt', 'Erinnerungsq.'))
    for s_ in stufen:
        idx = [i for i, r in enumerate(d) if r[var] == s_]
        k = kennwerte([d[i] for i in idx], [w[i] for i in idx])
        flag = '  !' if k['n'] < MIN_ZELLE else ''
        sag('   %-26s %5d %8.1f%% [%5.1f; %5.1f] %10.1f%% %11.1f%%%s'
            % (s_[:26], k['n'], k['gest'], k['ku'], k['ko'], k['ungest'], k['quote'], flag))
        if csv_rows is not None:
            csv_rows.append(dict(merkmal=var, auspraegung=s_, **{a: round(b, 2) for a, b in k.items()}))
    sag()


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    w = np.array([float(r['gewicht_quote']) for r in d])
    for r in d:
        r['_sp'] = marken_im_text(r['spontan']) if r['spontan'].strip() else []
        r['region'] = NUTS1.get(r['bundesland_txt'], '')
        r['bildung3'] = BILDUNG3.get(r['bildung_txt'], '')
    n = len(d)

    sag('MARKENBEKANNTHEIT NACH DEMOGRAFIE - OESTERREICH')
    sag('=' * 80)
    sag('Basis: %d Faelle. Gestuetzte Werte gewichtet, Intervalle nach Wilson auf' % n)
    sag('dem effektiven n. Ungestuetzt als Anteil der jeweiligen Teilgruppe.')
    sag('Mit ! markierte Zellen haben weniger als %d Faelle und tragen keine' % MIN_ZELLE)
    sag('belastbare Aussage - sie stehen der Vollstaendigkeit halber da.')
    sag()

    rows = []
    sag('1. BIVARIATE TABELLEN')
    sag('-' * 80)
    tabelle(d, w, 'alter_txt', 'Alter:', csv_rows=rows)
    tabelle(d, w, 'geschlecht_txt', 'Geschlecht:', csv_rows=rows)
    tabelle(d, w, 'region', 'Region (NUTS-1):', ['Ost', 'Süd', 'West'], csv_rows=rows)
    tabelle(d, w, 'bundesland_txt', 'Bundesland:', csv_rows=rows)
    tabelle(d, w, 'bildung3', 'Bildung (drei Stufen):',
            ['Pflichtschule/Lehre', 'Matura', 'Hochschule'], csv_rows=rows)
    tabelle(d, w, 'bildung_txt', 'Bildung (Rohkategorien):', csv_rows=rows)
    tabelle(d, w, 'einkommen_txt', 'Haushaltseinkommen:',
            ['Unter 1.000 Euro', '1.000 - 1.999 Euro', '2.000 - 2.999 Euro',
             '3.000 - 3.999 Euro', '4.000 - 4.999 Euro', '5.000 Euro oder mehr',
             'Keine Angabe'], csv_rows=rows)

    # ---------------------------------------------------------------- 2
    sag('2. MULTIVARIAT: WAS TRAEGT, WENN MAN DIE ANDEREN KONTROLLIERT')
    sag('-' * 80)
    sag('Logistische Regression auf die gestuetzte Bekanntheit. Alter stetig')
    sag('kodiert (Bandmitte in Jahren, 60+ als 67), Bildung als Stufenzahl,')
    sag('Einkommen als Klassennummer ohne "Keine Angabe".')
    sag()
    ALTER_MITTE = {'2': 24.0, '3': 35.0, '4': 45.0, '5': 55.0, '6': 67.0}
    BILD_STUFE = {'Pflichtschule/Lehre': 1.0, 'Matura': 2.0, 'Hochschule': 3.0}
    X, y, idx = [], [], []
    for i, r in enumerate(d):
        a = ALTER_MITTE.get(r['alter'])
        b = BILD_STUFE.get(r['bildung3'])
        e = r['einkommen']
        if a is None or b is None or not e.strip() or e == '7' or not r['region']:
            continue
        X.append([a, 1.0 if r['geschlecht'] == '2' else 0.0, b, float(e),
                  1.0 if r['region'] == 'West' else 0.0,
                  1.0 if r['region'] == 'Süd' else 0.0])
        y.append(1.0 if r['neoh_bekannt'] == '1' else 0.0)
        idx.append(i)
    X, y = np.array(X), np.array(y)
    namen = ['Alter (Jahre)', 'weiblich', 'Bildung (1-3)', 'Einkommen (1-6)',
             'Region West', 'Region Süd']
    m = sm.Logit(y, sm.add_constant(X, has_constant='add')).fit(disp=0)
    sag('n = %d (ohne "Keine Angabe" beim Einkommen), Pseudo-R2 = %.3f'
        % (len(y), m.prsquared))
    sag('%-20s %9s %8s %9s %9s %s' % ('', 'b', 'SE', 'p', 'Odds', ''))
    for i, nm in enumerate(['(Konstante)'] + namen):
        stern = '***' if m.pvalues[i] < .001 else '**' if m.pvalues[i] < .01 \
            else '*' if m.pvalues[i] < .05 else ''
        sag('%-20s %9.4f %8.4f %9.4f %9.3f %s'
            % (nm, m.params[i], m.bse[i], m.pvalues[i], math.exp(m.params[i]), stern))
    sag()
    od_alter = math.exp(m.params[1] * 10)
    sag('Zehn Jahre mehr Lebensalter verändern die Chance auf Bekanntheit um den')
    sag('Faktor %.3f, also um %.0f Prozent.' % (od_alter, 100 * (od_alter - 1)))
    sag()
    sag('Referenz der Region ist Ost. West und Sued werden dagegen geschaetzt.')
    sag()

    # ---------------------------------------------------------------- 3
    sag('3. IST NEOHS ALTERSGEFAELLE UNGEWOEHNLICH?')
    sag('-' * 80)
    sag('Differenz der gestuetzten Bekanntheit zwischen 18-29 und 60+, je Marke.')
    sag('Ein hoher Wert heisst: Die Marke erreicht die Jungen deutlich besser.')
    sag()
    import json
    q = json.load(io.open(QSF, encoding='utf-8'))
    marken = {}
    for e in q['SurveyElements']:
        p = e.get('Payload')
        if e['Element'] == 'SQ' and isinstance(p, dict) and p.get('DataExportTag') == 'bekanntheit':
            rc = p['RecodeValues']
            marken = {rc[str(k)]: p['Choices'][str(k)]['Display']
                      for k in p['ChoiceOrder'] if rc[str(k)] != '99'}
    jung = np.array([r['alter'] == '2' for r in d], dtype=bool)
    alt_ = np.array([r['alter'] == '6' for r in d], dtype=bool)
    reihen = []
    for c, nm in marken.items():
        bek = np.array([r['bekanntheit_%s' % c] == '1' for r in d], dtype=bool)
        if bek.sum() < 30:
            continue
        pj = 100 * w[jung & bek].sum() / w[jung].sum()
        pa = 100 * w[alt_ & bek].sum() / w[alt_].sum()
        reihen.append((nm, pj, pa, pj - pa))
    reihen.sort(key=lambda t: -t[3])
    sag('%-24s %9s %9s %10s' % ('Marke', '18-29', '60+', 'Differenz'))
    for nm, pj, pa, diff in reihen:
        mark = '  <<<' if nm == 'NEOH' else ''
        sag('%-24s %8.1f%% %8.1f%% %9.1f%s' % (nm[:24], pj, pa, diff, mark))
    rang = [nm for nm, _, _, _ in reihen].index('NEOH') + 1
    med = float(np.median([x[3] for x in reihen]))
    sag()
    sag('NEOH: Rang %d von %d, Median aller Marken %.1f Prozentpunkte.'
        % (rang, len(reihen), med))
    sag()

    with io.open(AUS_CSV, 'w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=['merkmal', 'auspraegung', 'n', 'gest',
                                            'ku', 'ko', 'ungest', 'quote'])
        wr.writeheader()
        wr.writerows(rows)
    sag('Geschrieben: %s, %s' % (AUS_TXT, AUS_CSV))
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
