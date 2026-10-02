# -*- coding: utf-8 -*-
"""Stufe 1 der Auswertung: Funnel im Wettbewerbsvergleich, Oesterreich.

Aufruf:  python3 analyse_funnel_at.py

Liest NEOH_AT_analyse.csv (erzeugt von aufbereitung_at.py) und berechnet je
Marke die drei Funnel-Stufen und die Uebergangsraten dazwischen. Schreibt

  ERGEBNISSE_AT_funnel.csv   Tabelle je Marke, fuer Slides und Dashboard
  ERGEBNISSE_AT_funnel.txt   lesbare Fassung mit allen Kennwerten

Gewichtung: gewicht_quote (Nachschichtung Alter x Geschlecht auf den
Quotenplan). Konfidenzintervalle nach Wilson auf dem effektiven n nach Kish,
nicht auf der rohen Fallzahl - sonst waeren sie bei gewichteten Anteilen zu
eng. Solange gewicht_bev leer ist, sind alle Anteile NICHT
bevoelkerungsrepraesentativ; siehe FELDBERICHT_AT.md, Abschnitt 5.

Die Funnel-Stufen werden hierarchisch gebildet: Betracht und Kauf zaehlen nur
unter den Kennern der jeweiligen Marke. Im Rohdatensatz gibt es dazu wenige
Abweichungen (Feldbericht, Abschnitt 6); sie werden hier bereinigt und
ausgewiesen.
"""
import csv, io, json, math, statistics, collections

DATEN = 'NEOH_AT_analyse.csv'
QSF = 'NEOH_AT_Sep2026.qsf'
AUS_CSV = 'ERGEBNISSE_AT_funnel.csv'
AUS_TXT = 'ERGEBNISSE_AT_funnel.txt'
NEOH = '13'
KEINE = '99'

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def markennamen(pfad):
    d = json.load(io.open(pfad, encoding='utf-8'))
    for e in d['SurveyElements']:
        p = e.get('Payload', {})
        if e['Element'] == 'SQ' and p.get('DataExportTag') == 'bekanntheit':
            rc = p.get('RecodeValues') or {}
            return {str(rc.get(k, k)): v['Display'] for k, v in p['Choices'].items()}
    raise SystemExit('bekanntheit nicht gefunden')


def wilson(p, n, z=1.96):
    """Wilson-Intervall fuer einen Anteil p bei (effektiver) Fallzahl n."""
    if n <= 0:
        return (0.0, 0.0)
    nenner = 1 + z * z / n
    mitte = (p + z * z / (2 * n)) / nenner
    halb = z * math.sqrt(max(0.0, p * (1 - p) / n + z * z / (4 * n * n))) / nenner
    return (max(0.0, mitte - halb), min(1.0, mitte + halb))


def anteil(faelle, gew, treffer):
    """Gewichteter Anteil mit Wilson-Intervall auf dem effektiven n."""
    basis = sum(gew)
    if basis <= 0:
        return 0.0, 0, 0.0, (0.0, 0.0)
    p = sum(g for f, g in zip(faelle, gew) if treffer(f)) / basis
    n_eff = basis ** 2 / sum(g * g for g in gew)
    roh = sum(1 for f in faelle if treffer(f))
    return p, roh, n_eff, wilson(p, n_eff)


