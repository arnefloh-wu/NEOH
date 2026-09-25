# Codebuch AT / DE — NEOH Markenstudie Sep 2026

Referenz für das Stapeln der beiden Länderdatensätze. Die Länderzugehörigkeit steht
in der Embedded-Data-Variable `land` (`AT` / `DE`), die als erstes Element im Survey
Flow gesetzt wird.

Dateien: `NEOH_AT_Sep2026.qsf` (AT), `NEOH_DE_Sep2026.qsf` (DE). Beide Instrumente sind
strukturgleich: identische Fragen, Export-Tags, Blockfolge, Logik und Randomisierung.
Sie unterscheiden sich ausschliesslich in `einleitung`, `bundesland`, `bildung` und der
Markenliste der drei Raster.

## 1. Markenraster

Betrifft `bekanntheit` (gestützte Bekanntheit), `betracht` (Consideration) und
`kauf_3monate` (Kauf letzte 3 Monate). Alle drei Fragen verwenden in beiden Ländern
dieselben Exportcodes; die Spaltensuffixe im Export sind damit direkt vergleichbar.

| Code | Marke | AT | DE |
|-----:|-------|:--:|:--:|
| 1 | Balisto | x | x |
| 2 | BE-KIND | x | x |
| 3 | Bounty | x | x |
| 4 | Corny | x | x |
| 5 | Dragee Keksi (Napoli) | x | — |
| 6 | Hanuta | x | x |
| 7 | Ketofabrik (Keast) | x | — |
| 8 | Kinder | x | x |
| 9 | Knoppers | x | x |
| 10 | Manner | x | x |
| 11 | Mars | x | x |
| 12 | Milka | x | x |
| **13** | **NEOH** | x | x |
| 14 | Nicks | x | x |
| 15 | Nucao | x | x |
| 16 | Pick Up! | x | x |
| 17 | Snickers | x | x |
| 18 | AHEAD | x | x |
| 19 | More Nutrition | x | x |
| 20 | Foodspring | x | — |
| 90 | Barebells | — | x |
| 91 | Xucker | — | x |
| 92 | Duplo | — | x |
| 99 | KEINE Marke (exklusiv) | x | x |

Darstellung: Die drei Raster laufen über **drei Spalten**. 21 Optionen teilen sich ohne
Rest auf 7 je Spalte, sodass "KEINE Marke" als letzte Option unten rechts steht und keine
Marke optisch darunter liegt. Bei vier Spalten wäre die erste Spalte eine Zeile länger
gewesen, was die Absicht der Endposition unterlaufen hätte.

Regeln:

- **Codes 5, 7 und 20 bleiben in DE unbesetzt** und werden dort nie neu vergeben.
  Ein Code bedeutet in beiden Ländern dieselbe Marke oder gar nichts.
- **NEOH ist Code 13**, nicht 14. Die interne Choice-ID ist 14 — darauf greifen die
  Skip-Logik (`bekanntheit`) und die Display-Logik von `H1` zu. Auswertungen
  verwenden den Exportcode 13.
- Länderspezifische Marken liegen im 90er-Bereich, die Ausweichoption bei 99.
  Für einen reinen Ankervergleich AT/DE also Codes < 90 filtern.

### Länderentscheidungen

- **Dragee Keksi (Napoli)** — Marke von Manner, ausschließlich auf Österreich
  ausgerichtet. In DE nicht sinnvoll abfragbar.
- **Ketofabrik** — Firmensitz Salzburg, primär AT-Distribution. Die Marke firmiert
  inzwischen unter "Keast". Das Label lautet deshalb "Ketofabrik (Keast)": Es fängt
  Befragte ab, die nur einen der beiden Namen kennen, und ist gegen den Stand des
  Rebrands im Handel robust. Der Exportcode 7 bleibt unverändert.
- **Foodspring** — das kundenseitige Geschäft wurde zum 30.06.2025 eingestellt. In DE
  nicht aufgenommen, in AT bewusst beibehalten: Markenwissen überlebt die Distribution,
  die gestützte Bekanntheit bleibt also aussagekräftig. **Bei `betracht` und
  `kauf_3monate` ist Code 20 dagegen nicht interpretierbar** und in der Auswertung
  gesondert zu behandeln.
