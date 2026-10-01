# -*- coding: utf-8 -*-
"""Aufbereitung des oesterreichischen Rohdatensatzes zum analysefertigen Datensatz.

Aufruf:  python3 aufbereitung_at.py [rohdaten.csv]

Liest den Qualtrics-Export (drei Kopfzeilen), wendet die im Codebuch
festgelegten Ausschluss- und Konsistenzregeln an, rekodiert nach den
Choice-Labels der QSF-Datei und berechnet Gewichte. Erzeugt werden

  NEOH_AT_analyse.csv        analysefertiger Datensatz, ohne Panel-ID
  AUFBEREITUNG_AT_log.txt    Protokoll aller Schritte mit Fallzahlen

Die Labels werden aus NEOH_AT_Sep2026.qsf gelesen, nicht im Skript gepflegt.
Damit koennen Fragebogen und Aufbereitung nicht auseinanderlaufen.

Gewichtung: siehe GEWICHTUNG weiter unten. Es gibt zwei Gewichte, eines
gegen den vereinbarten Quotenplan und eines gegen die Bevoelkerung. Das
zweite bleibt leer, solange keine amtlichen Randverteilungen hinterlegt sind.
"""
import csv, io, json, math, sys, collections, statistics

ROHDATEN = 'NEOH_AT_Sep2026_October+1,+2026_10.56.csv'
QSF = 'NEOH_AT_Sep2026.qsf'
ZIELE = 'gewichtung_ziele_AT.csv'
AUS_CSV = 'NEOH_AT_analyse.csv'
AUS_LOG = 'AUFBEREITUNG_AT_log.txt'

# --- Ausschlusskriterien -------------------------------------------------
ATTENTION_MIN = 90      # Codebuch 3c: darunter gilt die Pruefung als nicht bestanden
SPEEDER_ANTEIL = 1/3    # Bearbeitungszeit unter diesem Anteil des Medians
ALTER_SCREENOUT = '1'   # "Unter 18 Jahre" - haette terminieren muessen
RECAPTCHA_MIN = 0.5     # Qualtrics-Botscore, darunter nur markiert

# Straightliner werden markiert, aber nicht ausgeschlossen: Die fuenf Slider
# messen verwandte Konstrukte, identische Werte koennen ein echtes Urteil sein.
# Die Variable straightliner erlaubt die Sensitivitaetsrechnung im Report.
SLIDER = ['emotion_1', 'qualität_1', 'plv_1', 'zufriedenheit_1', 'wom_1']

NEOH = '13'             # Exportcode von NEOH in allen drei Markenrastern
KEINE = '99'            # "KEINE Marke", exklusiv gesetzt
RASTER = ['bekanntheit', 'betracht', 'kauf_3monate']

protokoll = []
def sag(zeile=''):
    protokoll.append(zeile)
    print(zeile)


def labels_aus_qsf(pfad):
    """Choice-Labels je Exporttag, Schluessel sind die Recode-Werte."""
    d = json.load(io.open(pfad, encoding='utf-8'))
    out = {}
    for e in d['SurveyElements']:
        if e['Element'] != 'SQ':
            continue
        p = e['Payload']
        ch, rc = p.get('Choices') or {}, p.get('RecodeValues') or {}
        if ch:
            out[p.get('DataExportTag')] = {str(rc.get(k, k)): v['Display'] for k, v in ch.items()}
    return out


def lies_roh(pfad):
    """Qualtrics-Export: Zeile 1 Variablennamen, Zeile 2 Fragetext, Zeile 3 ImportId."""
    rows = list(csv.reader(io.open(pfad, encoding='utf-8-sig')))
    kopf = rows[0]
    return kopf, [dict(zip(kopf, r)) for r in rows[3:]]


