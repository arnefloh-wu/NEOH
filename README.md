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

Beide Fassungen enthalten die Panel-Weiterleitungen (Complete `ergebnis=5`, Screen-out
`ergebnis=31`) bereits im QSF; die Links sind für Österreich und Deutschland identisch.
Die österreichische Fassung ist in dieser Form erfolgreich nach Qualtrics importiert und
die Rückleitung mit `?PID=%id%` geprüft worden (siehe Codebuch, Panel-Anbindung).

Die zugehörigen `.docx` sind die Fragebogendokumentation, erzeugt aus den QSF-Dateien.

[`CODEBOOK_AT_DE.md`](CODEBOOK_AT_DE.md) hält die Markencodes beider Länder, das
ISCED-Mapping der Bildungsabschlüsse, die Altersbänder, die Panel-Anbindung und die
Konsistenzregeln für die Datenaufbereitung fest. Ohne dieses Dokument sind die beiden
Exporte nicht sinnvoll zu stapeln.

[`SOFTLAUNCH_DE.md`](SOFTLAUNCH_DE.md) beschreibt den Soft-Launch.

## Auswertung

Das Feld Österreich lief vom 25. bis 30. September 2026 und lieferte 596
abgeschlossene Interviews.

```
python3 aufbereitung_at.py
```

Das Skript liest den Qualtrics-Rohexport, wendet die Ausschluss- und
Konsistenzregeln des Codebuchs an, rekodiert anhand der Choice-Labels aus
`NEOH_AT_Sep2026.qsf` und berechnet die Gewichte. Es schreibt
`NEOH_AT_analyse.csv` (567 Fälle, nicht versioniert, siehe `.gitignore`) und
`AUFBEREITUNG_AT_log.txt`.

Die Zielverteilungen der Gewichtung stehen in
[`gewichtung_ziele_AT.csv`](gewichtung_ziele_AT.csv). Die Spalte
`soll_bevoelkerung` ist **leer und von Hand zu füllen** — bis dahin gibt es
kein bevölkerungsbezogenes Gewicht, und das Skript sagt das im Protokoll.

```
python3 analyse_funnel_at.py
```

Stufe 1 der Auswertung: Funnel im Wettbewerbsvergleich. Schreibt
`ERGEBNISSE_AT_funnel.csv` (Tabelle je Marke) und `ERGEBNISSE_AT_funnel.txt`.
Die lesbare Fassung mit Einordnung steht in
[`ERGEBNISSE_AT_funnel.md`](ERGEBNISSE_AT_funnel.md).

```
python3 analyse_brandhealth_at.py
```

Stufe 2: Dimensionalität der fünf Brand-Health-Slider, Reliabilität, Index,
Preis-Qualitäts-Schere und Brand Health entlang des Funnels. Lesbare Fassung in
[`ERGEBNISSE_AT_brandhealth.md`](ERGEBNISSE_AT_brandhealth.md).

```
python3 analyse_treiber_at.py
```

Stufe 3: Treiber des Markenurteils, logistische Modelle fuer die beiden Tore
des Funnels, die genannten Kaufbarrieren und die Kontaktkanaele. Lesbare
Fassung in [`ERGEBNISSE_AT_treiber.md`](ERGEBNISSE_AT_treiber.md).

```
python3 analyse_segmente_text_at.py
```

Stufe 4: Schwelle oder Gradient bei `zucker`, ungestützte Bekanntheit und Top
of Mind aus den Spontannennungen, thematische Codierung der offenen
Beschreibungen. Lesbare Fassung in
[`ERGEBNISSE_AT_segmente_text.md`](ERGEBNISSE_AT_segmente_text.md).

```
python3 analyse_bekanntheit_at.py
```

Vertiefung zur gestützten und ungestützten Bekanntheit: Erinnerungsquote je
Marke, Share of Mind, Top of Mind und Nennposition, und ob Erinnerung die
Erwägung unabhängig vom Markenurteil erhöht. Lesbare Fassung in
[`ERGEBNISSE_AT_bekanntheit.md`](ERGEBNISSE_AT_bekanntheit.md).

```
python3 analyse_bekanntheit_demografie_at.py
```

Bekanntheit nach Alter, Geschlecht, Region (NUTS-1), Bundesland, Bildung und
Einkommen — bivariat mit Konfidenzintervallen, dann multivariat, weil Bildung
mit Alter und Einkommen mit Bildung korreliert. Dazu der Vergleich des
Altersgefälles über alle Marken. Lesbare Fassung in
[`ERGEBNISSE_AT_bekanntheit_demografie.md`](ERGEBNISSE_AT_bekanntheit_demografie.md).

```
python3 slides_at.py --pdf
```

Erzeugt `SLIDES_AT.html` und rendert daraus `SLIDES_AT.pdf` (20 Folien).
Logo, Produktbilder und Markenfarben sind optional und werden aus `assets/`
gelesen: Bilder als Dateien, Farben und Schrift als `assets/marke.json`. Ohne
diese Dateien rendert das Deck in der validierten Standardpalette. Siehe
[`assets/README.md`](assets/README.md).

```
python3 analyse_kanaele_at.py
python3 analyse_kanaele_detail_at.py --png
python3 analyse_weitere_at.py
```

