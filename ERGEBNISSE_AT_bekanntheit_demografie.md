# Markenbekanntheit nach Demografie — Österreich

Basis: 567 Fälle. Gestützte Werte gewichtet, Konfidenzintervalle nach Wilson auf
dem effektiven n. Reproduzierbar mit
`python3 analyse_bekanntheit_demografie_at.py`; vollständige Ausgabe in
`ERGEBNISSE_AT_bekanntheit_demografie.txt`, Tabelle in der zugehörigen `.csv`.

Regionen nach **NUTS-1**, nicht nach einer frei gezogenen Ost-West-Linie:
Ost (Wien, Niederösterreich, Burgenland), Süd (Steiermark, Kärnten), West
(Oberösterreich, Salzburg, Tirol, Vorarlberg).

---

## 1. Das Ergebnis vorweg

Von fünf geprüften Merkmalen tragen **zwei**. Alter und Geschlecht erklären die
Bekanntheit; Bildung, Einkommen und Region tun es nicht, sobald man für die
anderen kontrolliert.

| Prädiktor | b | SE | p | Odds |
|---|---:|---:|---:|---:|
| **Alter (Jahre)** | −0,0432 | 0,0072 | **<0,0001** | 0,958 |
| **weiblich** | 1,1789 | 0,1986 | **<0,0001** | **3,25** |
| Bildung (1–3) | 0,0659 | 0,1237 | 0,595 | 1,07 |
| Einkommen (1–6) | 0,0739 | 0,0687 | 0,282 | 1,08 |
| Region West | −0,4304 | 0,2287 | 0,060 | 0,65 |
| Region Süd | 0,1576 | 0,2762 | 0,568 | 1,17 |

