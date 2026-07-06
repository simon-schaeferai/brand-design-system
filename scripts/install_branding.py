#!/usr/bin/env python3
"""Verankert ein gebautes Brand-Kit GLOBAL in Claude Code (~/.claude/branding/<slug>/).

Damit greift jedes Projekt auf dem Rechner auf die Marke zu — nicht nur das,
in dem der Skill lief. Zwei Stufen:

  1. Kit schreiben (immer): ~/.claude/branding/<slug>/ mit brand.md (Agenten-
     Briefing), tokens.css, fonts/, assets/, design-system.json (Projekt-ID).
  2. CLAUDE.md-Block (nur mit --write-claude-md, nach Zustimmung des Users):
     idempotenter Marker-Block in ~/.claude/CLAUDE.md, der Claude anweist, bei
     Visual-/Design-Arbeit zuerst das brand.md zu laden. Pro Marke ein Block,
     rückstandslos entfernbar (Marker-Kommentare).

Aufruf:
  python3 install_branding.py <arbeitsordner> \
      --brand "Acme" --slug acme --domain https://acme.de \
      --project-id <uuid> --project-name "Acme Design System" \
      [--character-file charakter.md]   # vom Agenten geschriebener Charakter-Abschnitt
      [--write-claude-md]               # NUR nach expliziter User-Zustimmung
      [--home <pfad>]                   # Override für Tests (Default: echtes Home)

Idempotent: erneuter Lauf überschreibt das Kit und ersetzt den eigenen Block.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys

MARKER_RE = re.compile(r'^<!-- @dsCard group="([^"]+)" -->')


def parse_tokens(tokens_css: str) -> list:
    root = tokens_css.split("}", 1)[0]
    out = []
    for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root):
        out.append((name, re.sub(r"/\*.*?\*/", "", value).strip()))
    return out


def group_tokens(tokens: list) -> dict:
    groups = {"Farben": [], "Typografie": [], "Skalen": [], "Motion": [], "Gradients": [], "Sonstiges": []}
    for name, value in tokens:
        if name.startswith(("--gradient",)):
            groups["Gradients"].append((name, value))
        elif name.startswith(("--dur", "--ease", "--spring")):
            groups["Motion"].append((name, value))
        elif name.startswith(("--font", "--text", "--leading")):
            groups["Typografie"].append((name, value))
        elif name.startswith(("--space", "--radius", "--shadow")) or name.endswith(("-radius", "-width")):
            groups["Skalen"].append((name, value))
        elif name.startswith("--color") or name.endswith(("-border", "-bg")) or name.startswith(("--glow", "--ui-")):
            groups["Farben"].append((name, value))
        else:
            groups["Sonstiges"].append((name, value))
    return {k: v for k, v in groups.items() if v}


def build_brand_md(args, tokens, fonts, cards, today) -> str:
    lines = [
        f"# Brand-Kit: {args.brand}",
        "",
        f"> Quelle: {args.domain} · Design-System: „{args.project_name}\" auf claude.ai/design "
        f"(Projekt `{args.project_id}`) · Stand: {today}",
        "> CI-Quelle für ALLE Visual-/Design-Arbeit mit dieser Marke. Werte sind aus der echten",
        "> Seite extrahiert — nie raten, nie abweichen. `tokens.css` im selben Ordner ist der",
        "> kanonische Block zum direkten Einbinden.",
        "",
    ]
    if args.character_file and os.path.isfile(args.character_file):
        lines += ["## Charakter", "", open(args.character_file, encoding="utf-8").read().strip(), ""]
    for group, items in group_tokens(tokens).items():
        lines += [f"## {group}", "", "| Token | Wert |", "|---|---|"]
        lines += [f"| `{n}` | `{v}` |" for n, v in items]
        lines.append("")
    if fonts:
        lines += ["## Font-Dateien (fonts/)", ""]
        lines += [f"- `{f}`" for f in fonts]
        lines.append("")
    if cards:
        lines += ["## Karten im Design-System", ""]
        lines += [f"- {c['path']} ({c['group']})" for c in cards]
        lines.append("")
    return "\n".join(lines)


def patch_claude_md(claude_md_path: str, slug: str, brand: str, kit_dir_display: str) -> str:
    start = f"<!-- brand-design-system:{slug}:start -->"
    end = f"<!-- brand-design-system:{slug}:end -->"
    block = (
        f"{start}\n"
        f"## Branding: {brand}\n"
        f"Bei JEDER Visual-/Design-Arbeit für {brand} (Bilder, UI, Slides, Thumbnails, Landingpages) "
        f"zuerst `{kit_dir_display}/brand.md` als CI-Quelle laden — exakte Farben/Fonts/Skalen, nie raten. "
        f"`{kit_dir_display}/tokens.css` ist der kanonische Token-Block.\n"
        f"{end}"
    )
    existing = ""
    if os.path.isfile(claude_md_path):
        existing = open(claude_md_path, encoding="utf-8").read()
    if start in existing and end in existing:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        updated = pattern.sub(block, existing)
        action = "ersetzt"
    else:
        sep = "\n\n" if existing and not existing.endswith("\n\n") else ""
        updated = existing + sep + block + "\n"
        action = "angehängt"
    with open(claude_md_path, "w", encoding="utf-8") as f:
        f.write(updated)
    return action


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("workdir")
    p.add_argument("--brand", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--domain", required=True)
    p.add_argument("--project-id", required=True)
    p.add_argument("--project-name", required=True)
    p.add_argument("--character-file")
    p.add_argument("--write-claude-md", action="store_true")
    p.add_argument("--home", default=os.path.expanduser("~"))
    args = p.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        print("FEHLER: --slug nur Kleinbuchstaben/Ziffern/Bindestriche")
        return 2
    tokens_path = os.path.join(args.workdir, "tokens.css")
    if not os.path.isfile(tokens_path):
        print(f"FEHLER: {tokens_path} fehlt")
        return 2

    kit_dir = os.path.join(args.home, ".claude", "branding", args.slug)
    os.makedirs(kit_dir, exist_ok=True)

    shutil.copy2(tokens_path, os.path.join(kit_dir, "tokens.css"))
    fonts, cards = [], []
    for sub in ("fonts", "assets"):
        src = os.path.join(args.workdir, sub)
        if os.path.isdir(src):
            dst = os.path.join(kit_dir, sub)
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
            if sub == "fonts":
                fonts = sorted(os.listdir(dst))
    cards_dir = os.path.join(args.workdir, "cards")
    if os.path.isdir(cards_dir):
        for name in sorted(os.listdir(cards_dir)):
            if name.endswith(".html"):
                m = MARKER_RE.match(open(os.path.join(cards_dir, name), encoding="utf-8").readline())
                cards.append({"path": f"cards/{name}", "group": m.group(1) if m else "?"})

    today = datetime.date.today().isoformat()
    tokens = parse_tokens(open(tokens_path, encoding="utf-8").read())
    with open(os.path.join(kit_dir, "brand.md"), "w", encoding="utf-8") as f:
        f.write(build_brand_md(args, tokens, fonts, cards, today))
    with open(os.path.join(kit_dir, "design-system.json"), "w", encoding="utf-8") as f:
        json.dump({
            "brand": args.brand, "slug": args.slug, "domain": args.domain,
            "projectId": args.project_id, "projectName": args.project_name,
            "installedAt": today, "cards": cards, "fonts": fonts,
        }, f, ensure_ascii=False, indent=2)

    kit_display = "~/.claude/branding/" + args.slug
    print(f"OK — Brand-Kit geschrieben: {kit_dir}")
    print(f"     brand.md ({len(tokens)} Tokens) · tokens.css · {len(fonts)} Fonts · {len(cards)} Karten referenziert")

    if args.write_claude_md:
        claude_md = os.path.join(args.home, ".claude", "CLAUDE.md")
        action = patch_claude_md(claude_md, args.slug, args.brand, kit_display)
        print(f"OK — Block in {claude_md} {action} (Marker: brand-design-system:{args.slug})")
    else:
        print("Hinweis: CLAUDE.md nicht angefasst (--write-claude-md fehlt). Erst den User fragen!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
