# Phase 5 — Global in Claude Code verankern

> Ziel: Die Marke ist danach in JEDEM Projekt auf dem Rechner verfügbar — Claude lädt bei
> Visual-/Design-Arbeit automatisch die echte CI, statt zu raten. Claude Design bleibt die
> Karten-Referenz, das globale Kit ist das Arbeits-Briefing für Claude Code.

## Was installiert wird

```
~/.claude/branding/<slug>/
├── brand.md              Agenten-Briefing: Charakter + alle Tokens als Tabellen + Font-Liste
│                         + Karten-Verzeichnis + Projekt-ID. Das ist die Datei, die Claude
│                         bei Marken-Arbeit ZUERST liest.
├── tokens.css            der kanonische :root-Block — direkt einbindbar in jedes HTML/CSS
├── fonts/*.woff2         die echten Schriften
├── assets/…              Logo & Co.
└── design-system.json    Maschinen-Metadaten (Projekt-ID, Karten, Installations-Datum)
```

Slug-Regel: kleingeschrieben, aus der Domain (`acme.de` → `acme`), nur `a-z0-9-`.
Mehrere Marken = mehrere Slugs nebeneinander (Agentur-Fall) — jede bekommt ihren eigenen
Ordner und ihren eigenen CLAUDE.md-Block.

## Ablauf im Skill-Lauf

1. **Charakter-Datei schreiben** (der einzige LLM-Anteil): 3-5 Sätze in eine kleine Datei —
   hell/dunkel, flat/verspielt, welcher Akzent, was trägt die Betonung, die wichtigsten Don'ts
   (z.B. „Orange ist Licht, nie Lesefarbe"). Aus der Extraktions-Evidenz, nicht erfunden.
2. **Kit schreiben** (immer, kein Risiko):
   ```
   python3 scripts/install_branding.py <arbeitsordner> \
     --brand "Acme" --slug acme --domain https://acme.de \
     --project-id <uuid> --project-name "Acme Design System" \
     --character-file charakter.md
   ```
3. **User fragen** (AskUserQuestion, eine Frage): „Darf ich den Lade-Block in deine globale
   `~/.claude/CLAUDE.md` eintragen, damit jedes Projekt das Branding automatisch nutzt?"
   - Ja → denselben Aufruf mit `--write-claude-md` wiederholen.
   - Nein → dem User den Block zum manuellen Einfügen zeigen (steht unten). Fertig.
   **Ohne Ja wird die globale CLAUDE.md NIE angefasst** — das ist die persönliche Datei des Users.

## Der CLAUDE.md-Block (was --write-claude-md einträgt)

```markdown
<!-- brand-design-system:<slug>:start -->
## Branding: <Brand>
Bei JEDER Visual-/Design-Arbeit für <Brand> (Bilder, UI, Slides, Thumbnails, Landingpages)
zuerst `~/.claude/branding/<slug>/brand.md` als CI-Quelle laden — exakte Farben/Fonts/Skalen,
nie raten. `~/.claude/branding/<slug>/tokens.css` ist der kanonische Token-Block.
<!-- brand-design-system:<slug>:end -->
```

- **Idempotent:** existiert der Block schon (Marker), wird er ersetzt, nie dupliziert.
- **Entfernbar:** Block zwischen den Markern löschen, Kit-Ordner löschen — rückstandsfrei.
- Der Block gehört in die GLOBALE `~/.claude/CLAUDE.md`. Soll die Marke nur in einem Projekt
  gelten, stattdessen in die Projekt-CLAUDE.md einfügen (gleicher Block, Kit bleibt global).

## Update-Läufe

Marke neu extrahiert (Rebrand, neue Tokens)? Einfach den ganzen Skill neu laufen lassen —
`install_branding.py` überschreibt das Kit und ersetzt den eigenen CLAUDE.md-Block. Projekt-ID
bleibt stabil, solange dasselbe Claude-Design-Projekt aktualisiert wird.

## Abgrenzung

- **Claude Design „als Standard setzen"** (Projekt-Einstellung in der UI) sorgt dafür, dass NEUE
  Designs auf claude.ai die CI ziehen — das ist der claude.ai-Hebel, manuell durch den User.
- **Dieses Kit** sorgt dafür, dass Claude Code überall die CI kennt — das ist der lokale Hebel.
  Beides zusammen = Branding einmal extrahiert, überall wirksam.
