# -*- coding: utf-8 -*-
"""Die bisher nur als Kovariaten verwendeten Variablen, Oesterreich.

Aufruf:  python3 analyse_weitere_at.py

Fuenf Variablen sind in den Stufen 1 bis 4 nur als Praediktoren aufgetaucht
und nie in eigener Form berichtet worden, drei weitere gar nicht:

  1  intention   Kaufabsicht naechster Monat (1-7)
  2  empfehlung  Weiterempfehlung (0-10), ausgewertet als NPS
  3  bedürfnis   Beduerfniserfuellung (0-10)
  4  bedeutsam   Persoenliche Bedeutsamkeit (0-10)
  5  haeufigkeit Kategorienutzung (1 taeglich bis 7 nie)
  6  t_spontan, t_raster, t_sentiment - die drei Timing-Fragen

Die Timing-Fragen wurden eigens fuer die Feldsteuerung eingebaut und sind
bisher nur als Gesamt-LOI in den Feldbericht eingegangen. Hier werden sie
aufgeschluesselt und gegen die Antwortqualitaet geprueft.

Schreibt ERGEBNISSE_AT_weitere.txt
"""
import csv, io, math, collections
import numpy as np
from scipy import stats

DATEN = 'NEOH_AT_analyse.csv'
AUS_TXT = 'ERGEBNISSE_AT_weitere.txt'
NEOH = '13'

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def num(r, v):
    return float(r[v]) if r[v].strip() else np.nan


def gew_mittel(x, w):
    m = ~np.isnan(x)
    return float((x[m] * w[m]).sum() / w[m].sum()) if m.any() else float('nan')


