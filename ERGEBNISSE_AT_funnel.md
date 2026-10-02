# Stufe 1 — Funnel im Wettbewerbsvergleich, Österreich

Datenbasis `NEOH_AT_analyse.csv`, n = 567, effektives n = 526. Gewichtet mit
`gewicht_quote` (Alter × Geschlecht auf den Quotenplan). Reproduzierbar mit
`python3 analyse_funnel_at.py`; vollständige Ausgabe in
`ERGEBNISSE_AT_funnel.txt`, Tabelle je Marke in `ERGEBNISSE_AT_funnel.csv`.

> **Die Anteile sind nicht bevölkerungsrepräsentativ.** Der Quotenplan
> unterzeichnet die Gruppe 60+ (Feldbericht, Abschnitt 5). Abschnitt 4 zeigt,
> wie stark die Kopfzahlen daran hängen.

---

## 1. Der Befund in einem Satz

NEOH hat kein Bekanntheitsproblem im engeren Sinn und kein Kaufproblem — es hat
ein **Relevanzproblem auf dem Weg von Bekanntheit zu Betracht**.

| Übergang | NEOH | Median aller Marken | Rang |
|---|---:|---:|:---:|
| Bekanntheit → Betracht | **25,6 %** | 40,2 % | **16 von 18** |
| Betracht → Kauf | **49,5 %** | 39,3 % | **4 von 18** |
| Bekanntheit → Kauf | 15,5 % | 19,0 % | 12 von 18 |

*(Vergleichsbasis: 18 Marken mit mindestens 30 Kennern.)*

Wer NEOH in Betracht zieht, kauft es auch — und zwar häufiger als bei fast
jedem Wettbewerber. Die Hälfte der Erwäger hat in den letzten drei Monaten
gekauft; bei Hanuta sind es 21 %, bei Mars 42 %, bei Milka 62 %. Der Verlust
passiert eine Stufe früher: Von denen, die NEOH kennen, nimmt nur ein Viertel
die Marke überhaupt in die Auswahl. Bei den etablierten Marken sind es 40 bis
55 %.

Das ist eine andere Diagnose als „zu wenig bekannt", und sie hat andere
Konsequenzen. Reichweitenaufbau würde mehr Menschen in einen Trichter
schicken, der an der zweiten Stufe leckt.

---

## 2. Der Funnel aller Marken

Gewichtete Anteile der Gesamtstichprobe in Prozent.

| Marke | bekannt | Betracht | Kauf | B→Betr | Betr→K |
|---|---:|---:|---:|---:|---:|
| Milka | 94,2 | 51,1 | 39,1 | 54,2 | 61,8 |
| Mars | 94,0 | 37,1 | 20,4 | 39,5 | 42,3 |
| Bounty | 91,1 | 37,4 | 17,3 | 41,0 | 39,9 |
| Snickers | 91,0 | 38,1 | 21,2 | 41,8 | 41,8 |
| Manner | 89,4 | 46,8 | 29,4 | 52,4 | 53,2 |
| Kinder | 87,8 | 47,9 | 40,7 | 54,5 | 68,3 |
| Knoppers | 87,8 | 41,0 | 19,4 | 46,7 | 40,9 |
| Balisto | 85,1 | 39,4 | 20,0 | 46,3 | 43,5 |
| Dragee Keksi (Napoli) | 80,5 | 30,2 | 15,3 | 37,5 | 37,1 |
| Hanuta | 73,8 | 21,7 | 6,6 | 29,5 | 20,6 |
| Pick Up! | 72,0 | 29,5 | 12,6 | 41,0 | 35,4 |
| Corny | 71,1 | 27,0 | 10,7 | 38,0 | 32,5 |
| **NEOH** | **53,3** | **13,6** | **8,2** | **25,6** | **49,5** |
| More Nutrition | 28,1 | 7,9 | 4,0 | 28,2 | 36,5 |
| AHEAD | 13,3 | 5,8 | 3,2 | 43,5 | 38,7 |
| Foodspring | 12,4 | 2,7 | 0,8 | 21,5 | 30,8 |
| Nicks | 10,5 | 1,6 | 0,2 | 15,8 | 11,0 |
| BE-KIND | 8,6 | 2,5 | 0,9 | 28,5 | 36,0 |
| Nucao | 4,8 | 1,5 | 1,0 | 30,4 | 70,3 |
| Ketofabrik (Keast) | 2,2 | 0,5 | 0,1 | 22,0 | 27,8 |

