# Codebuch AT / DE — NEOH Markenstudie Sep 2026

Referenz für das Stapeln der beiden Länderdatensätze. Die Länderzugehörigkeit steht
in der Embedded-Data-Variable `land` (`AT` / `DE`), die als erstes Element im Survey
Flow gesetzt wird.

Dateien: `NEOH_AT_Sep2026_V7.qsf` (AT), `NEOH_DE_Sep2026.qsf` (DE). Beide Instrumente sind
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

## 3a. Altersgruppe (`altersgruppe`)

Embedded-Data-Variable, im Survey Flow direkt nach dem Screening-Block berechnet. `alter`
bleibt als offene Zahleneingabe erhalten; `altersgruppe` dient der Quotierung und der
Gewichtung.

| Wert | Alter |
|---|---|
| `16-24` | 16 bis 24 |
| `25-34` | 25 bis 34 |
| `35-49` | 35 bis 49 |
| `50-64` | 50 bis 64 |
| `65+` | 65 und älter |

Technisch als Kaskade umgesetzt: Der Ausgangswert `65+` wird von vier Branches mit
`alter < 65`, `< 50`, `< 35` und `< 25` schrittweise überschrieben. Der zuletzt zutreffende
Branch gewinnt. Bewusst nur mit dem Operator "kleiner als", ohne Und-Verknüpfungen —
das ist robuster und im Survey Flow leichter zu kontrollieren.

## 3b. Abbruchpfade und Feldkonfiguration

Beide Fassungen haben zwei Screen-out-Pfade, beide als Branch im Survey Flow mit einem
eigenen End-of-Survey-Element:

| Position im Flow | Bedingung | Bedeutung |
|---|---|---|
| nach dem Screening-Block | `alter < 16` | Screen-out Alter |
| nach dem Block Markenbekanntheit | NEOH bei `bekanntheit` nicht ausgewählt | Screen-out Bekanntheit |

Der Bekanntheitsscreener war zuvor eine Skip Logic an der Frage. Skip Logic nutzt immer
die globale Abschlussaktion — die Screen-outs wären also auf dem Complete-Link des
Panelanbieters gelandet und als abgeschlossene Interviews abgerechnet worden. Als Branch
mit eigenem End-of-Survey-Element lässt sich pro Pfad eine eigene Weiterleitung setzen.

Vor dem Feld im Qualtrics-UI zu ergänzen:

1. **Panel-ID aufnehmen**: im Embedded-Data-Element ganz oben neben `land` ein Feld mit
   dem Feldnamen des Anbieters anlegen, Wert leer lassen. Qualtrics befüllt es aus dem
   Query String des Einstiegslinks.
2. **Weiterleitungen**: je End-of-Survey-Element "Umfrageoptionen überschreiben" →
   "Zu einer URL weiterleiten", mit dem Screen-out-Link des Anbieters und angehängter ID,
   z. B. `...?pid=${e://Field/PID}`. Der Complete-Link gehört in die globale
   Abschlussaktion, der Quota-full-Link an das Quota-Element.
3. **Quota-Element**: zwischen die `altersgruppe`-Branches und den Block Markenbekanntheit
   setzen. Die Position ist entscheidend — quotiert wird die Allgemeinbevölkerung, nicht
   die Teilstichprobe der NEOH-Kenner. Läge das Element hinter dem Bekanntheitsscreener,
   würde die Awareness-Rate selbst verzerrt.

Quotenvorschlag: `altersgruppe` × `geschlecht` interlocked, dazu eine Regionquote. Bei den
16 deutschen Bundesländern nicht einzeln quotieren, sondern zu Nielsen-Gebieten
zusammenfassen, sonst blockieren kleine Länder das Feld.

## 3c. Aufmerksamkeitsprüfung (`attention`)

Instructed-Response-Item, in beiden Fassungen identisch. Steht als dritter von fünf
Slidern im Block Markengesundheit, damit es sich formal nicht von den umgebenden Items
unterscheidet. Skala −100 bis +100 wie die Brand-Health-Slider, Antwortpflicht, keine
Ausweichoption.

Wortlaut: "Diese Frage prüft nur, ob die Fragen aufmerksam gelesen werden. Bitte ziehen
Sie den Schieberegler ganz nach rechts auf 100."

**Das Item terminiert nicht.** Es wird erhoben und in der Aufbereitung als
Ausschlusskriterium verwendet — ein Abbruch im Feld führt zu Abrechnungsstreit mit dem
Panelanbieter und verzerrt die Screen-out-Statistik.

Auswertungsregel: `attention < 90` gilt als nicht bestanden. Die Schwelle statt exakt 100,
weil der Regler nicht einrastet (`SnapToGrid` ist aus) und ein Ziehen ans rechte Ende
minimal darunter liegen kann. Der Anteil nicht bestandener Fälle ist zu berichten.

Das Item liegt hinter dem NEOH-Bekanntheitsscreener und erfasst damit nur qualifizierte
Befragte. Für Screen-outs bleiben Bearbeitungsdauer und offene Angaben die einzigen
Qualitätsindikatoren.

## 4. Identisch gehaltene Variablen

Bewusst nicht lokalisiert, um die Messäquivalenz nicht zu gefährden: `haeufigkeit`,
`alter`, `geschlecht`, `spontan`, `kanal`, alle Brand-Health-Slider, `bedürfnis`,
`bedeutsam`, `H1`, `beschreibung`, `erfahrung`, `intention`, `empfehlung`,
`einkommen` (beide Länder Eurozone, identische Klassen), `zucker` und `attention`.
Ebenso die Ausweichoption der fünf Slider, die in beiden Fassungen "Weiß nicht" heißt.

## 5. Konsistenzprüfungen für die Datenaufbereitung

- `kauf_3monate_13 = 1` bei gleichzeitig `bekanntheit_13 = 0` ist inkonsistent:
  Das Kaufraster läuft im Fragebogen vor der gestützten Bekanntheit, die
  gleichzeitig der Screener ist.
- `*_99` (KEINE Marke) ist exklusiv gesetzt; jede Kombination mit einer Markenangabe
  deutet auf einen Fehler in der Feldkonfiguration hin.
- Die Slider (`emotion`, `qualität`, `plv`, `zufriedenheit`, `wom`) haben eine
  "Nicht zutreffend"-Option. Diese Antworten sind als fehlend zu behandeln, **nicht**
  als Skalenmitte 0.
- Alle Markenmetriken sind konditional auf die NEOH-Bekanntheit (Screener). Die
  Awareness-Basis ist bei jedem Ländervergleich mit zu berichten.
- `attention < 90` markiert nicht bestandene Aufmerksamkeitsprüfungen. Ausschluss in
  beiden Ländern nach derselben Regel, Anteil berichten.
- In AT ist Code 20 (Foodspring) nur bei `bekanntheit` interpretierbar, nicht bei
  `betracht` und `kauf_3monate`.
