# Quelle der Bekanntheit — Kontaktkanäle, Österreich

Basis: 287 NEOH-Kenner. Reproduzierbar mit `python3 analyse_kanaele_at.py`;
vollständige Ausgabe in `ERGEBNISSE_AT_kanaele.txt`, Tabelle in der
zugehörigen `.csv`.

> **Die Frage ging nur an NEOH-Kenner.** Wer die Marke nicht kennt, wurde nicht
> gefragt und hätte auch keinen Kontakt berichten können. Jeder Zusammenhang
> zwischen Kanal und Erwägung ist deshalb ein Zusammenhang, keine Wirkung.

---

## 1. Der Handel trägt die Marke

| Kanal | n | Anteil | 95-%-Intervall |
|---|---:|---:|---|
| **Supermarkt (Regal, Display)** | 131 | **46,5 %** | 40,6 – 52,4 |
| Instagram/Facebook | 64 | 24,4 % | 19,6 – 29,9 |
| **In keinem dieser Kanäle** | 70 | **22,6 %** | 18,0 – 28,0 |
| TV-Werbung | 40 | 14,3 % | 10,6 – 19,0 |
| Printwerbung | 28 | 9,2 % | 6,3 – 13,3 |
| TikTok | 20 | 8,7 % | 5,9 – 12,7 |
| Werbung auf Websites | 24 | 8,1 % | 5,4 – 12,0 |
| Mundpropaganda | 22 | 7,7 % | 5,0 – 11,5 |
| Außenwerbung | 20 | 7,2 % | 4,7 – 11,0 |
| YouTube | 16 | 6,8 % | 4,3 – 10,4 |
| Influencer-Empfehlungen | 13 | 4,8 % | 2,8 – 8,1 |

Nach Gruppen: Handel 46,5 %, Digital und Social 34,4 %, klassische Medien
26,0 %, persönlich 7,7 %.

