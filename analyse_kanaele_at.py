# -*- coding: utf-8 -*-
"""Quelle der Bekanntheit: Kontaktkanaele, Oesterreich.

Aufruf:  python3 analyse_kanaele_at.py

Die Frage `kanal` ("In welchen der folgenden Kanaele haben Sie im letzten
Monat von NEOH gehoert oder NEOH gesehen?") wurde bisher nur als
Haeufigkeitstabelle berichtet. Dieses Skript wertet sie vollstaendig aus:

  1  Reichweite je Kanal, mit Konfidenzintervallen
  2  Zahl der Kontaktpunkte je Person
  3  Kanal und Erwaegung - und was diese Zahlen NICHT zeigen
  4  Wer ueber welchen Kanal erreicht wird (Demografie)
  5  Die Kontaktlosen: Markenkenntnis ohne juengsten Kontakt
  6  Traegt Kontakt etwas bei, wenn das Markenurteil kontrolliert ist?

Eine Einschraenkung gilt durchgehend und wird nicht wegerklaert: Die Frage
ging nur an NEOH-Kenner. Wer die Marke nicht kennt, hatte keine Gelegenheit,
einen Kontakt zu berichten. Jeder Zusammenhang zwischen Kanal und Erwaegung
ist deshalb ein Zusammenhang, keine Wirkung - wer eine Marke erwaegt, nimmt
ihre Werbung auch eher wahr und erinnert sie besser.

Schreibt ERGEBNISSE_AT_kanaele.txt und ERGEBNISSE_AT_kanaele.csv
"""
import csv, io, math, collections
import numpy as np
import statsmodels.api as sm
from scipy import stats

from analyse_segmente_text_at import marken_im_text

DATEN = 'NEOH_AT_analyse.csv'
AUS_TXT = 'ERGEBNISSE_AT_kanaele.txt'
AUS_CSV = 'ERGEBNISSE_AT_kanaele.csv'

KANAL = {1: 'TV-Werbung', 2: 'Printwerbung', 3: 'Werbung auf Websites',
         4: 'Instagram/Facebook', 5: 'YouTube', 6: 'TikTok',
         7: 'Influencer-Empfehlungen', 8: 'Supermarkt (Regal, Display)',
         9: 'Mundpropaganda', 10: 'Außenwerbung', 11: 'In keinem dieser Kanäle'}
GRUPPE = {'Handel': [8], 'Klassische Medien': [1, 2, 10],
          'Digital und Social': [3, 4, 5, 6, 7], 'Persönlich': [9]}
SLIDER = ['emotion_1', 'qualität_1', 'plv_1', 'zufriedenheit_1']
LADUNG = np.array([0.844, 0.866, 0.608, 0.831])

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def num(r, v):
    return float(r[v]) if r[v].strip() else np.nan


def wilson(p, n, z=1.96):
    if n <= 0:
        return (0.0, 0.0)
    nenner = 1 + z * z / n
    mitte = (p + z * z / (2 * n)) / nenner
    halb = z * math.sqrt(max(0.0, p * (1 - p) / n + z * z / (4 * n * n))) / nenner
    return (max(0.0, mitte - halb), min(1.0, mitte + halb))