- **Barebells** (deutsche Tochter Hamburg, bei REWE und EDEKA gelistet), **Xucker**
  (Berlin, dm und Rossmann) und **Duplo** (meistverkaufter Schokoriegel Deutschlands)
  ergänzen in DE das Wettbewerbsumfeld.
- **Manner** bleibt in beiden Ländern: eigenes Vertriebsbüro in Deutschland, dort aber
  als Low-Awareness-Anker zu lesen.

Anmerkung zur Distribution: NEOH ist in Deutschland bundesweit bei REWE und Müller
gelistet, dazu Kaufland und Lekkerland, **nicht** bei dm und Rossmann. Die
`H1`-Antwortoption "Nicht in meinem bevorzugten Geschäft erhältlich" dürfte in DE
deshalb deutlich stärker besetzt sein als in AT.

## 2. Bildungsabschluss (`bildung`)

Die Kategorien sind länderspezifisch und **nicht** über den Rohcode vergleichbar.
Für gepoolte Analysen über die ISCED-Spalte rekodieren.

| AT Code | AT Kategorie | ISCED | DE Code | DE Kategorie |
|--------:|--------------|:-----:|--------:|--------------|
| — | — | 0–1 | 1 | Kein Schulabschluss |
| 1 | Pflichtschule | 2 | 2 | Hauptschul-/Volksschulabschluss |
| 1 | Pflichtschule | 2 | 3 | Mittlere Reife / Realschulabschluss |
| 2 | Lehre/Berufsausbildung | 3–4 | 4 | Abgeschlossene Berufsausbildung (Lehre) |
| 3 | Matura/Abitur | 3–4 | 5 | Fachhochschulreife / Abitur |
| 4 | Bachelor | 6 | 6 | Bachelor |
| 5 | Master/Magister/Diplom | 7 | 7 | Master / Diplom / Magister / Staatsexamen |
| 6 | Doktorat/PhD | 8 | 8 | Promotion |
| 7 | Sonstiges | n/a | 9 | Sonstiges |

AT fasst Haupt- und Realschulniveau unter "Pflichtschule" zusammen; DE trennt beide.
Beim Pooling werden die deutschen Codes 2 und 3 auf ISCED 2 zusammengeführt.

## 3. Region (`bundesland`)

AT: 9 Bundesländer (Codes 1–9). DE: 16 Bundesländer (Codes 1–16, alphabetisch).
Nicht ineinander überführbar — für den Ländervergleich als getrennte
Gewichtungsvariable behandeln (Statistik Austria bzw. Destatis).

## 3a. Alter (`alter`)

Geschlossene Einfachauswahl mit den Kategorien, nach denen der Panelanbieter aussteuert.
Beide Länder identisch.

| Code | Kategorie |
|---:|---|
| 1 | Unter 18 Jahre — **terminiert** |
| 2 | 18 bis 29 Jahre |
| 3 | 30 bis 39 Jahre |
| 4 | 40 bis 49 Jahre |
| 5 | 50 bis 59 Jahre |
| 6 | 60 Jahre und älter |

Code 1 kommt im Datensatz nicht vor: Wer ihn wählt, wird im Branch
`Screen-out: unter 18 Jahre` terminiert. Die Kategorie existiert nur, damit ein
Fehlversand nicht stillschweigend als 18-Jähriger gezählt wird.

Eine frühere Fassung erhob das Alter als offene Zahleneingabe und leitete daraus die
Embedded-Data-Variable `altersgruppe` ab. Beides ist entfallen — `alter` trägt die
Bandzuordnung jetzt selbst, die Kaskade im Survey Flow ist weg.

**Konsequenz für die Auswertung:** Das Alter liegt nur noch kategorial vor. Median- oder
Mittelwertaussagen zum Alter sind nicht mehr möglich, Alter als stetige Kovariate ebenso
wenig, und eine Umgruppierung auf ein anderes Bandschema (etwa für die Gewichtung gegen
eine Statistik mit abweichenden Klassen) geht nicht mehr. Dafür stimmen Fragebogen und
Anbieteraussteuerung exakt überein.

## 3b. Abbruchpfade und Feldkonfiguration

Beide Fassungen haben zwei Screen-out-Pfade, beide als Branch im Survey Flow mit einem
eigenen End-of-Survey-Element:

