# -*- coding: utf-8 -*-
"""Stufe 3 der Auswertung: Treiber und die beiden Tore des Funnels.

Aufruf:  python3 analyse_treiber_at.py

Stufe 1 hat den Engpass zwischen Bekanntheit und Betracht verortet, Stufe 2
hat gezeigt, dass dort nicht der Preis entscheidet. Dieses Skript trennt die
beiden Tore des Funnels und prueft, was an welchem wirkt:

  Tor 1  Bekanntheit -> Betracht   (Basis: Kenner)
  Tor 2  Betracht -> Kauf          (Basis: Erwaeger)

Schreibt ERGEBNISSE_AT_treiber.txt.

Zur Einordnung der Treiberrechnung: bedürfnis, bedeutsam und die
Brand-Health-Slider sind zeitgleich erhobene Einstellungsmasse. Was hier
berechnet wird, ist eine Varianzzerlegung, keine Kausalitaet. Relative
Gewichte nach Johnson (2000), weil die Praediktoren bis r = 0,79
interkorrelieren und rohe Regressionskoeffizienten dann nicht mehr sinnvoll
zu interpretieren sind.
"""
import csv, io, math, collections
import numpy as np
import statsmodels.api as sm
from scipy import stats

DATEN = 'NEOH_AT_analyse.csv'
AUS_TXT = 'ERGEBNISSE_AT_treiber.txt'

H1_LABEL = {1: 'Zu teuer', 2: 'Nicht im bevorzugten Geschaeft',
            3: 'Sehe ich nie im Regal', 4: 'Begrenzte Geschmacksauswahl',
            5: 'Packungsgroesse fehlt', 6: 'Nie im Angebot',
            7: 'Haushalt bevorzugt sie nicht', 8: 'Weiss nicht genug darueber',
            9: 'Sonstiges'}
KANAL_LABEL = {1: 'TV-Werbung', 2: 'Printwerbung', 3: 'Werbung auf Websites',
               4: 'Instagram/Facebook', 5: 'YouTube', 6: 'TikTok',
               7: 'Influencer', 8: 'Supermarkt (Regal, Display)',
               9: 'Mundpropaganda', 10: 'Aussenwerbung', 11: 'In keinem'}

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def num(r, v):
    return float(r[v]) if r[v].strip() else np.nan


def relative_gewichte(X, y, namen):
    """Johnsons relative Gewichte: Varianzanteil je Praediktor an R^2.

    Die Praediktoren werden symmetrisch orthogonalisiert (Z = X V D^0.5 V'),
    y auf die orthogonalen Z regressiert und die Beta-Quadrate ueber die
    quadrierten Transformationsgewichte auf die Originalvariablen
    zurueckverteilt. Das Verfahren bleibt auch bei starker Kollinearitaet
    interpretierbar, anders als rohe Betas.
    """
    X = (X - X.mean(0)) / X.std(0, ddof=1)
    y = (y - y.mean()) / y.std(ddof=1)
    R = np.corrcoef(X, rowvar=False)
    werte, V = np.linalg.eigh(R)
    werte = np.maximum(werte, 1e-10)
    L = V @ np.diag(np.sqrt(werte)) @ V.T       # X ~ Z L'
    Z = X @ np.linalg.inv(L).T
    beta = np.linalg.lstsq(Z, y, rcond=None)[0]
    eps = (L ** 2) @ (beta ** 2)
    r2 = float(np.corrcoef(X @ np.linalg.lstsq(X, y, rcond=None)[0], y)[0, 1] ** 2)
    return sorted(zip(namen, eps, 100 * eps / eps.sum()), key=lambda t: -t[1]), r2


def logit(X, y, namen):
    Xc = sm.add_constant(X, has_constant='add')
    m = sm.Logit(y, Xc).fit(disp=0)
    out = []
    for i, nm in enumerate(['(Konstante)'] + namen):
        out.append((nm, m.params[i], m.bse[i], m.pvalues[i], math.exp(m.params[i])))
    return out, m


