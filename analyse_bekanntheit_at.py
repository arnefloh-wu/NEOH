# -*- coding: utf-8 -*-
"""Vertiefung: gestuetzte und ungestuetzte Markenbekanntheit, Oesterreich.

Aufruf:  python3 analyse_bekanntheit_at.py

Stufe 4 hat die Luecke zwischen Wiedererkennung und Erinnerung gezeigt. Dieses
Skript geht darauf ein:

  1  Erinnerungsquote je Marke (ungestuetzt geteilt durch gestuetzt)
  2  Share of Mind gegen Share of Recognition
  3  Top of Mind und Nennposition
  4  Mentale Verfuegbarkeit: wie viele Marken nennt eine Person
  5  Ungestuetzte Bekanntheit nach Untergruppen
  6  Traegt Erinnerung mehr zur Erwaegung bei als Wiedererkennung?
  7  Unterscheiden sich Erinnerer im Markenurteil?

Schreibt ERGEBNISSE_AT_bekanntheit.txt und ERGEBNISSE_AT_bekanntheit.csv
(Kennwerte je Marke, aggregiert, fuer Slides und Dashboard).
"""
import csv, io, math, collections
import numpy as np
import statsmodels.api as sm
from scipy import stats

from analyse_segmente_text_at import marken_im_text, IM_RASTER