Das Regal ist der mit Abstand wichtigste Kontaktpunkt — und damit der Grund,
warum die Distributionsbarrieren aus Stufe 3 („nie im Angebot", „sehe ich nie
im Regal") so schwer wiegen. **Wo die Marke nicht im Regal steht, gibt es kaum
einen zweiten Kontaktweg.**

Die Zahl der Kontaktpunkte ist niedrig: Median 1, Mittelwert 1,32. Fast ein
Viertel hatte gar keinen.

| Kontaktpunkte | 0 | 1 | 2 | 3 | 4+ |
|---|---:|---:|---:|---:|---:|
| Personen | 70 | 127 | 47 | 24 | 19 |
| Anteil | 24,4 % | 44,3 % | 16,4 % | 8,4 % | 6,6 % |

---

## 2. Wen welcher Kanal erreicht

Das ist der praktisch brauchbarste Teil: keine Wirkung, sondern Reichweite
innerhalb der Kenner.

| Kanal | 18–29 | 30–39 | 40–49 | 50–59 | 60+ |
|---|---:|---:|---:|---:|---:|
| **Supermarkt** | 48,3 % | 38,0 % | 54,1 % | 51,4 % | 38,5 % |
| Instagram/Facebook | **36,7 %** | 26,0 % | 23,1 % | 10,2 % | **6,1 %** |
| TikTok | **20,0 %** | 5,2 % | 5,2 % | 1,6 % | **0,0 %** |
| TV-Werbung | 15,0 % | 15,1 % | 17,5 % | 8,6 % | 12,2 % |
| Printwerbung | 5,0 % | 11,4 % | 7,3 % | 12,1 % | **16,2 %** |
| kein Kontakt | 13,3 % | 28,9 % | 18,0 % | 25,3 % | **41,0 %** |

Drei Dinge stehen hier:

**Der Supermarkt ist der einzige Kanal ohne Altersgefälle** — zwischen 38 und
54 % in jeder Gruppe. Alles andere ist alterssegmentiert, teils extrem: TikTok
erreicht ein Fünftel der Jüngsten und niemanden über 60.

**Bei den Über-60-Jährigen hatten 41 % gar keinen Kontakt** — fast dreimal so
viele wie bei den Jüngsten. Die Gruppe, in der NEOH die niedrigste Bekanntheit
hat, ist auch die, die am wenigsten erreicht wird.

Nach Geschlecht sind die Unterschiede kleiner, aber systematisch: Außenwerbung
11,3 % bei Männern gegen 4,5 % bei Frauen, TikTok 12,1 % gegen 6,3 % — und
umgekehrt Print 11,6 % bei Frauen gegen 5,7 %.

---

## 3. Was die Erwägungsquote je Kanal nicht zeigt

| Kanal | n | erwägen NEOH | 95-%-Intervall |
|---|---:|---:|---|
| Mundpropaganda | 22 | 42,6 % | 24,1 – 63,5 |
| Werbung auf Websites | 24 | 42,9 % | 25,0 – 62,8 |
| Supermarkt | 131 | 34,8 % | 26,9 – 43,6 |
| Instagram/Facebook | 64 | 32,9 % | 22,4 – 45,6 |
| TikTok | 20 | 29,6 % | 14,0 – 52,0 |
| Printwerbung | 28 | 24,4 % | 12,0 – 43,3 |
| TV-Werbung | 40 | 23,1 % | 12,5 – 38,6 |
| kein Kontakt | 70 | 17,1 % | 9,9 – 28,0 |
| *alle Kenner* | 287 | 25,6 % | |

**Diese Tabelle ist die am leichtesten misszuverstehende der ganzen Studie.**
Sie zeigt nicht, welcher Kanal Erwägung erzeugt. Wer eine Marke erwägt, nimmt
ihre Werbung aufmerksamer wahr und erinnert den Kontakt besser — die Kausalität
läuft in beide Richtungen, und ein Querschnitt kann sie nicht trennen. Dazu
überlappen alle Intervalle.

Die entscheidende Prüfung ist eine andere:

| Modell | n | Pseudo-R² | AIC |
|---|---:|---:|---:|
| nur Markenurteil | 260 | 0,210 | **246,4** |
| + Zahl der Kontaktkanäle | 260 | 0,213 | 247,5 |

> Die Zahl der Kontaktkanäle trägt **nichts** bei, sobald das Markenurteil im
> Modell steht (b = 0,121, p = 0,342) — und das Modell wird nach AIC sogar
> schlechter.

Das ist der Gegensatz zum Befund aus der Bekanntheitsvertiefung. Dort erhöhte
die **ungestützte Erinnerung** die Chance auf Erwägung um das Siebenfache,
unabhängig vom Markenurteil. Hier trägt der **berichtete Werbekontakt des
letzten Monats** nichts.

Die beiden Befunde zusammen ergeben eine brauchbare Unterscheidung: Was zählt,
ist nicht, ob jemand kürzlich Werbung gesehen hat, sondern ob die Marke im
Gedächtnis sitzt. Kontakt ist Mittel, Verankerung ist Ziel.

---

## 4. Die Kontaktlosen

70 Kenner (22,6 %) hatten im letzten Monat in keinem Kanal Kontakt — sie kennen
die Marke aus früherer Zeit.

| | ohne Kontakt | mit Kontakt |
|---|---:|---:|
| erwägen NEOH | 17,1 % | 28,0 % |
| haben gekauft | 11,1 % | 16,7 % |
| nennen NEOH ungestützt | 7,1 % | 8,6 % |
| Brand-Health-Index | **−0,271** | **+0,081** |

Der Unterschied im Markenurteil ist statistisch gesichert (t = −2,59,
p = 0,011). Ob der fehlende Kontakt die schwächere Bindung erzeugt oder die
schwächere Bindung dazu führt, dass Kontakte nicht erinnert werden, entscheidet
auch diese Erhebung nicht.

Praktisch heißt es trotzdem etwas: Ein Fünftel der Kenner ist aus der aktiven
Reichweite herausgefallen, und diese Gruppe ist überdurchschnittlich alt.

---

## 5. Was daraus folgt

1. **Der Handel ist nicht ein Kanal unter vielen, sondern der Kanal.** Fast die
   Hälfte aller Markenkontakte, und der einzige ohne Altersgefälle. Das verbindet
   die Kanalfrage direkt mit den Kaufbarrieren aus Stufe 3.
2. **Digitale Kanäle erreichen die Jungen und sonst niemanden.** Für die
   Über-50-Jährigen, wo die Bekanntheit am niedrigsten ist, bleiben Regal, TV
   und Print.
3. **Mehr Kontaktpunkte allein bringen nichts.** Die Zahl der Kanäle trägt zur
   Erwägung nichts bei, sobald das Markenurteil kontrolliert ist. Was zählt, ist
   die Verankerung — und die misst die ungestützte Bekanntheit.
4. **Für eine Wirkungsaussage reicht diese Erhebung nicht.** Wer wissen will,
   welcher Kanal wirkt, braucht eine Wiederholungsmessung mit Kontaktprotokoll
   oder ein Experiment. Das ist eine Designfrage für Welle 2, kein Defizit
   dieser Auswertung.
