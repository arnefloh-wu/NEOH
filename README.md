# NEOH — Markenstudie Österreich / Deutschland, September 2026

Qualtrics-Fragebögen einer Zwei-Länder-Markenstudie zu NEOH im Schokoladen- und
Snackriegelmarkt. Erhebung von Markenbekanntheit, Brand-Health-Metriken nach
BrandIndex-Vorbild und Kaufverhalten.

Forschungsprojekt der WU Wien, Kontakt: Dr. Arne Floh, arne.floh@wu.ac.at

## Aktuelle Fassungen

Für das Feld sind ausschließlich diese Dateien zu verwenden:

| Land | Datei | `SurveyName` in Qualtrics |
|---|---|---|
| Österreich | [`NEOH_AT_Sep2026_V7.qsf`](NEOH_AT_Sep2026_V7.qsf) | `NEOH_AT_Sep2026` |
| Deutschland | [`NEOH_DE_Sep2026.qsf`](NEOH_DE_Sep2026.qsf) | `NEOH_DE_Sep2026` |

[`CODEBOOK_AT_DE.md`](CODEBOOK_AT_DE.md) hält die Markencodes beider Länder, das
ISCED-Mapping der Bildungsabschlüsse und die Konsistenzregeln für die
Datenaufbereitung fest. Ohne dieses Dokument sind die beiden Exporte nicht sinnvoll
zu stapeln.

Die beiden Instrumente sind strukturgleich: identische Fragen, Export-Tags,
Blockfolge, Logik und Randomisierung. Sie unterscheiden sich ausschließlich in
`einleitung`, `bundesland`, `bildung` und der Markenliste der drei Raster. Die
Länderzugehörigkeit steht in der Embedded-Data-Variable `land` (`AT` / `DE`).

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
- Alter 15 terminiert, Alter 17 läuft durch.
- Ohne NEOH-Auswahl bei `bekanntheit` terminiert die Umfrage.
- NEOH bei `betracht` angekreuzt, bei `kauf_3monate` nicht → `H1` erscheint.

Dazu ein Testexport, der bestätigt, dass die Spaltensuffixe aus den Recode-Werten
gebildet werden (NEOH ist Exportcode **13**, nicht 14).

## Vor dem Feldstart offen

Außerhalb der QSF-Dateien zu erledigen:

- Panel-Redirects für Complete, Screen-out und Quota-full
- Einwilligungstext und Datenschutz-Link in `einleitung`, abzustimmen mit der
  WU-Datenschutzstelle
- Attention-Check sowie Speeder- und Straightliner-Regeln
- Quoten: Alter × Geschlecht interlocked, Region, Bildung — Altersuntergrenze 16
- Soft-Launch zur Incidence-Messung, besonders in Deutschland, wo die
  NEOH-Bekanntheit deutlich unter der österreichischen liegen dürfte
- Feldzeitpunkte möglichst nah beieinander: der Süßwarenmarkt ist saisonal, ein
  großer Abstand konfundiert den Ländereffekt mit einem Saisoneffekt
