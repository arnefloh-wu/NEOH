# Stufe 2 — Brand Health, Österreich

Basis: 287 NEOH-Kenner von 567 Befragten. Skala der fünf Slider −100 bis
+100, keine Ausweichoption. Reproduzierbar mit
`python3 analyse_brandhealth_at.py`; vollständige Kennwerte in
`ERGEBNISSE_AT_brandhealth.txt`, Index je Fall in
`ERGEBNISSE_AT_brandhealth.csv`.

---

## 1. Die Hypothese aus Stufe 1 trägt nicht

Ich hatte vermutet, die Erwägungsschwelle falle mit der
Preis-Leistungs-Wahrnehmung zusammen — die Schere zwischen `qualität`
(M = 46,2) und `plv` (M = 3,5) legte das nahe. **Die Daten sagen etwas
anderes.**

Vergleich der Kenner, die NEOH nicht erwägen, mit denen, die es erwägen:

| Slider | nicht erwägt | erwägt | Differenz | p |
|---|---:|---:|---:|---:|
| `zufriedenheit` | 19,9 | 63,0 | +43,1 | 4·10⁻¹⁵ |
| `emotion` | 25,8 | 67,7 | +41,9 | 2·10⁻¹⁵ |
| `qualität` | 34,3 | 73,2 | +38,9 | 2·10⁻¹⁶ |
| `wom` | 8,2 | 17,5 | +9,3 | 0,047 |
| **`plv`** | **−0,1** | **11,3** | **+11,4** | **0,079** |

`plv` ist der **einzige** Slider, der die beiden Gruppen nicht trennt. Emotion,
Qualität und Zufriedenheit unterscheiden sich um rund 40 Skalenpunkte mit
p < 10⁻¹⁴; der Preis um 11 Punkte, nicht signifikant.

Wer NEOH nicht in Betracht zieht, hält es also nicht für zu teuer — er hat
schlicht kein positives Markenurteil. Das ist eine andere Diagnose als die
naheliegende, und sie verschiebt die Handlungsempfehlung: Preisargumente
adressieren nicht den Engpass aus Stufe 1.

**Was die Preis-Qualitäts-Schere trotzdem ist.** Sie ist real und groß: paarweise
beträgt die Differenz M = 42,7 Punkte (SD = 44,9), t(261) = 15,38, d_z = 0,95,
und bei 77,1 % der Befragten liegt das Qualitätsurteil über dem Preisurteil.
Sie ist nur nicht das, was über Erwägung entscheidet. Sie beschreibt, wie die
Marke wahrgenommen wird — teuer, aber gut —, nicht, warum sie nicht auf die
Liste kommt.

---

## 2. Die Skala misst eine Dimension

| Faktor | Eigenwert | Zufallsdaten (Parallelanalyse) | |
|---|---:|---:|---|
| 1 | **3,114** | 1,277 | behalten |
| 2 | 0,769 | 1,134 | — |
| 3 | 0,599 | 1,042 | — |

Ein Faktor, 62,3 % der Varianz. Die Hauptachsenanalyse:

| Variable | Ladung | Kommunalität |
|---|---:|---:|
| `qualität` | 0,866 | 0,750 |
| `emotion` | 0,844 | 0,713 |
| `zufriedenheit` | 0,831 | 0,691 |
| `plv` | 0,608 | 0,369 |
| `wom` | **0,459** | **0,211** |

Drei Items bilden einen engen Kern (Interkorrelationen 0,68 bis 0,79), `plv`
hängt mäßig daran, `wom` nur schwach.

**Reliabilität:** α = 0,846, ω = 0,852 über alle fünf. Aufschlussreich ist,
was beim Weglassen passiert:

| | α | ω |
|---|---:|---:|
| alle fünf | 0,846 | 0,852 |
| ohne `wom` | **0,857** | **0,871** |
| ohne `plv` | 0,846 | 0,847 |
| ohne `qualität` | 0,786 | 0,789 |

`wom` ist das einzige Item, dessen Entfernung die Reliabilität **erhöht**.
Psychometrisch gehört es nicht in die Skala — inhaltlich ist das stimmig, denn
Weiterempfehlungsbereitschaft ist eine Verhaltensabsicht und damit eher
Ergebnis als Bestandteil der Markenwahrnehmung.

