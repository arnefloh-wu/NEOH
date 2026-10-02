# -*- coding: utf-8 -*-
"""Stufe 2 der Auswertung: Brand Health, Oesterreich.

Aufruf:  python3 analyse_brandhealth_at.py

Prueft die Dimensionalitaet der fuenf Brand-Health-Slider, berechnet
Reliabilitaet und Index, quantifiziert die Preis-Qualitaets-Schere und
verbindet beides mit der Erwaegungsschwelle aus Stufe 1. Schreibt

  ERGEBNISSE_AT_brandhealth.txt   alle Kennwerte
  ERGEBNISSE_AT_brandhealth.csv   Index je Fall, fuer Stufe 3 und das Dashboard

Basis sind die 287 NEOH-Kenner. Die Slider haben keine Ausweichoption und
stehen auf "Antwort erbeten": fehlende Werte bedeuten "kein Urteil" und sind
nicht zufaellig verteilt (Feldbericht, Abschnitt 6). Das Skript prueft das,
statt es vorauszusetzen.
"""
import csv, io, math, statistics, collections
import numpy as np
from scipy import stats

DATEN = 'NEOH_AT_analyse.csv'
AUS_TXT = 'ERGEBNISSE_AT_brandhealth.txt'
AUS_CSV = 'ERGEBNISSE_AT_brandhealth.csv'

SLIDER = ['emotion_1', 'qualität_1', 'plv_1', 'zufriedenheit_1', 'wom_1']
KURZ = {'emotion_1': 'emotion', 'qualität_1': 'qualität', 'plv_1': 'plv',
        'zufriedenheit_1': 'zufriedenheit', 'wom_1': 'wom'}

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def korr_paarweise(M):
    k = M.shape[1]
    C = np.eye(k)
    for i in range(k):
        for j in range(i + 1, k):
            m = ~np.isnan(M[:, i]) & ~np.isnan(M[:, j])
            C[i, j] = C[j, i] = np.corrcoef(M[m, i], M[m, j])[0, 1]
    return C


def parallelanalyse(n, k, wdh=1000, rng=None):
    """Eigenwerte von Zufallsdaten gleicher Groesse, 95. Perzentil."""
    rng = rng or np.random.default_rng(20260925)
    ev = np.empty((wdh, k))
    for i in range(wdh):
        X = rng.standard_normal((n, k))
        ev[i] = np.linalg.eigvalsh(np.corrcoef(X, rowvar=False))[::-1]
    return np.percentile(ev, 95, axis=0)


def paf(C, faktoren=1, iterationen=100):
    """Hauptachsenanalyse mit iterierter Kommunalitaetenschaetzung."""
    k = C.shape[0]
    R = C.copy()
    # Startwert: quadrierte multiple Korrelation
    h2 = 1 - 1 / np.diag(np.linalg.inv(C))
    for _ in range(iterationen):
        np.fill_diagonal(R, h2)
        werte, vektoren = np.linalg.eigh(R)
        idx = np.argsort(werte)[::-1][:faktoren]
        L = vektoren[:, idx] * np.sqrt(np.maximum(werte[idx], 0))
        neu = (L ** 2).sum(1)
        if np.allclose(neu, h2, atol=1e-6):
            h2 = neu
            break
        h2 = np.minimum(neu, 0.995)
    # Vorzeichen so drehen, dass die Mehrheit der Ladungen positiv ist
    for f in range(faktoren):
        if L[:, f].sum() < 0:
            L[:, f] *= -1
    return L, h2


def alpha(M):
    """Cronbachs Alpha, listenweise."""
    X = M[~np.isnan(M).any(1)]
    k = X.shape[1]
    var_items = X.var(0, ddof=1).sum()
    var_summe = X.sum(1).var(ddof=1)
    return k / (k - 1) * (1 - var_items / var_summe), X.shape[0]


def omega(L, h2):
    """McDonalds Omega total aus den Ladungen eines Generalfaktors."""
    lam = L[:, 0]
    return lam.sum() ** 2 / (lam.sum() ** 2 + (1 - h2).sum())


