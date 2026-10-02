# Stufe 3 — Treiber und die beiden Tore des Funnels, Österreich

Basis: 287 NEOH-Kenner, davon 74 Erwäger und 47 Käufer. Reproduzierbar mit
`python3 analyse_treiber_at.py`; alle Kennwerte in
`ERGEBNISSE_AT_treiber.txt`.

> **Varianzzerlegung, keine Kausalität.** `bedürfnis`, `bedeutsam` und die
> Brand-Health-Slider sind zeitgleich erhobene Einstellungsmaße. Relative
> Gewichte nach Johnson, weil die Prädiktoren bis r = 0,79 interkorrelieren
> und rohe Regressionskoeffizienten dann nicht mehr sinnvoll zu lesen sind.

---

## 1. Die Preisfrage löst sich auf — an der richtigen Stelle

Stufe 2 hatte gezeigt, dass der Preis nicht entscheidet, ob jemand NEOH in
Betracht zieht. Stufe 3 zeigt, wo er dann doch entscheidet. Die Frage `H1`
geht an Erwäger, die zuletzt nicht gekauft haben (n = 35):

| Genannte Barriere | n | Anteil |
|---|---:|---:|
| **Zu teuer** | **19** | **54,3 %** |
| Nie im Angebot | 9 | 25,7 % |
| Sonstiges | 9 | 25,7 % |
| Haushalt bevorzugt sie nicht | 7 | 20,0 % |
| Nicht im bevorzugten Geschäft | 3 | 8,6 % |
| Begrenzte Geschmacksauswahl | 3 | 8,6 % |
| Sehe ich nie im Regal | 2 | 5,7 % |
| Packungsgröße fehlt | 1 | 2,9 % |
| Weiß nicht genug darüber | 1 | 2,9 % |

Damit fügt sich das Bild zusammen, und der scheinbare Widerspruch zwischen
Stufe 2 und der Preis-Qualitäts-Schere verschwindet:

> **Tor 1 (Bekanntheit → Betracht) entscheidet das Markenurteil. Tor 2
> (Betracht → Kauf) entscheidet der Preis.** Der Preis bestimmt nicht, ob
> NEOH auf die Liste kommt — sondern ob es vom Regal in den Korb wandert.

Und beide Maße stützen sich gegenseitig: Wer „zu teuer" nennt, bewertet auch
`plv` schlechter (M = 7,9 gegenüber 37,5), t = −2,01, p = 0,054. Bei n = 33
ist das knapp an der Konvention — als Beleg für die konvergente Validität des
Sliders taugt es, als gesicherter Befund nicht.

Zwei Nennungen hinter dem Preis verdienen Beachtung, weil sie konkret
adressierbar sind: **„Nie im Angebot"** (25,7 %) und **„Nicht im bevorzugten
Geschäft / Sehe ich nie im Regal"** (zusammen 14,3 %). Das sind
Distributions- und Promotionsfragen, keine Markenfragen.

Bei n = 35 ist die Rangfolge der ersten beiden Nennungen deutlich, alles
darunter bewegt sich im Bereich weniger Fälle. Das deutsche Sample wird hier
belastbare Zahlen liefern.

---

## 2. Was das Markenurteil erzeugt

Abhängige: Brand-Health-Index aus vier Items (ohne `wom`, nach der Empfehlung
aus Stufe 2). n = 258, R² = 0,581.

| Prädiktor | rel. Gewicht | Anteil an R² | r mit Index |
|---|---:|---:|---:|
| `bedürfnis` | 0,320 | **55,0 %** | +0,730 |
| `bedeutsam` | 0,214 | **36,7 %** | +0,650 |
| `zucker` | 0,044 | 7,6 % | +0,311 |
| `alter` | 0,003 | 0,5 % | +0,051 |
| `haeufigkeit` | 0,001 | 0,2 % | −0,054 |
| `einkommen` | 0,000 | 0,0 % | −0,001 |

Über neunzig Prozent der erklärten Varianz entfallen auf zwei Variablen:
**Bedürfniserfüllung** und **persönliche Bedeutsamkeit**. Demografie trägt
nichts bei — `einkommen` liegt exakt bei null.

