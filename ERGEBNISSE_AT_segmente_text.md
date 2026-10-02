# Stufe 4 — Segmente und offene Angaben, Österreich

Basis: 567 Fälle, davon 287 NEOH-Kenner. Reproduzierbar mit
`python3 analyse_segmente_text_at.py`; vollständige Ausgabe in
`ERGEBNISSE_AT_segmente_text.txt`.

> **Zur Textauswertung:** Die Codierung erfolgt über Stichwortregeln, die im
> Skript stehen und damit prüfbar sind. Das ist kein Sprachmodell und keine
> manuelle Inhaltsanalyse. Trefferquoten werden ausgewiesen, nicht behauptet;
> nicht zugeordnete Texte sind gezählt und beispielhaft abgedruckt.

---

## 1. `zucker` ist eine Schwelle, kein Gradient

Stufe 1 zeigte einen Sprung zwischen den Stufen 3 und 4, Stufe 2 einen
monotonen Zusammenhang mit der Bewertung. Der Modellvergleich entscheidet:

**Tor 1 — Erwägung (n = 285)**

| Modell | LogLik | AIC | Pseudo-R² |
|---|---:|---:|---:|
| stetig (linear) | −155,98 | 315,97 | 0,044 |
| **dichotom (≥ 4)** | **−153,38** | **310,76** | **0,060** |
| fünf Stufen (Dummies) | −152,71 | 315,43 | 0,064 |

**Bekanntheit (n = 565)**

| Modell | LogLik | AIC | Pseudo-R² |
|---|---:|---:|---:|
| stetig (linear) | −388,23 | 780,46 | 0,009 |
| **dichotom (≥ 4)** | **−385,92** | **775,84** | **0,015** |
| fünf Stufen (Dummies) | −383,72 | 777,45 | 0,020 |

Auf beiden Toren hat die **dichotome Form die niedrigste AIC**. Die
Fünf-Stufen-Lösung passt zwar minimal besser (höheres Pseudo-R²), bezahlt das
aber mit drei zusätzlichen Parametern, die nichts hinzufügen.

**Konsequenz für Analyse und Slides:** `zucker` ≥ 4 als Segmentvariable
verwenden, nicht als stetige Kovariate. Das Segment umfasst 348 von 567
Befragten (61,4 %). Für die *Bewertung* bleibt der stetige Zusammenhang aus
Stufe 2 gültig (ρ = 0,270) — die Schwelle gilt fürs Verhalten, der Gradient
für die Einstellung.

---

## 2. Die ungestützte Bekanntheit entlarvt die gestützte

566 von 567 Befragten nannten spontan mindestens eine Schokoriegelmarke;
94,7 % der Antworten ließen sich einer Marke zuordnen.

| Marke | ungestützt | Top of Mind | im Raster? |
|---|---:|---:|:---:|
| Mars | 43,1 % | 21,2 % | ja |
| Milka | 37,6 % | 23,5 % | ja |
| Kinder | 31,4 % | 17,0 % | ja |
| **Twix** | **25,1 %** | 3,5 % | **nein** |
| Snickers | 23,9 % | 4,6 % | ja |
| Bounty | 20,5 % | 1,2 % | ja |
| Duplo | 11,1 % | 3,2 % | nein |
| Lindt | 7,6 % | 2,1 % | nein |
| Balisto | 7,4 % | 1,2 % | ja |
| KitKat | 6,9 % | 1,2 % | nein |
| … | | | |
| **NEOH** | **4,4 %** | **2,1 %** | ja |

> **NEOH kommt ungestützt auf 4,4 % — gegenüber 53,3 % gestützt.** Unter den
> 287 gestützten Kennern nennen nur 24 die Marke spontan, also **8,4 %**.

Das ist der schärfste Einzelbefund der ganzen Auswertung. Die gestützte
Bekanntheit misst *Wiedererkennung*; sie ist bei NEOH hoch. Die ungestützte
misst *Erinnerung*; sie ist niedrig. Elf von zwölf Kennern haben die Marke
nicht präsent, wenn sie an Schokoriegel denken.

Damit präzisiert sich der Engpass aus Stufe 1 noch einmal: Es geht nicht nur
darum, dass NEOH für viele nicht relevant ist, sondern dass es im
Entscheidungsmoment gar nicht erst im Kopf auftaucht. Ein Relevanzproblem und
ein Salienzproblem, nicht ein Reichweitenproblem.

Der Top-of-Mind-Wert von 2,1 % ist dabei bemerkenswert stabil relativ zur
ungestützten Nennung: Wer NEOH überhaupt erinnert, nennt es zur Hälfte zuerst.
Die kleine Gruppe, die die Marke präsent hat, hat sie *sehr* präsent.

### Eine Lücke im Markenraster

| Spontan genannt, nicht im gestützten Raster | Anteil |
|---|---:|
| Twix | 25,1 % |
| Duplo | 11,1 % |
| Lindt | 7,6 % |
| KitKat | 6,9 % |
| Milky Way | 5,7 % |
| Ritter Sport | 4,9 % |
| Lion | 4,6 % |
| Nussini | 4,1 % |
| Suchard | 3,9 % |
| Ferrero | 2,7 % |

