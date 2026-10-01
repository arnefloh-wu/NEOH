# Feldbericht Österreich — NEOH Markenstudie, September 2026

Erstellt am 1. Oktober 2026 aus dem Qualtrics-Export vom selben Tag.
Alle Zahlen sind mit `aufbereitung_at.py` reproduzierbar; das vollständige
Protokoll steht in `AUFBEREITUNG_AT_log.txt`.

---

## 1. Das Wichtigste vorab

Das Feld ist technisch sauber gelaufen. 596 vollständige Interviews, keine
doppelten Panel-IDs, die Panel-ID ist in allen Fällen zurückgekommen, und nach
Ausschluss von 29 Fällen (4,9 %) bleibt eine **Nettostichprobe von 567**. Das
liegt über dem Soll von 500.

Drei Punkte verlangen eine Entscheidung, bevor Ergebnisse berichtet werden:

**Erstens: Der vereinbarte Quotenplan bildet die österreichische Bevölkerung
nicht ab.** Er sieht für die Gruppe 60+ einen Anteil von 16 % vor. Nach den
Eckzahlen von Statistik Austria zum 1. 1. 2026 (2,59 Mio. Personen ab 60 von
7,91 Mio. ab 15 Jahren) liegt der tatsächliche Anteil bei rund einem Drittel
der erwachsenen Bevölkerung. Der Plan unterzeichnet die Älteren also etwa um
den Faktor zwei. Eine Gewichtung auf den Quotenplan korrigiert diesen Fehler
**nicht** — sie zementiert ihn. Details in Abschnitt 5.

**Zweitens: Die Quoten wurden im Feld nicht eingehalten.** Die jüngste Gruppe
blieb mit 88 von 120 Soll deutlich zurück, die Männer ab 60 wurden mit 73 statt
40 um 83 % überliefert. Ohne Gewichtung ist der Datensatz in der Altersstruktur
schief.

**Drittens: Die Rohdaten liegen in einem öffentlichen GitHub-Repository.** Sie
enthalten Panel-IDs, Alter, Geschlecht, Bundesland, Einkommen, Bildung und
offene Textantworten. Das ist eine datenschutzrechtliche Frage, keine
technische; siehe Abschnitt 8.

---

## 2. Feldverlauf

| | |
|---|---|
| Feldbeginn | 25. September 2026, 09:21 |
| Feldende | 30. September 2026, 06:35 |
| Felddauer | 5 Tage |
| Abgeschlossene Interviews | 596 |
| Abbrüche im Export | keine (alle `Finished = 1`) |
| Verteilungskanal | anonymer Link, Sprache DE |

Der Rücklauf war ungleich verteilt: 187 Interviews am ersten Tag, 243 am
28. September, der Rest verteilt. Für die Auswertung ist das unerheblich,
für eine spätere Feldplanung aber eine brauchbare Referenz.

**Bearbeitungsdauer (LOI)**

| Perzentil | P5 | P25 | Median | P75 | P95 |
|---|---:|---:|---:|---:|---:|
| Sekunden | 71 | 132 | **195** | 275 | 551 |

Der Median liegt bei 3,2 Minuten. Erwartungsgemäß trennt sich das Feld nach
der Bekanntheitsfrage: NEOH-Kenner durchlaufen sechs zusätzliche Module und
brauchen im Median 251 Sekunden, Nicht-Kenner 138. Die 3,2 Minuten sind damit
ein Mischwert und für eine Preisverhandlung über eine Folgewelle nur
eingeschränkt brauchbar — relevant ist die Dauer bei der erwarteten
Bekanntheitsquote.

---

## 3. Ausschlüsse

| Kriterium | n | Anteil |
|---|---:|---:|
| Alter „Unter 18 Jahre" | 1 | 0,2 % |
| Aufmerksamkeitsprüfung < 90 | 17 | 2,9 % |
| Speeder (< 65 s, ein Drittel des Medians) | 25 | 4,2 % |
| *davon mehrfach auffällig* | *14* | |
| **Ausgeschlossen gesamt** | **29** | **4,9 %** |
| **Nettostichprobe** | **567** | |

Die starke Überschneidung ist ein gutes Zeichen: Von den 43 Markierungen
entfallen 14 auf Fälle, die gleich zwei Kriterien verletzen. Wer durchklickt,
scheitert auch an der Aufmerksamkeitsprüfung. Das spricht dafür, dass beide
Indikatoren dasselbe Verhalten messen und nicht zufällig Fälle aussortieren.