**Empfehlung:** Den Brand-Health-Index aus den vier Items `emotion`,
`qualität`, `plv`, `zufriedenheit` bilden und `wom` in Stufe 3 als eigene
abhängige Variable führen. Für die Zwei-Länder-Analyse ist diese Struktur
ohnehin auf Messinvarianz zu prüfen; eine Vier-Item-Lösung ist dafür die
bessere Ausgangslage.

Eine Einschränkung: Hauptachsenanalyse und Parallelanalyse sind explorativ.
Eine konfirmatorische Prüfung mit Fit-Indizes gehört in `lavaan` und sollte
spätestens beim Ländervergleich nachgezogen werden.

---

## 3. Die Niveaus

| Variable | n | M ungew. | M gew. | SD | 95-%-KI |
|---|---:|---:|---:|---:|---|
| `qualität` | 272 | 45,9 | 46,2 | 41,2 | 41,0 – 50,8 |
| `emotion` | 263 | 37,8 | 37,7 | 44,7 | 32,4 – 43,2 |
| `zufriedenheit` | 252 | 33,4 | 33,0 | 43,8 | 28,0 – 38,8 |
| `wom` | 251 | 11,4 | 11,4 | 31,8 | 7,5 – 15,3 |
| `plv` | 264 | 4,0 | 3,5 | 45,3 | −1,5 – 9,4 |

Das Konfidenzintervall von `plv` schließt die Null ein: Im Mittel ist das
Preis-Leistungs-Urteil **neutral**, nicht negativ. Die Marke wird nicht als zu
teuer verurteilt, sie wird preislich als unauffällig wahrgenommen — bei
gleichzeitig deutlich positivem Qualitätsurteil.

---

## 4. Die fehlenden Urteile verzerren nach oben

| Variable | fehlend | Anteil |
|---|---:|---:|
| `qualität` | 15 | 5,2 % |
| `plv` | 23 | 8,0 % |
| `emotion` | 24 | 8,4 % |
| `zufriedenheit` | 35 | 12,2 % |
| `wom` | 36 | 12,5 % |

Bei 53 Kennern (18,5 %) fehlt mindestens ein Urteil. Der im Feldbericht
geäußerte Verdacht bestätigt sich:

> Befragte mit mindestens einem fehlenden Urteil bewerten NEOH in den
> **übrigen** Slidern deutlich schlechter: M = 9,2 gegenüber M = 28,7 bei den
> vollständigen Fällen, t = 3,59, p = 0,001.

Wer kein Urteil abgibt, ist also nicht neutral, sondern tendenziell negativ.
**Die berichteten Mittelwerte sind damit nach oben verzerrt**, und zwar umso
stärker, je höher die Ausfallquote des Items. Für `wom` und `zufriedenheit`
mit über 12 % Ausfall gilt das am meisten.

Praktische Folgen: listenweiser Ausschluss ist keine Option, paarweise
Berechnung ist das Minimum, und für Stufe 3 sollte die Robustheit gegen eine
multiple Imputation geprüft werden. In den Slides gehört ein Hinweis darauf,
dass die Markenkennwerte eher die obere Grenze beschreiben.

---

## 5. Brand Health entlang des Funnels

| | n | `emotion` | `qualität` | `plv` | `zufriedenheit` | `wom` |
|---|---:|---:|---:|---:|---:|---:|
| Kenner, erwägt nicht | 213 | 25,8 | 34,3 | −0,1 | 19,9 | 8,2 |
| Erwäger, nicht gekauft | 35 | 63,9 | 73,7 | 21,4 | 59,2 | 17,3 |
| Käufer (3 Monate) | 47 | 70,5 | 72,8 | 4,1 | 65,8 | 17,6 |

Der große Sprung liegt zwischen Zeile 1 und 2 — genau dort, wo Stufe 1 den
Engpass verortet hat. Zwischen Erwägern und Käufern ist **keine** Differenz
statistisch gesichert (alle p > 0,11 bei n = 35 und 47).

