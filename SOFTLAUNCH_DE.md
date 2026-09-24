# Soft-Launch-Plan Deutschland

> **Stand nach dem Angebot des Panelanbieters.** Die ursprüngliche Hauptaufgabe dieses
> Plans — die Incidence Rate messen, um die Bruttostichprobe zu dimensionieren — ist
> entfallen. Der Anbieter setzt eine IR von mindestens 80 % voraus, und die
> Feldausrichtung erreicht praktisch 100 %, weil nur nach Alter und Quote
> ausgesteuert wird. Die Fallzahlen stehen fest (AT 500, DE 1.000), die Quotierung
> übernimmt der Anbieter.
>
> Damit bleibt als Zweck: die **Bearbeitungsdauer** prüfen, weil das Angebot mit 10
> Minuten kalkuliert, sowie der technische Durchlauf von Weiterleitungen und Logik. Dafür
> genügen 50 bis 100 Fälle statt der unten hergeleiteten 300. Die Abschnitte 1 und 2
> dokumentieren die ursprüngliche Herleitung und sind nur noch historisch relevant;
> Abschnitt 4 (Messplan) und die Timing-Elemente (`CODEBOOK_AT_DE.md`, Abschnitt 3e)
> gelten unverändert.


Instrument: `NEOH_DE_Sep2026.qsf`. Ziel des Soft-Launch ist, die drei Grössen zu messen,
die das Budget und die Machbarkeit der Hauptwelle bestimmen, bevor die Stichprobe
beauftragt wird — und das Instrument unter Feldbedingungen zu prüfen.

Der kritische Parameter ist die **Incidence Rate (IR)**: der Anteil der Befragten, die
NEOH bei `bekanntheit` angeben und damit den Screener passieren. NEOH ist eine
österreichische Marke, in Deutschland bundesweit bei REWE und Müller gelistet, nicht bei
dm und Rossmann. Die IR ist dort mit hoher Wahrscheinlichkeit deutlich niedriger als in
Österreich, und niemand weiss, wie viel niedriger.

## 1. Warum die IR das ganze Budget trägt

Alle Kernblöcke (Medien, Markengesundheit, Markenwahrnehmung, Bedürfnisse, Markteffekte,
Markensentiment) liegen hinter dem Bekanntheitsscreener. Die benötigten Bruttostarts
skalieren mit `1/IR`:

| IR | Brutto für n=250 | Brutto für n=400 | Brutto für n=500 |
|---:|---:|---:|---:|
| 5 % | 5.556 | 8.889 | 11.112 |
| 8 % | 3.473 | 5.556 | 6.945 |
| 10 % | 2.778 | 4.445 | 5.556 |
| 15 % | 1.852 | 2.963 | 3.704 |
| 20 % | 1.389 | 2.223 | 2.778 |
| 30 % | 926 | 1.482 | 1.852 |
| 40 % | 695 | 1.112 | 1.389 |

Annahme: 90 % Abschlussquote unter den Qualifizierten. n bezieht sich auf NEOH-kennende
Vollinterviews.

Zwischen 5 % und 20 % IR liegt ein Faktor vier im Brutto. Eine Beauftragung ohne
IR-Messung ist deshalb keine Schätzung, sondern ein Ratespiel.

## 2. Stichprobengrösse des Soft-Launch

Die Präzision der IR-Schätzung bestimmt, wie eng das Budget geplant werden kann.
95-%-Konfidenzintervalle für die IR, nach Zahl der **gescreenten** Personen:

| gescreent | bei IR ≈ 10 % | bei IR ≈ 15 % | bei IR ≈ 25 % |
|---:|:---:|:---:|:---:|
| 100 | ± 5,9 pp | ± 7,0 pp | ± 8,5 pp |
| 200 | ± 4,2 pp | ± 4,9 pp | ± 6,0 pp |
| **300** | **± 3,4 pp** | **± 4,0 pp** | **± 4,9 pp** |
| 500 | ± 2,6 pp | ± 3,1 pp | ± 3,8 pp |

Bei n = 100 und einer beobachteten IR von 15 % reicht das Intervall von 8 % bis 22 % —
die Bruttoplanung für n = 400 schwankt damit zwischen rund 2.000 und 5.600 Starts, also
um den Faktor 2,8. Bei n = 300 schrumpft die Spanne auf etwa Faktor 1,7.

**Empfehlung: 300 gescreente Personen.** Screen-outs sind bei den meisten Anbietern
deutlich günstiger als Vollinterviews, die Mehrkosten gegenüber n = 100 sind gering und
sparen bei der Hauptwelle ein Vielfaches.