Die Quelle der Bekanntheit (`kanal`) und die Variablen, die in den Stufen 1
bis 4 nur als Kovariaten vorkamen: `intention`, `empfehlung` als NPS,
`bedürfnis`, `bedeutsam`, `haeufigkeit` und die drei Timing-Fragen. Lesbare
Fassungen in [`ERGEBNISSE_AT_kanaele.md`](ERGEBNISSE_AT_kanaele.md) und
[`ERGEBNISSE_AT_weitere.md`](ERGEBNISSE_AT_weitere.md); die Tabelle am Ende
der zweiten Datei hält fest, welche Variable wo ausgewertet ist.
[`ERGEBNISSE_AT_kanaele_detail.md`](ERGEBNISSE_AT_kanaele_detail.md) geht auf
exklusive Reichweite, Reichweitenaufbau, Überlappung und Zielgruppenindex ein;
die Grafiken dazu liegen in `grafiken/` als SVG und PNG.

```
python3 dashboard_at.py
```

Erzeugt `DASHBOARD_AT.html`, ein eigenständiges interaktives Dashboard mit
Funnel, Markenbild und Wettbewerbsvergleich, filterbar nach Alter, Geschlecht
und Zuckersegment. Die Seite wird zweimal geschrieben: als `DASHBOARD_AT.html`
und als `docs/index.html` für GitHub Pages (siehe [`docs/README.md`](docs/README.md)).
Sie enthält **keine Falldaten**, sondern einen
vorberechneten Würfel aus 20 Zellen; die kleinste hat 12 Fälle. Die Region
ist bewusst keine Filterdimension — mit ihr hätte der Würfel Zellen mit einer
einzigen Person, und die Stichprobe trägt Regionalaussagen ohnehin nicht.

[`FELDBERICHT_AT.md`](FELDBERICHT_AT.md) hält Feldverlauf, Ausschüsse,
Quotenerfüllung, Gewichtung und Datenqualität fest. **Vor jeder Auswertung
lesen:** Der vereinbarte Quotenplan bildet die Altersstruktur der
Bevölkerung nicht ab, und die Rohdaten liegen derzeit in einem öffentlichen
Repository.

Die beiden Länderfassungen sind strukturgleich: identische Fragen, Export-Tags,
Blockfolge, Logik und Randomisierung. Sie unterscheiden sich ausschließlich in
`einleitung`, `bundesland`, `bildung` und der Markenliste der drei Raster. Das
deutsche Raster führt seit Oktober 2026 **24 Marken statt 20** — Twix, KitKat, Lindt
und Ritter Sport sind nach einem Befund aus den Spontannennungen ergänzt worden
(Codebuch, Abschnitt 1). Die
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

## Vor dem Import prüfen

Qualtrics lehnt fehlerhafte QSF-Dateien beim Import wortlos ab. Zwei Fehlversuche gingen
auf Reste zurück, die beim Umbauen von Fragen liegengeblieben waren — ein Objekt im
`QC`-Payload, wo `null` erwartet wird, und der Key `SearchSource` auf einer Frage, die von
Texteingabe auf Auswahl umgestellt wurde. Beides ist mit blossem Auge nicht zu sehen.

```
python3 qsf_pruefen.py NEOH_AT_Sep2026.qsf NEOH_DE_Sep2026.qsf
```

Das Skript vergleicht gegen [`referenz_import_ok.qsf`](referenz_import_ok.qsf), eine
Fassung, die nachweislich importiert hat: erlaubte Keys je Fragetyp, Payload-Typen der
Nicht-SQ-Elemente, Vollständigkeit der Block- und Flow-Verweise, Gültigkeit aller
Logik-Locatoren und Eindeutigkeit der Export-Tags. Nach jeder Änderung an einer QSF-Datei
laufen lassen.

## Nach dem Qualtrics-Import zu prüfen

Der Import legt jeweils eine neue Umfrage mit neuer `SurveyID` an; bestehende
Projekte bleiben unberührt. Je Länderfassung im Preview testen:

- Die Markenreihenfolge wechselt bei mehrfachem Aufruf, "KEINE Marke" bleibt unten.
- Die Alterskategorie kommt im Datensatz an (Codes 2 bis 6, Code 1 nie).
- Ohne NEOH-Auswahl bei `bekanntheit` werden die sechs Markenmodule übersprungen und die
  Umfrage läuft bis zum Ende durch.
- `alter` = "Unter 18 Jahre" terminiert und ruft `ergebnis=31` auf, nicht `ergebnis=5`.
- `attention` unter 90 terminiert und ruft `ergebnis=42` auf. Im Umfrageverlauf muss der
  Branch als "attention Is Less Than 90" lesbar sein, nicht als "Invalid Logic".
- NEOH bei `betracht` angekreuzt, bei `kauf_3monate` nicht → `H1` erscheint.

Dazu ein Testexport, der bestätigt, dass die Spaltensuffixe aus den Recode-Werten
gebildet werden (NEOH ist Exportcode **13**, nicht 14).

## Vor dem Feldstart offen

Außerhalb der QSF-Dateien zu erledigen:

- Rückleitung der DE-Fassung nach dem Import einmal mit `?PID=test123` prüfen, wie für
  Österreich geschehen. Quotierung übernimmt der Anbieter, ein Quota-full-Link wird
  nicht benötigt.
- Einwilligungstext und Datenschutz-Link in `einleitung`, abzustimmen mit der
  WU-Datenschutzstelle
- Mit dem Anbieter schriftlich klären, wie Quality Terminates (`ergebnis=42`, nicht
  bestandene Aufmerksamkeitsprüfung) abgerechnet und ob sie ersetzt werden
- Speeder- und Straightliner-Regeln für die Aufbereitung (der Attention-Check
  `attention` terminiert im Feld, siehe Codebuch 3c)
- Soft-Launch zur Messung der Bearbeitungsdauer (siehe `SOFTLAUNCH_DE.md`)
- Feldzeitpunkte möglichst nah beieinander: der Süßwarenmarkt ist saisonal, ein
  großer Abstand konfundiert den Ländereffekt mit einem Saisoneffekt