| Position im Flow | Bedingung | Bedeutung |
|---|---|---|
| nach dem Screening-Block | `alter` = Kategorie 1 (unter 18) | Screen-out Alter |
| nach dem Block Markenbekanntheit | NEOH bei `bekanntheit` nicht ausgewählt | Screen-out Bekanntheit |

Der Bekanntheitsscreener war zuvor eine Skip Logic an der Frage. Skip Logic nutzt immer
die globale Abschlussaktion — die Screen-outs wären also auf dem Complete-Link des
Panelanbieters gelandet und als abgeschlossene Interviews abgerechnet worden. Als Branch
mit eigenem End-of-Survey-Element lässt sich pro Pfad eine eigene Weiterleitung setzen.

### Panel-Anbindung

Die Respondenten-ID wird im Embedded-Data-Element ganz oben als Feld **`PID`** geführt.
Entscheidend: Das Feld wird **nur deklariert, nicht zugewiesen** — in der Qualtrics-Oberfläche
steht daneben "Wert wird aus Panel oder URL gesetzt", kein Eingabefeld mit Wert. Wird
stattdessen ein leerer Wert zugewiesen, überschreibt der Survey Flow den aus dem Query
String gelesenen Wert, und die Rückleitung übergibt eine leere ID. Genau dieser Fehler ist
in der ersten Feldkonfiguration aufgetreten.

`land` ist der Gegenfall: Dort ist eine Zuweisung gewollt (`AT` bzw. `DE`). Der Anbieter hängt
seinen Platzhalter entsprechend an:

```
https://wumarketing.qualtrics.com/jfe/form/SV_XXXXXXXX?PID=%id%
```

Achtung, die Parameternamen sind auf Hin- und Rückweg **nicht identisch**: Der
Einstiegslink trägt `PID` (unser Feldname in Qualtrics), der Rückweg trägt `i_survey`
(der Feldname im System des Anbieters). Ein Testaufruf des Qualtrics-Links mit
`?i_survey=...` läuft deshalb ins Leere — Qualtrics kennt kein Feld dieses Namens,
`PID` bleibt leer, und die Rückleitung endet auf `i_survey=`.

Weiterleitungen (Anbieter: Loopster Panel). In der AT-Fassung sind sie **im QSF
hinterlegt**: Complete in den Umfrageoptionen (`SurveyTermination: Redirect` +
`EOSRedirectURL`), Screen-out als `EndingType: Advanced` am End-of-Survey-Element im
Branch `Screen-out: unter 18 Jahre`. Der Platzhalter `%id%` aus den Vorlagen des
Anbieters ist jeweils durch `${e://Field/PID}` ersetzt:

| Ausgang | ergebnis | Wo hinterlegt |
|---|---|---|
| Complete | 5 | Umfrageoptionen → Umfrageende → Zu einer URL weiterleiten |
| Screen-out Alter | 31 | End-of-Survey im Branch `Screen-out: unter 18 Jahre`, dort "Umfrageoptionen überschreiben" |
| Quota-full | entfällt | Aussteuerung erfolgt beim Anbieter |
| Quality terminate | 42 | nicht verwendet, siehe unten |

Die Links liegen bisher nur für Österreich vor; die DE-Fassung enthält sie noch nicht.

Testaufruf der Rückleitung (privates Fenster, da `BallotBoxStuffingPrevention` aktiv ist):

```
https://wumarketing.qualtrics.com/jfe/form/SV_XXXXXXXX?PID=test123
```

Danach muß die Zielseite auf `...?i_survey=test123&autostart=1&ergebnis=5` enden und die
Spalte `PID` in Daten & Analysen `test123` enthalten.

**Stand Österreich: geprüft.** Der Feldname `PID` ist bestätigt, der Einstiegslink lautet
`?PID=%id%`. Die vom Anbieter vorgeschlagene Alternative `${e://Field/id}` ist damit
gegenstandslos. Für Deutschland gilt derselbe Feldname; dort fehlen nur noch die
Rückleitungs-URLs des Anbieters.