**Der Fall mit „Unter 18 Jahre" hätte nicht im Datensatz sein dürfen.** Der
Screen-out-Branch war im Feld aktiv und leitet diese Kategorie auf
`ergebnis=31`. Warum ein Fall durchgekommen ist, lässt sich aus dem Export
nicht klären — denkbar ist ein Zurückspringen im Fragebogen nach bereits
passiertem Branch. Der Fall ist ausgeschlossen; für die DE-Welle wäre zu
prüfen, ob der Zurück-Button deaktiviert bleiben soll.

**Die Aufmerksamkeitsprüfung terminierte in Österreich noch nicht.** Der
Quality-terminate-Branch (`ergebnis=42`) wurde erst nach Feldstart gebaut. Die
17 Fälle sind deshalb im Datensatz und werden hier in der Aufbereitung
ausgeschlossen, statt im Feld ersetzt worden zu sein. Für Deutschland ist der
Branch im Instrument; dort sinkt die Nettoausfallquote entsprechend, und die
Fälle werden vom Anbieter nachgeliefert. **Das macht die Ausschlussquoten der
beiden Länder nicht unmittelbar vergleichbar** und gehört in den Methodenteil.

### Nur markiert, nicht ausgeschlossen

| Indikator | n | Anteil |
|---|---:|---:|
| Straightliner über alle fünf Slider | 6 | 1,0 % |
| reCAPTCHA-Score < 0,5 | 45 | 7,6 % |
| Privates Browserfenster erkannt | 88 | 14,8 % |

Diese drei stehen als Variablen im analysefertigen Datensatz, damit die
Entscheidung über sie im Analyseplan fällt und nicht stillschweigend in der
Aufbereitung.

Mein Vorschlag: **Straightliner drin lassen** (sechs Fälle, und die fünf Slider
messen verwandte Konstrukte — ein durchgehend gleiches Urteil kann echt sein),
**privates Browserfenster ignorieren** (14,8 % sind zu viele für ein
Qualitätssignal; das misst Browsergewohnheiten, nicht Antwortverhalten), und
den **reCAPTCHA-Score als Sensitivitätsrechnung** führen. Die 44 betroffenen
Fälle der Nettostichprobe überschneiden sich mit keinem einzigen
Straightliner, was eher gegen ein gemeinsames Täuschungsmuster spricht. Würden
die zentralen Kennwerte ohne sie kippen, wäre das ein Befund; tun sie es
nicht, ist die Frage erledigt.

---

## 4. Quotenerfüllung

Vereinbart war Alter × Geschlecht interlocked, je 250 Frauen und Männer.

| Zelle | Soll | Ist | Soll-% | Ist-% | Abweichung |
|---|---:|---:|---:|---:|---:|
| 18–29 männlich | 60 | 44 | 12,0 % | 7,8 % | −27 % |
| 18–29 weiblich | 60 | 44 | 12,0 % | 7,8 % | −27 % |
| 30–39 männlich | 50 | 55 | 10,0 % | 9,7 % | +10 % |
| 30–39 weiblich | 50 | 63 | 10,0 % | 11,1 % | +26 % |
| 40–49 männlich | 50 | 56 | 10,0 % | 9,9 % | +12 % |
| 40–49 weiblich | 50 | 52 | 10,0 % | 9,2 % | +4 % |
| 50–59 männlich | 50 | 65 | 10,0 % | 11,5 % | +30 % |
| 50–59 weiblich | 50 | 75 | 10,0 % | 13,2 % | +50 % |
| 60+ männlich | 40 | 73 | 8,0 % | 12,9 % | **+83 %** |
| 60+ weiblich | 40 | 40 | 8,0 % | 7,1 % | ±0 % |

*(Ist-Werte nach Ausschlüssen, n = 567.)*

Das Muster ist typisch für ein schnell gefülltes Panel: Die leicht erreichbaren
Zellen laufen über, die jungen Männer und Frauen bleiben zurück. Die
Geschlechterbilanz insgesamt stimmt annähernd (293 männlich, 274 weiblich), die
**Altersverteilung nicht**.

Die Randquote nach Bundesland, die im Angebot erwähnt, aber nie als Tabelle
vorgelegt wurde, lässt sich daher nicht gegen ein Soll prüfen. Beobachtet:

| Bundesland | n | Anteil |
|---|---:|---:|
| Wien | 139 | 24,5 % |
| Niederösterreich | 127 | 22,4 % |
| Oberösterreich | 104 | 18,3 % |
| Steiermark | 67 | 11,8 % |
| Tirol | 42 | 7,4 % |
| Kärnten | 26 | 4,6 % |
| Burgenland | 22 | 3,9 % |
| Salzburg | 21 | 3,7 % |
| Vorarlberg | 19 | 3,4 % |