def main():
    namen = markennamen(QSF)
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    w = [float(r['gewicht_quote']) for r in d]
    n = len(d)
    n_eff = sum(w) ** 2 / sum(g * g for g in w)
    marken = sorted((c for c in namen if c != KEINE), key=lambda c: int(c))

    sag('FUNNEL IM WETTBEWERBSVERGLEICH - OESTERREICH')
    sag('=' * 78)
    sag('Datenbasis: %s, n = %d, effektives n = %.0f' % (DATEN, n, n_eff))
    sag('Gewicht:    gewicht_quote (Alter x Geschlecht auf den Quotenplan)')
    sag('ACHTUNG:    nicht bevoelkerungsgewichtet, siehe FELDBERICHT_AT.md 5')
    sag('')

    # Hierarchische Bereinigung: Betracht/Kauf nur unter Kennern.
    # Vorher die unbereinigten NEOH-Werte festhalten, damit der Einfluss
    # der Entscheidung sichtbar bleibt statt stillschweigend einzugehen.
    roh_neoh = {s: anteil(d, w, lambda r, s=s: r[s] == '1')[0]
                for s in ('neoh_bekannt', 'neoh_betracht', 'neoh_kauf')}
    korrekturen = collections.Counter()
    zellen = 0
    for r in d:
        for c in marken:
            zellen += 1
            if r['bekanntheit_%s' % c] != '1':
                for stufe in ('betracht', 'kauf_3monate'):
                    if r['%s_%s' % (stufe, c)] == '1':
                        korrekturen[stufe] += 1
                        r['%s_%s' % (stufe, c)] = '0'
                        if c == NEOH:
                            r['neoh_betracht' if stufe == 'betracht' else 'neoh_kauf'] = '0'
    sag('Hierarchische Bereinigung (Angabe ohne gestuetzte Bekanntheit):')
    for stufe in ('betracht', 'kauf_3monate'):
        sag('   %-14s %4d von %d Marke-Person-Zellen auf 0 gesetzt (%.1f %%)' % (
            stufe + ':', korrekturen[stufe], zellen, 100 * korrekturen[stufe] / zellen))
    sag('   Einfluss auf NEOH:  Betracht %.1f %% -> %.1f %%,  Kauf %.1f %% -> %.1f %%' % (
        100 * roh_neoh['neoh_betracht'], 100 * anteil(d, w, lambda r: r['neoh_betracht'] == '1')[0],
        100 * roh_neoh['neoh_kauf'], 100 * anteil(d, w, lambda r: r['neoh_kauf'] == '1')[0]))
    sag('')

    zeilen_csv = []
    for c in marken:
        bek = anteil(d, w, lambda r, c=c: r['bekanntheit_%s' % c] == '1')
        bet = anteil(d, w, lambda r, c=c: r['betracht_%s' % c] == '1')
        kauf = anteil(d, w, lambda r, c=c: r['kauf_3monate_%s' % c] == '1')
        # Uebergaenge in der jeweiligen Teilstichprobe
        kenner = [r for r in d if r['bekanntheit_%s' % c] == '1']
        kenner_w = [g for r, g in zip(d, w) if r['bekanntheit_%s' % c] == '1']
        erwaeger = [r for r in d if r['betracht_%s' % c] == '1']
        erwaeger_w = [g for r, g in zip(d, w) if r['betracht_%s' % c] == '1']
        u1 = anteil(kenner, kenner_w, lambda r, c=c: r['betracht_%s' % c] == '1') if kenner else (0, 0, 0, (0, 0))
        u2 = anteil(erwaeger, erwaeger_w, lambda r, c=c: r['kauf_3monate_%s' % c] == '1') if erwaeger else (0, 0, 0, (0, 0))
        zeilen_csv.append({
            'code': c, 'marke': namen[c],
            'bekanntheit': round(100 * bek[0], 1), 'bekanntheit_n': bek[1],
            'bekanntheit_ku': round(100 * bek[3][0], 1), 'bekanntheit_ko': round(100 * bek[3][1], 1),
            'betracht': round(100 * bet[0], 1), 'betracht_n': bet[1],
            'kauf': round(100 * kauf[0], 1), 'kauf_n': kauf[1],
            'konv_bek_bet': round(100 * u1[0], 1), 'konv_bet_kauf': round(100 * u2[0], 1),
            'konv_bek_kauf': round(100 * kauf[0] / bek[0], 1) if bek[0] > 0 else 0.0,
        })

    zeilen_csv.sort(key=lambda z: -z['bekanntheit'])
    with io.open(AUS_CSV, 'w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(zeilen_csv[0].keys()))
        wr.writeheader()
        wr.writerows(zeilen_csv)

    sag('1. FUNNEL JE MARKE  (gewichtete Anteile der Gesamtstichprobe, %)')
    sag('-' * 78)
    sag('%-22s %8s %8s %8s   %7s %7s' % ('Marke', 'bekannt', 'Betracht', 'Kauf', 'B->Betr', 'Betr->K'))
    for z in zeilen_csv:
        mark = ' <<<' if z['code'] == NEOH else ''
        sag('%-22s %7.1f%% %7.1f%% %7.1f%%   %6.1f%% %6.1f%%%s' % (
            z['marke'][:22], z['bekanntheit'], z['betracht'], z['kauf'],
            z['konv_bek_bet'], z['konv_bet_kauf'], mark))
    sag('')

    keine = anteil(d, w, lambda r: r['bekanntheit_%s' % KEINE] == '1')
    sag('"KEINE Marke" bei bekanntheit: %.1f %% (n = %d)' % (100 * keine[0], keine[1]))
    sag('')

    # --- NEOH im Vergleich ------------------------------------------------
    nz = [z for z in zeilen_csv if z['code'] == NEOH][0]
    rang = zeilen_csv.index(nz) + 1
    sag('2. NEOH IM VERGLEICH')
    sag('-' * 78)
    sag('Bekanntheit:  %.1f %% [%.1f; %.1f]  - Rang %d von %d Marken' % (
        nz['bekanntheit'], nz['bekanntheit_ku'], nz['bekanntheit_ko'], rang, len(zeilen_csv)))
    sag('Betracht:     %.1f %%   Kauf: %.1f %%' % (nz['betracht'], nz['kauf']))
    sag('')
    for feld, titel in [('konv_bek_bet', 'Bekanntheit -> Betracht'),
                        ('konv_bet_kauf', 'Betracht -> Kauf'),
                        ('konv_bek_kauf', 'Bekanntheit -> Kauf')]:
        vergleich = [z for z in zeilen_csv if z['bekanntheit_n'] >= 30]
        werte = sorted((z[feld] for z in vergleich), reverse=True)
        med = statistics.median(werte)
        rang_f = werte.index(nz[feld]) + 1
        sag('%-26s NEOH %5.1f %%   Median %5.1f %%   Rang %d von %d' % (
            titel + ':', nz[feld], med, rang_f, len(werte)))
    sag('')
    sag('(Vergleichsbasis: Marken mit mindestens 30 Kennern, damit die')
    sag(' Uebergangsraten nicht auf Einzelfaellen beruhen.)')
    sag('')

    # --- Funnel nach Untergruppen ----------------------------------------
    sag('3. NEOH-FUNNEL NACH UNTERGRUPPEN')
    sag('-' * 78)
    for var, titel in [('alter_txt', 'Alter'), ('geschlecht_txt', 'Geschlecht'),
                       ('zucker', 'Zuckerreduktion wichtig (1 = gar nicht, 5 = sehr)')]:
        sag(titel + ':')
        sag('   %-24s %5s %9s %9s %9s' % ('', 'n', 'bekannt', 'Betracht', 'Kauf'))
        for stufe in sorted({r[var] for r in d if r[var].strip()}):
            teil = [r for r in d if r[var] == stufe]
            teil_w = [g for r, g in zip(d, w) if r[var] == stufe]
            b = anteil(teil, teil_w, lambda r: r['neoh_bekannt'] == '1')
            t = anteil(teil, teil_w, lambda r: r['neoh_betracht'] == '1')
            k = anteil(teil, teil_w, lambda r: r['neoh_kauf'] == '1')
            sag('   %-24s %5d %8.1f%% %8.1f%% %8.1f%%' % (
                stufe[:24], len(teil), 100 * b[0], 100 * t[0], 100 * k[0]))
        sag('')

    # --- Was haengt am Altersgewicht? -------------------------------------
    # Die Bekanntheit faellt steil mit dem Alter, und der Quotenplan setzt die
    # Gruppe 60+ auf 16 Prozent. Die Rechnung zeigt, wie stark der Kopfwert am
    # Anteil der Aeltesten haengt - die Szenarien sind KEINE amtlichen Werte,
    # sondern Spannweiten, bis gewicht_bev vorliegt (FELDBERICHT_AT.md 5).
    sag('4. EMPFINDLICHKEIT GEGEN DEN ALTERSANTEIL')
    sag('-' * 78)
    baender = ['18 bis 29 Jahre', '30 bis 39 Jahre', '40 bis 49 Jahre',
               '50 bis 59 Jahre', '60 Jahre und älter']
    plan = [0.24, 0.20, 0.20, 0.20, 0.16]
    quoten = {}
    for b in baender:
        teil = [r for r in d if r['alter_txt'] == b]
        teil_w = [g for r, g in zip(d, w) if r['alter_txt'] == b]
        quoten[b] = {s: anteil(teil, teil_w, lambda r, s=s: r[s] == '1')[0]
                     for s in ('neoh_bekannt', 'neoh_betracht', 'neoh_kauf')}
    sag('%-28s %9s %9s %9s' % ('Anteil 60+ in der Grundgesamtheit', 'bekannt', 'Betracht', 'Kauf'))
    for anteil_60 in (0.16, 0.25, 0.33):
        rest = [p / sum(plan[:4]) * (1 - anteil_60) for p in plan[:4]] + [anteil_60]
        werte = {s: sum(p * quoten[b][s] for b, p in zip(baender, rest))
                 for s in ('neoh_bekannt', 'neoh_betracht', 'neoh_kauf')}
        kennz = ' (Quotenplan)' if anteil_60 == 0.16 else ''
        sag('%-28s %8.1f%% %8.1f%% %8.1f%%%s' % (
            '%.0f %%' % (100 * anteil_60), 100 * werte['neoh_bekannt'],
            100 * werte['neoh_betracht'], 100 * werte['neoh_kauf'], kennz))
    sag('')
    sag('Die Szenarien sind Rechengroessen, keine amtlichen Anteile. Sie zeigen,')
    sag('dass die berichtete Bekanntheit mit dem Altersanteil um mehrere')
    sag('Prozentpunkte wandert - der Kopfwert ist ohne gewicht_bev nicht final.')
    sag('')

    sag('Geschrieben: %s, %s' % (AUS_CSV, AUS_TXT))
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')


if __name__ == '__main__':
    main()