Das ist weniger trivial, als es zunächst klingt. `bedürfnis` fragt „Inwieweit
erfüllt NEOH Ihre Bedürfnisse bei Schokoladen-/Snackriegeln?" — das ist ein
**Passungsurteil, kein Qualitätsurteil**. Die Marke wird gut bewertet, wenn
sie zum eigenen Bedarf passt, nicht wenn sie für objektiv gut gehalten wird.
Das deckt sich mit Stufe 1: NEOH ist breit bekannt, aber nur für einen Teil
relevant.

---

## 3. Tor 1 — wer erwägt NEOH

Logistische Regression, Basis Kenner.

**Modell A** (n = 260, Pseudo-R² = 0,220)

| | b | SE | p | Odds |
|---|---:|---:|---:|---:|
| `bh_index` | 1,506 | 0,237 | <0,0001 | **4,51** |
| `zucker` | 0,282 | 0,175 | 0,107 | 1,33 |
| `alter` | −0,094 | 0,128 | 0,464 | 0,91 |
| `einkommen` | 0,035 | 0,096 | 0,715 | 1,04 |
| `haeufigkeit` | 0,006 | 0,134 | 0,967 | 1,01 |

Das Markenurteil dominiert: Eine Standardabweichung mehr vervierfacht die
Chance auf Erwägung. Alles andere trägt nichts bei.

**Bemerkenswert ist, was mit `zucker` passiert.** In Stufe 1 war die
Zuckermotivation der stärkste Prädiktor der Erwägung (Sprung von 3,5 % auf
19,2 %). Sobald der Markenindex im Modell steht, verliert sie ihre Wirkung
(p = 0,107). Zusammen mit der Rangkorrelation aus Stufe 2 (ρ = 0,270) ist das
**das Muster einer Mediation**: Die Zuckermotivation wirkt nicht neben dem
Markenurteil, sondern durch es hindurch. Ein formaler Mediationstest wäre der
nächste Schritt; mit dem deutschen Sample lässt er sich sauber rechnen.

**Modell B** (nur die Slider, n = 245, Pseudo-R² = 0,317)

| | b | SE | p |
|---|---:|---:|---:|
| `zufriedenheit` | 0,030 | 0,007 | 0,0001 |
| `qualität` | 0,020 | 0,009 | 0,027 |
| `emotion` | 0,005 | 0,007 | 0,526 |
| `plv` | **−0,015** | 0,005 | **0,001** |

Der negative `plv`-Koeffizient ist eine **Suppression**, kein Befund.
Bivariat hängt `plv` mit der Erwägung praktisch nicht zusammen (Stufe 2:
+11,4 Punkte, p = 0,079); erst unter Kontrolle der drei anderen Slider dreht
das Vorzeichen. Bei Interkorrelationen bis 0,79 ist das zu erwarten.
Inhaltlich darf daraus **nicht** gelesen werden, dass ein besseres Preisurteil
die Erwägung senkt. Der belastbare Teil des Modells: `zufriedenheit` und
`qualität` tragen Tor 1, `plv` trägt nichts bei.

---

## 4. Tor 2 — wer kauft

Logistische Regression, Basis Erwäger. n = 72, davon 39 Käufer.

| | b | SE | p |
|---|---:|---:|---:|
| `plv` | −0,005 | 0,005 | 0,304 |
| `einkommen` | 0,094 | 0,154 | 0,541 |
| `haeufigkeit` | −0,098 | 0,210 | 0,641 |

**Nichts wird signifikant.** Bei 72 Fällen und drei Prädiktoren ist das
erwartbar; das Modell steht hier als Hinweis, nicht als Befund. Die
Selbstauskunft aus Abschnitt 1 ist für Tor 2 derzeit die belastbarere Quelle.

Dass `plv` auch hier nicht trägt, während über die Hälfte der Nichtkäufer
„zu teuer" nennt, ist kein Widerspruch: Der Slider misst das *Verhältnis* von
Preis und Leistung, die H1-Nennung die *konkrete Kaufbarriere*. Ein Produkt
kann seinen Preis wert sein und trotzdem zu teuer für den Anlass. Für das
deutsche Sample mit vierfacher Fallzahl ist das die interessanteste zu
prüfende Unterscheidung.