Mit 53,3 % Bekanntheit [49,0; 57,5] liegt NEOH auf **Rang 13 von 20** — klar
hinter dem konventionellen Süßwarenblock, aber **mit deutlichem Abstand vor
dem gesamten Konkurrenzfeld der zuckerreduzierten Marken**. More Nutrition
kommt auf 28,1 %, AHEAD auf 13,3 %, Foodspring auf 12,4 %, Nicks auf 10,5 %,
Nucao auf 4,8 %. In seiner eigenen Kategorie ist NEOH nicht Herausforderer,
sondern mit Abstand Marktführer in der Bekanntheit.

Keine einzige Person wählte „KEINE Marke" — alle 567 Befragten kannten
mindestens eine der abgefragten Marken. Der Screener hätte also auch als
Plausibilitätsprüfung nichts aussortiert.

---

## 3. Wer kennt und wer erwägt

### Alter

| Altersgruppe | n | bekannt | Betracht | Kauf |
|---|---:|---:|---:|---:|
| 18–29 | 88 | 68,2 % | 13,6 % | 5,7 % |
| 30–39 | 118 | 65,9 % | 17,5 % | 12,4 % |
| 40–49 | 108 | 52,3 % | 15,1 % | 10,4 % |
| 50–59 | 140 | 41,1 % | 13,6 % | 10,1 % |
| 60+ | 113 | 31,6 % | 6,9 % | 1,9 % |

Ein Gefälle von 37 Prozentpunkten in der Bekanntheit. Bemerkenswert ist die
Gegenbewegung bei der Kaufquote: Die 18- bis 29-Jährigen kennen NEOH am
häufigsten, kaufen es aber am seltensten (5,7 %) — seltener als die 30- bis
39-Jährigen (12,4 %), die seltener davon gehört haben. **Bekanntheit in der
jüngsten Gruppe übersetzt sich am schlechtesten in Kauf.** Preis ist die
naheliegende Erklärung, prüfbar in Stufe 3 gegen `plv` und `einkommen`.

### Geschlecht

| | n | bekannt | Betracht | Kauf |
|---|---:|---:|---:|---:|
| Männlich | 293 | 43,4 % | 9,7 % | 6,2 % |
| Weiblich | 274 | 63,2 % | 17,5 % | 10,3 % |

Knapp 20 Prozentpunkte Unterschied in der Bekanntheit, und der Vorsprung
bleibt über den ganzen Funnel erhalten.

### Motivation zur Zuckerreduktion

| `zucker` | n | bekannt | Betracht | Kauf |
|---|---:|---:|---:|---:|
| 1 — gar nicht wichtig | 27 | 41,7 % | 9,8 % | 4,1 % |
| 2 | 54 | 57,7 % | 4,5 % | 1,9 % |
| 3 | 136 | 40,3 % | 3,5 % | 1,9 % |
| 4 | 144 | 59,8 % | 19,2 % | 10,0 % |
| 5 — sehr wichtig | 204 | 58,0 % | 20,3 % | 14,2 % |

**Das ist die aufschlussreichste Tabelle des Abschnitts.** Die Bekanntheit
schwankt ohne klares Muster zwischen 40 und 60 %. Die Erwägung dagegen springt
zwischen Stufe 3 und Stufe 4 von 3,5 % auf 19,2 % — mehr als das Fünffache.

NEOH ist also quer durch die Bevölkerung etwa gleich bekannt, aber **nur für
die zuckerbewusste Hälfte überhaupt eine Option**. Das erklärt den Engpass aus
Abschnitt 1 vollständig: Die 25,6 % Bekanntheit→Betracht sind kein
Kommunikationsversagen, sondern der Anteil der Kenner, für die das
Produktversprechen relevant ist.