DATEN = 'NEOH_AT_analyse.csv'
FUNNEL = 'ERGEBNISSE_AT_funnel.csv'
AUS_TXT = 'ERGEBNISSE_AT_bekanntheit.txt'
AUS_CSV = 'ERGEBNISSE_AT_bekanntheit.csv'
NEOH = '13'

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def num(r, v):
    return float(r[v]) if r[v].strip() else np.nan


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    fu = {r['marke']: r for r in csv.DictReader(io.open(FUNNEL, encoding='utf-8-sig'))}
    w = np.array([float(r['gewicht_quote']) for r in d])
    n = len(d)

    # Spontannennungen je Fall, in Reihenfolge
    for r in d:
        r['_sp'] = marken_im_text(r['spontan']) if r['spontan'].strip() else []
    mit_text = [r for r in d if r['spontan'].strip()]

    sag('GESTUETZTE UND UNGESTUETZTE BEKANNTHEIT - OESTERREICH')
    sag('=' * 78)
    sag('Basis: %d Faelle, davon %d mit Spontannennung' % (n, len(mit_text)))
    sag('Gestuetzte Werte gewichtet, ungestuetzte als Anteil der Antwortenden.')
    sag('')

    ung = collections.Counter()
    tom = collections.Counter()
    pos = collections.defaultdict(list)
    for r in mit_text:
        for i, nm in enumerate(r['_sp']):
            ung[nm] += 1
            pos[nm].append(i + 1)
        if r['_sp']:
            tom[r['_sp'][0]] += 1
    nennungen_gesamt = sum(ung.values())

    # ---------------------------------------------------------------- 1
    sag('1. ERINNERUNGSQUOTE: WIE VIEL WIEDERERKENNUNG WIRD ZU ERINNERUNG')
    sag('-' * 78)
    sag('Erinnerungsquote = ungestuetzte Nennung geteilt durch gestuetzte Bekanntheit.')
    sag('Sie misst, wie fest eine Marke im Gedaechtnis verankert ist - unabhaengig')
    sag('davon, wie viele Menschen sie ueberhaupt kennen.')
    sag('')
    reihen = []
    for m, r in fu.items():
        g = float(r['bekanntheit'])
        if g < 5:
            continue
        u = 100 * ung.get(m, 0) / len(mit_text)
        reihen.append({'marke': m, 'gestuetzt': g, 'ungestuetzt': u,
                       'erinnerungsquote': 100 * u / g if g else 0,
                       'tom': 100 * tom.get(m, 0) / len(mit_text),
                       'tom_anteil_ung': 100 * tom.get(m, 0) / ung[m] if ung.get(m) else 0,
                       'pos_median': float(np.median(pos[m])) if pos.get(m) else float('nan'),
                       'nennungen': ung.get(m, 0)})
    reihen.sort(key=lambda z: -z['erinnerungsquote'])
    sag('%-22s %10s %11s %14s' % ('Marke', 'gestuetzt', 'ungestuetzt', 'Erinnerungsq.'))
    for z in reihen:
        mark = '  <<<' if z['marke'] == 'NEOH' else ''
        sag('%-22s %9.1f%% %10.1f%% %13.1f%%%s' % (
            z['marke'][:22], z['gestuetzt'], z['ungestuetzt'], z['erinnerungsquote'], mark))
    sag('')
    nz = [z for z in reihen if z['marke'] == 'NEOH'][0]
    med = float(np.median([z['erinnerungsquote'] for z in reihen]))
    rang = reihen.index(nz) + 1
    sag('NEOH: %.1f %% Erinnerungsquote, Rang %d von %d. Median %.1f %%.' % (
        nz['erinnerungsquote'], rang, len(reihen), med))
    sag('')

    # ---------------------------------------------------------------- 2
    sag('2. SHARE OF MIND GEGEN SHARE OF RECOGNITION')
    sag('-' * 78)
    sag('Share of Mind: Anteil an allen %d Spontannennungen.' % nennungen_gesamt)
    sag('Share of Recognition: Anteil an der Summe der gestuetzten Bekanntheiten')
    sag('aller im Raster abgefragten Marken.')
    sag('')
    summe_gest = sum(float(r['bekanntheit']) for r in fu.values())
    sag('%-22s %10s %10s %10s' % ('Marke', 'SoM', 'SoR', 'SoM/SoR'))
    som_reihen = []
    for z in sorted(reihen, key=lambda x: -x['nennungen']):
        som = 100 * z['nennungen'] / nennungen_gesamt
        sor = 100 * z['gestuetzt'] / summe_gest
        som_reihen.append((z['marke'], som, sor))
        mark = '  <<<' if z['marke'] == 'NEOH' else ''
        sag('%-22s %9.1f%% %9.1f%% %9.2f%s' % (z['marke'][:22], som, sor, som / sor if sor else 0, mark))
    sag('')
    sag('Ein Wert unter 1 heisst: Die Marke wird seltener erinnert, als ihre')
    sag('Bekanntheit erwarten liesse.')
    sag('')

    # ---------------------------------------------------------------- 3
    sag('3. TOP OF MIND UND NENNPOSITION')
    sag('-' * 78)
    sag('%-22s %9s %16s %14s' % ('Marke', 'TOM', 'TOM je Nennung', 'Median-Position'))
    for z in sorted(reihen, key=lambda x: -x['tom'])[:14]:
        mark = '  <<<' if z['marke'] == 'NEOH' else ''
        sag('%-22s %8.1f%% %15.0f%% %14.1f%s' % (
            z['marke'][:22], z['tom'], z['tom_anteil_ung'], z['pos_median'], mark))
    sag('')
    sag('"TOM je Nennung" ist der Anteil der Nennungen, bei denen die Marke')
    sag('zuerst genannt wurde - ein Mass fuer Dominanz im Gedaechtnis der')
    sag('Menschen, die sie ueberhaupt erinnern.')
    sag('')

    # ---------------------------------------------------------------- 4
    sag('4. MENTALE VERFUEGBARKEIT DER KATEGORIE')
    sag('-' * 78)
    anzahl = np.array([len(r['_sp']) for r in mit_text])
    sag('Genannte Marken je Person: M = %.2f, Median = %.0f, Maximum = %d' % (
        anzahl.mean(), np.median(anzahl), anzahl.max()))
    vert = collections.Counter(anzahl)
    for k in sorted(vert):
        sag('   %2d Marken: %3d Personen (%4.1f %%)' % (k, vert[k], 100 * vert[k] / len(mit_text)))
    sag('')
    neoh_erinnert = np.array([('NEOH' in r['_sp']) for r in mit_text], dtype=bool)
    sag('Wer NEOH spontan nennt, nennt insgesamt %.2f Marken;' % anzahl[neoh_erinnert].mean())
    sag('wer es nicht nennt, %.2f. t = %.2f, p = %.3f' % (
        anzahl[~neoh_erinnert].mean(),
        *stats.ttest_ind(anzahl[neoh_erinnert], anzahl[~neoh_erinnert], equal_var=False)))
    sag('')
    sag('Das trennt zwei Erklaerungen: Wird NEOH nur von Menschen genannt, denen')
    sag('ohnehin viele Marken einfallen, oder verdraengt es andere Marken?')
    sag('')

    # ---------------------------------------------------------------- 5
    sag('5. UNGESTUETZTE BEKANNTHEIT VON NEOH NACH UNTERGRUPPEN')
    sag('-' * 78)
    sag('%-30s %6s %11s %11s %13s' % ('', 'n', 'gestuetzt', 'ungestuetzt', 'Erinnerungsq.'))
    for var, titel in [('alter_txt', 'Alter'), ('geschlecht_txt', 'Geschlecht'),
                       ('zucker', 'Zuckerreduktion wichtig')]:
        sag(titel + ':')
        for stufe in sorted({r[var] for r in mit_text if r[var].strip()}):
            teil = [r for r in mit_text if r[var] == stufe]
            tw = np.array([float(r['gewicht_quote']) for r in teil])
            g = 100 * tw[np.array([r['neoh_bekannt'] == '1' for r in teil], dtype=bool)].sum() / tw.sum()
            u = 100 * sum(1 for r in teil if 'NEOH' in r['_sp']) / len(teil)
            sag('   %-27s %6d %10.1f%% %10.1f%% %12.1f%%' % (
                stufe[:27], len(teil), g, u, 100 * u / g if g else 0))
        sag('')

    # ---------------------------------------------------------------- 6
    sag('6. TRAEGT ERINNERUNG MEHR BEI ALS WIEDERERKENNUNG?')
    sag('-' * 78)
    sag('Ein Modell ueber die ganze Stichprobe waere hier wertlos: Wer NEOH nicht')
    sag('gestuetzt kennt, kann es per Fragebogenlogik auch nicht erwaegen. Der')
    sag('Praediktor "gestuetzt" trennt die Faelle damit vollstaendig, und die')
    sag('Schaetzung divergiert. Die beantwortbare Frage lautet deshalb: Traegt die')
    sag('Erinnerung INNERHALB der Kenner etwas bei?')
    sag('')
    kenner = [r for r in mit_text if r['bekanntheit_%s' % NEOH] == '1']
    e = np.array([1.0 if 'NEOH' in r['_sp'] else 0.0 for r in kenner])
    b = np.array([1.0 if r['betracht_%s' % NEOH] == '1' else 0.0 for r in kenner])
    sag('Unter den %d Kennern:' % len(kenner))
    sag('   erinnern spontan (n = %3d): %.1f %% erwaegen' % (int(e.sum()), 100 * b[e == 1].mean()))
    sag('   erkennen nur     (n = %3d): %.1f %% erwaegen' % (int((1 - e).sum()), 100 * b[e == 0].mean()))
    t, p = stats.ttest_ind(b[e == 1], b[e == 0], equal_var=False)
    sag('   t = %.2f, p = %.4f' % (t, p))
    sag('')
    sag('Ist das nur ein Nebeneffekt des Markenurteils? Kontrolle dafuer:')
    IDX = ['emotion_1', 'qualität_1', 'plv_1', 'zufriedenheit_1']
    Xi = np.array([[num(r, v) for v in IDX] for r in kenner])
    lad = np.array([0.844, 0.866, 0.608, 0.831])
    mu, sd = np.nanmean(Xi, 0), np.nanstd(Xi, 0, ddof=1)
    Zi = (Xi - mu) / sd
    bh = np.array([float((z_[~np.isnan(z_)] * lad[~np.isnan(z_)]).sum() /
                         lad[~np.isnan(z_)].sum()) if (~np.isnan(z_)).sum() >= 3 else np.nan
                   for z_ in Zi])
    ok = ~np.isnan(bh)
    for titel, X, namen in [('nur Markenurteil', bh[ok].reshape(-1, 1), ['bh_index']),
                            ('Markenurteil + Erinnerung', np.column_stack([bh[ok], e[ok]]),
                             ['bh_index', 'erinnert'])]:
        m = sm.Logit(b[ok], sm.add_constant(X, has_constant='add')).fit(disp=0)
        sag('   %-28s n = %d, Pseudo-R2 = %.3f, AIC = %.1f' % (titel, ok.sum(), m.prsquared, m.aic))
        for i, nm in enumerate(['(Konstante)'] + namen):
            sag('        %-12s b = %6.3f  SE = %5.3f  p = %6.4f  Odds = %6.2f' % (
                nm, m.params[i], m.bse[i], m.pvalues[i], math.exp(m.params[i])))
    sag('')

    # ---------------------------------------------------------------- 7
    sag('7. UNTERSCHEIDEN SICH ERINNERER IM MARKENURTEIL?')
    sag('-' * 78)
    SL = [('emotion_1', 'emotion'), ('qualität_1', 'qualität'), ('plv_1', 'plv'),
          ('zufriedenheit_1', 'zufriedenheit'), ('wom_1', 'wom')]
    sag('%-16s %12s %12s %9s %8s' % ('', 'erinnern', 'erkennen nur', 'Diff', 'p'))
    for v, lab in SL:
        a = np.array([num(r, v) for r in kenner if 'NEOH' in r['_sp']])
        c = np.array([num(r, v) for r in kenner if 'NEOH' not in r['_sp']])
        a, c = a[~np.isnan(a)], c[~np.isnan(c)]
        t, p = stats.ttest_ind(a, c, equal_var=False)
        sag('%-16s %11.1f %12.1f %9.1f %8.3f' % (lab, a.mean(), c.mean(), a.mean() - c.mean(), p))
    sag('')

    with io.open(AUS_CSV, 'w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=['marke', 'gestuetzt', 'ungestuetzt',
                                            'erinnerungsquote', 'tom', 'tom_anteil_ung',
                                            'pos_median', 'nennungen'])
        wr.writeheader()
        for z in sorted(reihen, key=lambda x: -x['gestuetzt']):
            wr.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in z.items()})
    sag('Geschrieben: %s, %s' % (AUS_TXT, AUS_CSV))
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