---

## 5. Die jüngste Altersgruppe bleibt ungeklärt

Stufe 1 hatte das Rätsel aufgeworfen: Die 18- bis 29-Jährigen kennen NEOH am
häufigsten (68,2 %), kaufen es aber am seltensten (5,7 %). Die drei
naheliegenden Erklärungen halten nicht:

| 18–29 gegen 30–59 | M | M | t | p |
|---|---:|---:|---:|---:|
| `plv` | −1,3 | 3,2 | −0,66 | 0,509 |
| `bh_index` | −0,08 | 0,02 | −0,67 | 0,506 |
| `einkommen` | 4,22 | 4,33 | −0,36 | 0,717 |

Die jüngste Gruppe bewertet NEOH nicht schlechter, hält es nicht für teurer
und hat kein geringeres Einkommen. **Der Befund bleibt offen** — was sich
ausschließen lässt, ist eine Preis- oder Budgeterklärung.

Eine Vermutung, die das Instrument nicht prüfen kann: Die jüngste Gruppe
könnte später in Kontakt gekommen sein und sich noch früher in der
Adoptionskurve befinden. Bekanntheit wäre dann vorhanden, Kaufroutine noch
nicht. Das wäre mit einer Wiederholungsmessung prüfbar, nicht mit dieser
Welle.

---

## 6. Kontaktkanäle

Nur Kenner, letzter Monat. **Endogen** — wer die Marke erwägt, nimmt sie auch
eher wahr. Keine Werbewirkungsaussage.

| Kanal | n | Anteil |
|---|---:|---:|
| Supermarkt (Regal, Display) | 131 | 45,6 % |
| In keinem dieser Kanäle | 70 | 24,4 % |
| Instagram/Facebook | 64 | 22,3 % |
| TV-Werbung | 40 | 13,9 % |
| Printwerbung | 28 | 9,8 % |
| Werbung auf Websites | 24 | 8,4 % |
| Mundpropaganda | 22 | 7,7 % |

Der Handel ist der mit Abstand wichtigste Kontaktpunkt — was zur
H1-Nennung „Nie im Angebot" passt und die Distributions- und Promotionsebene
weiter aufwertet.

---

## 7. Das Gesamtbild nach drei Stufen

```
Bekanntheit 53 %
     │
     │  TOR 1 — Markenurteil entscheidet
     │  bedürfnis + bedeutsam erzeugen das Urteil (92 % der Varianz)
     │  zucker wirkt mediiert, nicht direkt
     │  Preis spielt hier KEINE Rolle
     ▼
Betracht 14 %   ← der Engpass: 26 % statt 40 % im Marktvergleich
     │
     │  TOR 2 — Preis und Verfügbarkeit entscheiden
     │  54 % der Nichtkäufer nennen "zu teuer", 26 % "nie im Angebot"
     │  NEOH konvertiert hier überdurchschnittlich (50 %, Rang 4 von 18)
     ▼
Kauf 8 %
```

Was daraus für die Empfehlungen folgt, würde ich in den Slides so trennen:

1. **Reichweite ist nicht das Problem.** NEOH ist in seiner Kategorie
   Bekanntheitsführer mit großem Abstand. Mehr Reichweite füllt Tor 1 nicht.
2. **Tor 1 ist eine Relevanzfrage.** Es geht darum, bei mehr Menschen ein
   Passungsurteil zu erzeugen — `bedürfnis`, nicht `qualität`. Die
   Zuckermotivation ist der Hebel, aber sie wirkt über das Markenurteil.
3. **Tor 2 ist eine Preis- und Handelsfrage.** Hier ist NEOH bereits stark;
   der verbleibende Verlust ist zur Hälfte Preis, zu einem Viertel fehlende
   Aktionen. Beides ist operativ adressierbar.

Offen bleiben: die jüngste Altersgruppe, ein formaler Mediationstest für
`zucker`, und die Trennung von Preis-Leistungs-Urteil und absoluter
Preisbarriere. Alle drei brauchen die Fallzahl des deutschen Samples.