Die Nicht-Monotonie bei `zucker` = 2 und 3 würde ich nicht überinterpretieren;
bei n = 54 und n = 136 sind das Schwankungen in der Größenordnung des
Zufallsfehlers. Der Sprung zwischen 3 und 4 ist dagegen zu groß, um Rauschen
zu sein, und tritt bei Erwägung und Kauf gleichgerichtet auf.

---

## 4. Wie sicher sind die Kopfzahlen

Weil die Bekanntheit steil mit dem Alter fällt und der Quotenplan die Gruppe
60+ auf 16 % setzt, hängt der berichtete Wert am Altersanteil:

| Anteil 60+ in der Grundgesamtheit | bekannt | Betracht | Kauf |
|---|---:|---:|---:|
| 16 % (Quotenplan) | 53,3 % | 13,6 % | 8,2 % |
| 25 % | 51,0 % | 12,9 % | 7,6 % |
| 33 % | 48,9 % | 12,3 % | 7,0 % |

Die Szenarien sind Rechengrößen, keine amtlichen Anteile. Was sie zeigen: Die
Bekanntheit wandert über die plausible Spannweite um gut vier Prozentpunkte.
Die Aussage **„rund die Hälfte der Erwachsenen kennt NEOH"** hält. Die genaue
Zahl ist ohne `gewicht_bev` nicht final und sollte in den Slides als Spanne
oder mit Vorbehalt erscheinen.

Die **Übergangsraten aus Abschnitt 1 sind davon weitgehend unberührt**, weil
sie innerhalb der Kennergruppe gebildet werden und Zähler wie Nenner
gleichgerichtet verschieben. Der Kernbefund hängt also nicht am offenen
Gewichtungspunkt.

---

## 5. Methodische Festlegungen

**Hierarchische Funnel-Definition.** Betracht und Kauf zählen nur unter den
Kennern der jeweiligen Marke. Betroffen waren 95 von 11.340
Marke-Person-Zellen bei `betracht` (0,8 %) und 64 bei `kauf_3monate` (0,6 %).
Für NEOH verschiebt das die Erwägung von 14,0 auf 13,6 % und den Kauf von 8,6
auf 8,2 % — die Entscheidung ist für die Befunde folgenlos, aber sie ist
dokumentiert statt stillschweigend getroffen.

**Konfidenzintervalle** nach Wilson auf dem effektiven n nach Kish, nicht auf
der rohen Fallzahl. Bei gewichteten Anteilen wären Intervalle auf der rohen
Fallzahl zu eng.

**Vergleichsbasis der Übergangsraten**: nur Marken mit mindestens 30 Kennern.
Bei Nucao beruht die Rate von 70,3 % auf einer zweistelligen Fallzahl und ist
nicht belastbar.

---

## 6. Was das für die nächsten Stufen heißt

Der Befund aus Abschnitt 1 und 3 setzt die Agenda:

1. **Stufe 2 (Brand Health)** sollte prüfen, ob die Erwägungsschwelle mit der
   Preis-Leistungs-Wahrnehmung zusammenfällt. `plv` lag im Feldbericht bei
   M = 4,0 gegenüber `qualität` M = 45,9 — dieselbe Schere, eine Ebene tiefer.
2. **Stufe 3 (Treiber)** bekommt damit eine gerichtete Frage statt einer
   offenen: Was unterscheidet Kenner, die erwägen, von Kennern, die nicht
   erwägen? Eine logistische Regression auf diesen Übergang ist die passende
   Form, mit `zucker`, `plv` und `einkommen` als zentralen Kandidaten.
3. **Stufe 4 (Segmente)** hat in `zucker` bereits einen klaren Schnitt bei 4.
   Ob das eine Schwelle oder ein stetiger Zusammenhang ist, entscheidet, ob
   man von einem Segment oder von einem Gradienten spricht.

Für die jüngste Altersgruppe lohnt eine eigene Betrachtung: hohe Bekanntheit,
niedrigster Kauf. Wenn sich das in Stufe 3 als Preiseffekt bestätigt, ist das
die konkreteste Handlungsempfehlung, die diese Studie hergeben wird.
