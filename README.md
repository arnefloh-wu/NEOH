# NEOH — Markenstudie Österreich / Deutschland, September 2026

Qualtrics-Fragebögen einer Zwei-Länder-Markenstudie zu NEOH im Schokoladen- und
Snackriegelmarkt. Erhebung von Markenbekanntheit, Brand-Health-Metriken nach
BrandIndex-Vorbild und Kaufverhalten.

Forschungsprojekt der WU Wien, Kontakt: Dr. Arne Floh, arne.floh@wu.ac.at

## Aktuelle Fassungen

| Land | Datei | `SurveyName` in Qualtrics |
|---|---|---|
| Österreich | [`NEOH_AT_Sep2026.qsf`](NEOH_AT_Sep2026.qsf) | `NEOH_AT_Sep2026` |
| Deutschland | [`NEOH_DE_Sep2026.qsf`](NEOH_DE_Sep2026.qsf) | `NEOH_DE_Sep2026` |

Diese beiden Dateien enthalten **keine** Panel-Weiterleitungen; die werden im
Qualtrics-UI gesetzt (siehe Codebuch, Panel-Anbindung).

Zusätzlich liegt [`NEOH_AT_Sep2026_Redirects.qsf`](NEOH_AT_Sep2026_Redirects.qsf) bereit —
inhaltlich identisch, aber mit den beiden österreichischen Weiterleitungen bereits im
Survey Flow. Die dafür nötige Struktur der End-of-Survey-Optionen liess sich nicht gegen
einen echten Qualtrics-Export prüfen; falls diese Datei importiert, spart sie die
Handarbeit, falls nicht, ist die Fassung ohne Redirects der verlässliche Weg.

Die zugehörigen `.docx` sind die Fragebogendokumentation, erzeugt aus den QSF-Dateien.

[`CODEBOOK_AT_DE.md`](CODEBOOK_AT_DE.md) hält die Markencodes beider Länder, das
ISCED-Mapping der Bildungsabschlüsse, die Altersbänder, die Panel-Anbindung und die
Konsistenzregeln für die Datenaufbereitung fest. Ohne dieses Dokument sind die beiden
Exporte nicht sinnvoll zu stapeln.

[`SOFTLAUNCH_DE.md`](SOFTLAUNCH_DE.md) beschreibt den Soft-Launch.

Die beiden Länderfassungen sind strukturgleich: identische Fragen, Export-Tags,
Blockfolge, Logik und Randomisierung. Sie unterscheiden sich ausschließlich in
`einleitung`, `bundesland`, `bildung` und der Markenliste der drei Raster. Die
Länderzugehörigkeit steht in der Embedded-Data-Variable `land` (`AT` / `DE`).

## Feldausrichtung

Ausgesteuert wird nur über Alter (ab 18) und die Quoten des Panelanbieters. Wer NEOH
nicht kennt, überspringt die sechs Markenmodule und schließt die Umfrage regulär ab —
die Incidence Rate liegt damit praktisch bei 100 %, und die Markenbekanntheit wird
bevölkerungsbezogen geschätzt statt aus einer Screen-out-Quote rekonstruiert.

Eine frühere Variante terminierte NEOH-Unkenner. Sie wurde verworfen, weil sie die vom
Panelanbieter vorausgesetzte Bedingung "IR mindestens 80 %" verletzt. Die
Entwicklungsstände V1 bis V7 sind aus dem Arbeitsverzeichnis entfernt und nur noch über
die Git-Historie erreichbar.

## Nach dem Qualtrics-Import zu prüfen

Der Import legt jeweils eine neue Umfrage mit neuer `SurveyID` an; bestehende
Projekte bleiben unberührt. Je Länderfassung im Preview testen:

- Die Markenreihenfolge wechselt bei mehrfachem Aufruf, "KEINE Marke" bleibt unten.
- Alter 17 terminiert, Alter 19 läuft durch; `altersgruppe` kommt im Datensatz an
  (Alter 30 muss `30-39` ergeben).
- Ohne NEOH-Auswahl bei `bekanntheit` werden die sechs Markenmodule übersprungen und die
  Umfrage läuft bis zum Ende durch.
- Alter 17 terminiert; nach dem Setzen der Redirects prüfen, dass dabei `ergebnis=31`
  aufgerufen wird und nicht `ergebnis=5`.
- NEOH bei `betracht` angekreuzt, bei `kauf_3monate` nicht → `H1` erscheint.

Dazu ein Testexport, der bestätigt, dass die Spaltensuffixe aus den Recode-Werten
gebildet werden (NEOH ist Exportcode **13**, nicht 14).

## Vor dem Feldstart offen

Außerhalb der QSF-Dateien zu erledigen:

- Panel-Redirects beider Fassungen im Qualtrics-UI setzen (siehe Codebuch,
  Panel-Anbindung). Quotierung übernimmt der Anbieter, ein Quota-full-Link wird
  nicht benötigt.
- Einwilligungstext und Datenschutz-Link in `einleitung`, abzustimmen mit der
  WU-Datenschutzstelle
- Speeder- und Straightliner-Regeln für die Aufbereitung (der Attention-Check
  `attention` ist im Instrument, siehe Codebuch 3c)
- Soft-Launch zur Messung der Bearbeitungsdauer (siehe `SOFTLAUNCH_DE.md`)
- Feldzeitpunkte möglichst nah beieinander: der Süßwarenmarkt ist saisonal, ein
  großer Abstand konfundiert den Ländereffekt mit einem Saisoneffekt