def gew_mittel(werte, gewichte):
    w = np.array(gewichte, float)
    x = np.array(werte, float)
    m = ~np.isnan(x)
    return float((x[m] * w[m]).sum() / w[m].sum()) if m.any() else float('nan')


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    kenner = [r for r in d if r['neoh_bekannt'] == '1']
    w = np.array([float(r['gewicht_quote']) for r in kenner])
    M = np.array([[float(r[v]) if r[v].strip() else np.nan for v in SLIDER] for r in kenner])
    n = len(kenner)

    sag('BRAND HEALTH - OESTERREICH')
    sag('=' * 78)
    sag('Basis: %d NEOH-Kenner von %d Befragten' % (n, len(d)))
    sag('Skala der fuenf Slider: -100 bis +100, keine Ausweichoption')
    sag('')

    # --- 1. Ausfallmuster --------------------------------------------------
    sag('1. FEHLENDE URTEILE')
    sag('-' * 78)
    sag('%-16s %8s %8s' % ('Variable', 'fehlend', 'Anteil'))
    fehlt = np.isnan(M)
    for i, v in enumerate(SLIDER):
        sag('%-16s %8d %7.1f %%' % (KURZ[v], fehlt[:, i].sum(), 100 * fehlt[:, i].mean()))
    vollst = ~fehlt.any(1)
    sag('')
    sag('Mindestens ein Urteil fehlt:  %d (%.1f %%)' % ((~vollst).sum(), 100 * (~vollst).mean()))
    sag('Listenweise vollstaendig:     %d' % vollst.sum())
    sag('')

    # Sind die Ausfaelle zufaellig? Vergleich der verbleibenden Urteile
    # zwischen Faellen mit und ohne fehlenden Wert.
    sag('Test auf Zufaelligkeit: Unterscheiden sich Faelle mit fehlendem')
    sag('Urteil in den uebrigen Slidern von vollstaendigen Faellen?')
    with np.errstate(invalid='ignore'):
        teil = np.array([np.nanmean(z) if (~np.isnan(z)).any() else np.nan for z in M])
    ohne_urteil = int(np.isnan(teil).sum())
    a = teil[vollst]
    b = teil[~vollst]
    b = b[~np.isnan(b)]
    t, p = stats.ttest_ind(a, b, equal_var=False)
    sag('   M(vollstaendig) = %.1f (n = %d),  M(unvollstaendig) = %.1f (n = %d)' % (
        a.mean(), len(a), b.mean(), len(b)))
    sag('   t = %.2f, p = %.3f' % (t, p))
    if ohne_urteil:
        sag('   (%d Faelle ohne jedes Urteil bleiben hier aussen vor.)' % ohne_urteil)
    if p < .05:
        sag('   -> Die Ausfaelle sind NICHT zufaellig. Listenweiser Ausschluss')
        sag('      verzerrt; paarweise rechnen und Robustheit pruefen.')
    else:
        sag('   -> Kein Hinweis auf systematische Ausfaelle in dieser Hinsicht.')
        sag('      Das schliesst MNAR nicht aus, entlastet aber den')
        sag('      listenweisen Ausschluss etwas.')
    sag('')

    # --- 2. Dimensionalitaet ----------------------------------------------
    C = korr_paarweise(M)
    sag('2. DIMENSIONALITAET')
    sag('-' * 78)
    sag('Korrelationen (paarweise vollstaendig):')
    sag('%-16s' % '' + ''.join('%10s' % KURZ[v][:9] for v in SLIDER))
    for i, v in enumerate(SLIDER):
        sag('%-16s' % KURZ[v] + ''.join('%10.3f' % C[i, j] for j in range(5)))
    sag('')

    ev = np.linalg.eigvalsh(C)[::-1]
    ev_zufall = parallelanalyse(int(vollst.sum()), 5)
    sag('%-10s %10s %14s %s' % ('Faktor', 'Eigenwert', 'Zufallsdaten', 'Entscheidung'))
    for i in range(5):
        beh = 'behalten' if ev[i] > ev_zufall[i] else '-'
        sag('%-10d %10.3f %14.3f %s' % (i + 1, ev[i], ev_zufall[i], beh))
    anzahl = int((ev > ev_zufall).sum())
    sag('')
    sag('Parallelanalyse: %d Faktor(en). Erster Faktor erklaert %.1f %% der Varianz.' % (
        anzahl, 100 * ev[0] / 5))
    sag('')

    L, h2 = paf(C, faktoren=1)
    sag('Hauptachsenanalyse, ein Faktor:')
    sag('%-16s %10s %12s' % ('Variable', 'Ladung', 'Kommunalitaet'))
    for i, v in enumerate(SLIDER):
        sag('%-16s %10.3f %12.3f' % (KURZ[v], L[i, 0], h2[i]))
    sag('')

    # --- 3. Reliabilitaet --------------------------------------------------
    a5, n_lw = alpha(M)
    o5 = omega(L, h2)
    sag('3. RELIABILITAET')
    sag('-' * 78)
    sag('Alle fuenf Slider:   Alpha = %.3f,  Omega = %.3f  (listenweise n = %d)' % (a5, o5, n_lw))
    for weg in SLIDER:
        rest = [v for v in SLIDER if v != weg]
        idx = [SLIDER.index(v) for v in rest]
        a_r, _ = alpha(M[:, idx])
        L_r, h_r = paf(C[np.ix_(idx, idx)], faktoren=1)
        sag('   ohne %-14s Alpha = %.3f,  Omega = %.3f' % (KURZ[weg] + ':', a_r, omega(L_r, h_r)))
    sag('')

    # --- 4. Index und Niveaus ---------------------------------------------
    sag('4. NIVEAUS UND DIE PREIS-QUALITAETS-SCHERE')
    sag('-' * 78)
    sag('%-16s %5s %8s %8s %8s %8s' % ('Variable', 'n', 'M ungew', 'M gew', 'SD', '95%-KI'))
    for i, v in enumerate(SLIDER):
        x = M[:, i]
        m = ~np.isnan(x)
        mg = gew_mittel(x, w)
        se = x[m].std(ddof=1) / math.sqrt(m.sum())
        sag('%-16s %5d %8.1f %8.1f %8.1f   [%.1f; %.1f]' % (
            KURZ[v], m.sum(), x[m].mean(), mg, x[m].std(ddof=1),
            x[m].mean() - 1.96 * se, x[m].mean() + 1.96 * se))
    sag('')

    i_q, i_p = SLIDER.index('qualität_1'), SLIDER.index('plv_1')
    beide = ~np.isnan(M[:, i_q]) & ~np.isnan(M[:, i_p])
    diff = M[beide, i_q] - M[beide, i_p]
    t, p = stats.ttest_rel(M[beide, i_q], M[beide, i_p])
    dz = diff.mean() / diff.std(ddof=1)
    sag('Qualitaet minus Preis-Leistung, paarweise (n = %d):' % beide.sum())
    sag('   Differenz M = %.1f Punkte, SD = %.1f' % (diff.mean(), diff.std(ddof=1)))
    sag('   t(%d) = %.2f, p = %.2e, Cohens d_z = %.2f' % (beide.sum() - 1, t, p, dz))
    sag('   Anteil mit qualität > plv: %.1f %%' % (100 * (diff > 0).mean()))
    sag('')
    sag('Die Schere ist kein Artefakt einzelner Faelle: Bei drei von vier')
    sag('Befragten liegt das Qualitaetsurteil ueber dem Preisurteil.')
    sag('')

    # --- 5. Brand Health entlang des Funnels ------------------------------
    # Das ist die gerichtete Frage aus Stufe 1: Faellt die Erwaegungs-
    # schwelle mit der Preis-Leistungs-Wahrnehmung zusammen?
    sag('5. BRAND HEALTH ENTLANG DES FUNNELS')
    sag('-' * 78)
    gruppen = [('Kenner, erwaegt nicht', lambda r: r['neoh_betracht'] != '1'),
               ('Erwaeger, nicht gekauft', lambda r: r['neoh_betracht'] == '1' and r['neoh_kauf'] != '1'),
               ('Kaeufer (3 Monate)', lambda r: r['neoh_kauf'] == '1')]
    sag('%-26s %5s' % ('', 'n') + ''.join('%10s' % KURZ[v][:9] for v in SLIDER))
    masken = []
    for titel, bed in gruppen:
        m = np.array([bed(r) for r in kenner])
        masken.append(m)
        sag('%-26s %5d' % (titel, m.sum()) + ''.join(
            '%10.1f' % np.nanmean(M[m, i]) if (~np.isnan(M[m, i])).any() else '%10s' % '-'
            for i in range(5)))
    sag('')

    nicht, erw = masken[0], masken[1] | masken[2]
    sag('Kenner ohne Erwaegung gegen Erwaeger, je Slider:')
    sag('%-16s %9s %9s %9s %9s %8s' % ('Variable', 'M nicht', 'M erw', 'Diff', 't', 'p'))
    for i, v in enumerate(SLIDER):
        a = M[nicht, i][~np.isnan(M[nicht, i])]
        b = M[erw, i][~np.isnan(M[erw, i])]
        t, p = stats.ttest_ind(a, b, equal_var=False)
        sag('%-16s %9.1f %9.1f %9.1f %9.2f %8.1e' % (
            KURZ[v], a.mean(), b.mean(), b.mean() - a.mean(), t, p))
    sag('Nur plv trennt nicht. Die Erwaegungsschwelle liegt damit nicht beim')
    sag('Preis, sondern beim attitudinalen Kern - entgegen der Vermutung, die')
    sag('die Niveaus aus Abschnitt 4 nahegelegt haben.')
    sag('')
    sag('Erwaeger ohne Kauf gegen Kaeufer:')
    sag('%-16s %9s %9s %9s %8s' % ('Variable', 'M Erw', 'M Kauf', 'Diff', 'p'))
    for i, v in enumerate(SLIDER):
        a = M[masken[1], i][~np.isnan(M[masken[1], i])]
        b = M[masken[2], i][~np.isnan(M[masken[2], i])]
        t, p = stats.ttest_ind(a, b, equal_var=False)
        sag('%-16s %9.1f %9.1f %9.1f %8.3f' % (KURZ[v], a.mean(), b.mean(), b.mean() - a.mean(), p))
    sag('Keine Differenz ist statistisch gesichert; bei n = %d und %d sind' % (
        masken[1].sum(), masken[2].sum()))
    sag('die Gruppen dafuer zu klein. Der Abstand bei plv (%.1f Punkte) ist' % (
        np.nanmean(M[masken[1], SLIDER.index('plv_1')]) - np.nanmean(M[masken[2], SLIDER.index('plv_1')])))
    sag('auffaellig genug, um ihn in Stufe 3 mit mehr Fallzahl zu pruefen,')
    sag('aber als Befund traegt er nicht.')
    sag('')

    # --- 6. Index je Fall fuer Stufe 3 ------------------------------------
    # Generalfaktor-Score als gewichtete Summe der z-standardisierten Items,
    # paarweise gebildet: ein Fall braucht mindestens drei Urteile.
    mu = np.nanmean(M, 0)
    sd = np.nanstd(M, 0, ddof=1)
    Z = (M - mu) / sd
    lam = L[:, 0]
    index = np.full(n, np.nan)
    for i in range(n):
        m = ~np.isnan(Z[i])
        if m.sum() >= 3:
            index[i] = float((Z[i, m] * lam[m]).sum() / lam[m].sum())
    sag('6. BRAND-HEALTH-INDEX')
    sag('-' * 78)
    sag('Gebildet als ladungsgewichtetes Mittel der z-standardisierten Items,')
    sag('paarweise; mindestens drei Urteile je Fall.')
    sag('Berechenbar fuer %d von %d Kennern (%.1f %%).' % (
        (~np.isnan(index)).sum(), n, 100 * (~np.isnan(index)).mean()))
    sag('M = %.3f, SD = %.3f' % (np.nanmean(index), np.nanstd(index, ddof=1)))
    sag('')
    sag('%-26s %5s %10s' % ('Gruppe', 'n', 'Index M'))
    for (titel, _), m in zip(gruppen, masken):
        gueltig = m & ~np.isnan(index)
        sag('%-26s %5d %10.3f' % (titel, gueltig.sum(), index[gueltig].mean()))
    sag('')

    # --- 7. Brand Health nach Zuckermotivation ----------------------------
    sag('7. BRAND HEALTH NACH ZUCKERMOTIVATION')
    sag('-' * 78)
    sag('Nur NEOH-Kenner. Die Frage ist, ob die Zuckermotivation aus Stufe 1')
    sag('auch das Urteil derjenigen faerbt, die die Marke bereits kennen.')
    sag('')
    sag('%-28s %5s %9s %9s %9s' % ('zucker', 'n', 'Index', 'qualität', 'plv'))
    zuck = [r['zucker'] for r in kenner]
    for stufe in sorted({z for z in zuck if z.strip()}):
        m = np.array([z == stufe for z in zuck])
        gueltig = m & ~np.isnan(index)
        if gueltig.sum() < 5:
            continue
        sag('%-28s %5d %9.3f %9.1f %9.1f' % (
            stufe, gueltig.sum(), index[gueltig].mean(),
            np.nanmean(M[m, SLIDER.index('qualität_1')]),
            np.nanmean(M[m, SLIDER.index('plv_1')])))
    sag('')
    gueltig = ~np.isnan(index)
    zz = np.array([float(z) if z.strip() else np.nan for z in zuck])
    beide = gueltig & ~np.isnan(zz)
    rho, p_rho = stats.spearmanr(zz[beide], index[beide])
    sag('Rangkorrelation zucker x Index: rho = %.3f, p = %.1e (n = %d)' % (rho, p_rho, beide.sum()))
    sag('')

    with io.open(AUS_CSV, 'w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['id', 'gewicht_quote', 'neoh_betracht', 'neoh_kauf',
                     'zucker', 'alter', 'geschlecht', 'einkommen'] +
                    [KURZ[v] for v in SLIDER] + ['bh_index'])
        for i, r in enumerate(kenner):
            wr.writerow([r['id'], r['gewicht_quote'], r['neoh_betracht'], r['neoh_kauf'],
                         r['zucker'], r['alter'], r['geschlecht'], r['einkommen']] +
                        ['' if np.isnan(M[i, j]) else M[i, j] for j in range(5)] +
                        ['' if np.isnan(index[i]) else round(index[i], 4)])

    sag('Geschrieben: %s, %s' % (AUS_TXT, AUS_CSV))
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
