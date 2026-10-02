# Markenauftritt für das Deck

Dieser Ordner ist optional. Liegt nichts darin, rendert `slides_at.py` das Deck
in der validierten Standardpalette — es fehlt dann nichts, was für die Aussage
nötig wäre.

## Bilder

| Datei | Wo sie erscheint |
|---|---|
| `neoh-logo.svg` (oder `.png`) | oben links auf der Titelfolie |
| `produkt-1.jpg`, `produkt-2.jpg`, `produkt-3.jpg` | rechts unten auf der Titelfolie |

Erkannt werden `.svg`, `.png`, `.jpg`, `.jpeg` und `.webp`. Die Bilder werden
beim Erzeugen als data-URI eingebettet, damit das PDF eigenständig bleibt —
300 bis 600 KB je Produktbild genügen.

## Farben und Schrift

`marke.json` setzt den Auftritt des ganzen Decks:

```json
{
  "akzent":  "#1f6f3f",
  "zweit":   "#c75b2a",
  "flaeche": "#fbfaf7",
  "ink":     "#12201a",
  "schrift": "Georgia, \"Times New Roman\", serif"
}
```

Pflicht ist nur `akzent`. Alles Übrige hat Vorgabewerte.

| Schlüssel | Wirkung |
|---|---|
| `akzent` | Hervorhebungen, Kennzahlen, hervorgehobene Balken, mittlere Funnel-Stufe |
| `zweit` | zweite Serie im Punktvergleich (gestützt gegen ungestützt) |
| `flaeche` | Folienhintergrund |
| `ink` | Schriftfarbe; Grau-, Raster- und Achsentöne werden daraus gemischt |
| `schrift` | CSS-`font-family`, muss auf dem rendernden Rechner installiert sein |

Die **ordinale Funnel-Rampe wird aus dem Akzent abgeleitet**, nicht frei
gesetzt. Eine Rampe für geordnete Stufen muss eine Farbfamilie behalten und
gleichmäßig heller werden — eine beliebige Markenpalette erfüllt das nicht von
selbst, und ein Regenbogen über Funnel-Stufen ist ein Lesefehler, kein
Geschmacksfrage.

Beim Erzeugen prüft das Skript zwei Dinge und meldet sie auf der Konsole:

- Der Akzent sollte gegen die Fläche mindestens **3:1** erreichen, sonst sind
  Balken auf dem Hintergrund schwer zu unterscheiden.
- Die hellste Funnel-Stufe sollte mindestens **2:1** erreichen, sonst verschwimmt
  sie mit dem Hintergrund.

Unterschreitet eine Farbe das, rendert das Deck trotzdem — die Warnung sagt nur,
worauf beim Lesen zu achten ist. Schriftfarben bleiben in jedem Fall in `ink`,
nie im Akzent.

## Warum die Dateien nicht von selbst kommen

Die Netzwerkrichtlinie dieser Arbeitsumgebung weist `neoh.com`, `www.neoh.com`
und `cdn.shopify.com` am Proxy mit 403 ab. Logo, Produktbilder und die
Markenfarben lassen sich von hier aus nicht laden.
