---
name: brand-design-system
description: Baut aus einer beliebigen Webseiten-Domain automatisch ein vollständiges Marken-Design-System in Claude Design (claude.ai/design) — echte Farben, Schriften, Spacing, Motion, Gradients, Logo-Suite, Icons und Bildsprache werden aus der Live-Seite extrahiert, als Karten gebaut, verifiziert, über das DesignSync-Tool gepusht und optional als globales Brand-Kit (~/.claude/branding/) projektübergreifend in Claude Code verankert. Nutze diesen Skill, wenn der User ein Design-System aus seiner Webseite/Domain/Brand will — „mach ein Design-System aus meiner Seite", „meine Brand in Claude Design", „Design-System für <domain>", „extrahier meine Marke", „Branding global einrichten", „/brand-design-system".
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

1. DesignSync-Tool laden: `ToolSearch("select:DesignSync")`. Ist es nicht verfügbar oder meldet später „needs a claude.ai login": **nicht abbrechen** — dem User wörtlich sagen, er soll im Terminal `/design-login` ausführen (alternativ `/login` mit dem Abo-Account), sich authentifizieren und „weiter" schreiben. Bis dahin alles Lokale trotzdem fertig bauen.
2. Browser-Verfügbarkeit prüfen: `bash scripts/render_cards.sh --detect` (Pfade relativ zu diesem Skill-Ordner). Ergebnis merken für Phase 3. Meldet der Check `none`, dem User JETZT (nicht erst in Phase 3) die Installation anbieten: `npm install -g agent-browser` (öffentliches npm-Paket, vercel-labs) — damit wird jede Karte vor dem Push echt gerendert und gesichtet statt nur statisch geprüft. Lehnt er ab oder gibt es kein npm, weiterarbeiten und den statischen Fallback ehrlich ausweisen.
3. Dem User den einen manuellen Schritt ankündigen: Schriften müssen am Ende einmal über „Upload fonts" in Claude Design hochgeladen werden.
4. Arbeitsordner anlegen (z.B. `./claude-design-build/` oder ein Scratch-Verzeichnis) mit Unterordnern `cards/`, `fonts/`, `assets/`.

### Phase 1 — Marke ehrlich extrahieren

**Vollständige Anleitung: [references/extraction.md](references/extraction.md) — vor der Extraktion lesen.** Die vier harten Regeln, an denen reine Prompts nachweislich scheitern:

1. **Verlinkte Stylesheets sind PFLICHT.** Gerendertes HTML holen UND jede verlinkte CSS-Datei (theme/base/component) herunterladen und lesen. Nie aus den inline `:root`-Tokens allein auf die Marke schließen — Motion, Gradients und Component-States stehen fast immer in den verlinkten CSS.
2. **Grep-before-skip.** „Keine Motion" / „keine Gradients" darf nur behauptet werden, wenn die Suche in ALLEN geladenen CSS leer war (Suchlisten in extraction.md). Jeder Fund = eigene Karte.
3. **Mehr als die Startseite crawlen.** Zusätzlich 2-3 markante Seiten (Kategorie/Produkt/Kampagnen-Landingpage) — Hero-Backgrounds und Lifestyle-Bilder leben oft NICHT auf der Home.
4. **Assets aktiv ernten** (Logo-Suite, Inline-SVG-Icons, ggf. Payment-Badges, Hintergründe/Hero, Bildsprache-Beispiele, OG-Image/Favicon) — echte Dateien nach `assets/` laden. Große Bilder als Thumbnail, nie 4096²-Originale. Schriften nach der Beschaffungs-Reihenfolge in extraction.md nach `fonts/`.

Danach in **EINE kanonische `tokens.css`** normalisieren (`:root{...}`, einheitliche Namen: `--color-*`, `--font-*`, `--text-*`, `--leading-*`, `--space-*`, `--radius-*`, `--shadow-*`, `--dur-*`, `--ease-*`, `--gradient-*`). Abgeleitete Werte mit `/* derived */` markieren. Fehlende Werte systematisch ableiten und berichten — nur bei blockierender Unklarheit fragen.

### Checkpoint — Go einholen