`ergebnis=42` (Quality terminate) bleibt bewusst ungenutzt: Die Aufmerksamkeitsprüfung
`attention` terminiert nicht, der Ausschluss erfolgt in der Aufbereitung (Abschnitt 3c).
Ein Feldabbruch bei nicht bestandener Prüfung würde die Screen-out-Statistik verzerren
und Abrechnungsdiskussionen erzeugen.

Die Weiterleitungen der DE-Fassung folgen, sobald die Links vorliegen.

Die Sollvorgabe für Österreich lautet `alter` × `geschlecht` interlocked (je 250 Frauen
und Männer, Kategorien 2 bis 6) mit Bundesland als Randquote.

## 3c. Aufmerksamkeitsprüfung (`attention`)

Instructed-Response-Item, in beiden Fassungen identisch. Steht als letzte Frage im Block
Screening und Demografie, damit jeder Befragte es an derselben Stelle durchläuft — auch
wer NEOH nicht kennt und die sechs Markenmodule überspringt. Skala −100 bis +100 wie die
Brand-Health-Slider, Antwortpflicht, keine Ausweichoption.

Wortlaut: "Diese Frage prüft nur, ob die Fragen aufmerksam gelesen werden. Bitte ziehen
Sie den Schieberegler ganz nach rechts auf 100."

**Das Item terminiert nicht.** Es wird erhoben und in der Aufbereitung als
Ausschlusskriterium verwendet — ein Abbruch im Feld führt zu Abrechnungsstreit mit dem
Panelanbieter und verzerrt die Screen-out-Statistik.

Auswertungsregel: `attention < 90` gilt als nicht bestanden. Die Schwelle statt exakt 100,
weil der Regler nicht einrastet (`SnapToGrid` ist aus) und ein Ziehen ans rechte Ende
minimal darunter liegen kann. Der Anteil nicht bestandener Fälle ist zu berichten.

Weil das Item vor der Markenbekanntheit liegt, trifft die Ausschlussregel NEOH-Kenner und
Nicht-Kenner an derselben Stelle und mit derselben Ermüdung gleich streng.

## 3d. Feldausrichtung

Ausgesteuert wird nur über Alter (ab 18) und die Quoten des Panelanbieters. Die sechs
NEOH-Module (Medien, Markengesundheit, Markenwahrnehmung, Bedürfnisse und Bedeutung,
Markteffekte, Markensentiment) liegen in einem Branch, der sie bei bekanntem NEOH
einblendet und sonst überspringt. Wer NEOH nicht kennt, beantwortet Demografie,
`spontan`, die drei Markenraster, `attention` und `zucker` und schließt regulär ab.

Was das für die Auswertung bedeutet:

- **Die NEOH-Bekanntheit wird direkt geschätzt**, nicht aus der Screen-out-Quote
  rekonstruiert. Nenner ist die gewichtete Gesamtstichprobe.
- **Die Markenmetriken sind weiterhin konditional** auf die Bekanntheit — aber die
  Selektion ist beobachtet statt durch Feldausschluss erzeugt und damit modellierbar.
- **Der Wettbewerbs-Funnel für alle 21 Optionen** liegt auf der Allgemeinbevölkerung.
  Nur so sind Bekanntheit, Consideration und Kauf zwischen NEOH und den übrigen Marken
  direkt vergleichbar.
- **`attention` steht im Screening-Block**, damit es jeder Befragte an derselben Stelle
  durchläuft und die Ausschlussregel beide Gruppen gleich streng trifft.
- `einleitung` enthält **keine Dauerangabe**. Die gegenüber dem Panelanbieter
  kalkulierte LOI ist dadurch nicht an eine Zusage im Fragebogen gebunden; die
  tatsächliche Bearbeitungsdauer wird über die Timing-Elemente gemessen (Abschnitt 3e).

Eine frühere Variante terminierte NEOH-Unkenner. Sie wurde verworfen, weil sie die vom
Panelanbieter vorausgesetzte Bedingung "IR mindestens 80 %" verletzt, und ist nur noch
über die Git-Historie erreichbar.

## 3e. Zeitmessung

Drei unsichtbare Timing-Elemente auf den drei zeitkritischen Seiten. Für die Befragten
ändert sich nichts; sie dienen der Diagnose, falls die Bearbeitungsdauer über der
gegenüber dem Panelanbieter kalkulierten LOI liegt.

