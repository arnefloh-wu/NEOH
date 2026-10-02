# Weitere Variablen — Österreich

Fünf Variablen waren in den Stufen 1 bis 4 nur Prädiktoren und nie in eigener
Form berichtet, drei weitere gar nicht. Hier werden sie nachgetragen.
Reproduzierbar mit `python3 analyse_weitere_at.py`; vollständige Ausgabe in
`ERGEBNISSE_AT_weitere.txt`.

---

## 1. Kaufabsicht

`intention`, Skala 1 (sehr unwahrscheinlich) bis 7 (sehr wahrscheinlich), nur
Kenner.

| Stufe | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Anteil | **39,5 %** | 14,3 % | 11,1 % | 11,2 % | 11,2 % | 6,6 % | 5,7 % |

M = 2,83 (gewichtet), Median 2.

**Vier von zehn Kennern schließen einen Kauf im nächsten Monat praktisch aus.**
Die Top-2-Box liegt bei 12,3 % der Kenner — bezogen auf die Gesamtbevölkerung
sind das **6,5 %**. Das deckt sich fast exakt mit der berichteten Kaufquote der
letzten drei Monate (8,2 %), was für die Konsistenz der beiden Maße spricht.

Erwäger kommen auf M = 4,61 gegenüber 2,32, Käufer auf 4,68 gegenüber 2,56.

---

## 2. Weiterempfehlung als NPS

`empfehlung`, Skala 0 bis 10, nur Kenner (n = 286).

| | Anteil | n |
|---|---:|---:|
| Promotoren (9–10) | 10,3 % | 32 |
| Passive (7–8) | 11,6 % | 35 |
| Detraktoren (0–6) | 78,0 % | 219 |

> **NPS = −68** über alle Kenner.

Diese Zahl darf nicht als Kundenzufriedenheit gelesen werden. Die NPS-Definition
unterstellt Kunden; hier antworten alle Kenner, auch die 239, die nie gekauft
haben. 93 von ihnen geben eine glatte 0 — bei einer Marke, die vier von fünf
Kennern nie gekauft haben, ist das erwartbar und kein Qualitätsurteil.

Unter den **Käufern** (n = 47) sieht es anders aus: 32,2 % Promotoren, 42,9 %
Detraktoren, **NPS = −11**. Immer noch kein guter Wert, aber eine andere
Größenordnung — und bei 47 Fällen mit entsprechender Unsicherheit.

Für die Berichterstattung: Wenn ein NPS genannt wird, dann der auf Käuferbasis
und mit der Fallzahl daneben. Der Wert über alle Kenner ist irreführend.

---

## 3. Bedürfniserfüllung und Bedeutsamkeit

Beide 0 bis 10, nur Kenner.

| | n | M | SD | Erwäger | übrige |
|---|---:|---:|---:|---:|---:|
| `bedürfnis` | 282 | 5,10 | 2,96 | **7,61** | 4,21 |
| `bedeutsam` | 285 | 2,83 | 2,96 | **5,16** | 2,01 |

Beide trennen hochsignifikant (t = 11,32 bzw. 8,08, p < 10⁻¹²). Das bestätigt
Stufe 3, wo die beiden zusammen über 90 % der erklärbaren Varianz des
Markenurteils trugen.

Als Schwellenwert gelesen:

> Wer die Bedürfniserfüllung mit **7 oder höher** bewertet (35,3 % der Kenner),
> erwägt NEOH zu **53,1 %**. Bei allen übrigen sind es **10,5 %**.

Das ist der schärfste Einzelschnitt in den gesamten Daten — schärfer als jedes
demografische Merkmal und schärfer als das Zuckersegment.

Bemerkenswert ist das Niveau von `bedeutsam`: M = 2,83 bei 102 Nullen. Für die
große Mehrheit der Kenner ist NEOH persönlich bedeutungslos. Bei einer
Snackmarke ist das normal und kein Alarmzeichen, aber es begrenzt, was
Markenbindungsmaßnahmen hier erreichen können.

---

## 4. Kategorienutzung

`haeufigkeit`, alle 567 Befragten.

