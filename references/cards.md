# Phase 2 — Karten bauen

## Generator-Muster (Pflicht)

Alle Karten entstehen aus **einem** Generator-Script (Kopie von `assets/gen_cards_template.py`
im Arbeitsordner), das den kanonischen `TOKENS_CSS`-Block in jede Karte injiziert:

- Token ändern → **alle** Karten neu generieren. Nie eine Karte von Hand nachpatchen.
- Jede Karte ist eine **eigenständige** HTML-Datei: eigener `@font-face`-Block (lokale
  `../fonts/*.woff2`), eigener Token-Block, keine externen Abhängigkeiten außer `../fonts/` und
  `../assets/`.
- Erste Zeile **byte-genau**: `<!-- @dsCard group="Brand|Foundations|Components" -->` — kein BOM,
  kein führendes Leerzeichen, keine Leerzeile davor. (Das `page()`-Template erledigt das.)
- Gleiche Grundfläche, gleicher Kicker-/Titel-Aufbau in jedem `page()`-Aufruf, damit der Satz als
  EIN System wirkt.

## Craft-Regel: Das Finish der Marke reproduzieren

Craft ist bedingt, nie automatisch obendrauf. Erst aus der Evidenz klassifizieren: Nutzt die Seite
Schatten? Gradients? Textur? Rahmen statt Schatten zur Trennung? Genau dieses Finish reproduzieren.
Ist die Marke flach und minimal → flach bleiben (Flachheit ist dann das Handwerk). Ist sie bunt und
verspielt (Feder-Easings, Flavor-Gradients, Hover-Lifts) → genau das zeigen, auch als **laufende
CSS-Demos** auf den Karten (Marquee, Shimmer, Hover-Lift funktionieren als reine CSS-Animation im
Karten-Preview). Immer gültig: eine Lichtrichtung, lesbarer Kontrast, Zurückhaltung beim Akzent.

## Standard-Karten-Satz

An die echte Komplexität der Marke anpassen. Motion/Gradients/Assets sind **reguläre Karten,
keine Rand-Optionen** — weglassen nur mit Beleg (leere Grep, nichts gefunden).

| Karte | Gruppe | Inhalt | Weglassen wenn |
|---|---|---|---|
| Overview | Brand | Logo, Name, ein Satz Essenz, Font-Probe, Farb-Strip | nie |
| Colors | Foundations | Swatch-Grid nach Rollen gruppiert + **WCAG-Tabelle** (echte Ratios, FAILs markiert) | nie |
| Typography | Foundations | alle Font-Rollen mit echten Schriften, Größen-Skala mit px-Angaben | nie |
| Gradients | Foundations | Flavor-Familien + funktionale Verläufe (Shimmer läuft live) | Grep leer |
| Spacing & Radii (+Shadow) | Foundations | Spacing-Balken, Radius-Chips, Schatten-Inventar | nie |
| Color-Schemes / Themes | Foundations | Sektions-Schemes bzw. Hell/Dunkel mit Kontrast-Angabe | nur 1 Scheme |
| Motion | Foundations | Dauer-Skala, Easings (Feder hervorheben), **Live-Hover-Demos** | Grep leer |
| Buttons | Components | Hierarchie, States, Größen, invers auf dunkler Fläche | nie |
| Cards / Surfaces | Components | Karten-Typen inkl. echtem Hover-State als Demo | nie |
| Inputs & Forms | Components | Default/Focus/Error/Success, Auswahl-Pills | nie |
| Badges & Status | Components | Produkt-Badges, Status-Chips, Bewertung | nichts dergleichen auf der Seite |
| Iconography | Components | echte Inline-SVGs, `currentColor` in 3 Farben, Größenreihe, auf dunkel | keine Icons gefunden |
| Payment & Trust | Components | echte Badge-SVGs als Kacheln + Footer-Row | kein E-Com |
| Announcement / Marquee | Components | Laufschrift/Utility-Bar, wenn die Seite eine hat | nicht vorhanden |
| Logo & Clear-Space | Brand | volle Logo-Suite (echte Assets), Clear-Space, Mindestgröße, Don'ts | nie |
| Imagery & Backgrounds | Brand | Bildsprache-Regeln + echte Thumbnails (Hero/Lifestyle/Kategorie) | keine Bilder (selten) |
| Voice & Tone | Brand | nur wenn die Seiten-Texte genug hergeben (echte Headlines zitieren) | Texte zu dünn |

## Token-Hygiene auf den Karten

- Jeder gezeigte Wert trägt seinen Token-Namen (`.mono`-Label), damit das System als Referenz
  taugt — nicht nur als Poster.
- Abgeleitete Werte: `/* derived */` + ein Satz warum (z.B. „Warning-Text abgedunkelt, Original-
  Paar erreicht nur 2,3:1").
- WCAG: `wcag(fg, bg)` aus dem Template nutzen. Body-Grenze 4,5:1, groß/UI 3:1. FAILs sichtbar
  ausweisen mit Hinweis, wofür das Paar trotzdem taugt (große Schrift, dekorativ) — nie still
  ausliefern.

## Nach dem Generieren

`python3 <skill>/scripts/check_cards.py <arbeitsordner>` — muss `bad: 0` melden, sonst beheben und
neu generieren. Erst dann rendern (Phase 3), erst nach Sichtprüfung pushen (Phase 4).