Der Abstand bei `plv` (21,4 gegenüber 4,1) ist der auffälligste, aber mit
p = 0,119 nicht belastbar. Die Lesart läge nahe — man erwägt auf Qualität,
kauft, und findet den Preis dann hoch —, aber die Fallzahl trägt sie nicht.
Für Stufe 3 ist das eine zu prüfende Hypothese, kein Befund. Mit dem
deutschen Sample (n ≈ 1.000) wird die Gruppe groß genug sein.

**Brand-Health-Index** (ladungsgewichtetes Mittel der z-standardisierten
Items, paarweise, mindestens drei Urteile; berechenbar für 264 von 287):

| Gruppe | n | Index M |
|---|---:|---:|
| Kenner, erwägt nicht | 192 | −0,233 |
| Erwäger, nicht gekauft | 33 | +0,520 |
| Käufer | 47 | +0,507 |

Eine Stufe, kein Gefälle: Der Index trennt Erwägung, nicht Kauf.

---

## 6. Die Zuckermotivation färbt auch das Urteil

Nur unter Kennern — also bei Menschen, die die Marke bereits beurteilen können:

| `zucker` | n | Index | `qualität` | `plv` |
|---|---:|---:|---:|---:|
| 1 — gar nicht wichtig | 10 | −0,850 | 10,9 | −46,5 |
| 2 | 23 | −0,290 | 28,5 | 0,8 |
| 3 | 50 | −0,253 | 32,9 | −0,4 |
| 4 | 77 | +0,046 | 49,5 | 5,7 |
| 5 — sehr wichtig | 104 | +0,215 | 57,5 | 10,4 |

Rangkorrelation ρ = 0,270, p = 8·10⁻⁶ (n = 264).

Der Zusammenhang ist hier **monoton**, anders als bei der Erwägung in Stufe 1,
wo es eine Schwelle zwischen 3 und 4 gab. Das ist eine saubere Trennung:

- Die **Bewertung** steigt graduell mit der Zuckermotivation.
- Die **Erwägung** springt an einer Schwelle.

Mit anderen Worten: Alle werten NEOH umso besser, je wichtiger ihnen
Zuckerreduktion ist — aber erst ab einer gewissen Motivation schlägt das in
Verhalten um. Für Stufe 4 heißt das, dass `zucker` sowohl als stetige
Kovariate (für die Bewertung) als auch dichotomisiert (für die Erwägung)
sinnvoll ist.

Die Gruppe `zucker` = 1 bewertet mit `plv` = −46,5 extrem negativ, aber bei
n = 10 ist das keine belastbare Zahl.

---

## 7. Was in Stufe 3 zu prüfen ist

Die Fragestellung hat sich durch Abschnitt 1 verschoben. Nicht mehr „ist es
der Preis?", sondern:

1. **Was erzeugt das positive Markenurteil?** Der Index trennt Erwäger von
   Nicht-Erwägern fast perfekt, aber er ist selbst erklärungsbedürftig.
   Kandidaten aus dem Instrument: `bedürfnis`, `bedeutsam`, die Mediennutzung
   (`kanal`) und die Kaufhäufigkeit in der Kategorie (`haeufigkeit`).
2. **Logistische Regression auf die Erwägung** unter Kennern, mit dem
   Brand-Health-Index, `zucker`, `alter` und `einkommen`. Die Erwartung nach
   Stufe 2: Der Index dominiert, `plv` trägt nichts bei.
3. **Die Preisfrage an der richtigen Stelle.** Wenn `plv` nicht über Erwägung
   entscheidet, dann vielleicht über die Kaufhäufigkeit unter Käufern — dafür
   reicht das österreichische Sample nicht, das deutsche wird es.
4. **Die jüngste Altersgruppe** aus Stufe 1 (höchste Bekanntheit, niedrigster
   Kauf) gegen `plv` und `einkommen` prüfen. Nach den Befunden hier würde ich
   erwarten, dass sich der Effekt *nicht* über den Preis erklärt — aber genau
   deshalb ist er zu testen.

Für die Treibermodelle gilt die Warnung aus Abschnitt 4: paarweise rechnen,
Robustheit gegen multiple Imputation prüfen, und wegen der hohen
Interkorrelationen im Kern (bis 0,79) relative Gewichte statt roher
Regressionskoeffizienten.
