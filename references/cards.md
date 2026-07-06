# Phase 2 — Karten bauen

## Der Tiefen-Standard (PFLICHT — das unterscheidet ein Design-System von einer Token-Liste)

Eine Karte, die nur Swatches und Tabellen zeigt, ist eine Token-Liste. Ein Design-System erklärt
sich selbst. **Jede Karte braucht alle fünf Elemente:**

1. **These + Doktrin.** Die Überschrift ist eine Haltung, kein Label („Tiefe wird gebaut, nicht
   behauptet" statt „Shadows"). Darunter ein Doktrin-Absatz, der das SYSTEM erklärt: warum die
   Marke so aussieht, welche Regel dahinter steckt — aus der Extraktions-Evidenz, nicht erfunden.
2. **Demonstration mit Rezept-Transparenz.** Nicht nur zeigen WAS, sondern WIE: jede Demo trägt
   ein Mono-Rezept (`.recipe`), das den Aufbau oder Einsatz benennt (z.B. „+ Kontaktschatten 1–2px,
   + weicher Bodenschatten 4–10px" oder „Glow liegt HINTER dem Element, opacity .16").
3. **Nutzungsregeln.** Wann welcher Wert, und was verboten ist („Grün nur am Kauf-CTA", „Orange
   ist Licht, nie Lesefarbe"). Verbote sind oft die wertvollste Zeile der Karte.
4. **Token-Label an jedem gezeigten Wert** (`.mono`), damit die Karte als Referenz taugt.
5. **Mindestens 3 Sektionen** (`.section-label`) und echte Substanz — die Gates in check_cards.py
   erzwingen ≥6 KB und ≥3 Sektionen. Referenz-Karten guter Systeme liegen bei 6–26 KB.

**Struktur nachahmen, Look extrahieren:** Die Pflicht-Referenz [../assets/example-card.html](../assets/example-card.html)
zeigt das Struktur-Niveau an einer Fantasie-Marke. Ihre STRUKTUR (These → Doktrin → Demo mit
Rezepten → Regeln) gilt für jede Marke. Ihr LOOK gilt nicht — der kommt ausschließlich aus der
Evidenz der jeweils extrahierten Marke.

## Atmosphäre: Die Karte selbst ist im Marken-Finish gebaut

Die Karten-Fläche ist keine weiße Doku-Seite. Sie IST die Marke:

- Dunkle Premium-Marke mit Canvas-Verläufen/Grain → Karten-Body bekommt genau diesen
  Radial-Verlauf und Grain-Layer (Werte aus der Extraktion).
- Helle Flat-Marke → Karten-Body bleibt hell und flat, Trennung wie auf der echten Seite
  (Border statt Schatten). Flat ist dann das Handwerk, kein Mangel.
- Das Generator-Template hat dafür den ATMOSPHERE-Block — pro Marke einmal definieren,
  gilt für alle Karten (ein Lichtmodell, eine Fläche, ein System).

## Generator-Muster (Pflicht)

Alle Karten entstehen aus **einem** Generator-Script (Kopie von `assets/gen_cards_template.py`
im Arbeitsordner), das den kanonischen `TOKENS_CSS`-Block in jede Karte injiziert:

- Token ändern → **alle** Karten neu generieren. Nie eine Karte von Hand nachpatchen.
- Jede Karte ist eine **eigenständige** HTML-Datei: eigener `@font-face`-Block (lokale
  `../fonts/*.woff2`), eigener Token-Block, keine externen Abhängigkeiten außer `../fonts/` und
  `../assets/`.
- Erste Zeile **byte-genau**: `<!-- @dsCard group="Brand|Foundations|Components" -->` — kein BOM,
  kein führendes Leerzeichen. (Das `page()`-Template erledigt das.)
- Gleiche Grundfläche und Atmosphäre in jedem `page()`-Aufruf, damit der Satz als EIN System wirkt.

## Standard-Karten-Satz

An die echte Komplexität der Marke anpassen. **Coverage-Erwartung: Eine typische Marke ergibt
10+ Karten.** Jede Auslassung braucht einen Evidenz-Beleg im Checkpoint (leere Grep, nichts
gefunden) — „weniger Arbeit" ist kein Beleg.

| Karte | Gruppe | Pflicht-Inhalt (Tiefen-Standard konkretisiert) | Weglassen nur wenn |
|---|---|---|---|
| Overview | Brand | Logo, Marken-Essenz als These, Font-Probe im Lockup-Stil, Farb-Strip, Zwei-Schichten-Hinweis falls vorhanden | nie |
| Colors | Foundations | Swatch-Grid nach ROLLEN gruppiert + **WCAG-Tabelle** (berechnete Ratios, FAILs markiert) + Verwendungsregeln je Rolle (inkl. Verbote) | nie |
| Typography | Foundations | alle Font-Rollen mit echten Schriften, Größen-Skala mit px, Lockup-/Versalien-Konventionen als Regel, Betonungs-Doktrin | nie |
| Headline-Lockup | Brand/Foundations | das Marken-Lockup als eigenes Muster (z.B. Sans-ExtraBold + Serif-Italic-Akzentwort): Aufbau-Rezept, Do/Don't-Beispiele | Marke hat kein Lockup-Muster |
| Gradients | Foundations | Familien (Flavor/funktional) mit exakten Stops, Einsatz-Rezept je Verlauf, Live-Demo (Shimmer läuft) | Grep leer |
| Elevation & Light | Foundations | Stufen-Modell (z.B. E0–E4) mit **Rezept je Stufe** (welche Schatten-Schichten), eine Lichtquelle benannt, Einsatz-Regel je Stufe | Seite hat kein Tiefen-/Schatten-System (flat = stattdessen Flat-Doktrin auf Cards/Surfaces) |
| Materials & Surfaces | Foundations | Flächen-Materialien (Glas/Blur/Solid/Textur) mit Aufbau-Rezept und wann welches Material | keine Material-Differenzierung |
| Atmosphere | Foundations | Canvas-Verläufe, Grain, Glows: exakte Werte + Schichtungs-Rezept (was liegt worüber) | Fläche ist einfarbig/flat |
| Spacing & Radii (+Shadow) | Foundations | Skalen als Balken/Chips + die Ausnahme-Regel (z.B. Pill nur Buttons) + Schatten-Inventar | nie |
| Color-Schemes / Themes | Foundations | Schemes mit Kontrast-Angabe + Regel, wann welches Scheme | nur 1 Scheme |
| Motion | Foundations | Dauer-Skala, Easings (Signatur-Kurve hervorheben), **Live-Demos**, Einsatz-Regel je Easing | Grep leer |
| Buttons | Components | Hierarchie-Doktrin (was ist wofür reserviert), States, Größen, invers auf Gegenfläche, Verbote | nie |
| Cards / Surfaces | Components | Karten-Typen inkl. echtem Hover-State als Demo + Trennungs-Doktrin (Border vs. Schatten) | nie |
| Inputs & Forms | Components | Default/Focus/Error/Success + der bewusste Stil-Kontrast (z.B. eckig vs. Pill) als Regel | nie |
| Badges & Status | Components | Badge-Sprache (welche Farbe sagt was), Status-Paare, Bewertung | nichts dergleichen |
| Iconography | Components | echte Inline-SVGs, currentColor-Doktrin, Größenreihe, auf Gegenfläche | keine Icons gefunden |
| Payment & Trust | Components | echte Badge-SVGs + Trust-Sprache der Marke | kein E-Com |
| Announcement / Marquee | Components | Laufschrift/Utility-Bar als Live-Demo + Rolle im Layout | nicht vorhanden |
| Logo & Clear-Space | Brand | volle Suite (echte Assets), Clear-Space-Regel, Mindestgröße, Don'ts | nie |
| Imagery & Backgrounds | Brand | Bildsprache-REGELN (nicht nur Thumbnails): was ist erlaubt, was nie, mit echten Beispielen | keine Bilder (selten) |
| Voice & Tone | Brand | Ton-Regeln aus echten Seiten-Texten, zitierte Beispiele | Texte zu dünn |

## Token-Hygiene auf den Karten

- Abgeleitete Werte: `/* derived */` + ein Satz warum.
- WCAG: `wcag(fg, bg)` aus dem Template nutzen. Body-Grenze 4,5:1, groß/UI 3:1. FAILs sichtbar
  ausweisen mit Hinweis, wofür das Paar trotzdem taugt — nie still ausliefern.

## Nach dem Generieren

`python3 <skill>/scripts/check_cards.py <arbeitsordner>` — muss `bad: 0` melden (prüft auch
Tiefe: ≥6 KB, ≥3 Sektionen, WCAG auf der Colors-Karte). Dann rendern (Phase 3) und bei der
Sichtprüfung JEDE Karte gegen den Tiefen-Standard halten: These? Doktrin? Rezepte? Regeln?
Atmosphäre im Marken-Finish? Erst wenn alles ja ist, pushen.
