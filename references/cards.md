# Phase 2 — Karten bauen (Enterprise-Niveau)

## Der Tiefen-Standard (PFLICHT — jede Karte ist ein erklärtes System, keine Token-Liste)

Jede Karte braucht alle fünf Elemente:

1. **These + Doktrin.** Titel ist eine Haltung, kein Label („Tiefe wird gebaut, nicht behauptet"
   statt „Shadows"). Darunter ein Doktrin-Absatz, der das SYSTEM erklärt — aus der Evidenz.
2. **Demonstration mit Rezept-Transparenz.** Jede Demo trägt ein Mono-Rezept (`.recipe`): wie ein
   Wert gebaut/eingesetzt wird.
3. **Nutzungsregeln inkl. Verbote.** Wann welcher Wert, was verboten ist.
4. **Token-Label an jedem gezeigten Wert** (`.mono`).
5. **≥3 Sektionen, echte Substanz** (Gate: ≥6 KB, ≥3 Sektionen).

## Specimen- & Kontext-Standard (das hebt „solide" auf „Top")

- **Specimen statt Labels.** Typography zeigt einen **Pangram** + einen **echten Fließtext-Absatz**
  in realen Größen, nicht nur „Body 15px". Colors zeigt zusätzlich ein **reales Mini-UI-Snippet**
  (z.B. eine kleine Karte mit Titel, Text, Badge, Button), das die Palette in Aktion zeigt.
- **Komponenten IM KONTEXT.** Jede Komponente zusätzlich in einem realistischen Mini-Layout
  (Button in einer Karte, Input in einem Formular mit Label + Hint + Error, Badge auf einer Zeile),
  nicht nur isoliert nebeneinander.
- **State-Matrix.** Interaktive Komponenten zeigen default / hover / active / focus-visible /
  disabled zusammen in einer Reihe, jeweils beschriftet.
- **Anatomie-Diagramm.** Komplexe Komponenten (Input, Card, Modal, Table-Row) bekommen eine
  beschriftete Anatomie (Teile benannt: Label, Feld, Hint, Icon, …), gern mit Redline-Maßen.
- **A11y-Notiz.** Jede Komponenten-Karte nennt Focus-Ring, Touch-Target (≥44px) und das relevante
  Kontrast-Paar.

## Atmosphäre: Die Karte IST die Marke

Die Karten-Fläche ist keine weiße Doku-Seite, sondern das echte Finish der Marke (dunkle Marke =
Canvas-Verlauf/Grain; helle Flat-Marke = flat, Border-Trennung). ATMOSPHERE-Block im Generator.

## Geteilte Komponenten (EIN System-Gefühl, kein Drift)

Der Generator definiert **einen** `COMPONENTS_CSS`-Block (Chrome + Komponenten-Klassen:
`.kicker .card-title .doctrine .section-label .recipe .mono .rules .btn .input .badge .swatch …`)
und injiziert ihn **byte-identisch** in jede Karte. Zusätzlich wird er als `components.css` in den
Build geschrieben und im Manifest als `globalCssPaths` registriert. Effekt: Buttons/Inputs/Badges
sehen über alle Karten identisch aus, der Satz wirkt als ein System. Das Gate prüft die Byte-Gleichheit
(Konsistenz-Beweis). **Nie eine Komponenten-Klasse pro Karte umdefinieren** — Änderung = im Block,
dann alle Karten neu generieren.

Struktur nachahmen, Look extrahieren: die Pflicht-Referenz [../assets/example-card.html](../assets/example-card.html)
zeigt das Struktur-Niveau (These → Doktrin → Specimen/Kontext → State-Matrix → Anatomie → A11y → Regeln)
an einer Fantasie-Marke. Struktur gilt immer, Look kommt aus der jeweils extrahierten Marke.

## Der Enterprise-Karten-Kanon (evidenz-gegated)

Ziel für eine reiche Marke: **≥18 Karten**. Jede Auslassung braucht einen Evidenz-Beleg im Checkpoint
(leere Grep / Komponente nicht auf der Seite gefunden). „Weniger Arbeit" ist nie ein Beleg.

### Foundations
| Karte | Pflicht-Contract | Weglassen nur wenn |
|---|---|---|
| Overview (Cover) | Logo, Marken-Essenz als These, Font-Probe im Lockup, Farb-Signatur-Strip, Zwei-Schichten-Hinweis falls vorhanden, Grundsätze | nie |
| Principles | 3-5 Marken-Design-Grundsätze als benannte Doktrinen (z.B. „Ein Akzent", „Tiefe wird gebaut"), je mit Do/Don't | Marke gibt keine Haltung her (selten) |
| Colors | Rollen-Grid + **WCAG-Tabelle** (berechnete Ratios, FAILs markiert) + Verwendungsregeln je Rolle + **Mini-UI-Snippet** | nie |
| Typography | alle Rollen mit echten Schriften, **Pangram + echter Absatz**, Größen-Skala (echt vs. abgeleitet), Betonungs-Doktrin | nie |
| Headline-Lockup | Lockup-Muster (z.B. Sans + Serif-Akzentwort): Aufbau-Rezept, Richtig/Falsch-Beispiel | kein Lockup-Muster |
| Spacing | Basis-Einheit + Leiter als Balken, Anwendungs-Rhythmus | nie |
| Grid & Layout | Breakpoints, Container-Breiten, Spalten/Gutter als Raster-Demo | Layout-Grep leer |
| Radii & Borders | Radius-Chips + Border-Breiten/Hairline + Ausnahme-Regel (z.B. Pill nur Buttons) | nie |
| Elevation | Stufen-Modell mit Rezept je Stufe + Lichtquelle + Einsatz-Regel | flat-Marke ohne Schatten-System (dann minimale, abgeleitete Leiter zeigen) |
| Materials | Flächen-Materialien (Glas/Blur/Solid/Textur) mit Rezept | keine Material-Differenzierung |
| Atmosphere | Canvas/Grain/Glow-Schichten + Schichtungs-Rezept | Fläche einfarbig/flat |
| Gradients | Familien + funktionale Verläufe (Live-Shimmer) + Einsatz-Rezept | Grep leer |
| Motion | Dauer-Skala, Easings (Signatur hervorheben), **Live-Demos**, `prefers-reduced-motion`-Regel | Grep leer |
| Iconography | echte Inline-SVGs, **Grid + Stroke-Doktrin**, currentColor in 3 Farben, Größenreihe, auf Gegenfläche | keine Icons |
| Data-Viz | Serien-Palette (`--chart-*`), ein Beispiel-Chart (Bar/Line als CSS), Farb-Reihenfolge-Regel | keine Charts/kein Dashboard-Charakter |

### Brand
| Karte | Pflicht-Contract | Weglassen nur wenn |
|---|---|---|
| Logo & Clear-Space | volle Suite (echte Assets), Clear-Space-Regel, Mindestgröße, Don'ts, auf hell/dunkel | nie |
| Imagery & Art-Direction | **Regeln** (Crop/Subjekt/Treatment/Freisteller) aus Vision-Analyse + echte Beispiel-Thumbnails + Do/Don't | keine Bilder (selten) |
| Voice & Tone | Ton-Regeln + **echte Zitate** von der Seite (Headlines/CTAs/Microcopy) | Seiten-Text zu dünn |

### Components (je: isoliert + IM KONTEXT + State-Matrix + A11y-Notiz)
| Karte | Pflicht-Contract | Weglassen nur wenn |
|---|---|---|
| Buttons | Hierarchie-Doktrin, State-Matrix, Größen, invers auf Gegenfläche, Rezept, Verbote | nie |
| Inputs & Forms | Default/Focus/Error/Success/Disabled, **Anatomie** (Label/Feld/Hint/Error), im Formular-Kontext | nie |
| Cards & Surfaces | Karten-Typen inkl. Hover-State-Demo + Trennungs-Doktrin (Border vs. Schatten) | nie |
| Badges & Status | Badge-Sprache (welche Farbe sagt was), Status-Paare, im Zeilen-Kontext | nichts dergleichen |
| Navigation & Tabs | Nav-Bar / Tabs / Breadcrumb mit Active-State und Hover, im Layout-Kontext | keine Navigation gefunden |
| Table | Tabelle mit Header, Zebra/Border, Zell-Ausrichtung, Sort-Indikator, Hover-Row | keine Tabellen/kein Daten-Charakter |
| Modal & Drawer | Overlay + Panel mit Anatomie (Titel/Body/Actions/Close), Backdrop, Elevation-Bezug | keine Overlays |
| Toast & Alert | Info/Success/Warning/Error-Varianten mit Icon + Text + Action | keine Notifications |
| Tooltip | Tooltip mit Pfeil, Positions-Regel, Trigger | keine Tooltips |
| Avatar | Größen, Fallback-Initialen, Status-Punkt, Gruppe/Stack | keine Avatare/keine Personen |
| Progress & Skeleton | Progress-Bar/Spinner + Skeleton-Loading-Muster (Live) | keine Ladezustände |
| Pagination | Seiten-Steuerung mit Active/Disabled, im Listen-Kontext | keine Paginierung |

### Accessibility
| Karte | Pflicht-Contract |
|---|---|
| Accessibility | WCAG-Kontrast-Matrix der Kern-Paare, Focus-Ring-Standard (2px, sichtbar, Akzent), Touch-Target ≥44px, `prefers-reduced-motion`, Mindest-Body-Font, Text-auf-Bild-Legibilität |

## Generator-Muster (Pflicht)

- Alle Karten aus **einem** Generator-Script (Kopie von `assets/gen_cards_template.py`), das
  TOKENS_CSS + COMPONENTS_CSS + ATMOSPHERE in jede Karte injiziert. Token ändern → alles neu.
- Erste Zeile byte-genau `<!-- @dsCard group="Brand|Foundations|Components" -->`.
- Echte Schriften per `@font-face` auf `../fonts/*.woff2`, kein Font-CDN.
- Abgeleitete Werte tragen `/* derived */` + einen `derived`-Tag auf der Karte.
- WCAG: `wcag(fg,bg)` aus dem Template. Body 4,5:1, groß/UI 3:1. FAILs sichtbar, nie still.

## Nach dem Generieren

`python3 <skill>/scripts/check_cards.py <arbeitsordner>` → `bad: 0` (prüft Tiefe, Shared-CSS-Konsistenz,
Specimen-Heuristik, A11y). Dann rendern (Phase 3) und die **Design-QA-Rubric** ([design-qa.md](design-qa.md))
auf jede gerenderte Karte anwenden. Erst wenn jede Karte ≥3 in allen Dimensionen ist, pushen.
