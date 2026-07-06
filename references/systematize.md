# Systematisieren & vervollständigen — das Maximum aus dem Rohmaterial holen

> Eine Webseite liefert Rohmaterial, kein fertiges System. Ein Top-Designer veredelt es zu einem
> kohärenten Ganzen, OHNE die Marke zu verraten. Das ist der Unterschied zwischen „reproduziert,
> was da ist" und „liefert ein System, für das ein Kunde zahlt".

## Die eine Grundregel

**Extrahiertes hat Vorrang. Abgeleitetes wird sichtbar markiert.** Jeder nicht direkt gefundene Wert
trägt im Token-Block `/* derived */` und wird auf der Karte als abgeleitet ausgewiesen (z.B. kleiner
`derived`-Tag). Im Abschlussbericht stehen extrahiert und abgeleitet in getrennten Listen. Nichts
still erfinden, aber Lücken NICHT offen lassen — ein halbes System ist kein Top-System.

## B1 · Neutral-Ramp herleiten (aus 2-3 Grautönen → 50-900)

Viele Marken definieren nur `bg`, `border`, ein `muted`. Für Tabellen, Zebra-Streifen, Disabled-
States, Trennlinien braucht ein System eine echte Neutralleiter.

- Nimm den dunkelsten und hellsten vorhandenen Neutralton als Anker.
- Interpoliere 7-9 Stufen im SELBEN Farbton (Hue) und mit der Chroma-Tendenz der Marke (warm/kühl).
  Bei kühl-grauer Marke bleiben alle Stufen leicht bläulich, bei warmer leicht bräunlich.
- Benenne `--neutral-50 … --neutral-900`. Die real gefundenen Werte auf die nächste Stufe legen und
  als „echt" markieren, den Rest `/* derived */`.
- Prüfe: aufeinanderfolgende Stufen sind visuell unterscheidbar, aber keine Sprünge.

## B2 · Typo-Skala rationalisieren (ad-hoc Größen → modulare Skala)

Seiten haben oft 6-10 zufällige `font-size`-Werte. Ein System hat eine Skala.

- Sammle alle real genutzten Größen. Bestimme das Body-Maß (häufigste Lauftext-Größe).
- Lege eine modulare Skala mit passendem Ratio darüber (1.2 Minor Third, 1.25 Major Third, 1.333
  Perfect Fourth — wähle das, das die real genutzten Kern-Größen am besten trifft).
- Mappe die echten Größen auf die nächste Skalen-Stufe; ergänze fehlende Stufen `/* derived */`.
- Zeige auf der Typography-Karte beides: „echt genutzt" (aus der Seite) vs „zur Skala ergänzt".
- Zeilenhöhen: falls nicht je Größe definiert, nach Regel ableiten (Headlines ~1.1-1.2, Body ~1.5-1.7).

## B3 · State-Farben & Focus-Ring ableiten

Fast nie vollständig auf der Seite. Nach fester Regel aus der Basisfarbe:

- **Hover:** Basis um 6-8% abdunkeln (helle Marke) bzw. aufhellen (dunkle Marke), oder Deckkraft-Layer.
- **Active/Pressed:** wie Hover, eine Stufe stärker + optional inneren Schatten.
- **Disabled:** Basis auf ~38% Deckkraft ODER auf einen Neutral-Ton; Cursor `not-allowed`.
- **Focus-Ring:** aus dem Akzent, sichtbar, 2px, mit 2px Offset (`box-shadow: 0 0 0 2px <ring>`), so
  dass er auf hell UND dunkel ausreichend Kontrast hat (≥3:1 gegen die Fläche).
- Alle als `/* derived */` markieren und in der State-Matrix der Komponenten zeigen.

## B4 · Minimale Elevation herleiten (wenn keine da ist)

Nicht jede Marke hat ein Schatten-System. Ein Top-System braucht trotzdem eine konsistente
Tiefen-Sprache — aber marken-treu:

- **Flache/helle Marke:** sehr subtile Leiter, überwiegend Border-basiert. E0 = Hairline, E1 = Border
  + 1px Kontaktschatten, E2 = weicher Bodenschatten mit niedriger Deckkraft (rgba ~0.08-0.12), warm
  oder kühl je nach Marke. KEIN Glas, KEIN Glow — das wäre eine Fremd-Doktrin.
- **Dunkle/tiefe Marke:** geschichtete Schatten mit Specular-Lichtkante (siehe Beispiel im Exemplar).
- Eine Lichtquelle (oben) über alle Stufen. Als abgeleitet ausweisen und die Doktrin nennen
  („Trennung über Border, Schatten nur für schwebende Ebenen").

## B5 · Semantische Farben komplettieren (success/warning/error/info)

Fehlt oft. Aus harmonischen, marken-nahen Tönen ableiten:

- Grün/Bernstein/Rot/Blau in der Sättigung und Helligkeit der Marken-Palette (nicht knallige
  Default-Ampel, wenn die Marke gedämpft ist).
- Jeweils ein `-bg` (sehr helle/dunkle Tönung für Flächen) + ein `-fg` (lesbarer Text/Icon-Ton).
- **Jedes Paar WCAG-prüfen** (fg auf bg ≥ 4.5:1 für Text). Fällt es durch, den fg-Ton anpassen und das
  als `/* derived */` notieren.
- Nie ein bestehendes funktionales Signal überschreiben (z.B. wenn die Marke Grün schon exklusiv für
  einen Zweck nutzt — dann Success anders lösen und die Regel respektieren).

## Was NICHT abgeleitet wird

Logo, echte Schriften, echte Bilder, echte Marken-Farben, Voice. Das wird extrahiert oder als offen
gemeldet — nie erfunden. Ableitung gilt nur für **strukturelle Vervollständigung** (Rampen, Skalen,
States, minimale Elevation, semantische Paare), damit das System vollständig und benutzbar ist.
