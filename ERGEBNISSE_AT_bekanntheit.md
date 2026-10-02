# Vertiefung — gestützte und ungestützte Markenbekanntheit, Österreich

Basis: 567 Fälle, davon 566 mit Spontannennung, 1.586 Markennennungen
insgesamt. Reproduzierbar mit `python3 analyse_bekanntheit_at.py`;
Kennwerte je Marke in `ERGEBNISSE_AT_bekanntheit.csv`.

---

## 1. Die Lücke ist normal — und NEOH schneidet darin überdurchschnittlich ab

In Stufe 4 stand der Kontrast nackt da: 53,3 % gestützt gegen 4,4 % ungestützt.
Das liest sich dramatisch, ist aber ohne Vergleichsmaßstab nicht zu bewerten.
Der richtige Maßstab ist die **Erinnerungsquote** — wie viel der
Wiedererkennung eine Marke in Erinnerung übersetzt:

> Erinnerungsquote = ungestützte Nennung ÷ gestützte Bekanntheit

| Marke | gestützt | ungestützt | Erinnerungsquote |
|---|---:|---:|---:|
| Mars | 94,0 % | 43,1 % | 45,9 % |
| Milka | 94,2 % | 37,6 % | 39,9 % |
| Kinder | 87,8 % | 31,4 % | 35,8 % |
| Snickers | 91,0 % | 23,9 % | 26,2 % |
| Bounty | 91,1 % | 20,5 % | 22,5 % |
| Balisto | 85,1 % | 7,4 % | 8,7 % |
| **NEOH** | **53,3 %** | **4,4 %** | **8,3 %** |
| Corny | 71,1 % | 5,7 % | 8,0 % |
| More Nutrition | 28,1 % | 1,8 % | 6,3 % |
| Knoppers | 87,8 % | 4,8 % | 5,4 % |
| AHEAD | 13,3 % | 0,7 % | 5,3 % |
| Manner | 89,4 % | 3,0 % | 3,4 % |
| Pick Up! | 72,0 % | 1,4 % | 2,0 % |
| Hanuta | 73,8 % | 0,7 % | 1,0 % |
| Dragee Keksi | 80,5 % | 0,0 % | 0,0 % |

**NEOH liegt auf Rang 7 von 18, über dem Median von 5,9 %.** Die Marke ist
also pro Einheit Bekanntheit *besser* im Gedächtnis verankert als Knoppers,
Manner, Pick Up!, Hanuta und Corny — alles Marken mit jahrzehntelanger
Präsenz und einer gestützten Bekanntheit um die 80 %.

Das korrigiert die Lesart aus Stufe 4 in einem wesentlichen Punkt: **Die
niedrige ungestützte Zahl ist kein Verankerungsproblem, sondern eine Folge der
kleineren Basis.** NEOH holt aus seiner Bekanntheit mehr heraus als die meisten
etablierten Marken — es hat nur weniger Bekanntheit, aus der es schöpfen kann.

Dragee Keksi ist der Gegenfall und verdeutlicht den Maßstab: 80,5 % gestützte
Bekanntheit, **null** Spontannennungen. Eine Marke, die jeder wiedererkennt
und niemand erinnert.

---

## 2. Wer NEOH erinnert, nennt es meist zuerst

| Marke | Top of Mind | TOM je Nennung | Median-Position |
|---|---:|---:|---:|
| Milka | 23,5 % | 62 % | 1,0 |
| Kinder | 17,0 % | 54 % | 1,0 |
| Mars | 21,2 % | 49 % | 2,0 |
| **NEOH** | **2,1 %** | **48 %** | **2,0** |
| Corny | 2,3 % | 41 % | 2,0 |
| Manner | 0,9 % | 29 % | 2,0 |
| Knoppers | 1,2 % | 26 % | 3,0 |
| Snickers | 4,6 % | 19 % | 2,0 |
| Balisto | 1,2 % | 17 % | 3,0 |
| Bounty | 1,2 % | 6 % | 3,0 |

„TOM je Nennung" ist der Anteil der Nennungen, bei denen die Marke
**zuerst** genannt wurde — ein Maß für Dominanz im Gedächtnis derjenigen, die
sie überhaupt erinnern.

Mit 48 % liegt NEOH auf dem Niveau von Mars (49 %) und deutlich über
Snickers (19 %) und Bounty (6 %). Bei den Menschen, die NEOH präsent haben,
ist es also **keine Randmarke, sondern die erste Assoziation**. Die Marke ist
bei wenigen verankert, dort aber tief.

---

## 3. Erinnerung ist nicht einfach ein Spiegel der Zuneigung

Das wäre der naheliegende Einwand: Wer die Marke mag, erinnert sie auch — und
erwägt sie deshalb. Die Daten sagen etwas anderes.

**Unter den 287 Kennern:**

| | n | erwägen NEOH |
|---|---:|---:|
| erinnern die Marke spontan | 24 | **62,5 %** |
| erkennen sie nur wieder | 263 | **22,4 %** |

t = 3,85, p = 0,0007.

Kontrolliert man das Markenurteil, bleibt der Effekt bestehen:

| Modell | n | Pseudo-R² | AIC |
|---|---:|---:|---:|
| nur Markenurteil | 260 | 0,210 | 246,4 |
| **Markenurteil + Erinnerung** | 260 | **0,250** | **236,0** |

| Prädiktor | b | SE | p | Odds |
|---|---:|---:|---:|---:|
| `bh_index` | 1,624 | 0,239 | <0,0001 | 5,07 |
| `erinnert` | **1,966** | 0,580 | **0,0007** | **7,14** |

Und umgekehrt: Erinnerer bewerten die Marke **nicht signifikant besser**.