def verteilung(kenner, w, var, stufen, labels=None):
    x = np.array([num(r, var) for r in kenner])
    out = []
    for s_ in stufen:
        m = x == s_
        out.append((labels[s_] if labels else str(int(s_)), int(m.sum()),
                    100 * float(w[m].sum() / w.sum())))
    return x, out


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    kenner = [r for r in d if r['neoh_bekannt'] == '1']
    w = np.array([float(r['gewicht_quote']) for r in kenner])
    wa = np.array([float(r['gewicht_quote']) for r in d])
    erw = np.array([r['neoh_betracht'] == '1' for r in kenner], dtype=bool)
    kauf = np.array([r['neoh_kauf'] == '1' for r in kenner], dtype=bool)

    sag('WEITERE VARIABLEN - OESTERREICH')
    sag('=' * 78)
    sag('Basis der Abschnitte 1 bis 4: %d NEOH-Kenner. Abschnitt 5 und 6: alle %d.'
        % (len(kenner), len(d)))
    sag('')

    # ---------------------------------------------------------------- 1
    sag('1. KAUFABSICHT (intention, 1 sehr unwahrscheinlich bis 7 sehr wahrscheinlich)')
    sag('-' * 78)
    x, vert = verteilung(kenner, w, 'intention', [1, 2, 3, 4, 5, 6, 7])
    for lab, n_, p in vert:
        sag('   %-4s %4d %6.1f %%  %s' % (lab, n_, p, '#' * int(round(p / 2))))
    sag('')
    sag('M = %.2f (gewichtet %.2f), SD = %.2f, Median = %.0f'
        % (np.nanmean(x), gew_mittel(x, w), np.nanstd(x, ddof=1), np.nanmedian(x)))
    top = np.array([v >= 6 for v in x], dtype=bool)
    sag('Top-2-Box (6 und 7): %.1f %% der Kenner, also %.1f %% der Bevölkerung.'
        % (100 * float(w[top].sum() / w.sum()),
           100 * float(w[top].sum() / wa.sum())))
    sag('Bottom-Box (1): %.1f %% - mehr als ein Drittel schliesst einen Kauf aus.'
        % (100 * float(w[x == 1].sum() / w.sum())))
    sag('')
    for lab, m in [('Erwäger', erw), ('Käufer', kauf)]:
        sag('   %-10s M = %.2f gegen %.2f bei den übrigen'
            % (lab, np.nanmean(x[m]), np.nanmean(x[~m])))
    sag('')

    # ---------------------------------------------------------------- 2
    sag('2. WEITEREMPFEHLUNG ALS NPS (empfehlung, 0 bis 10)')
    sag('-' * 78)
    e = np.array([num(r, 'empfehlung') for r in kenner])
    gueltig = ~np.isnan(e)
    pro = (e >= 9) & gueltig
    pas = (e >= 7) & (e <= 8) & gueltig
    det = (e <= 6) & gueltig
    basis = w[gueltig].sum()
    a_pro = 100 * w[pro].sum() / basis
    a_pas = 100 * w[pas].sum() / basis
    a_det = 100 * w[det].sum() / basis
    sag('Promotoren (9-10):  %5.1f %%   n = %3d' % (a_pro, int(pro.sum())))
    sag('Passive   (7-8):    %5.1f %%   n = %3d' % (a_pas, int(pas.sum())))
    sag('Detraktoren (0-6):  %5.1f %%   n = %3d' % (a_det, int(det.sum())))
    sag('')
    sag('NPS = %+.0f   (Basis: %d Kenner mit Angabe)' % (a_pro - a_det, int(gueltig.sum())))
    sag('')
    sag('Der Wert ist niedrig, aber er misst hier etwas anderes als ueblich: Die')
    sag('NPS-Definition unterstellt Kunden. Hier antworten alle Kenner, auch die')
    sag('%d, die nie gekauft haben. Unter den Kaeufern sieht es anders aus:'
        % int((gueltig & ~kauf).sum()))
    k_basis = w[gueltig & kauf].sum()
    if k_basis > 0:
        sag('   nur Käufer (n = %d): Promotoren %.1f %%, Detraktoren %.1f %%, NPS = %+.0f'
            % (int((gueltig & kauf).sum()),
               100 * w[pro & kauf].sum() / k_basis,
               100 * w[det & kauf].sum() / k_basis,
               100 * (w[pro & kauf].sum() - w[det & kauf].sum()) / k_basis))
    sag('')
    sag('Die Nullen dominieren die Verteilung: %d der %d Kenner geben 0 an.'
        % (int((e == 0).sum()), int(gueltig.sum())))
    sag('Das ist bei einer Marke, die vier von fuenf Kennern nie gekauft haben,')
    sag('zu erwarten und kein Qualitaetsurteil.')
    sag('')

    # ---------------------------------------------------------------- 3
    sag('3. BEDUERFNISERFUELLUNG UND BEDEUTSAMKEIT (0 bis 10)')
    sag('-' * 78)
    sag('%-14s %6s %8s %8s %8s %10s %10s' %
        ('', 'n', 'M', 'gew. M', 'SD', 'Erwäger', 'übrige'))
    for var in ['bedürfnis', 'bedeutsam']:
        x = np.array([num(r, var) for r in kenner])
        sag('%-14s %6d %8.2f %8.2f %8.2f %10.2f %10.2f'
            % (var, int((~np.isnan(x)).sum()), np.nanmean(x), gew_mittel(x, w),
               np.nanstd(x, ddof=1), np.nanmean(x[erw]), np.nanmean(x[~erw])))
    sag('')
    for var in ['bedürfnis', 'bedeutsam']:
        x = np.array([num(r, var) for r in kenner])
        t, p = stats.ttest_ind(x[erw][~np.isnan(x[erw])], x[~erw][~np.isnan(x[~erw])],
                               equal_var=False)
        sag('   %-12s Erwäger gegen übrige: t = %5.2f, p = %.2e' % (var, t, p))
    sag('')
    x = np.array([num(r, 'bedürfnis') for r in kenner])
    hoch = np.array([v >= 7 for v in x], dtype=bool)
    sag('Bedürfniserfüllung 7 oder höher: %.1f %% der Kenner. Deren Erwägungsquote'
        % (100 * float(w[hoch].sum() / w.sum())))
    sag('liegt bei %.1f %%, bei den übrigen bei %.1f %%.'
        % (100 * w[hoch & erw].sum() / w[hoch].sum(),
           100 * w[~hoch & erw].sum() / w[~hoch].sum()))
    sag('')

    # ---------------------------------------------------------------- 4
    sag('4. KATEGORIENUTZUNG (haeufigkeit, alle Befragten)')
    sag('-' * 78)
    LAB = {1: 'Täglich', 2: 'Mehrmals pro Woche', 3: 'Wöchentlich',
           4: 'Mehrmals pro Monat', 5: 'Monatlich', 6: 'Seltener', 7: 'Nie'}
    xa = np.array([num(r, 'haeufigkeit') for r in d])
    bek = np.array([r['neoh_bekannt'] == '1' for r in d], dtype=bool)
    betr = np.array([r['neoh_betracht'] == '1' for r in d], dtype=bool)
    kaufa = np.array([r['neoh_kauf'] == '1' for r in d], dtype=bool)
    sag('%-22s %6s %9s %10s %10s %10s' % ('', 'n', 'Anteil', 'kennt', 'erwägt', 'gekauft'))
    for s_ in range(1, 8):
        m = xa == s_
        if m.sum() < 5:
            continue
        sag('%-22s %6d %8.1f%% %9.1f%% %9.1f%% %9.1f%%'
            % (LAB[s_], int(m.sum()), 100 * wa[m].sum() / wa.sum(),
               100 * wa[m & bek].sum() / wa[m].sum(),
               100 * wa[m & betr].sum() / wa[m].sum(),
               100 * wa[m & kaufa].sum() / wa[m].sum()))
    sag('')
    viel = np.array([v <= 3 for v in xa], dtype=bool)
    sag('Wöchentlich oder häufiger (%.1f %% der Bevölkerung): Bekanntheit %.1f %%,'
        % (100 * wa[viel].sum() / wa.sum(), 100 * wa[viel & bek].sum() / wa[viel].sum()))
    sag('Kaufquote %.1f %%. Seltener als wöchentlich: %.1f %% und %.1f %%.'
        % (100 * wa[viel & kaufa].sum() / wa[viel].sum(),
           100 * wa[~viel & bek].sum() / wa[~viel].sum(),
           100 * wa[~viel & kaufa].sum() / wa[~viel].sum()))
    sag('')

    # ---------------------------------------------------------------- 5
    sag('5. DIE DREI TIMING-FRAGEN')
    sag('-' * 78)
    sag('Zeit bis zum Absenden der jeweiligen Seite, in Sekunden.')
    sag('')
    sag('%-16s %6s %8s %8s %8s %8s' % ('', 'n', 'P25', 'Median', 'P75', 'P95'))
    T = [('t_spontan_s', 'Spontannennung', d), ('t_raster_s', 'Markenraster', d),
         ('t_sentiment_s', 'Markensentiment', kenner)]
    for var, lab, basis_ in T:
        x = np.array([num(r, var) for r in basis_])
        x = x[~np.isnan(x)]
        sag('%-16s %6d %8.0f %8.0f %8.0f %8.0f'
            % (lab, len(x), np.percentile(x, 25), np.median(x),
               np.percentile(x, 75), np.percentile(x, 95)))
    sag('')
    sag('Das Markenraster ist mit Abstand die teuerste Seite - 21 Marken in drei')
    sag('Fragen. Es allein macht rund ein Drittel der gesamten Bearbeitungszeit aus.')
    sag('')
    sag('Hängt die Zeit am Markenraster mit der Zahl der Kreuze zusammen?')
    raster = np.array([num(r, 't_raster_s') for r in d])
    marken = sorted({k.split('_', 1)[1] for k in d[0] if k.startswith('bekanntheit_')},
                    key=lambda c: int(c))
    kreuze = np.array([sum(1 for c in marken if r['bekanntheit_%s' % c] == '1') for r in d])
    ok = ~np.isnan(raster)
    rho, p = stats.spearmanr(raster[ok], kreuze[ok])
    sag('   Rangkorrelation Zeit x Zahl der bekannten Marken: rho = %.3f, p = %.1e'
        % (rho, p))
    schnell = ok & (raster < np.percentile(raster[ok], 10))
    sag('   Die schnellsten 10 %% (unter %.0f s) kreuzen im Mittel %.1f Marken an,'
        % (np.percentile(raster[ok], 10), kreuze[schnell].mean()))
    sag('   alle übrigen %.1f.' % kreuze[ok & ~schnell].mean())
    sag('')
    sag('Ein positiver Zusammenhang spricht dafuer, dass die Zeit Verarbeitung')
    sag('misst und nicht blosses Zoegern: Wer mehr Marken kennt, braucht laenger.')
    sag('Das stuetzt die Verwendung der Gesamtdauer als Speeder-Kriterium.')
    sag('')

    sag('Geschrieben: %s' % AUS_TXT)
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
