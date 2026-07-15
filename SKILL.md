---
name: brand-design-system
description: Baut aus einer beliebigen Webseiten-Domain automatisch ein vollständiges Marken-Design-System auf Agentur-Niveau in Claude Design (claude.ai/design) — extrahiert Farben, Schriften, Layout, Motion, Gradients, Icons, Bildsprache und Voice, veredelt Lücken systematisch (Ramps/Skalen/States), baut einen Enterprise-Karten-Satz (~22: Foundations + volle Komponenten + Accessibility) mit geteilten Komponenten, prüft jede Karte gegen eine bewertete Design-QA-Rubric, pusht über DesignSync und verankert das Branding optional global in Claude Code (~/.claude/branding/). Nutze diesen Skill, wenn der User ein Design-System aus seiner Webseite/Domain/Brand will — „mach ein Design-System aus meiner Seite", „meine Brand in Claude Design", „Design-System für <domain>", „extrahier meine Marke", „Branding global einrichten", „/brand-design-system".
trigger-phrases:
  - "brand design system"
  - "design system aus meiner webseite"
  - "design-system für meine domain"
  - "meine brand in claude design"
  - "marke extrahieren"
  - "design system erstellen"
compatibility: Benötigt das DesignSync-Tool (claude.ai-Login mit Design-Zugang) und Python 3 (nur Stdlib). Für die Render-Verifikation wird agent-browser empfohlen (npm install -g agent-browser); alternativ vorhandenes Playwright, sonst ehrlicher statischer Fallback.
---

# brand-design-system

Extrahiert die **echte Marke** aus einer Webseite und legt daraus ein Design-System-Projekt in Claude Design an. Regel Nr. 1: **Nichts erfinden.** Die Marke reproduzieren — inklusive Verspieltheit, Farbigkeit und Bewegung, wenn die Seite sie zeigt. Kein eigener Haus-Stil.

## Input

Der User gibt nur seine **Domain** (z.B. `https://acme.de`). Optional: Notizen oder ein Repo-Pfad (Repo ist als Quelle genauer als die Live-Seite).

