# -*- coding: utf-8 -*-
"""Strukturpruefung einer QSF-Datei gegen eine als importierbar bekannte Referenz.

Aufruf:  python3 qsf_pruefen.py NEOH_AT_Sep2026.qsf NEOH_DE_Sep2026.qsf

Hintergrund: Qualtrics lehnt QSF-Dateien beim Import wortlos ab, wenn die
Struktur nicht stimmt. Zwei Fehlversuche gingen auf Reste zurueck, die beim
Umbauen von Fragen liegengeblieben sind - ein Objekt im QC-Payload, wo null
erwartet wird, und der Key SearchSource auf einer Frage, die von Texteingabe
auf Auswahl umgestellt wurde. Beides ist mit blossem Auge nicht zu sehen.

referenz_import_ok.qsf ist eine Fassung, die nachweislich importiert hat. Das
Skript vergleicht dagegen: erlaubte Keys je Fragetyp, Payload-Typen der
Nicht-SQ-Elemente, Vollstaendigkeit der Block- und Flow-Verweise, Gueltigkeit
aller Logik-Locatoren und Eindeutigkeit der Export-Tags.
"""
import json, re, sys

def lade(p):
    d = json.load(open(p, encoding='utf-8'))
    return d, {e['Payload']['QuestionID']: e['Payload'] for e in d['SurveyElements'] if e['Element'] == 'SQ'}

def pruefe(pfad, refpfad):
    d, Q = lade(pfad); rd, RQ = lade(refpfad)
    BL = [e['Payload'] for e in d['SurveyElements'] if e['Element'] == 'BL'][0]
    FL = [e['Payload'] for e in d['SurveyElements'] if e['Element'] == 'FL'][0]
    fehler, hinweise = [], []

    # 1) Keys je Fragetyp gegen die Referenz
    erlaubt = {}
    for p in RQ.values():
        erlaubt.setdefault((p['QuestionType'], p.get('Selector')), set()).update(p.keys())
    for qid, p in Q.items():
        k = (p['QuestionType'], p.get('Selector'))
        if k in erlaubt:
            fremd = set(p) - erlaubt[k]
            if fremd:
                fehler.append(f"{qid} ({p['DataExportTag']}, {k[0]}/{k[1]}): fremde Keys {sorted(fremd)}")
        else:
            hinweise.append(f"{qid} ({p['DataExportTag']}): Typ {k} kommt in der Referenz nicht vor")

    # 2) Nicht-SQ-Payload-Typen
    tref = {e['Element']: type(e['Payload']).__name__ for e in rd['SurveyElements'] if e['Element'] != 'SQ'}
    for e in d['SurveyElements']:
        if e['Element'] != 'SQ' and e['Element'] in tref:
            if type(e['Payload']).__name__ != tref[e['Element']]:
                fehler.append(f"{e['Element']}: Payload-Typ {type(e['Payload']).__name__}, Referenz {tref[e['Element']]}")

    # 3) Bloecke: existieren alle referenzierten Fragen?
    inblock = []
    for b in BL.values():
        for be in b['BlockElements']:
            if be['Type'] == 'Question':
                inblock.append(be['QuestionID'])
                if be['QuestionID'] not in Q:
                    fehler.append(f"Block '{b['Description']}' verweist auf fehlende Frage {be['QuestionID']}")
    verwaist = set(Q) - set(inblock)
    if verwaist: fehler.append(f"Fragen ohne Block: {sorted(verwaist)}")

    # 4) Flow: Block-IDs, FlowIDs, Logik-Locatoren
    blockids = {b['ID'] for b in BL.values()}
    fids = []
    def lauf(flow):
        for x in flow:
            fids.append(x.get('FlowID'))
            if x.get('ID') and x['ID'] not in blockids:
                fehler.append(f"Flow verweist auf unbekannten Block {x['ID']}")
            for lg in (x.get('BranchLogic') or {}).values():
                if not isinstance(lg, dict): continue
                for c in lg.values():
                    if isinstance(c, dict) and 'LeftOperand' in c:
                        loc = c['LeftOperand']
                        m = re.match(r'q://(QID\d+)/SelectableChoice/(\d+)', loc)
                        if m:
                            q, ch = m.groups()
                            if q not in Q: fehler.append(f"Logik verweist auf fehlende Frage {q}")
                            elif ch not in Q[q]['Choices']:
                                fehler.append(f"Logik verweist auf fehlende Antwort {q}/{ch}")
                        elif '/ChoiceTextEntryValue' in loc:
                            q = loc.split('/')[2]
                            if q not in Q or Q[q]['QuestionType'] != 'TE':
                                fehler.append(f"Logik nutzt Texteingabe-Locator auf {q}, das keine TE-Frage ist")
            if x.get('Flow'): lauf(x['Flow'])
    lauf(FL['Flow'])
    if len(fids) != len(set(fids)): fehler.append("doppelte FlowIDs")

    # 5) Display-Logik
    for qid, p in Q.items():
        for g in (p.get('DisplayLogic') or {}).values():
            if not isinstance(g, dict): continue
            for c in g.values():
                if isinstance(c, dict) and c.get('QuestionID'):
                    if c['QuestionID'] not in Q:
                        fehler.append(f"{qid}: Display-Logik verweist auf fehlende Frage {c['QuestionID']}")
    # 6) Tags
    tags = [p['DataExportTag'] for p in Q.values()]
    dopp = {t for t in tags if tags.count(t) > 1}
    if dopp: fehler.append(f"doppelte Export-Tags: {sorted(dopp)}")
    return fehler, hinweise

REFERENZ = 'referenz_import_ok.qsf'

for f in sys.argv[1:]:
    fe, hi = pruefe(f, REFERENZ)
    print('===', f)
    for x in fe: print('  FEHLER  ', x)
    for x in hi: print('  Hinweis ', x)
    if not fe: print('  keine Strukturfehler')