Auffällig ist Salzburg mit 3,7 %. Ob das innerhalb der vereinbarten Toleranz
liegt, kann ohne die Solltabelle niemand sagen — die sollte vom Anbieter
nachgefordert werden.

---

## 5. Gewichtung

Berechnet ist eine **Nachschichtung auf die zehn Zellen Alter × Geschlecht**
gegen den vereinbarten Quotenplan. Variable `gewicht_quote`.

| | |
|---|---|
| Gewichtsspanne | 0,621 bis 1,546 |
| Designeffekt | 1,078 |
| Effektives n | 526 von 567 |

Die Gewichte sind moderat, kein Fall wird dominant, Trimmen ist nicht nötig.
Der Verlust an effektivem Stichprobenumfang beträgt 41 Fälle — vertretbar.

### Warum dieses Gewicht nicht genügt

`gewicht_quote` korrigiert die Abweichung des **Feldes vom Plan**. Es korrigiert
nicht die Abweichung des **Plans von der Bevölkerung**. Nach Gewichtung liegt
der Anteil der 60-Jährigen und Älteren bei exakt 16 % — dem Planwert. Der
Anteil in der österreichischen Wohnbevölkerung ab 18 liegt bei etwa einem
Drittel.

> Für bevölkerungsbezogene Aussagen — und die Markenbekanntheit ist eine
> solche — ist `gewicht_quote` damit **nicht** das richtige Gewicht.

Die Datei `gewichtung_ziele_AT.csv` enthält dafür eine zweite, derzeit leere
Spalte `soll_bevoelkerung`. Sobald dort die amtlichen Randverteilungen stehen,
berechnet dasselbe Skript die Variable `gewicht_bev`. Solange sie leer ist,
bleibt `gewicht_bev` im Datensatz leer, und das Skript weist im Protokoll
ausdrücklich darauf hin.

**Was dafür gebraucht wird:** die Bevölkerung Österreichs zum 1. 1. 2026 nach
Alter und Geschlecht, aufgeteilt auf die fünf Bänder 18–29, 30–39, 40–49,
50–59, 60+. Die Quelle ist die Tabelle „Bevölkerung nach Alter und
Geschlecht" von Statistik Austria. Ich konnte sie aus dieser Arbeitsumgebung
nicht abrufen — `statistik.at` ist vom Netzwerk-Proxy gesperrt. Die oben
genannten Eckzahlen stammen aus einer Suchmaschinenzusammenfassung und sind
**vor Verwendung gegen die Originaltabelle zu prüfen**.

Eine Einschränkung aus dem Fragebogendesign: `alter` liegt nur kategorial vor
(Codebuch 3a). Eine Umgruppierung auf ein abweichendes Bandschema ist nicht
möglich. Die amtlichen Werte müssen daher auf genau diese fünf Bänder
aggregiert werden.

---

## 6. Datenqualität des Datensatzes

**Konsistenzprüfungen nach Codebuch, Abschnitt 5**

| Prüfung | Verstöße |
|---|---:|
| Kauf NEOH ohne gestützte Bekanntheit | 2 |
| „KEINE Marke" nicht exklusiv (drei Raster) | 0 |
| Kein einziges Kreuz bei `bekanntheit` | 0 |

Die zwei inkonsistenten Fälle sind nicht ausgeschlossen, weil zwei Fälle keine
Quote bewegen und ein Ausschluss die Kaufquote künstlich senken würde. Für die
Funnel-Darstellung schlage ich vor, die Stufen **hierarchisch** zu definieren
(Kauf nur unter Bekannten zu zählen) und die Abweichung in einer Fußnote zu
nennen.

**Fehlende Werte der Brand-Health-Slider.** Die fünf Slider stehen auf
„Antwort erbeten", nicht auf Antwortpflicht, und haben seit dem Entfernen der
Weiß-nicht-Kategorie keine Ausweichoption. Wer kein Urteil hat, klickt weiter.

| Slider | fehlend | von 287 NEOH-Kennern |
|---|---:|---:|
| `qualität` | 15 | 5,2 % |
| `plv` | 23 | 8,0 % |
| `emotion` | 24 | 8,4 % |
| `zufriedenheit` | 35 | 12,2 % |
| `wom` | 36 | 12,5 % |

Das Muster ist systematisch und inhaltlich plausibel: Ein Qualitätsurteil
trauen sich mehr Befragte zu als eine Weiterempfehlung. **Die Ausfälle sind
damit vermutlich nicht zufällig** (nicht MCAR), was für die Treiberanalyse
relevant ist — eine listenweise Fallausschlussrechnung über alle fünf Slider
verlöre rund ein Fünftel der Kenner und zöge die Stichprobe in Richtung der
Urteilssicheren. Ich schlage vor, paarweise zu rechnen und die Robustheit
gegen eine multiple Imputation zu prüfen.