| | Anteil | kennt NEOH | erwägt | gekauft |
|---|---:|---:|---:|---:|
| Täglich | 2,1 % | 56,9 % | 6,3 % | 6,3 % |
| Mehrmals pro Woche | 10,9 % | 41,6 % | 12,6 % | 5,8 % |
| Wöchentlich | 24,9 % | 59,9 % | 16,2 % | 10,6 % |
| Mehrmals pro Monat | 29,0 % | 56,2 % | 14,0 % | 10,5 % |
| Monatlich | 18,8 % | 48,9 % | 12,2 % | 8,1 % |
| Seltener | 13,0 % | 50,7 % | 16,6 % | 4,6 % |
| Nie | 1,3 % | 45,1 % | 0,0 % | 0,0 % |

**Hier steht ein Nullbefund, und er ist aufschlussreich.** Wer wöchentlich oder
häufiger Riegel kauft (37,9 % der Bevölkerung), kennt NEOH zu 54,5 % und kauft
es zu 9,0 %. Bei allen anderen sind es 52,6 % und 8,3 %. Kein Unterschied.

Schwere Kategorienutzer sind also **nicht** die naheliegende Zielgruppe. Das
passt zum Relevanzbefund: NEOH wird nicht über die Kategorie erschlossen,
sondern über die Zuckermotivation — und die ist von der Kaufhäufigkeit
unabhängig.

---

## 5. Die drei Timing-Fragen

Zeit bis zum Absenden der Seite, in Sekunden.

| Seite | n | P25 | Median | P75 | P95 |
|---|---:|---:|---:|---:|---:|
| Spontannennung | 567 | 14 | 24 | 40 | 98 |
| **Markenraster** | 567 | 46 | **58** | 72 | 111 |
| Markensentiment | 287 | 20 | 28 | 40 | 67 |

Das Markenraster ist die teuerste Seite — 21 Marken in drei Fragen — und macht
allein rund ein Drittel der gesamten Bearbeitungszeit aus. Für eine
Instrumentenkürzung wäre das der erste Ansatzpunkt. Die deutsche Fassung mit
24 Marken wird hier entsprechend länger brauchen.

**Validierung des Speeder-Kriteriums.** Die Zeit am Markenraster korreliert
positiv mit der Zahl der angekreuzten Marken (ρ = 0,217, p < 10⁻⁶). Die
schnellsten 10 % (unter 36 Sekunden) kreuzen im Mittel 8,2 Marken an, alle
übrigen 11,7.

Das spricht dafür, dass die Zeit tatsächlich Verarbeitung misst und nicht bloß
Zögern — und stützt damit die Verwendung der Gesamtdauer als Speeder-Kriterium
im Feldbericht. Ein Gegenbefund wäre gewesen, wenn Schnelle genauso viele
Marken angekreuzt hätten: Dann hätte die Zeit nichts über die Sorgfalt gesagt.

---

## 6. Was jetzt vollständig ausgewertet ist

| Variable | Ausgewertet in |
|---|---|
| `bekanntheit`, `betracht`, `kauf_3monate` | Stufe 1, Pyramide |
| `spontan` | Stufe 4, Bekanntheitsvertiefung |
| `beschreibung` | Stufe 4 |
| `emotion`, `qualität`, `plv`, `zufriedenheit`, `wom` | Stufe 2 |
| `bedürfnis`, `bedeutsam` | Stufe 3, hier Abschnitt 3 |
| `intention` | hier Abschnitt 1 |
| `empfehlung` | Pyramide, hier Abschnitt 2 |
| `H1` | Stufe 3 |
| `kanal` | `ERGEBNISSE_AT_kanaele.md` |
| `haeufigkeit` | hier Abschnitt 4 |
| `zucker` | Stufe 1, 2, 4 |
| `alter`, `geschlecht`, `bundesland`, `bildung`, `einkommen` | Demografie |
| `attention` | Feldbericht |
| `t_spontan`, `t_raster`, `t_sentiment` | hier Abschnitt 5 |

Nicht ausgewertet bleibt `einleitung` — das ist der Begrüßungstext, keine Frage.