**Twix ist die viertmeistgenannte Marke Österreichs und stand nicht im
Raster** — obwohl Mars, Snickers und Bounty desselben Herstellers drin sind.
Duplo ist in der deutschen Fassung enthalten, in der österreichischen nicht.

Für die bisherigen Befunde ist das weitgehend folgenlos: Die
Übergangsraten aus Stufe 1 werden je Marke auf der eigenen Kennerbasis
gebildet, nicht auf einem Anteil am Gesamtset. Relevant wird es für jede
Aussage über *Anteile am Relevant Set* und für eine Folgewelle. **Empfehlung:
Twix, Lindt, KitKat und Ritter Sport ins Raster aufnehmen, bevor das
Instrument erneut ins Feld geht.** Für Deutschland ist das vor Feldstart noch
möglich.

---

## 3. Wie Kenner die Marke beschreiben

266 von 287 Kennern (92,7 %) gaben eine auswertbare Beschreibung ab, im Median
25 Zeichen. Mehrfachcodierung möglich.

| Thema | n | Anteil |
|---|---:|---:|
| Zucker / zuckerfrei | 67 | 25,2 % |
| Geschmack positiv | 48 | 18,0 % |
| **Kennt es nicht / nie probiert** | **38** | **14,3 %** |
| Gesund / Ernährung | 34 | 12,8 % |
| Preis / teuer | 31 | 11,7 % |
| Innovativ / anders | 31 | 11,7 % |
| Protein / Eiweiß | 11 | 4,1 % |
| Nur Kategorie („ein Schokoriegel") | 10 | 3,8 % |
| Geschmack negativ | 8 | 3,0 % |
| Knusprig / Textur | 4 | 1,5 % |
| Verpackung / Optik | 4 | 1,5 % |
| Österreichisch / regional | 2 | 0,8 % |
| *(keinem Thema zugeordnet)* | *55* | *20,7 %* |

Die 20,7 % ohne Zuordnung sind überwiegend idiosynkratisch („Pappig", „einer
der immer da ist wenn man ihn braucht") — für regelbasierte Codierung eine
normale Restgröße, die ich nicht durch immer speziellere Regeln kleinrechnen
will.

### Der Befund in den Worten der Befragten

**14,3 % der Kenner können die Marke, die sie im Raster angekreuzt haben,
inhaltlich nicht beschreiben.** Rechnet man die zehn rein kategorialen
Beschreibungen hinzu, sind es 18,0 %. Und das trennt scharf:

| | Erwägungsquote |
|---|---:|
| kann die Marke nicht beschreiben (n = 38) | **5,3 %** |
| alle übrigen (n = 228) | **30,7 %** |

| | Erwägungsquote |
|---|---:|
| nennt Zucker als Merkmal (n = 67) | **41,8 %** |
| nennt ihn nicht (n = 199) | **22,1 %** |

Das ist der Relevanzbefund aus Stufe 1, dieselbe Aussage aus einer
unabhängigen Datenquelle und in den eigenen Worten der Befragten: **Wer das
Produktversprechen benennen kann, erwägt die Marke. Wer nur den Namen kennt,
nicht.**

Bemerkenswert auch, was *nicht* genannt wird. Nur 4,1 % erwähnen Protein,
obwohl das ein zentrales Produktmerkmal der Kategorie ist, und nur 0,8 % die
österreichische Herkunft. Zucker dominiert das Markenbild mit großem Abstand —
NEOH ist in den Köpfen die Zuckerreduktionsmarke und sonst wenig.

Der Preis taucht mit 11,7 % auch unaufgefordert in der Beschreibung auf. In
einer Frage, die nach dem *Wesen* der Marke fragt, ist das viel: Für jeden
achten Kenner gehört „teuer" zur Markendefinition.

---

## 4. Was Stufe 4 für das Reporting ändert

1. **Die Hauptbotschaft verschiebt sich.** Nicht „NEOH ist zur Hälfte
   bekannt", sondern „NEOH wird zur Hälfte wiedererkannt, aber nur von einem
   Zwölftel der Kenner erinnert". Beide Zahlen gehören auf dieselbe Folie,
   sonst entsteht ein zu günstiges Bild.
2. **Das Segment ist definiert**: `zucker` ≥ 4, 61,4 % der Stichprobe. Eine
   saubere, modellgestützte Schwelle statt einer gesetzten.
3. **Die Zuckerreduktion ist Stärke und Grenze zugleich.** Sie ist das einzige
   Merkmal, das im Markenbild verankert ist — und sie begrenzt die Erwägung
   auf jene, denen sie wichtig ist. Jede Empfehlung zur Verbreiterung muss an
   einem zweiten Merkmal ansetzen; Protein und Geschmack sind im Markenbild
   bisher praktisch nicht belegt.
4. **Eine Instrumentenkorrektur vor dem DE-Feld**: fehlende Marken ins Raster.

Damit sind die vier Analysestufen abgeschlossen. Was für die Slides noch
fehlt, ist die Entscheidung über das Bevölkerungsgewicht (Feldbericht,
Abschnitt 5) — alle Anteile hier sind quotengewichtet.