| | erinnern | erkennen nur | Differenz | p |
|---|---:|---:|---:|---:|
| `emotion` | 52,0 | 36,4 | +15,6 | 0,053 |
| `zufriedenheit` | 48,1 | 32,1 | +16,1 | 0,112 |
| `qualität` | 57,3 | 44,8 | +12,5 | 0,153 |
| `wom` | 9,6 | 11,6 | −1,9 | 0,709 |
| `plv` | −0,8 | 4,4 | −5,1 | 0,592 |

> **Mentale Verfügbarkeit wirkt eigenständig, zusätzlich zur Einstellung.**
> Das ist der empirisch sauberste Beleg dieser Studie für die These, dass
> Präsenz im Entscheidungsmoment eine eigene Größe ist — und nicht bloß ein
> Nebenprodukt davon, dass man eine Marke gut findet.

Eine Einschränkung, die ich nicht kleinreden will: Die Gruppe der Erinnerer
umfasst **24 Fälle**. Der Effekt ist groß und signifikant, aber die Schätzung
ist entsprechend unsicher, und Kausalität lässt sich aus einem Querschnitt
ohnehin nicht ableiten — wer eine Marke erwägt, erinnert sie womöglich
deshalb. Das deutsche Sample wird hier vierfache Fallzahl liefern.

---

## 4. Wer NEOH nennt, kennt die Kategorie besser

Im Mittel nennen die Befragten 2,80 Marken (Median 3, Maximum 11). Ein Viertel
nennt nur eine einzige.

> Wer NEOH spontan nennt, nennt insgesamt **4,44** Marken; wer es nicht nennt,
> **2,73**. t = 4,58, p < 0,001.

NEOH wird also überproportional von Menschen mit hoher Kategoriekompetenz
genannt — es verdrängt keine andere Marke aus einem kurzen Set, sondern kommt
in längeren Sets vor. Zusammen mit dem TOM-Wert aus Abschnitt 2 ergibt das ein
konsistentes Bild: **eine Marke für Involvierte, bei denen sie dann aber ganz
vorne steht.**

Für die Interpretation der 4,4 % heißt das auch: Der Wert ist zum Teil ein
Artefakt der Abfrageform. Wer nur eine Marke nennt, nennt fast immer Milka,
Mars oder Kinder.

---

## 5. Wo die Erinnerung am besten funktioniert

| | n | gestützt | ungestützt | Erinnerungsquote |
|---|---:|---:|---:|---:|
| **Alter** | | | | |
| 18–29 | 88 | 68,2 % | 5,7 % | 8,3 % |
| 30–39 | 118 | 65,9 % | 6,8 % | **10,3 %** |
| 40–49 | 108 | 52,3 % | 2,8 % | 5,3 % |
| 50–59 | 139 | 41,4 % | 4,3 % | **10,4 %** |
| 60+ | 113 | 31,6 % | 2,7 % | 8,4 % |
| **Geschlecht** | | | | |
| Männlich | 292 | 43,5 % | 3,4 % | 7,9 % |
| Weiblich | 274 | 63,2 % | 5,5 % | 8,7 % |
| **Zuckerreduktion** | | | | |
| 1 — gar nicht wichtig | 27 | 41,7 % | 3,7 % | 8,9 % |
| 2 | 54 | 57,7 % | 1,9 % | 3,2 % |
| 3 | 136 | 40,3 % | 2,2 % | 5,5 % |
| 4 | 144 | 59,8 % | 4,2 % | 7,0 % |
| 5 — sehr wichtig | 203 | 58,2 % | 6,9 % | **11,8 %** |

Die höchste Erinnerungsquote liegt bei den stark Zuckerbewussten (11,8 %) —
dort, wo das Produktversprechen greift. Das bestätigt den Mediationsbefund aus
Stufe 3 auf einer weiteren Ebene: Relevanz erzeugt nicht nur Erwägung, sondern
auch Gedächtnisverankerung.

Die Altersgruppen 30–39 und 50–59 fallen mit je gut 10 % auf, die 40- bis
49-Jährigen mit 5,3 % ab. Bei Zellbesetzungen von rund 110 bis 140 Fällen und
drei bis acht Erinnerern je Gruppe würde ich daraus **kein Muster ableiten** —
das sind Schwankungen im Bereich weniger Personen.

---

## 6. Was das für die Interpretation ändert

1. **Die Salienz-Aussage bleibt, ihre Begründung ändert sich.** NEOH ist im
   Entscheidungsmoment selten präsent — aber nicht, weil die Marke schwach
   verankert wäre, sondern weil die Basis kleiner ist. Pro Einheit Bekanntheit
   arbeitet sie besser als die meisten etablierten Wettbewerber.
2. **Erinnerung ist ein eigener Hebel.** Sie erklärt Erwägung zusätzlich zum
   Markenurteil, mit einem Odds-Verhältnis von 7. Für die Steuerung heißt das:
   die ungestützte Bekanntheit als Leitindikator führen, nicht die gestützte.
3. **Das Wachstum liegt in der Breite der Bekanntheit, nicht in ihrer Tiefe.**
   Würde NEOH seine gestützte Bekanntheit von 53 auf 70 % steigern und die
   Erinnerungsquote halten, läge die ungestützte Nennung bei rund 5,8 % statt
   4,4 % — bei gleichbleibender Qualität der Verankerung.
4. **Dragee Keksi als Mahnung.** 80 % Bekanntheit bei null Erinnerung zeigen,
   dass Reichweite ohne Verankerung wertlos ist. NEOH hat das umgekehrte
   Profil, und das ist die bessere Ausgangslage.
