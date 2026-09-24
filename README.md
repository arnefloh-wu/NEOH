# NEOH — Markenstudie Österreich / Deutschland, September 2026

Qualtrics-Fragebögen einer Zwei-Länder-Markenstudie zu NEOH im Schokoladen- und
Snackriegelmarkt. Erhebung von Markenbekanntheit, Brand-Health-Metriken nach
BrandIndex-Vorbild und Kaufverhalten.

Forschungsprojekt der WU Wien, Kontakt: Dr. Arne Floh, arne.floh@wu.ac.at

## Aktuelle Fassungen

Es gibt je Land **zwei Feldvarianten** desselben Instruments. Fragen, Export-Tags, Codes
und Logik sind identisch; sie unterscheiden sich nur darin, was mit Befragten geschieht,
die NEOH nicht kennen. Vor dem Feldstart ist eine davon zu wählen — die Varianten eines
Landes sind nicht poolbar.

**Variante Screener** — Nicht-Kenner werden terminiert:

| Land | Datei | `SurveyName` |
|---|---|---|
| Österreich | [`NEOH_AT_Sep2026_V7.qsf`](NEOH_AT_Sep2026_V7.qsf) | `NEOH_AT_Sep2026` |
| Deutschland | [`NEOH_DE_Sep2026.qsf`](NEOH_DE_Sep2026.qsf) | `NEOH_DE_Sep2026` |

**Variante Vollstichprobe** — ausgesteuert wird nur über Alter und Quoten, Nicht-Kenner
durchlaufen einen Kurzpfad und schliessen ab:

| Land | Datei | `SurveyName` |
|---|---|---|
| Österreich | [`NEOH_AT_Sep2026_Vollstichprobe.qsf`](NEOH_AT_Sep2026_Vollstichprobe.qsf) | `NEOH_AT_Sep2026_Vollstichprobe` |
| Deutschland | [`NEOH_DE_Sep2026_Vollstichprobe.qsf`](NEOH_DE_Sep2026_Vollstichprobe.qsf) | `NEOH_DE_Sep2026_Vollstichprobe` |

[`CODEBOOK_AT_DE.md`](CODEBOOK_AT_DE.md) hält die Markencodes beider Länder, das
ISCED-Mapping der Bildungsabschlüsse und die Konsistenzregeln für die
Datenaufbereitung fest. Ohne dieses Dokument sind die beiden Exporte nicht sinnvoll
zu stapeln.

Innerhalb einer Variante sind die beiden Länderfassungen strukturgleich: identische
Fragen, Export-Tags, Blockfolge, Logik und Randomisierung. Sie unterscheiden sich
ausschließlich in `einleitung`, `bundesland`, `bildung` und der Markenliste der drei
Raster. Die Länderzugehörigkeit steht in der Embedded-Data-Variable `land` (`AT` / `DE`).

## Versionshistorie

V1 bis V6 dokumentieren die Entwicklung des österreichischen Masters und sind **nicht**
für das Feld bestimmt. Insbesondere hat V6 vier Defekte, die in V7 behoben sind: die
erweiterte Randomisierung liegt dort auf Fragen im Papierkorb und ist im Live-Fragebogen
wirkungslos, die Display-Logik von `H1` verweist ebenfalls auf Papierkorb-Fragen und
kann nie erfüllt werden, drei der fünf Brand-Health-Slider haben keine
"Nicht zutreffend"-Option, und die Export-Tags `betracht` und `kauf_3monate` sind
doppelt vergeben.

| Datei | Stand |
|---|---|
| `NEOH_AT_Sep2026.qsf` | Ausgangsversion |
| `NEOH_AT_Sep2026_V2.qsf` … `_V6.qsf` | Zwischenstände |
| `NEOH_AT_Sep2026_V7.qsf` | **aktuell, feldreif** |
| `NEOH_DE_Sep2026.qsf` | **aktuell, feldreif** |

Die `.docx`-Dateien sind die Word-Exporte des jeweiligen Fragebogens aus Qualtrics.
Für V7 und die deutsche Fassung stehen sie noch aus und sind nach dem Import
nachzutragen.

## Nach dem Qualtrics-Import zu prüfen

Der Import legt jeweils eine neue Umfrage mit neuer `SurveyID` an; bestehende
Projekte bleiben unberührt. Je Fassung im Preview testen:

- Die Markenreihenfolge wechselt bei mehrfachem Aufruf, "KEINE Marke" bleibt unten.
- Alter 17 terminiert, Alter 19 läuft durch; `altersgruppe` kommt im Datensatz an
  (Alter 30 muss `30-39` ergeben).
- Variante Screener: ohne NEOH-Auswahl bei `bekanntheit` terminiert die Umfrage.
- Variante Vollstichprobe: ohne NEOH-Auswahl werden die sechs Markenmodule übersprungen
  und die Umfrage läuft bis zum Ende durch.
- NEOH bei `betracht` angekreuzt, bei `kauf_3monate` nicht → `H1` erscheint.

Dazu ein Testexport, der bestätigt, dass die Spaltensuffixe aus den Recode-Werten
gebildet werden (NEOH ist Exportcode **13**, nicht 14).

## Vor dem Feldstart offen

Außerhalb der QSF-Dateien zu erledigen:

- Panel-Redirects der DE-Fassung (AT ist gesetzt; Quotierung übernimmt der Anbieter,
  ein Quota-full-Link wird daher nicht benötigt)
- Einwilligungstext und Datenschutz-Link in `einleitung`, abzustimmen mit der
  WU-Datenschutzstelle
- Speeder- und Straightliner-Regeln für die Aufbereitung (der Attention-Check
  `attention` ist im Instrument, siehe Codebuch 3c)
- Soft-Launch zur Messung der Bearbeitungsdauer (siehe `SOFTLAUNCH_DE.md`)
- Feldzeitpunkte möglichst nah beieinander: der Süßwarenmarkt ist saisonal, ein
  großer Abstand konfundiert den Ländereffekt mit einem Saisoneffekt
