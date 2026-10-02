# Bildmaterial für das Deck

Dieser Ordner ist optional. Liegen keine Dateien darin, rendert `slides_at.py`
das Deck ohne Bilder — es fehlt dann nichts, was für die Aussage nötig wäre.

| Dateiname | Wo es erscheint |
|---|---|
| `neoh-logo.svg` (oder `.png`) | oben links auf der Titelfolie |
| `produkt-1.jpg`, `produkt-2.jpg`, `produkt-3.jpg` | rechts unten auf der Titelfolie |

Erkannt werden `.svg`, `.png`, `.jpg`, `.jpeg` und `.webp`. Die Bilder werden
beim Erzeugen als data-URI eingebettet, damit das PDF eigenständig bleibt —
achte deshalb auf die Dateigröße, 300 bis 600 KB je Produktbild genügen.

Ich konnte die Dateien nicht selbst holen: Die Netzwerkrichtlinie dieser
Umgebung weist `neoh.com` und `neoh.at` am Proxy mit 403 ab.