Dem User zeigen: Token-Übersicht als Tabelle, den **Karten-Plan mit den geplanten Sektionen pro Karte** (nicht nur Namen — z.B. „Colors: Rollen-Grid · WCAG-Tabelle · Verwendungsregeln"), Schrift-Plan (einbettbar vs. lizenzierter Fallback), Asset-Fundliste (gefunden/nicht gefunden), Ziel-Projekt (neu oder bestehend). **Coverage:** Eine typische Marke ergibt 10+ Karten; planst du weniger, je Auslassung einen Evidenz-Beleg nennen (leere Grep / nicht vorhanden). „Weniger Arbeit" ist kein Beleg. **Auf Go warten, bevor Karten geschrieben werden.**

### Phase 2 — Karten bauen

**Karten-Satz, Tiefen-Standard und Generator-Muster: [references/cards.md](references/cards.md).** Vor dem Bauen die Pflicht-Referenz [assets/example-card.html](assets/example-card.html) ansehen — sie zeigt das Struktur-Niveau, das JEDE Karte erreichen muss: These-Titel → Doktrin-Absatz → Demonstration mit Rezepten → Nutzungsregeln (inkl. Verbote) → Token-Labels. Struktur nachahmen, Look aus der jeweiligen Marke extrahieren.

1. `assets/gen_cards_template.py` in den Arbeitsordner kopieren und füllen — der Token-Block wird EINMAL definiert und in jede Karte injiziert, nie pro Karte von Hand. Den ATMOSPHERE-Block auf das echte Flächen-Finish der Marke setzen (dunkle Marke = echter Canvas-Verlauf/Grain; helle Flat-Marke = flat lassen). Die Karte IST die Marke, keine weiße Doku-Seite.
2. Generator laufen lassen → `cards/*.html` + `tokens.css` entstehen im Arbeitsordner.
3. **Gate:** `python3 scripts/check_cards.py <arbeitsordner>` muss `bad: 0` melden. Prüft zusätzlich zum Basalen jetzt den Tiefen-Standard: ≥6 KB Substanz und ≥3 Sektionen pro Karte, WCAG-Ratios auf der Colors-Karte. Fehler beheben und neu generieren, bis grün — Tiefe kommt aus echtem Inhalt (Doktrin, Rezepte, Regeln), NIE aus Fülltext.

### Phase 3 — Echt rendern + Tiefen-Sichtprüfung

`bash scripts/render_cards.sh <arbeitsordner>` — screenshottet jede Karte.

- **Screenshots ANSEHEN** (mit dem Read-Tool). Pro Karte zwei Prüfungen:
  - **Technik:** Schriften greifen? Bilder laden? Nichts leer oder kaputt?
  - **Tiefe:** Trägt die Karte eine These (kein bloßes Label)? Erklärt die Doktrin das System? Hat jede Demonstration ein Rezept? Stehen Nutzungsregeln da? Ist die Fläche im Marken-Finish (Atmosphäre), nicht Doku-Weiß? Wirkt sie wie eine Seite aus einem Marken-Guide oder wie eine nackte Token-Liste?
- Eine Karte, die nur Swatches zeigt, geht zurück in Phase 2 (Doktrin/Rezepte/Regeln ergänzen), nicht in den Push.
- Kein Browser verfügbar → das Skript sagt es ehrlich (und nennt `npm install -g agent-browser`). Dann im Bericht klar ausweisen: „nur statisch geprüft, nicht gerendert". **Nie behaupten, eine Karte sei gerendert, wenn nichts lief.**

### Phase 4 — Push über DesignSync

**Vollständiges Protokoll: [references/push.md](references/push.md).** Kurzfassung:

1. `python3 scripts/build_manifest.py <arbeitsordner>` → baut `_ds_manifest.json` aus den Karten + tokens.css. **Das Manifest wird bei JEDEM Push mitgeschrieben** — auch beim ersten. (Grund: Die App baut den Karten-Index nur beim allerersten Projekt-Load selbst; nachgepushte Karten erscheinen sonst nie in der Sidebar. Belegt, nicht theoretisch.)
2. DesignSync-Reihenfolge: `list_projects` → ggf. `create_project` → `get_project` (Typ muss `PROJECT_TYPE_DESIGN_SYSTEM` sein) → `finalize_plan` (writes: `cards/*.html`, `tokens.css`, `fonts/*`, `assets/*`, `_ds_manifest.json`; localDir = Arbeitsordner) → `write_files` → `list_files` (Kontrolle) → `report_validate` mit den ehrlichen Zahlen.
3. Login-Fehler → Protokoll aus Phase 0 (Terminal-Ansage, warten, nahtlos weitermachen).
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