def matrix(faelle, variablen):
    X = np.array([[num(r, v) for v in variablen] for r in faelle])
    ok = ~np.isnan(X).any(1)
    return X, ok


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    kenner = [r for r in d if r['neoh_bekannt'] == '1']
    # Hierarchisch wie in Stufe 1: Erwaegung und Kauf nur unter Kennern.
    erwaeger = [r for r in kenner if r['neoh_betracht'] == '1']

    sag('TREIBER UND DIE BEIDEN TORE DES FUNNELS - OESTERREICH')
    sag('=' * 78)
    sag('Kenner: %d   Erwaeger: %d   Kaeufer: %d' % (
        len(kenner), len(erwaeger), sum(1 for r in kenner if r['neoh_kauf'] == '1')))
    sag('')

    # --- 1. Was erzeugt das Markenurteil? ---------------------------------
    sag('1. WAS ERZEUGT DAS MARKENURTEIL')
    sag('-' * 78)
    sag('Abhaengig: Brand-Health-Index (Stufe 2, vier Items ohne wom).')
    sag('Varianzzerlegung, keine Kausalitaet - alle Masse sind zeitgleich erhoben.')
    sag('')

    # Index neu bilden, ohne wom, damit er zur Empfehlung aus Stufe 2 passt
    IDX = ['emotion_1', 'qualität_1', 'plv_1', 'zufriedenheit_1']
    Xi = np.array([[num(r, v) for v in IDX] for r in kenner])
    mu, sd = np.nanmean(Xi, 0), np.nanstd(Xi, 0, ddof=1)
    Zi = (Xi - mu) / sd
    lad = np.array([0.844, 0.866, 0.608, 0.831])   # Ladungen aus Stufe 2
    bh = np.array([float((z[~np.isnan(z)] * lad[~np.isnan(z)]).sum() /
                         lad[~np.isnan(z)].sum()) if (~np.isnan(z)).sum() >= 3 else np.nan
                   for z in Zi])

    praed = ['bedürfnis', 'bedeutsam', 'zucker', 'haeufigkeit', 'einkommen', 'alter']
    Xp, ok_p = matrix(kenner, praed)
    ok = ok_p & ~np.isnan(bh)
    gew, r2 = relative_gewichte(Xp[ok], bh[ok], praed)
    sag('n = %d, R2 = %.3f' % (ok.sum(), r2))
    sag('%-16s %10s %10s   %s' % ('Praediktor', 'rel. Gew.', 'Anteil', 'r mit Index'))
    for nm, e, pct in gew:
        j = praed.index(nm)
        r = np.corrcoef(Xp[ok, j], bh[ok])[0, 1]
        sag('%-16s %10.4f %9.1f %%   %+.3f' % (nm, e, pct, r))
    sag('')
    sag('bedürfnis ("Inwieweit erfuellt NEOH Ihre Beduerfnisse?") dominiert.')
    sag('Das ist weniger trivial, als es klingt: Es ist ein Passungsurteil,')
    sag('kein Qualitaetsurteil. Die Marke wird gut bewertet, wenn sie zum')
    sag('eigenen Bedarf passt - nicht, wenn sie objektiv gut gefunden wird.')
    sag('')

    # --- 2. Tor 1: Bekanntheit -> Betracht --------------------------------
    sag('2. TOR 1 - WER ERWAEGT NEOH (Basis: Kenner)')
    sag('-' * 78)
    y = np.array([1.0 if r['neoh_betracht'] == '1' else 0.0 for r in kenner])
    for titel, variablen, extra in [
            ('Modell A: Markenurteil und Kontext', ['zucker', 'haeufigkeit', 'einkommen', 'alter'], True),
            ('Modell B: nur die Slider', ['plv_1', 'qualität_1', 'emotion_1', 'zufriedenheit_1'], False)]:
        X, ok_x = matrix(kenner, variablen)
        if extra:
            X = np.column_stack([bh, X])
            namen = ['bh_index'] + variablen
            ok_x = ok_x & ~np.isnan(bh)
        else:
            namen = variablen
        erg, m = logit(X[ok_x], y[ok_x], namen)
        sag('%s   (n = %d, Pseudo-R2 = %.3f)' % (titel, ok_x.sum(), m.prsquared))
        sag('%-16s %9s %8s %9s %9s' % ('', 'b', 'SE', 'p', 'Odds'))
        for nm, b, se, p, odds in erg:
            stern = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else ''
            sag('%-16s %9.3f %8.3f %9.4f %9.3f %s' % (nm, b, se, p, odds, stern))
        sag('')
    sag('Zum negativen plv-Koeffizienten in Modell B: Bivariat haengt plv mit')
    sag('der Erwaegung praktisch nicht zusammen (Stufe 2: +11,4 Punkte,')
    sag('p = 0,079). Erst unter Kontrolle der drei anderen Slider dreht das')
    sag('Vorzeichen ins Negative. Das ist das Muster einer Suppression und')
    sag('bei Interkorrelationen bis r = 0,79 nicht ueberraschend. Inhaltlich')
    sag('darf daraus NICHT gelesen werden, dass ein besseres Preisurteil die')
    sag('Erwaegung senkt. Der belastbare Befund bleibt: plv traegt zu Tor 1')
    sag('nichts bei, waehrend zufriedenheit und qualitaet es tragen.')
    sag('')
    sag('Ebenfalls bemerkenswert in Modell A: zucker verliert seine Wirkung,')
    sag('sobald der Markenindex im Modell steht (p = 0,107). Zusammen mit der')
    sag('Rangkorrelation aus Stufe 2 (rho = 0,270) ist das das Muster einer')
    sag('Mediation - die Zuckermotivation wirkt ueber das Markenurteil, nicht')
    sag('daneben. Ein formaler Mediationstest waere der naechste Schritt.')
    sag('')

    # --- 3. Tor 2: Betracht -> Kauf ---------------------------------------
    sag('3. TOR 2 - WER KAUFT (Basis: Erwaeger)')
    sag('-' * 78)
    yk = np.array([1.0 if r['neoh_kauf'] == '1' else 0.0 for r in erwaeger])
    X, ok_x = matrix(erwaeger, ['plv_1', 'einkommen', 'haeufigkeit'])
    sag('n = %d, davon Kaeufer %d. Das ist fuer ein Modell knapp;' % (ok_x.sum(), int(yk[ok_x].sum())))
    sag('die Schaetzung steht hier als Hinweis, nicht als Befund.')
    erg, m = logit(X[ok_x], yk[ok_x], ['plv_1', 'einkommen', 'haeufigkeit'])
    sag('%-16s %9s %8s %9s %9s' % ('', 'b', 'SE', 'p', 'Odds'))
    for nm, b, se, p, odds in erg:
        stern = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else ''
        sag('%-16s %9.3f %8.3f %9.4f %9.3f %s' % (nm, b, se, p, odds, stern))
    sag('')

    # --- 4. Die genannten Barrieren ---------------------------------------
    sag('4. WAS ERWAEGER VOM KAUF ABHAELT (H1, Selbstauskunft)')
    sag('-' * 78)
    h1 = [r for r in kenner if r['H1_1'] != '']
    sag('Gestellt an Erwaeger ohne Kauf in den letzten drei Monaten: n = %d' % len(h1))
    sag('Mehrfachnennung moeglich.')
    sag('')
    zaehl = [(H1_LABEL[i], sum(1 for r in h1 if r['H1_%d' % i] == '1')) for i in range(1, 10)]
    for lab, c in sorted(zaehl, key=lambda t: -t[1]):
        balken = '#' * int(round(30 * c / len(h1))) if h1 else ''
        sag('   %-32s %2d  %5.1f %%  %s' % (lab, c, 100 * c / len(h1), balken))
    sag('')
    sag('Der Preis ist hier mit Abstand die haeufigste Nennung - und das steht')
    sag('NICHT im Widerspruch zu Stufe 2. Dort ging es um Tor 1, hier um Tor 2.')
    sag('Preis entscheidet nicht, ob NEOH auf die Liste kommt, sondern ob es')
    sag('vom Regal in den Korb wandert.')
    sag('')
    sag('Zur Vorsicht: n = %d. Die Rangfolge der ersten beiden Nennungen ist' % len(h1))
    sag('deutlich, alles darunter liegt im Bereich weniger Faelle.')
    sag('')

    # --- 5. plv und die Selbstauskunft ------------------------------------
    sag('5. PASST DAS PREISURTEIL ZUR GENANNTEN PREISBARRIERE?')
    sag('-' * 78)
    teuer = np.array([r['H1_1'] == '1' for r in h1])
    plv = np.array([num(r, 'plv_1') for r in h1])
    a, b = plv[teuer & ~np.isnan(plv)], plv[~teuer & ~np.isnan(plv)]
    if len(a) > 2 and len(b) > 2:
        t, p = stats.ttest_ind(a, b, equal_var=False)
        sag('plv bei "zu teuer" genannt:      M = %6.1f  (n = %d)' % (a.mean(), len(a)))
        sag('plv bei "zu teuer" nicht genannt: M = %6.1f  (n = %d)' % (b.mean(), len(b)))
        sag('t = %.2f, p = %.3f' % (t, p))
    sag('')
    sag('Die beiden Masse zeigen in dieselbe Richtung: Wer den Preis als')
    sag('Barriere nennt, bewertet auch das Preis-Leistungs-Verhaeltnis')
    sag('schlechter, und zwar um knapp 30 Skalenpunkte. Das spricht fuer die')
    sag('konvergente Validitaet des Sliders. Mit p = 0.054 und n = 33 ist der')
    sag('Unterschied allerdings nur knapp an der Konvention - als Beleg taugt')
    sag('er, als gesicherter Befund nicht.')
    sag('')

    # --- 6. Die juengste Altersgruppe -------------------------------------
    sag('6. DIE JUENGSTE ALTERSGRUPPE (Stufe 1: hoechste Bekanntheit, niedrigster Kauf)')
    sag('-' * 78)
    sag('%-22s %5s %9s %9s %9s %9s' % ('Altersgruppe', 'n', 'plv', 'bh_index', 'einkommen', 'haeufigk.'))
    for a_code in ['2', '3', '4', '5', '6']:
        m = np.array([r['alter'] == a_code for r in kenner])
        if m.sum() < 5:
            continue
        txt = [r['alter_txt'] for r in kenner if r['alter'] == a_code][0]
        pl = np.array([num(r, 'plv_1') for r in kenner])[m]
        ein = np.array([num(r, 'einkommen') for r in kenner])[m]
        hf = np.array([num(r, 'haeufigkeit') for r in kenner])[m]
        sag('%-22s %5d %9.1f %9.3f %9.2f %9.2f' % (
            txt, m.sum(), np.nanmean(pl), np.nanmean(bh[m]), np.nanmean(ein), np.nanmean(hf)))
    sag('')
    jung = np.array([r['alter'] == '2' for r in kenner])
    rest = np.array([r['alter'] in ('3', '4', '5') for r in kenner])
    for v, arr in [('plv', np.array([num(r, 'plv_1') for r in kenner])),
                   ('bh_index', bh),
                   ('einkommen', np.array([num(r, 'einkommen') for r in kenner]))]:
        a, b = arr[jung], arr[rest]
        a, b = a[~np.isnan(a)], b[~np.isnan(b)]
        t, p = stats.ttest_ind(a, b, equal_var=False)
        sag('18-29 gegen 30-59, %-10s M = %6.1f gegen %6.1f,  t = %5.2f, p = %.3f' % (
            v, a.mean(), b.mean(), t, p))
    sag('')
    sag('Keiner der drei Kandidaten erklaert das Muster. Die juengste Gruppe')
    sag('bewertet NEOH nicht schlechter, haelt es nicht fuer teurer und hat')
    sag('kein geringeres Einkommen. Der Befund aus Stufe 1 bleibt damit')
    sag('offen - was er ausschliesst, ist eine Preis- oder Budgeterklaerung.')
    sag('')

    # --- 7. Kanaele, deskriptiv -------------------------------------------
    sag('7. KONTAKTKANAELE (nur Kenner, letzter Monat, deskriptiv)')
    sag('-' * 78)
    sag('Endogen: nur Kenner wurden gefragt. Keine Werbewirkungsaussage.')
    sag('')
    for i in sorted(range(1, 12), key=lambda i: -sum(1 for r in kenner if r['kanal_%d' % i] == '1')):
        c = sum(1 for r in kenner if r['kanal_%d' % i] == '1')
        sag('   %-28s %3d  %5.1f %%' % (KANAL_LABEL[i], c, 100 * c / len(kenner)))
    sag('')
    kein = np.array([r['kanal_11'] == '1' for r in kenner])
    sag('Wer in keinem Kanal Kontakt hatte (n = %d), erwaegt zu %.1f %%;' % (
        kein.sum(), 100 * np.mean([r['neoh_betracht'] == '1' for r, k in zip(kenner, kein) if k])))
    sag('wer mindestens einen Kontakt hatte (n = %d), zu %.1f %%.' % (
        (~kein).sum(), 100 * np.mean([r['neoh_betracht'] == '1' for r, k in zip(kenner, kein) if not k])))
    sag('Das ist ein Zusammenhang, keine Wirkung: Wer die Marke erwaegt,')
    sag('nimmt sie auch eher wahr.')
    sag('')

    sag('Geschrieben: %s' % AUS_TXT)
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