Darin enthalten sind je nach IR etwa 30 bis 60 Vollinterviews — genug, um Abbrüche,
Bearbeitungsdauer und Datenqualität zu beurteilen, zu wenig für belastbare
Markenkennzahlen. Das ist beabsichtigt.

## 3. Konfiguration des Soft-Launch

- **Quoten aktiv, auf Soft-Launch-Niveau skaliert.** Nicht nur um den Mechanismus zu
  testen, sondern weil die IR mit hoher Wahrscheinlichkeit stark nach Alter variiert.
  Ohne Quoten liefert das Panel die leicht erreichbaren Zellen und die IR ist nach oben
  oder unten verzerrt.
- **Alle Weiterleitungen scharf.** Complete, Screen-out (beide Pfade) und Quota-full. Der
  Soft-Launch ist der einzige Test, den diese Links vor dem Echtbetrieb bekommen; der
  Qualtrics-Preview durchläuft sie nicht.
- **Feldphase markieren.** Ein Embedded-Data-Feld `feldphase`, über den Query String des
  Einstiegslinks gesetzt (`soft` bzw. `main`), erlaubt das spätere Zusammenführen oder
  Trennen ohne Eingriff in den Fragebogen.
- **Instrument einfrieren.** Wenn nach dem Soft-Launch am Fragebogen etwas geändert wird,
  sind die Soft-Launch-Fälle nicht mehr mit der Hauptwelle poolbar. Deshalb: Soft-Launch
  nur starten, wenn der Fragebogen als final gilt. Änderungen danach bedeuten, die
  Soft-Launch-Fälle zu verwerfen — das ist der Preis, und er ist einkalkuliert.
- **Aufbereitungsskript vorher fertig.** Die 24–48-Stunden-Auswertung funktioniert nur,
  wenn das Skript beim Eintreffen der Daten läuft. Grundlage: `CODEBOOK_AT_DE.md`.

## 4. Was gemessen wird

### Primär — steuert die Beauftragung

| Kennzahl | Berechnung |
|---|---|
| IR gesamt | Anteil mit `bekanntheit_13 = 1` an allen, die den Screener erreichen |
| **IR je Zelle** | dieselbe Grösse nach `altersgruppe` × `geschlecht` |
| Abschlussquote | Vollinterviews / Qualifizierte |
| Median-LOI | Median der Bearbeitungsdauer, nicht Mittelwert — die Verteilung ist rechtsschief |

Die IR je Zelle ist der wichtigste Einzelwert. Wenn die NEOH-Bekanntheit stark auf jüngere
Altersgruppen konzentriert ist, sind die Zellen 50-64 und 65+ in der Hauptwelle
überproportional teuer, und die Bruttoplanung muss zellenweise statt pauschal erfolgen.

### Sekundär — prüft das Instrument

| Prüfung | Erwartung / Alarmschwelle |
|---|---|
| Abbrüche je Block | keine Häufung; Häufung deutet auf ein Problem in diesem Block |
| `KEINE Marke` in den drei Rastern | plausibel und exklusiv gesetzt; nie gemeinsam mit einer Marke |
| Anteil "Weiss nicht" auf den fünf Slidern | hoch = Brand-Health-Block in DE kaum beantwortbar |
| `H1` Einblendungsrate | > 0; zeigt, dass die Display-Logik auf QID45/QID46 greift |
| `altersgruppe` | vollständig besetzt, Bänder stimmen mit `alter` überein |
| Speeder | LOI < 40 % des Medians |
| Straightliner | identischer Wert auf allen fünf Slidern |
| offene Angaben | Anteil unbrauchbarer Einträge bei `spontan`, `beschreibung`, `erfahrung` |
| Weiterleitungen | Anbieter verbucht Completes und Screen-outs korrekt und getrennt |

### Inhaltlich — validiert die Markenliste

Die offene Frage `spontan` läuft vor dem gestützten Raster. Die ungestützten Nennungen der
ersten 300 Befragten zeigen unmittelbar, welche Marken die Kategorie in Deutschland
definieren — und ob in der Liste eine fehlt oder eine überflüssig ist. Das kostet nichts
extra und ist die einzige Gelegenheit, die Liste noch zu korrigieren.

Vorsicht: Eine Änderung der Markenliste macht die Soft-Launch-Fälle unbrauchbar für das
Pooling (siehe Abschnitt 3). Es ist also eine bewusste Abwägung, keine Routineanpassung.

## 5. Entscheidungsregeln

Vor dem Soft-Launch festgelegt, damit die Auswertung nicht zur Verhandlung wird.