- **Projektname ableiten:** `<Brand aus Domain> Design System` (acme.de → „Acme Design System").
- Nicht nach weiteren Inputs fragen. Domain da → loslegen.

## Ablauf (Phasen strikt in dieser Reihenfolge)

### Phase 0 — Preflight

1. DesignSync-Tool laden: `ToolSearch("select:DesignSync")`. Ist es nicht verfügbar oder meldet später „needs a claude.ai login": **nicht abbrechen** — dem User wörtlich sagen, er soll **in Claude Code** `/design-login` eingeben (alternativ `/login` mit dem Abo-Account), sich authentifizieren und „weiter" schreiben. NICHT „im Terminal" sagen — das verwirrt Desktop-App-Nutzer; `/design-login` funktioniert in Desktop-App und CLI. Bis dahin alles Lokale trotzdem fertig bauen.
2. Browser-Verfügbarkeit prüfen: `bash scripts/render_cards.sh --detect` (Pfade relativ zu diesem Skill-Ordner). Ergebnis merken für Phase 3. Meldet der Check `none`, dem User JETZT (nicht erst in Phase 3) die Installation anbieten: `npm install -g agent-browser` (öffentliches npm-Paket, vercel-labs) — damit wird jede Karte vor dem Push echt gerendert und gesichtet statt nur statisch geprüft. Lehnt er ab oder gibt es kein npm, weiterarbeiten und den statischen Fallback ehrlich ausweisen.
3. Dem User die möglichen manuellen Handgriffe **vorab** ankündigen, damit nichts überrascht: (a) beim ersten Push evtl. einmal `/design-login` in Claude Code (claude.ai-Auth für DesignSync — danach gemerkt); (b) Schriften am Ende einmal über „Upload fonts" in Claude Design hochladen.
4. Arbeitsordner anlegen (z.B. `./claude-design-build/` oder ein Scratch-Verzeichnis) mit Unterordnern `cards/`, `fonts/`, `assets/`.

### Phase 1 — Marke ehrlich extrahieren

**Vollständige Anleitung: [references/extraction.md](references/extraction.md) — vor der Extraktion lesen.** Die vier harten Regeln, an denen reine Prompts nachweislich scheitern:

1. **Verlinkte Stylesheets sind PFLICHT.** Gerendertes HTML holen UND jede verlinkte CSS-Datei (theme/base/component) herunterladen und lesen. Nie aus den inline `:root`-Tokens allein auf die Marke schließen — Motion, Gradients und Component-States stehen fast immer in den verlinkten CSS.
2. **Grep-before-skip.** „Keine Motion" / „keine Gradients" darf nur behauptet werden, wenn die Suche in ALLEN geladenen CSS leer war (Suchlisten in extraction.md). Jeder Fund = eigene Karte.
3. **Mehr als die Startseite crawlen.** Zusätzlich 2-3 markante Seiten (Kategorie/Produkt/Kampagnen-Landingpage) — Hero-Backgrounds und Lifestyle-Bilder leben oft NICHT auf der Home.
4. **Assets aktiv ernten** (Logo-Suite, Inline-SVG-Icons, ggf. Payment-Badges, Hintergründe/Hero, Bildsprache-Beispiele, OG-Image/Favicon) — echte Dateien nach `assets/` laden. Große Bilder als Thumbnail, nie 4096²-Originale. Schriften nach der Beschaffungs-Reihenfolge in extraction.md nach `fonts/`.

**System-zentriert, nicht nur Tokens** (extraction.md Abschnitt 4/4b): zusätzlich das **Layout-System** (Breakpoints, Container-Breiten, Grid), die **Interaktions-States** (hover/active/focus-visible/disabled je Komponente), die **Data-Viz-Palette** und **echte Copy** für Voice (Headlines/CTAs/Microcopy) minen. Bildsprache mit dem **Vision-Schritt** (Thumbnails ansehen) zu Art-Direction-Regeln verdichten.

Danach in **EINE kanonische `tokens.css`** normalisieren. Fehlende, aber für ein vollständiges System nötige Werte **systematisch veredeln** nach [references/systematize.md](references/systematize.md) (Neutral-Ramp aus 2-3 Grautönen, Typo-Skala rationalisieren, State-Farben + Focus-Ring ableiten, minimale marken-treue Elevation, semantische Paare) — jeder abgeleitete Wert trägt `/* derived */`. Das ist „das Maximum aus dem Rohmaterial holen", ohne die Marke zu verraten.

### Checkpoint — Go einholen

Dem User zeigen: Token-Übersicht als Tabelle (**extrahiert vs. abgeleitet getrennt**), den **Karten-Plan mit den geplanten Sektionen pro Karte** (nicht nur Namen — z.B. „Colors: Rollen-Grid · WCAG-Tabelle · Verwendungsregeln · Mini-UI"), Schrift-Plan, Asset-Fundliste, und je nicht geplanter Karte des Kanons einen **Evidenz-Beleg**. **Coverage-Anspruch: Enterprise-Kanon (~22 Karten, references/cards.md). Ziel ≥18 für eine reiche Marke.** Jede Auslassung nur mit Beleg (leere Grep / Komponente nicht auf der Seite gefunden). „Weniger Arbeit" ist kein Beleg. **Auf Go warten, bevor Karten geschrieben werden.**

### Phase 2 — Karten bauen

**Karten-Kanon, Content-Contracts, Tiefen-/Specimen-Standard: [references/cards.md](references/cards.md).** Vor dem Bauen die Pflicht-Referenz [assets/example-card.html](assets/example-card.html) ansehen — sie zeigt das Enterprise-Struktur-Niveau: These-Titel → Doktrin → Specimen/Komponente IM KONTEXT → State-Matrix → Anatomie mit Redline → A11y-Notiz → Nutzungsregeln → Token-Labels. Struktur nachahmen, Look aus der jeweiligen Marke.

1. `assets/gen_cards_template.py` in den Arbeitsordner kopieren und füllen. **Der `COMPONENTS_CSS`-Block ist geteilt** — er wird byte-identisch in jede Karte injiziert UND als `components.css` geschrieben (Manifest registriert ihn als `globalCssPaths`). So sehen Buttons/Inputs/Badges über alle Karten identisch aus, der Satz wirkt als EIN System. Nie eine Komponenten-Klasse pro Karte umdefinieren. Den ATMOSPHERE-Block auf das echte Marken-Finish setzen (dunkel = Canvas-Verlauf/Grain, hell = flat).
2. Karten nach den Content-Contracts in cards.md bauen: Specimen statt Labels (Pangram + echter Absatz), Komponenten im Kontext + State-Matrix, Anatomie für komplexe Komponenten, A11y-Notiz je Komponente. Abgeleitetes mit `/* derived */` + `derived`-Tag ausweisen.
3. Generator laufen lassen → `cards/*.html` + `tokens.css` + `components.css`.
4. **Gate:** `python3 scripts/check_cards.py <arbeitsordner>` muss `bad: 0` melden. Prüft: Tiefe (≥6 KB, ≥3 Sektionen), Shared-CSS-Isolation, **Komponenten-Block byte-identisch in allen Karten** (Konsistenz-Beweis), Specimen auf Typography, A11y (Focus-State bei Komponenten, reduced-motion bei Motion), WCAG auf Colors. Fehler beheben und neu generieren, bis grün.

### Phase 3 — Rendern + Design-QA-Rubric (der Qualitäts-Loop)

**Vollständig: [references/design-qa.md](references/design-qa.md).** Das ist der Mechanismus, der Top-Niveau MARKEN-UNABHÄNGIG macht — das Byte-Gate fängt Dünnes, die Rubric fängt Schwaches.

1. `bash scripts/render_cards.sh <arbeitsordner>` — screenshottet jede Karte.
2. **Jeden Screenshot mit dem Read-Tool ANSEHEN** und als kritischer Art-Director (nicht als Autor) auf 7 Dimensionen bewerten (0-4, Pass ab 3): Hierarchie · Spacing-Rhythmus · Specimen-Realismus · Doktrin-/Rezept-Klarheit · Atmosphäre im Marken-Finish · Kontrast/A11y · Set-Konsistenz. Leitfrage: „Würde ein Kunde dafür zahlen?"
3. **Loop:** Karten mit einer Dimension < 3 gehen zurück in Phase 2 (gezielt die schwache Dimension beheben), neu generieren, neu rendern, neu bewerten. **Max 2 Runden**, dann ehrlich berichten, was offen blieb.
4. **Kein Push, solange eine Karte eine Dimension < 3 hat** (außer der User winkt eine benannte Ausnahme durch). Set-Level-Urteil (Durchschnitt + schwächste 2 Karten) in den Bericht.
5. Kein Browser verfügbar → Skript sagt es ehrlich (nennt `npm install -g agent-browser`). Dann NUR statischer Check, im Bericht klar ausweisen. **Nie behaupten, eine Karte sei gerendert/bewertet, wenn nichts lief.**

### Phase 4 — Push über DesignSync

**Vollständiges Protokoll: [references/push.md](references/push.md).** Kurzfassung:

1. `python3 scripts/build_manifest.py <arbeitsordner>` → baut `_ds_manifest.json` aus den Karten + tokens.css. **Das Manifest wird bei JEDEM Push mitgeschrieben** — auch beim ersten. (Grund: Die App baut den Karten-Index nur beim allerersten Projekt-Load selbst; nachgepushte Karten erscheinen sonst nie in der Sidebar. Belegt, nicht theoretisch.)
2. DesignSync-Reihenfolge: `list_projects` → ggf. `create_project` → `get_project` (Typ muss `PROJECT_TYPE_DESIGN_SYSTEM` sein) → `finalize_plan` (writes: `cards/*.html`, `tokens.css`, `components.css`, `fonts/*`, `assets/*`, `_ds_manifest.json`; localDir = Arbeitsordner) → `write_files` → `list_files` (Kontrolle) → `report_validate` mit den ehrlichen Zahlen.
3. Login-Fehler → Protokoll aus Phase 0 (`/design-login` in Claude Code ansagen, warten, nahtlos weitermachen).
4. Bestandsprojekt: erst Diff zeigen, nie fremde Pfade löschen ohne namentliche Bestätigung.

### Phase 5 — Global in Claude Code verankern (empfohlen, mit Zustimmung)

**Details: [references/global.md](references/global.md).** Damit die Marke in JEDEM Projekt auf dem
Rechner verfügbar ist, nicht nur in Claude Design:

1. Kit schreiben (kein Risiko, immer machen):
   `python3 scripts/install_branding.py <arbeitsordner> --brand "<Brand>" --slug <slug> --domain <url> --project-id <uuid> --project-name "<name>" --character-file <charakter.md>`
   — legt `~/.claude/branding/<slug>/` an (brand.md als Agenten-Briefing, tokens.css, fonts/, assets/,
   design-system.json). Den Charakter-Abschnitt (3-5 Sätze: hell/dunkel, flat/verspielt, was trägt die
   Betonung, Don'ts) vorher als kleine Datei schreiben und übergeben.
2. **Den User EXPLIZIT fragen** (AskUserQuestion), ob der Lade-Block in die globale `~/.claude/CLAUDE.md`
   eingetragen werden darf („Bei Visual-/Design-Arbeit zuerst dieses brand.md laden"). Nur bei Ja den
   Lauf mit `--write-claude-md` wiederholen. Der Block ist idempotent (Marker-Kommentare) und
   rückstandslos entfernbar. NIEMALS ohne Zustimmung in die globale CLAUDE.md schreiben.

### Phase 6 — Bericht + der eine manuelle Schritt

Abschlussbericht: geladene Quellen (Seiten + CSS-Dateien), Token-Tabelle, eingebettete Assets (gefunden/nicht gefunden — ehrlich), angelegte Karten (Name, Gruppe), Annahmen/abgeleitete Werte, **welcher Verify-Pfad lief** (gerendert vs. nur statisch), und die exakte Font-Datei-Liste für den Upload: Projekt in Claude Design öffnen → „Upload fonts" → die `fonts/*.woff2` hineinziehen. Optional: Projekt als Standard setzen, damit neue Designs die CI automatisch ziehen.

## Leitplanken

- **Nie Marken-Werte oder Assets erfinden.** Kein Logo zeichnen, keinen Hintergrund „dazu-generieren". Nur echte Dateien referenzieren; wenn etwas nicht auffindbar ist, ehrlich als offen vermerken.
- **Keinen Signatur-Look aufzwingen.** Helle Marke = helle Karten. Flat = flat (Flachheit ist dann das Handwerk). Verspielt = verspielt.
- Ein Token-Block, eine Grundfläche, ein Lichtmodell über den ganzen Satz.
- Fremde Assets (Payment-Logos, lizenzierte Fonts) sind Referenz im eigenen System, kein Vertriebsgut — nicht weiterverteilen.
- WCAG-Kontraste auf Colors/Typography ausweisen; Paare unter 4,5:1 (Body) bzw. 3:1 (groß/UI) als FAIL markieren statt still ausliefern.
- Vor löschenden Eingriffen in ein Bestandsprojekt fragen.