*Logistische Regression auf die gestützte Bekanntheit, n = 499 (ohne „Keine
Angabe" beim Einkommen), Pseudo-R² = 0,123. Referenz der Region ist Ost.*

Zwei Zahlen zum Mitnehmen:

> **Zehn Jahre mehr Lebensalter senken die Chance auf Bekanntheit um 35 %.**
>
> **Frauen kennen NEOH mit 3,25-facher Chance** — bei gleichem Alter, gleicher
> Bildung, gleichem Einkommen und gleicher Region.

Der Geschlechtereffekt ist der stärkste einzelne Demografieeffekt der ganzen
Studie, und er ist kein Nebenprodukt von irgendetwas anderem.

---

## 2. Alter

| Altersgruppe | n | gestützt | 95-%-Intervall | ungestützt | Erinnerungsquote |
|---|---:|---:|---|---:|---:|
| 18–29 | 88 | **68,2 %** | 57,9 – 77,0 | 5,7 % | 8,3 % |
| 30–39 | 118 | 65,9 % | 57,0 – 73,9 | 6,8 % | 10,3 % |
| 40–49 | 108 | 52,3 % | 43,0 – 61,5 | 2,8 % | 5,3 % |
| 50–59 | 140 | 41,1 % | 33,3 – 49,4 | 4,3 % | 10,4 % |
| 60+ | 113 | **31,6 %** | 23,5 – 41,1 | 2,7 % | 8,4 % |

Ein Gefälle von **36,5 Prozentpunkten**, monoton über alle fünf Bänder. Die
Intervalle der Randgruppen überschneiden sich nicht.

Die Erinnerungsquote schwankt dagegen ohne Muster zwischen 5,3 und 10,4 %. Bei
drei bis acht Erinnerern je Gruppe ist das Rauschen — die Verankerung ist in
allen Altersgruppen ähnlich gut, nur die Basis unterscheidet sich.

---

## 3. Geschlecht

| | n | gestützt | 95-%-Intervall | ungestützt | Erinnerungsquote |
|---|---:|---:|---|---:|---:|
| Männlich | 293 | 43,4 % | 37,6 – 49,3 | 3,4 % | 7,9 % |
| Weiblich | 274 | **63,2 %** | 57,2 – 68,9 | 5,5 % | 8,7 % |

Knapp **20 Prozentpunkte** Unterschied, die Intervalle überschneiden sich nicht.
Und wie beim Alter: Die Erinnerungsquote ist praktisch gleich (7,9 gegen 8,7 %).
Frauen kennen die Marke häufiger, aber nicht *besser* — die Verankerung pro
Kenner ist dieselbe.

---

## 4. Region

| Region | n | gestützt | 95-%-Intervall |
|---|---:|---:|---|
| Ost | 288 | 52,4 % | 46,5 – 58,3 |
| Süd | 93 | 64,2 % | 53,7 – 73,5 |
| West | 186 | 49,2 % | 41,8 – 56,6 |

Die Intervalle überlappen durchgehend, und im multivariaten Modell trägt die
Region nichts (West p = 0,060, Süd p = 0,568). **Für eine Regionalaussage reicht
diese Stichprobe nicht**, und sie war auch nicht dafür ausgelegt — eine
Bundesland-Randquote wurde im Angebot erwähnt, aber nie als Solltabelle
vorgelegt (Feldbericht, Abschnitt 4).

Auf Bundeslandebene wird es noch dünner:

| Bundesland | n | gestützt | |
|---|---:|---:|---|
| Steiermark | 67 | 70,1 % | |
| Burgenland | 22 | 67,5 % | zu klein |
| Niederösterreich | 127 | 57,7 % | |
| Tirol | 42 | 52,7 % | |
| Salzburg | 21 | 51,8 % | zu klein |
| Oberösterreich | 104 | 49,4 % | |
| Kärnten | 26 | 48,5 % | zu klein |
| Wien | 139 | 44,9 % | |
| Vorarlberg | 19 | 37,0 % | zu klein |

Vier von neun Ländern haben unter 40 Fälle. Die Spanne von 37 bis 70 % sieht
nach einem Muster aus, ist aber mit Intervallen von ±20 Punkten vereinbar mit
„überall gleich". **Ich würde daraus keine regionale Mediaplanung ableiten.**

Eine Beobachtung, die der Erwähnung wert ist, weil sie der Intuition
widerspricht: Wien liegt mit 44,9 % am unteren Ende, nicht am oberen. Für eine
urbane, ernährungsbewusste Marke wäre das Gegenteil zu erwarten gewesen.

---

## 5. Bildung und Einkommen

| Bildung | n | gestützt | 95-%-Intervall | ungestützt |
|---|---:|---:|---|---:|
| Pflichtschule/Lehre | 239 | 49,2 % | 42,7 – 55,7 | 3,8 % |
| Matura | 160 | 58,3 % | 50,3 – 66,0 | 8,1 % |
| Hochschule | 152 | 53,9 % | 45,7 – 61,9 | 1,3 % |

| Haushaltseinkommen | n | gestützt | 95-%-Intervall |
|---|---:|---:|---|
| unter 1.000 € | 18 | 82,0 % | 58,3 – 93,7 *(zu klein)* |
| 1.000 – 1.999 € | 81 | 44,6 % | 33,9 – 55,8 |
| 2.000 – 2.999 € | 117 | 52,3 % | 43,0 – 61,4 |
| 3.000 – 3.999 € | 102 | 54,8 % | 44,9 – 64,4 |
| 4.000 – 4.999 € | 85 | 44,5 % | 34,0 – 55,5 |
| 5.000 € und mehr | 109 | 60,7 % | 51,0 – 69,7 |
| keine Angabe | 55 | 54,2 % | 40,7 – 67,1 |

**Beides trägt nicht.** Die Bildungsreihe ist nicht monoton — Matura liegt über
Hochschule —, und die Einkommensreihe springt ohne Richtung. Im multivariaten
Modell sind beide weit von Signifikanz entfernt.

Das ist ein inhaltlich brauchbares Ergebnis und keine Fehlanzeige: **NEOH ist
keine Akademikermarke und keine Einkommensmarke.** Die Bekanntheit verteilt
sich quer durch alle Schichten — begrenzt wird sie durch Alter und Geschlecht,
nicht durch Status.

Die auffällige Erinnerungsquote bei Matura (13,9 %) gegenüber Hochschule
(2,4 %) beruht auf 13 gegen 2 Spontannennungen. Das ist kein Befund.

---

## 6. Ist das Altersgefälle ungewöhnlich? Ja

Differenz der gestützten Bekanntheit zwischen 18–29 und 60+, je Marke:

| Marke | 18–29 | 60+ | Differenz |
|---|---:|---:|---:|
| More Nutrition | 48,9 % | 2,6 % | 46,2 |
| Corny | 85,2 % | 41,0 % | 44,2 |
| Pick Up! | 86,4 % | 45,2 % | 41,2 |
| **NEOH** | **68,2 %** | **31,6 %** | **36,5** |
| Kinder | 95,5 % | 67,1 % | 28,4 |
| Knoppers | 93,2 % | 73,1 % | 20,1 |
| Snickers | 95,5 % | 82,5 % | 13,0 |
| Hanuta | 76,1 % | 64,6 % | 11,6 |
| Balisto | 84,1 % | 76,2 % | 7,9 |
| Bounty | 94,3 % | 90,2 % | 4,1 |
| Mars | 95,5 % | 92,9 % | 2,5 |
| Milka | 94,3 % | 92,7 % | 1,6 |
| Manner | 93,2 % | 92,1 % | 1,0 |
| Dragee Keksi | 79,5 % | 82,2 % | −2,7 |

**NEOH liegt auf Rang 4 von 18, bei einem Median von 9,2 Prozentpunkten.**

Das Gesellschaft, in der NEOH sich befindet, ist aufschlussreich: More
Nutrition, Corny und Pick Up! — die funktionalen und modernen Snackmarken. Die
klassische Schokolade (Milka 1,6, Manner 1,0, Mars 2,5) ist altersneutral
bekannt.

Zwei Lesarten, und beide stimmen:

- **Positiv:** NEOH hat das Altersprofil seiner Kategorie, nicht das eines
  Nachzüglers. Marken wachsen über Kohorten, und die Marke besetzt die
  richtige.
- **Mahnend:** 60+ ist die größte Altersgruppe in Österreich und zugleich die,
  in der NEOH am schwächsten steht. Das ist der Grund, warum die
  Gewichtungsfrage aus dem Feldbericht Gewicht hat — der Kopfwert hängt genau
  daran.

---

## 7. Was daraus folgt

1. **Die Zielgruppenbeschreibung ist einfacher als erwartet.** Jünger und
   weiblich, sonst nichts. Keine Bildungs-, Einkommens- oder Regionalschnitte —
   das vereinfacht Mediaplanung und Zielgruppendefinition erheblich.
2. **Der Geschlechtereffekt verdient eine eigene Prüfung.** Odds 3,25 ist
   groß. Ob er auf Produkt, Kommunikation oder Kategorienutzung zurückgeht,
   beantwortet diese Welle nicht. Für Deutschland wäre das eine klare
   Hypothese, die sich mit n ≈ 1.000 sauber testen lässt.
3. **Regionalaussagen gehören nicht in den Bericht.** Die Stichprobe trägt sie
   nicht, und die fehlende Solltabelle des Anbieters macht es nicht besser.
4. **Die Älteren sind der eigentliche Hebel für Breite** — und zugleich der,
   bei dem die Relevanzfrage aus Stufe 3 am schärfsten steht. Eine Marke, die
   auf Zuckerreduktion positioniert ist, müsste dort eigentlich gut ankommen.
