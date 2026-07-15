# Phase 1 — Marke ehrlich extrahieren

> Grundregel: **Extrahieren, nicht raten.** Was nicht auffindbar ist, wird systematisch abgeleitet
> und mit `/* derived */` markiert — oder ehrlich als offen gemeldet. Nie erfunden.

## 1. Token-Quellen finden und ALLE lesen

### Quelle = Repo (wenn der User einen Pfad genannt hat — genauer als die Live-Seite)

- CSS Custom Properties: `:root { --… }` in `globals.css` oder einer branding/theme-CSS
- Tailwind: `tailwind.config.*` (`theme.extend`) oder Tailwind v4 `@theme` (auch `@theme inline`)
- Schrift-Setup: `next/font`, `@font-face`, Google-Fonts-Import in `layout`/`_app`
- `components.json` (shadcn), Token-Dateien (`tokens.json`, `theme.ts`), Assets in `/public`
- CSS-in-JS (styled-components, emotion, vanilla-extract): Theme-Objekt lesen
  (`theme.ts`, `createGlobalStyle`, `*.css.ts`)

### Quelle = Live-Domain

1. Gerendertes HTML der Startseite holen (curl mit Browser-User-Agent).
2. **PFLICHT: Jede verlinkte Stylesheet-Datei herunterladen und lesen** — alles, was im `<head>`
   als `rel="stylesheet"` hängt (theme-*.min.css, base.css, component-*.css, …).
   **Nie aus den inline `:root`-Tokens allein auf die Marke schließen.** Inline-Tokens sind fast
   immer unvollständig: Motion-Dauern/Easings, Gradient-Familien, Hover-/Component-States und
   benannte Animations-Klassen stehen in den verlinkten CSS. Wer nur die Startseiten-HTML liest,
   verpasst die halbe Marke — das ist der häufigste Extraktions-Fehler.
3. No-Code-Baukästen:
   - **Shopify:** inline `<style>`-Blöcke im `<head>` (Theme-Settings) + verlinkte Theme-Assets
     unter `/cdn/shop/t/<id>/assets/`
   - **Webflow:** `.w-`-Variablen + das `<style>` im `<head>`
   - **Framer:** `--framer-*`-Custom-Properties + Schriften von `framerusercontent.com`
   - **WordPress:** `theme.json` oder inline `--wp--preset--color--*`
   - **Squarespace/Wix:** Site-Design-Variablen im gerenderten CSS
4. Rendert die Seite rein per JavaScript (CSS fehlt im statischen HTML): dem User sagen und um
   Computed-CSS aus den DevTools oder das Repo bitten. **Keine Tokens aus Screenshots raten.**
5. Login/Bot-Schutz: um Repo oder exportiertes Stylesheet bitten.

## 2. Multi-Page-Crawl (nie nur die Startseite)

Zusätzlich zur Home **2-3 markante Seiten** laden:

- eine Kategorie-/Listing-Seite (Collection/PLP)
- eine Detail-/Produktseite (PDP)
- eine Kampagnen-/Brand-Landingpage (`/pages/*`, `/about`, `/lookbook`, Kampagnen-Slugs)

Grund: Hero-Backgrounds, Kampagnen-Himmel, Lifestyle-Imagery und Sektions-Muster leben oft
**nicht** auf der Startseite. Im Bericht auflisten, welche Seiten geladen wurden.

## 3. Grep-before-skip (Motion & Gradients)

Bevor „keine Motion" oder „keine Gradients" behauptet werden darf, ALLE geladenen CSS durchsuchen:

**Motion:** `--duration` · `--ease` · `cubic-bezier` · `@keyframes` · `animate-` · `transition:`
**Gradients:** `linear-gradient` · `radial-gradient` · `conic-gradient` · `--gradient-`

Jeder Fund ist ein Marken-Signal und gehört als Token + Karte ins System:

- Motion → Dauer-Skala, Easings (Feder-/Overshoot-Kurven besonders hervorheben — sie tragen den
  verspielten Charakter), benannte Hover-/Scroll-Animationen
- Gradients → Flavor-/Kategorie-Familien (wiederkehrende Winkel/Stops), funktionale Verläufe
  (Shimmer/Skeleton, Glow, Shine-Sweep, Tile-Hintergründe)

„Keine" ist nur erlaubt, wenn die Grep leer war — und das gehört so in den Bericht.

## 4. Vollständiger Token-Satz (system-zentriert, nicht nur Farbe/Typo)

Ein Design-System ist mehr als Farbe, Typo, Motion, Gradients. Diese Achsen ALLE mitziehen — sie
speisen die Enterprise-Karten (Grid, Data-Viz, Accessibility, State-Matrizen). Was fehlt, wird in
Phase „Systematisieren" ([systematize.md](systematize.md)) sauber abgeleitet, nie erfunden.

- **Farben:** Fläche(n), Text (primär/sekundär/gedämpft), Marken-Akzent(e), semantische Farben
  (Erfolg/Warnung/Fehler/Info), Rahmen/Ring, **State-Farben** (hover/active/disabled), und die
  **Data-Viz-Palette** (`--chart-*`, `--viz-*`, Serien-Farben in Charts). Fehlende Rollen ableiten.
- **Typografie:** Familien + Rollen (Headline/Body/Display/Mono), echte Gewichte, Größen-Skala
  mit Zeilenhöhen, Letter-Spacing, Versalien-/Italic-Konventionen, OpenType-Features falls genutzt.
- **Skalen:** Spacing (Basis-Einheit + Leiter), Radien, Border-Breiten/Hairline, Schatten/Elevation,
  Z-Index-/Layering-Skala.
- **Layout-System (PFLICHT, meist übersehen):** Breakpoints (`@media`-Werte), Container-max-widths,
  Grid-Spalten und Gutter, Sektions-Rhythmus (vertikale Abstände). Grep-Anker: `@media`,
  `max-width`, `grid-template-columns`, `gap`, `--container`, `--breakpoint`. → Karte „Grid & Layout".
- **Interaktions-States (PFLICHT für Komponenten + A11y):** je Komponente `:hover`, `:active`,
  `:focus-visible`, `:disabled`, `[aria-*]`. Grep-Anker: `:hover`, `:focus`, `:focus-visible`,
  `:active`, `:disabled`, `outline`, `box-shadow` auf Focus. → State-Matrizen + Accessibility-Karte.
- **Themes:** definiert die Seite hell+dunkel (`.dark`, `[data-theme]`, `prefers-color-scheme`),
  beide Token-Sätze extrahieren; Standard-Thema als Fläche, das zweite als Schemes-Karte.
  Kein Dunkel erzwingen, wenn die Marke hell-first ist — und umgekehrt.
- **Charakter ehrlich lesen:** hell/dunkel, minimal/kräftig, flat/verspielt, wie viel Bewegung,
  wie bunt. Genau DAS wird reproduziert.

## 4b. Voice & Copy minen (für die Voice-Karte)

Nicht nur Produktnamen. Aus HTML + Unterseiten echte Sprache sammeln: die stärksten **Headlines**,
**CTA-Texte** (Button-Beschriftungen), **Microcopy** (Labels, Hinweise), **Fehler-/Erfolgs-Meldungen**,
**Wertversprechen/Claims**. Daraus Ton-Regeln ableiten (kurz/lang, du/Sie/ihr, nüchtern/verspielt,
Fachsprache ja/nein) und mit **echten Zitaten** auf der Voice-Karte belegen. Gibt die Seite zu wenig
Text her, das ehrlich sagen und die Karte weglassen.

## 5. Asset-Beschaffung (so ernst wie die Tokens)

Echte Dateien nach `assets/` laden und lokal referenzieren (kein Hotlink in den finalen Karten).
Checkliste:

| Asset | Wo suchen | Hinweis |
|---|---|---|
| Logo-Suite | Header, Footer, `og:image`, `/public`, benannte "Logo_Suite"-Dateien | primär vs. sekundär (Signet); Invers nur per CSS-Filter + `/* derived */` |
| Icon-System | inline `<svg>`, `<symbol>`/`<use>`-Sprites, Icon-Fonts | echtes SVG einbetten, `currentColor` zeigen; **Grid-Größe + Stroke-Breite** bestimmen (z.B. 24er-Grid, 1.5px Stroke) → Iconography-Doktrin |
| Payment-/Trust-Badges | Footer/Checkout (E-Com) | echte SVGs laden; Achtung: gehashte Dateinamen exakt aus dem HTML nehmen |
| Hintergründe/Hero/Muster | CSS-`background-image` + Landingpages | genau das, was eine Startseiten-Extraktion verpasst |
| Bildsprache | Produkt-/Lifestyle-Bilder, Format-Raster | **Vision-Schritt (Pflicht):** die Thumbnails mit dem Read-Tool ANSEHEN und Art-Direction ableiten (Crop, Subjekt Mensch/Produkt, Freisteller ja/nein, Treatment/Duotone, Lichtstimmung). Imagery-Karte = REGELN + Beispiele, nicht nur Bilder |
| OG-Image + Favicon | `<meta property="og:image">`, `<link rel="icon">` | oft die beste Quelle für die Logo-Suite |

**Regeln:** Große Bilder als Thumbnail einbetten (Anzeigebreite begrenzen, kleinere Auflösung
laden — CDN-Parameter wie `?width=600` nutzen), nie 4096²-Originale pushen. Nach dem Download
prüfen, dass es echte Dateien sind (`file`-Check — CDNs liefern gern 404-HTML mit Status 200).
Fremde Marken-Assets sind Referenz, kein Vertriebsgut.

## 6. Schrift-Beschaffung (pro Familie, in dieser Reihenfolge)

1. **Selbst gehostet** (woff2/woff im Repo, `/public` oder same-origin/CDN der Marke):
   echte Datei nach `fonts/` laden, per `@font-face` einbinden.
2. **Google Fonts:** echte woff2 von den `fonts.gstatic.com`-URLs der `@font-face`-CSS laden,
   lokal ablegen, `src:` auf `../fonts/*.woff2` umschreiben. Selbst hosten ok — vermieden wird
   nur der Live-CDN-`<link>`.
3. **Lizenziert/nicht ladbar** (Adobe/Typekit/Monotype/verschleiert): **keine Datei erfinden.**
   CSS-Stack = echter Familienname + nächstbester Fallback (`"Foundry Sans", Inter, system-ui,
   sans-serif`), auf der Karte notieren: „Marken-Schrift X ist lizenziert und nicht einbettbar,
   angenähert mit Fallback — über ‚Upload fonts' hochladen für die echte Darstellung."
4. **Dateinamen:** `fonts/<familie>-<gewicht><-italic>.woff2`, klein, eine Datei je Gewicht+Stil.

## 7. Normalisieren in EINE Token-Quelle

Kanonische `tokens.css` (`:root{…}`) als einzige Wahrheit. Jede Karte wird aus genau diesem Block
generiert (Generator-Template injiziert ihn). Einheitliche Namen: `--color-bg/-surface/-text/
-muted/-accent/-border`, `--font-sans/-heading/-display/-mono`, `--text-*` + `--leading-*`,
`--space-*`, `--radius-*`, `--shadow-*`, `--dur-*`, `--ease-*`, `--gradient-*`.
Nur bei blockierender Unklarheit den User fragen (Schrift-Lizenz, welcher von zwei Akzenten primär
ist). Nicht-blockierende Lücken: ableiten, markieren, berichten, weiterarbeiten.