| Tag | Seite |
|---|---|
| `t_spontan` | offene Frage `spontan` |
| `t_raster` | die drei Markenraster (`bekanntheit`, `betracht`, `kauf_3monate`, zusammen 63 Items) |
| `t_sentiment` | `beschreibung`, `intention`, `empfehlung` |

Jedes Element liefert vier Spalten: `First Click`, `Last Click`, `Page Submit` und
`Click Count`. Relevant ist **`Page Submit`** — die Verweildauer auf der Seite in
Sekunden. Bei den offenen Fragen trennt die Differenz zwischen `First Click` und
`Page Submit` zusätzlich Nachdenk- von Tippzeit.

Auswertung immer über den **Median**, nie den Mittelwert: Die Verteilung ist stark
rechtsschief, weil einzelne Befragte den Tab offen liegen lassen. Dasselbe gilt für die
Gesamtdauer, die Qualtrics ohnehin als `Duration (in seconds)` exportiert.

Zwei Randbedingungen: Die Werte sind additiv, wenn eine Seite mehrfach aufgerufen wird.
Ein Zurück-Button existiert nicht (`BackButton` ist aus), aber `SaveAndContinue` ist
aktiv — wer unterbricht und später auf derselben Seite wieder einsteigt, erzeugt eine
aufgeblähte Zeit. Auch deshalb der Median.

Die LOI ist in den beiden Ländern **nicht vergleichbar**, obwohl der Fragebogen identisch
ist: NEOH-Kenner durchlaufen sechs zusätzliche Module. Bei hoher Bekanntheit (AT) liegt
die Misch-LOI nahe am langen Pfad, bei niedriger (DE) nahe am kurzen. Für das
Anbietergespräch ist der Median über alle Completes je Land getrennt zu berichten.

## 4. Identisch gehaltene Variablen

Bewusst nicht lokalisiert, um die Messäquivalenz nicht zu gefährden: `haeufigkeit`,
`alter`, `geschlecht`, `spontan`, `kanal`, alle Brand-Health-Slider, `bedürfnis`,
`bedeutsam`, `H1`, `beschreibung`, `intention`, `empfehlung`,
`einkommen` (beide Länder Eurozone, identische Klassen), `zucker` und `attention`.
Ebenso die fünf Brand-Health-Slider, die in beiden Fassungen ohne Ausweichoption laufen.

## 5. Konsistenzprüfungen für die Datenaufbereitung

- `kauf_3monate_13 = 1` bei gleichzeitig `bekanntheit_13 = 0` ist inkonsistent:
  Das Kaufraster läuft im Fragebogen vor der gestützten Bekanntheit, die
  gleichzeitig der Screener ist.
- `*_99` (KEINE Marke) ist exklusiv gesetzt; jede Kombination mit einer Markenangabe
  deutet auf einen Fehler in der Feldkonfiguration hin.
- Die fünf Brand-Health-Slider (`emotion`, `qualität`, `plv`, `zufriedenheit`, `wom`)
  haben **keine** Ausweichoption. Sie stehen auf "Antwort erbeten", nicht auf
  Antwortpflicht — wer kein Urteil abgeben kann oder will, klickt weiter, und der Wert
  bleibt leer. Solche Fälle sind als fehlend zu behandeln.
  **Nicht unterscheidbar** ist dadurch ein bewusst neutrales Urteil (Regler in der Mitte,
  Wert 0) von einem "weiß nicht": Wer den Regler antippt und mittig stehen lässt, erzeugt
  eine 0. Der Anteil leerer Werte je Slider ist deshalb mit zu berichten, besonders im
  Ländervergleich, wo die NEOH-Vertrautheit unterschiedlich hoch ist.
- Alle Markenmetriken sind konditional auf die NEOH-Bekanntheit (Screener). Die
  Awareness-Basis ist bei jedem Ländervergleich mit zu berichten.
- `alter` = 1 darf im Datensatz nicht vorkommen; solche Fälle werden terminiert.
- `attention < 90` markiert nicht bestandene Aufmerksamkeitsprüfungen. Ausschluss in
  beiden Ländern nach derselben Regel, Anteil berichten.
- In AT ist Code 20 (Foodspring) nur bei `bekanntheit` interpretierbar, nicht bei
  `betracht` und `kauf_3monate`.