def zahl(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def wilson(k, n, z=1.96):
    """Konfidenzintervall fuer einen Anteil, robust auch bei kleinen Zellen."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    nenner = 1 + z * z / n
    mitte = (p + z * z / (2 * n)) / nenner
    halb = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / nenner
    return (max(0.0, mitte - halb), min(1.0, mitte + halb))


# --- GEWICHTUNG ----------------------------------------------------------
# Nachschichtung auf die Zellen alter x geschlecht. Beide Zielspalten stehen
# in gewichtung_ziele_AT.csv:
#
#   soll_quotenplan  die mit dem Panelanbieter vereinbarte Sollverteilung
#                    (je 250 Frauen und Maenner, Kategorien 2 bis 6)
#   soll_bevoelkerung  amtliche Randverteilung, von Hand einzutragen
#
# Das Quotengewicht korrigiert die Abweichung des Feldes vom vereinbarten
# Plan. Es korrigiert NICHT die Abweichung des Plans von der Bevoelkerung -
# dafuer ist die zweite Spalte da. Siehe FELDBERICHT_AT.md, Abschnitt 5.

def nachschichtung(faelle, ziel, schluessel):
    """Gewicht = Sollanteil / Istanteil je Zelle, normiert auf Mittelwert 1."""
    ist = collections.Counter(schluessel(f) for f in faelle)
    n = len(faelle)
    summe_ziel = sum(ziel.values())
    w = {}
    for zelle, soll in ziel.items():
        if ist.get(zelle, 0) == 0:
            continue
        w[zelle] = (soll / summe_ziel) / (ist[zelle] / n)
    gew = [w.get(schluessel(f)) for f in faelle]
    vorhanden = [g for g in gew if g is not None]
    if not vorhanden:
        return gew, {}
    mittel = sum(vorhanden) / len(vorhanden)
    gew = [None if g is None else g / mittel for g in gew]
    vorhanden = [g for g in gew if g is not None]
    cv2 = statistics.pvariance(vorhanden) / (sum(vorhanden) / len(vorhanden)) ** 2
    deff = 1 + cv2
    return gew, {'min': min(vorhanden), 'max': max(vorhanden), 'deff': deff,
                 'n_eff': len(vorhanden) / deff, 'n_gewichtet': len(vorhanden)}


def lies_ziele(pfad):
    """Zielverteilungen je Zelle. Leere Felder bedeuten: Ziel nicht hinterlegt."""
    quote, bev = {}, {}
    for r in csv.DictReader(io.open(pfad, encoding='utf-8-sig')):
        zelle = (r['alter'], r['geschlecht'])
        if r['soll_quotenplan'].strip():
            quote[zelle] = float(r['soll_quotenplan'])
        if r['soll_bevoelkerung'].strip():
            bev[zelle] = float(r['soll_bevoelkerung'])
    return quote, bev


def main():
    pfad = sys.argv[1] if len(sys.argv) > 1 else ROHDATEN
    lab = labels_aus_qsf(QSF)
    kopf, roh = lies_roh(pfad)
    n_roh = len(roh)

    sag('AUFBEREITUNG NEOH OESTERREICH')
    sag('=' * 68)
    sag('Rohdatei:  %s' % pfad)
    sag('Fragebogen: %s' % QSF)
    sag('')
    sag('1. ROHDATENSATZ')
    sag('-' * 68)
    sag('Datensaetze im Export:            %4d' % n_roh)
    for v in ['Status', 'Finished', 'Progress']:
        z = collections.Counter(r[v] for r in roh)
        sag('%-33s %s' % (v + ':', dict(z)))
    sag('Panel-ID (PID) vorhanden:         %4d' % sum(1 for r in roh if r['PID'].strip()))
    doppelt = [k for k, v in collections.Counter(r['PID'] for r in roh).items() if v > 1 and k.strip()]
    sag('Doppelte Panel-IDs:               %4d' % len(doppelt))
    sag('')

    # --- 2. Ausschluesse ---------------------------------------------------
    dauer = sorted(z for z in (zahl(r['Duration (in seconds)']) for r in roh) if z is not None)
    median_dauer = statistics.median(dauer)
    schwelle = median_dauer * SPEEDER_ANTEIL

    for r in roh:
        a = zahl(r['attention_1'])
        d = zahl(r['Duration (in seconds)'])
        r['_unter18'] = r['alter'] == ALTER_SCREENOUT
        r['_attention'] = a is not None and a < ATTENTION_MIN
        r['_speeder'] = d is not None and d < schwelle
        werte = [r[v] for v in SLIDER]
        r['_straightliner'] = all(w.strip() for w in werte) and len(set(werte)) == 1
        r['_raus'] = r['_unter18'] or r['_attention'] or r['_speeder']

    sag('2. AUSSCHLUSSKRITERIEN')
    sag('-' * 68)
    sag('Median Bearbeitungszeit:          %4.0f s  (%.1f Min)' % (median_dauer, median_dauer / 60))
    sag('Speeder-Schwelle (1/3 des Medians): %3.0f s' % schwelle)
    sag('')
    for schluessel, text in [('_unter18', 'Alter "Unter 18 Jahre"'),
                             ('_attention', 'Aufmerksamkeitspruefung < %d' % ATTENTION_MIN),
                             ('_speeder', 'Speeder (< %.0f s)' % schwelle)]:
        k = sum(1 for r in roh if r[schluessel])
        sag('%-33s %4d   %5.1f %%' % (text + ':', k, 100 * k / n_roh))
    ueber = sum(1 for r in roh if sum([r['_unter18'], r['_attention'], r['_speeder']]) > 1)
    sag('%-33s %4d' % ('davon mehrfach auffaellig:', ueber))
    raus = sum(1 for r in roh if r['_raus'])
    sag('%-33s %4d   %5.1f %%' % ('AUSGESCHLOSSEN gesamt:', raus, 100 * raus / n_roh))
    sag('')
    sag('Nur markiert, nicht ausgeschlossen - die Entscheidung darueber gehoert')
    sag('in den Analyseplan, nicht in die Aufbereitung:')
    sl = sum(1 for r in roh if r['_straightliner'])
    sag('%-33s %4d   %5.1f %%' % ('Straightliner ueber 5 Slider:', sl, 100 * sl / n_roh))
    rc = sum(1 for r in roh
             if zahl(r['Q_RecaptchaScore']) is not None
             and zahl(r['Q_RecaptchaScore']) < RECAPTCHA_MIN)
    sag('%-33s %4d   %5.1f %%' % ('reCAPTCHA-Score < %.1f:' % RECAPTCHA_MIN, rc, 100 * rc / n_roh))
    pb = sum(1 for r in roh if r['Q_PrivateBrowserDetected'].strip())
    sag('%-33s %4d   %5.1f %%' % ('Privates Browserfenster:', pb, 100 * pb / n_roh))
    sag('')

    netto = [r for r in roh if not r['_raus']]
    n = len(netto)
    sag('NETTOSTICHPROBE:                  %4d' % n)
    sag('')

    # --- 3. Konsistenzpruefungen (Codebuch Abschnitt 5) --------------------
    sag('3. KONSISTENZPRUEFUNGEN')
    sag('-' * 68)
    kauf_ohne_bek = sum(1 for r in netto
                        if r['kauf_3monate_%s' % NEOH].strip() and not r['bekanntheit_%s' % NEOH].strip())
    sag('%-45s %4d' % ('Kauf NEOH ohne gestuetzte Bekanntheit:', kauf_ohne_bek))
    for g in RASTER:
        verletzt = sum(1 for r in netto if r['%s_%s' % (g, KEINE)].strip()
                       and any(r['%s_%s' % (g, c)].strip() for c in lab['bekanntheit'] if c != KEINE))
        sag('%-45s %4d' % ('"KEINE Marke" nicht exklusiv in %s:' % g, verletzt))
    ohne_angabe = sum(1 for r in netto if not any(r['bekanntheit_%s' % c].strip() for c in lab['bekanntheit']))
    sag('%-45s %4d' % ('Keine einzige Angabe bei bekanntheit:', ohne_angabe))
    kenner = [r for r in netto if r['bekanntheit_%s' % NEOH].strip()]
    sag('Fehlende Werte der Slider (ohne Ausweichoption, nur NEOH-Kenner):')
    for v in SLIDER:
        k = sum(1 for r in kenner if not r[v].strip())
        sag('   %-20s %4d fehlend von %d = %4.1f %%' % (v, k, len(kenner), 100 * k / len(kenner)))
    sag('')

    # --- 4. Gewichtung -----------------------------------------------------
    ziel_quote, ziel_bev = lies_ziele(ZIELE)
    zelle = lambda r: (r['alter'], r['geschlecht'])
    w_quote, kenn_quote = nachschichtung(netto, ziel_quote, zelle)
    w_bev, kenn_bev = ([None] * n, {}) if not ziel_bev else nachschichtung(netto, ziel_bev, zelle)

    sag('4. GEWICHTUNG')
    sag('-' * 68)
    sag('Zellen:  alter (5 Kategorien) x geschlecht, Nachschichtung')
    sag('')
    sag('%-14s %6s %6s %8s %8s %8s' % ('Zelle', 'Soll', 'Ist', 'Soll-%', 'Ist-%', 'Gewicht'))
    summe_soll = sum(ziel_quote.values())
    ist = collections.Counter(zelle(r) for r in netto)
    for z in sorted(ziel_quote, key=lambda x: (x[0], x[1])):
        g = [w for w, r in zip(w_quote, netto) if zelle(r) == z]
        sag('%-14s %6.0f %6d %7.1f%% %7.1f%% %8.3f' % (
            '%s/%s' % (lab['alter'][z[0]][:8], lab['geschlecht'][z[1]][:1]),
            ziel_quote[z], ist.get(z, 0),
            100 * ziel_quote[z] / summe_soll, 100 * ist.get(z, 0) / n,
            g[0] if g else float('nan')))
    sag('')
    if kenn_quote:
        sag('Gewichtsspanne:   %.3f bis %.3f' % (kenn_quote['min'], kenn_quote['max']))
        sag('Designeffekt:     %.3f' % kenn_quote['deff'])
        sag('Effektives n:     %.0f  (von %d)' % (kenn_quote['n_eff'], n))
    if not ziel_bev:
        sag('')
        sag('Bevoelkerungsgewicht: NICHT BERECHNET.')
        sag('In %s ist die Spalte soll_bevoelkerung leer.' % ZIELE)
        sag('Bis amtliche Randverteilungen eingetragen sind, ist jede')
        sag('bevoelkerungsbezogene Aussage unzulaessig.')
    sag('')

    # --- 5. Rekodierung und Ausgabe ---------------------------------------
    marken = sorted(lab['bekanntheit'], key=lambda c: int(c))
    felder = (['id', 'dauer_s', 'gewicht_quote', 'gewicht_bev', 'straightliner', 'recaptcha', 'privatbrowser',
               'alter', 'alter_txt', 'geschlecht', 'geschlecht_txt', 'bundesland', 'bundesland_txt',
               'bildung', 'bildung_txt', 'einkommen', 'einkommen_txt', 'haeufigkeit', 'haeufigkeit_txt',
               'attention', 'zucker']
              + ['%s_%s' % (g, c) for g in RASTER for c in marken]
              + ['neoh_bekannt', 'neoh_betracht', 'neoh_kauf']
              + SLIDER + ['bedürfnis', 'bedeutsam', 'intention', 'empfehlung']
              + ['kanal_%d' % i for i in range(1, 12)]
              + ['spontan', 'beschreibung']
              + ['t_spontan_s', 't_raster_s', 't_sentiment_s'])

    with io.open(AUS_CSV, 'w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=felder)
        wr.writeheader()
        for i, (r, wq, wb) in enumerate(zip(netto, w_quote, w_bev), start=1):
            o = {'id': 'AT%04d' % i,
                 'dauer_s': r['Duration (in seconds)'],
                 'gewicht_quote': '' if wq is None else round(wq, 6),
                 'gewicht_bev': '' if wb is None else round(wb, 6),
                 'straightliner': int(r['_straightliner']),
                 'recaptcha': r['Q_RecaptchaScore'],
                 'privatbrowser': int(bool(r['Q_PrivateBrowserDetected'].strip())),
                 'attention': r['attention_1'], 'zucker': r['zucker']}
            for v in ['alter', 'geschlecht', 'bundesland', 'bildung', 'einkommen', 'haeufigkeit']:
                o[v] = r[v]
                o[v + '_txt'] = lab[v].get(r[v], '')
            for g in RASTER:
                for c in marken:
                    o['%s_%s' % (g, c)] = 1 if r['%s_%s' % (g, c)].strip() else 0
            o['neoh_bekannt'] = o['bekanntheit_%s' % NEOH]
            o['neoh_betracht'] = o['betracht_%s' % NEOH]
            o['neoh_kauf'] = o['kauf_3monate_%s' % NEOH]
            for v in SLIDER + ['bedürfnis', 'bedeutsam', 'intention', 'empfehlung']:
                o[v] = r[v]
            for k in range(1, 12):
                o['kanal_%d' % k] = 1 if r['kanal_%d' % k].strip() else 0
            o['spontan'] = r['spontan'].replace('\n', ' ').strip()
            o['beschreibung'] = r['beschreibung'].replace('\n', ' ').strip()
            for t in ['t_spontan', 't_raster', 't_sentiment']:
                o[t + '_s'] = r['%s_Page Submit' % t]
            wr.writerow(o)

    # --- 6. Eckwerte fuer den Feldbericht ---------------------------------
    sag('5. ECKWERTE DER NETTOSTICHPROBE')
    sag('-' * 68)
    for stufe, spalte in [('bekannt', 'bekanntheit'), ('in Betracht', 'betracht'), ('gekauft (3 Mon.)', 'kauf_3monate')]:
        k = sum(1 for r in netto if r['%s_%s' % (spalte, NEOH)].strip())
        u, o = wilson(k, n)
        sag('NEOH %-18s %4d von %d = %5.1f %%   [%.1f; %.1f]' % (
            stufe + ':', k, n, 100 * k / n, 100 * u, 100 * o))
    sag('')
    sag('Slider (nur Faelle mit Urteil, ungewichtet):')
    for v in SLIDER:
        x = [zahl(r[v]) for r in netto if r[v].strip()]
        sag('   %-16s n=%3d  M=%6.1f  SD=%5.1f' % (v, len(x), statistics.mean(x), statistics.pstdev(x)))
    sag('')
    sag('Offene Angaben:')
    for v in ['spontan', 'beschreibung']:
        t = [r[v].strip() for r in netto if r[v].strip()]
        sag('   %-16s %4d Texte, Median %d Zeichen' % (v, len(t), statistics.median([len(x) for x in t])))
    sag('')
    sag('Geschrieben: %s (%d Faelle, %d Variablen)' % (AUS_CSV, n, len(felder)))
    sag('Die Panel-ID ist nicht enthalten; id ist eine studieninterne Laufnummer.')

    io.open(AUS_LOG, 'w', encoding='utf-8').write('\n'.join(protokoll) + '\n')


if __name__ == '__main__':
    main()