**Panel-Rückleitung.** Die Panel-ID ist in allen 596 Fällen vorhanden, keine
doppelt. Der im September diagnostizierte Fehler (`PID` als Custom Value statt
aus der URL) ist im Feld nicht mehr aufgetreten.

---

## 7. Eckwerte der Nettostichprobe

Zur Einordnung, noch ungewichtet und ohne Interpretation:

| Funnel-Stufe | n | Anteil | 95-%-Intervall |
|---|---:|---:|---|
| NEOH bekannt | 287 | 50,6 % | 46,5 – 54,7 % |
| NEOH in Betracht | 76 | 13,4 % | 10,8 – 16,5 % |
| NEOH gekauft (3 Monate) | 49 | 8,6 % | 6,6 – 11,2 % |

Mit `gewicht_quote` verschiebt sich die Bekanntheit auf 53,3 %, die Kaufquote
bleibt bei 8,6 %. Beide Werte sind vorläufig, bis das Bevölkerungsgewicht
vorliegt — und beide dürften sich dann nach unten bewegen, weil die Älteren
unterrepräsentiert sind und NEOH in dieser Gruppe erfahrungsgemäß weniger
bekannt ist.

| Slider (nur Fälle mit Urteil) | n | M | SD |
|---|---:|---:|---:|
| `qualität` | 272 | 45,9 | 41,1 |
| `emotion` | 263 | 37,8 | 44,7 |
| `zufriedenheit` | 252 | 33,4 | 43,7 |
| `wom` | 251 | 11,4 | 31,7 |
| `plv` | 264 | 4,0 | 45,2 |

Skala −100 bis +100. Die Spannweite zwischen `qualität` und `plv` beträgt 42
Punkte auf derselben Skala.

Offene Angaben: 566 Spontannennungen (Median 21 Zeichen), 271 Beschreibungen
(Median 25 Zeichen).

---

## 8. Offene Punkte

**Datenschutz, vorrangig.** Das Repository `arnefloh-wu/NEOH` ist öffentlich.
Es enthält die Rohexporte beider Länder mit Panel-IDs, Demografie und offenen
Texten. Die Panel-ID ist ein Pseudonym, über das der Anbieter die Person
zuordnen kann; in Kombination mit Bundesland, Alter, Geschlecht, Einkommen und
Bildung ist das personenbezogen im Sinne der DSGVO. Zu klären mit der
WU-Datenschutzstelle, aber die naheliegenden Schritte sind: Repository auf
privat stellen, Rohdaten aus der Git-Historie entfernen (nicht nur löschen —
alte Commits bleiben sonst abrufbar) und künftig nur den pseudonymisierten
Analysedatensatz versionieren. Ich habe hier nichts davon getan, weil beides
Entscheidungen sind, die Sie treffen müssen, und das Entfernen aus der Historie
alle bestehenden Klone ungültig macht.

**Beim Panelanbieter nachzufordern**

1. Screen-out- und Abbruchzahlen. Ohne sie ist die Incidence Rate nicht
   berechenbar und der Methodenteil unvollständig. Der Export enthält
   ausschließlich abgeschlossene Interviews.
2. Die Solltabelle der Bundesland-Randquote.
3. Eine Erklärung zur Quotenabweichung, insbesondere zu den 73 statt 40
   Männern ab 60 — und ob die Überlieferung von 596 statt 500 Interviews
   abgerechnet wird.

**Vor der Auswertung zu entscheiden**

4. Amtliche Randverteilungen für `gewicht_bev` (Abschnitt 5).
5. Umgang mit den 45 reCAPTCHA-Fällen (Abschnitt 3).
6. Funnel-Definition: hierarchisch oder wie erhoben (Abschnitt 6).

---

## Erzeugte Dateien

| Datei | Inhalt |
|---|---|
| `NEOH_AT_analyse.csv` | 567 Fälle, 112 Variablen, ohne Panel-ID |
| `AUFBEREITUNG_AT_log.txt` | vollständiges Protokoll aller Schritte |
| `aufbereitung_at.py` | das Skript, parametrisiert und wiederholbar |
| `gewichtung_ziele_AT.csv` | Zielverteilungen, Spalte `soll_bevoelkerung` offen |

Der Analysedatensatz führt statt der Panel-ID eine studieninterne Laufnummer
(`AT0001` …). Die Labels stammen aus `NEOH_AT_Sep2026.qsf`, nicht aus einer
Kopie im Skript — Fragebogen und Aufbereitung können damit nicht
auseinanderlaufen.