def anteil(maske, w):
    maske = np.asarray(maske, dtype=bool)
    if w.sum() <= 0:
        return 0.0, (0.0, 0.0)
    p = float(w[maske].sum() / w.sum())
    n_eff = w.sum() ** 2 / (w ** 2).sum()
    return 100 * p, tuple(100 * x for x in wilson(p, n_eff))


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    kenner = [r for r in d if r['neoh_bekannt'] == '1']
    w = np.array([float(r['gewicht_quote']) for r in kenner])
    n = len(kenner)
    for r in kenner:
        r['_k'] = {i: r['kanal_%d' % i] == '1' for i in range(1, 12)}
        r['_anz'] = sum(1 for i in range(1, 11) if r['_k'][i])
        r['_u'] = 'NEOH' in (marken_im_text(r['spontan']) if r['spontan'].strip() else [])
    erw = np.array([r['neoh_betracht'] == '1' for r in kenner], dtype=bool)
    kauf = np.array([r['neoh_kauf'] == '1' for r in kenner], dtype=bool)
    anz = np.array([r['_anz'] for r in kenner])

    # Markenurteil fuer die Kontrolle in Abschnitt 6
    M = np.array([[num(r, v) for v in SLIDER] for r in kenner])
    Z = (M - np.nanmean(M, 0)) / np.nanstd(M, 0, ddof=1)
    bh = np.array([float((z_[~np.isnan(z_)] * LADUNG[~np.isnan(z_)]).sum() /
                         LADUNG[~np.isnan(z_)].sum()) if (~np.isnan(z_)).sum() >= 3 else np.nan
                   for z_ in Z])

    sag('QUELLE DER BEKANNTHEIT - KONTAKTKANAELE, OESTERREICH')
    sag('=' * 78)
    sag('Basis: %d NEOH-Kenner. Die Frage ging nur an sie - Nicht-Kenner wurden' % n)
    sag('nicht gefragt und haetten auch keinen Kontakt berichten koennen.')
    sag('Mehrfachnennung, Bezug "im letzten Monat".')
    sag('')

    # ---------------------------------------------------------------- 1
    sag('1. REICHWEITE JE KANAL')
    sag('-' * 78)
    sag('%-28s %6s %9s %17s' % ('Kanal', 'n', 'Anteil', '95-%-Intervall'))
    rows = []
    for i in sorted(range(1, 12), key=lambda i: -sum(1 for r in kenner if r['_k'][i])):
        m = np.array([r['_k'][i] for r in kenner], dtype=bool)
        p, (u, o) = anteil(m, w)
        sag('%-28s %6d %8.1f%% [%5.1f; %5.1f]' % (KANAL[i], int(m.sum()), p, u, o))
        rows.append({'ebene': 'Kanal', 'name': KANAL[i], 'n': int(m.sum()),
                     'anteil': round(p, 1), 'ku': round(u, 1), 'ko': round(o, 1)})
    sag('')
    sag('Nach Kanalgruppen (mindestens ein Kontakt in der Gruppe):')
    for g, idx in GRUPPE.items():
        m = np.array([any(r['_k'][i] for i in idx) for r in kenner], dtype=bool)
        p, (u, o) = anteil(m, w)
        sag('   %-25s %6d %8.1f%% [%5.1f; %5.1f]' % (g, int(m.sum()), p, u, o))
        rows.append({'ebene': 'Gruppe', 'name': g, 'n': int(m.sum()),
                     'anteil': round(p, 1), 'ku': round(u, 1), 'ko': round(o, 1)})
    sag('')
    sag('Der Handel ist der mit Abstand wichtigste Kontaktpunkt. Das ist fuer eine')
    sag('Marke dieser Groesse erwartbar und zugleich der Grund, warum die')
    sag('Distributionsbarrieren aus Stufe 3 so schwer wiegen: Wo die Marke nicht')
    sag('im Regal steht, gibt es kaum einen zweiten Kontaktweg.')
    sag('')

    # ---------------------------------------------------------------- 2
    sag('2. WIE VIELE KONTAKTPUNKTE')
    sag('-' * 78)
    vert = collections.Counter(anz)
    for k in sorted(vert):
        sag('   %d Kanäle: %3d Personen (%4.1f %%)' % (k, vert[k], 100 * vert[k] / n))
    sag('')
    sag('Mittelwert %.2f, Median %.0f.' % (anz.mean(), np.median(anz)))
    sag('')
    for lab, m in [('erwägen NEOH', erw), ('haben gekauft', kauf),
                   ('nennen NEOH ungestützt', np.array([r['_u'] for r in kenner], dtype=bool))]:
        t, p = stats.ttest_ind(anz[m], anz[~m], equal_var=False)
        sag('%-26s M = %.2f Kanäle gegen %.2f, t = %5.2f, p = %.4f'
            % (lab + ':', anz[m].mean(), anz[~m].mean(), t, p))
    sag('')

    # ---------------------------------------------------------------- 3
    sag('3. KANAL UND ERWAEGUNG')
    sag('-' * 78)
    sag('%-28s %6s %11s %17s' % ('Kanal', 'n', 'erwägen', '95-%-Intervall'))
    for i in range(1, 12):
        m = np.array([r['_k'][i] for r in kenner], dtype=bool)
        if m.sum() < 15:
            continue
        p, (u, o) = anteil(erw[m], w[m])
        sag('%-28s %6d %10.1f%% [%5.1f; %5.1f]' % (KANAL[i], int(m.sum()), p, u, o))
        rows.append({'ebene': 'Erwägung je Kanal', 'name': KANAL[i], 'n': int(m.sum()),
                     'anteil': round(p, 1), 'ku': round(u, 1), 'ko': round(o, 1)})
    p_ges, _ = anteil(erw, w)
    sag('%-28s %6d %10.1f%%' % ('alle Kenner', n, p_ges))
    sag('')
    sag('Diese Tabelle ist die am leichtesten misszuverstehende der ganzen Studie.')
    sag('Sie zeigt NICHT, welcher Kanal Erwaegung erzeugt. Wer eine Marke erwaegt,')
    sag('nimmt ihre Werbung aufmerksamer wahr und erinnert den Kontakt besser -')
    sag('die Kausalitaet laeuft in beide Richtungen, und aus einem Querschnitt')
    sag('laesst sie sich nicht trennen. Fuer eine Wirkungsaussage braeuchte es')
    sag('eine Panelmessung oder ein Experiment.')
    sag('')

    # ---------------------------------------------------------------- 4
    sag('4. WER UEBER WELCHEN KANAL ERREICHT WIRD')
    sag('-' * 78)
    sag('Dieser Abschnitt ist der praktisch brauchbarste: Er beschreibt, wen ein')
    sag('Kanal unter den Kennern erreicht - keine Wirkung, sondern Reichweite.')
    sag('')
    gruppen = [('alter_txt', ['18 bis 29 Jahre', '30 bis 39 Jahre', '40 bis 49 Jahre',
                              '50 bis 59 Jahre', '60 Jahre und älter']),
               ('geschlecht_txt', ['Weiblich', 'Männlich'])]
    for var, stufen in gruppen:
        kopf = [s.replace(' Jahre', '').replace(' und älter', '+')[:9] for s in stufen]
        sag('%-28s' % '' + ''.join('%10s' % k for k in kopf))
        for i in sorted(range(1, 12), key=lambda i: -sum(1 for r in kenner if r['_k'][i])):
            if sum(1 for r in kenner if r['_k'][i]) < 20:
                continue
            werte = []
            for s_ in stufen:
                sel = np.array([r[var] == s_ for r in kenner], dtype=bool)
                if sel.sum() < 15:
                    werte.append(None)
                    continue
                m = np.array([r['_k'][i] for r in kenner], dtype=bool)
                werte.append(anteil(m[sel], w[sel])[0])
            sag('%-28s' % KANAL[i] + ''.join(
                '%9.1f%%' % v if v is not None else '%10s' % '–' for v in werte))
        sag('')

    # ---------------------------------------------------------------- 5
    sag('5. DIE KONTAKTLOSEN')
    sag('-' * 78)
    kein = np.array([r['_k'][11] for r in kenner], dtype=bool)
    p, (u, o) = anteil(kein, w)
    sag('%d Kenner (%.1f %% [%.1f; %.1f]) hatten im letzten Monat in keinem der'
        % (int(kein.sum()), p, u, o))
    sag('abgefragten Kanaele Kontakt - sie kennen die Marke aus frueherer Zeit.')
    sag('')
    sag('%-30s %12s %12s' % ('', 'ohne Kontakt', 'mit Kontakt'))
    for lab, arr in [('erwägen NEOH', erw), ('haben gekauft', kauf),
                     ('nennen NEOH ungestützt', np.array([r['_u'] for r in kenner], dtype=bool))]:
        a = anteil(arr[kein], w[kein])[0]
        b = anteil(arr[~kein], w[~kein])[0]
        sag('%-30s %11.1f%% %11.1f%%' % (lab, a, b))
    x = bh[kein][~np.isnan(bh[kein])]
    y = bh[~kein][~np.isnan(bh[~kein])]
    t, pp = stats.ttest_ind(x, y, equal_var=False)
    sag('%-30s %11.3f %11.3f   t = %.2f, p = %.4f' % ('Brand-Health-Index', x.mean(), y.mean(), t, pp))
    sag('')
    sag('Das ist die Gruppe, bei der Markenkenntnis ohne frischen Kontakt')
    sag('existiert - und sie steht in allen Kennwerten deutlich schlechter da.')
    sag('Ob der fehlende Kontakt die schwache Bindung erzeugt oder die schwache')
    sag('Bindung dazu fuehrt, dass Kontakte nicht erinnert werden, entscheidet')
    sag('auch diese Erhebung nicht.')
    sag('')

    # ---------------------------------------------------------------- 6
    sag('6. TRAEGT KONTAKT ETWAS BEI, WENN DAS MARKENURTEIL KONTROLLIERT IST?')
    sag('-' * 78)
    ok = ~np.isnan(bh)
    y = erw[ok].astype(float)
    X1 = bh[ok].reshape(-1, 1)
    X2 = np.column_stack([bh[ok], anz[ok]])
    for titel, X, namen in [('nur Markenurteil', X1, ['bh_index']),
                            ('+ Zahl der Kontaktkanäle', X2, ['bh_index', 'kanäle'])]:
        m = sm.Logit(y, sm.add_constant(X, has_constant='add')).fit(disp=0)
        sag('%-28s n = %d, Pseudo-R2 = %.3f, AIC = %.1f'
            % (titel, int(ok.sum()), m.prsquared, m.aic))
        for i, nm in enumerate(['(Konstante)'] + namen):
            sag('     %-12s b = %6.3f  SE = %5.3f  p = %6.4f  Odds = %5.2f'
                % (nm, m.params[i], m.bse[i], m.pvalues[i], math.exp(m.params[i])))
    sag('')

    with io.open(AUS_CSV, 'w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=['ebene', 'name', 'n', 'anteil', 'ku', 'ko'])
        wr.writeheader()
        wr.writerows(rows)
    sag('Geschrieben: %s, %s' % (AUS_TXT, AUS_CSV))
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