| Beobachtung | Konsequenz |
|---|---|
| IR ≥ 15 % | Hauptwelle wie geplant, Brutto nach Tabelle in Abschnitt 1 |
| IR 8–15 % | Hauptwelle mit zellenweiser Bruttoplanung; n_netto ggf. auf 250–300 reduzieren |
| IR < 8 % | Designentscheidung erforderlich, siehe Abschnitt 6 |
| Median-LOI > 15 min | Fragebogen kürzen oder LOI gegenüber dem Panel nachverhandeln |
| Abbrüche in einem Block > 10 % | Block prüfen, bevor die Hauptwelle startet |
| "Weiss nicht" auf einem Slider > 50 % | Kennzahl für DE als nicht belastbar kennzeichnen |
| `H1` Einblendungsrate = 0 | Display-Logik defekt, Feld stoppen |
| Speeder + Straightliner > 15 % | Qualitätsregeln mit dem Anbieter nachschärfen |

## 6. Wenn die IR sehr niedrig ist

Bei einer IR unter 8 % kostet eine Nettostichprobe von 400 mehr als 5.500 Bruttostarts.
Drei Optionen, in der Reihenfolge meiner Präferenz:

**(a) Screener aufheben und alle Befragten weiterführen.** Statt die NEOH-Unkenner zu
terminieren, erhalten sie einen Kurzpfad: Demografie und Funnel haben sie ohnehin schon
beantwortet. Damit bekommt man eine bevölkerungsrepräsentative Stichprobe für die
Funnel-Kennzahlen und eine kleinere Teilstichprobe für die Brand-Health-Metriken — und
jeder bezahlte Fall liefert verwertbare Daten. Das ist methodisch die sauberste Lösung:
die Awareness-Basis wird direkt geschätzt statt aus der Screen-out-Quote rekonstruiert,
und die Selektionsverzerrung der Markenmetriken lässt sich modellieren.

**(b) Nettostichprobe reduzieren.** n = 250 statt 400 kostet bei IR = 8 % rund 3.500 statt
5.500 Starts. Preis: breitere Konfidenzintervalle und kaum mögliche Subgruppenanalysen im
Brand-Health-Block.

**(c) Booster unter Kategorieverwendern.** Der Anbieter steuert gezielt Personen aus, die
Schokoriegel häufig kaufen. Senkt die Kosten, verzerrt aber die Stichprobe — die
Awareness-Rate ist dann nicht mehr bevölkerungsbezogen interpretierbar und der
AT-DE-Vergleich wird angreifbar. Nur mit expliziter Gewichtung und Dokumentation.

Option (a) erfordert einen Umbau des Survey Flow, der in wenigen Minuten gemacht ist: Der
Branch `Screen-out: NEOH nicht bekannt` wird durch einen Branch ersetzt, der die
NEOH-Blöcke überspringt statt zu terminieren.

## 7. Ablauf

| Schritt | Dauer |
|---|---|
| Fragebogen final, Weiterleitungen und Quoten konfiguriert, Preview-Tests bestanden | — |
| Aufbereitungsskript fertig und an AT-Testdaten geprüft | vor Feldstart |
| Soft-Launch, 300 gescreente Personen | 1–2 Tage |
| Feld pausieren, Auswertung nach Abschnitt 4 | 1 Tag |
| Entscheidung nach Abschnitt 5, Brutto mit dem Anbieter festlegen | 1 Tag |
| Hauptwelle | nach Feldplan |

Feld zwischen Soft-Launch und Hauptwelle **pausieren**, nicht weiterlaufen lassen. Sonst
ist die Entscheidungsgrundlage bereits überholt, wenn sie getroffen wird.

## 8. Vor dem Gespräch mit dem Panelanbieter

Den Anbieter vorab nach seiner eigenen Einschätzung der Kategorie-Incidence fragen — viele
haben Erfahrungswerte für zuckerreduzierte Riegel und können die Grössenordnung eingrenzen,
bevor überhaupt gefeldet wird. Ausserdem klären: Abrechnung von Screen-outs, ob
Quotenpufferung auf Anbieterseite erfolgt, und die Altersuntergrenze 16 statt der üblichen
18 (siehe `CODEBOOK_AT_DE.md`, Abschnitt 3b).

## 9. Saisonalität

Der Süsswarenmarkt ist ausgeprägt saisonal. Liegt die deutsche Hauptwelle deutlich später
als die österreichische, ist der Ländereffekt mit einem Saisoneffekt konfundiert und nicht
mehr trennbar. Der Soft-Launch verzögert die DE-Welle um etwa drei bis vier Tage — das ist
unkritisch, ein mehrwöchiger Abstand zur AT-Welle wäre es nicht. Wenn beide Länder parallel
laufen sollen, gehört der Soft-Launch entsprechend früh eingeplant.
