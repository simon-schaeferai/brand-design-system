#!/usr/bin/env python3
"""Baut _ds_manifest.json für ein Claude-Design-Design-System-Projekt.

WARUM: Die Claude-Design-App kompiliert den Karten-Index (_ds_manifest.json)
aus den @dsCard-Markern nur beim ALLERERSTEN Laden des Projekts. Karten, die
danach gepusht werden, erscheinen nie in der Sidebar — weder Reload noch
register_assets aktualisiert den Index. Deshalb: Manifest selbst bauen und
bei JEDEM Push (auch dem ersten) mitschreiben.

Quellen:
  - cards/*.html  → Karten-Liste (group aus dem @dsCard-Marker der ersten Zeile)
  - tokens.css    → Token-Liste mit kind-Heuristik + brandFonts aus @font-face-
                    Familien, die in --font-*-Tokens referenziert werden

Aufruf:  python3 build_manifest.py <arbeitsordner> [--namespace <name>]
Schreibt <arbeitsordner>/_ds_manifest.json und meldet Karten-/Token-Zahl.
"""
import json
import os
import re
import sys

MARKER_RE = re.compile(r'^<!-- @dsCard group="([^"]+)" -->')
GROUP_ORDER = {"Brand": 0, "Foundations": 1, "Components": 2}


def token_kind(name: str) -> str:
    if name.startswith(("--gradient", "--dur", "--ease")):
        return "other"
    if name.startswith(("--font", "--text", "--leading")):
        return "font"
    if name.startswith("--space") or name.endswith("-width"):
        return "spacing"
    if name.startswith("--radius") or name.endswith("-radius"):
        return "radius"
    if name.startswith("--shadow"):
        return "shadow"
    if name.startswith("--color") or name.endswith(("-border", "-bg")):
        return "color"
    return "other"


def parse_tokens(tokens_css: str) -> list:
    # nur der :root-Block (bis zur ersten schließenden Klammer)
    root = tokens_css.split("}", 1)[0]
    pairs = re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root)
    out = []
    for name, value in pairs:
        value = re.sub(r"/\*.*?\*/", "", value).strip()
        out.append({"name": name, "value": value, "kind": token_kind(name), "definedIn": "tokens.css"})
    return out


def brand_fonts(tokens: list) -> list:
    fonts = []
    for t in tokens:
        if t["kind"] == "font" and t["name"].startswith("--font-"):
            m = re.match(r'"([^"]+)"', t["value"])
            if m:
                fonts.append({
                    "family": m.group(1),
                    "status": "no-face",
                    "tokens": [t["name"]],
                    "path": "tokens.css",
                })
    # gleiche Familie unter mehreren Tokens zusammenfassen
    merged = {}
    for f in fonts:
        if f["family"] in merged:
            merged[f["family"]]["tokens"].extend(f["tokens"])
        else:
            merged[f["family"]] = f
    return list(merged.values())


def collect_cards(cards_dir: str) -> list:
    cards = []
    for name in sorted(os.listdir(cards_dir)):
        if not name.endswith(".html"):
            continue
        first = open(os.path.join(cards_dir, name), encoding="utf-8").readline()
        m = MARKER_RE.match(first)
        group = m.group(1) if m else "Components"
        cards.append({"path": f"cards/{name}", "group": group})
    cards.sort(key=lambda c: (GROUP_ORDER.get(c["group"], 9), c["path"]))
    return cards


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    workdir = sys.argv[1]
    namespace = None
    if "--namespace" in sys.argv:
        namespace = sys.argv[sys.argv.index("--namespace") + 1]

    cards_dir = os.path.join(workdir, "cards")
    tokens_path = os.path.join(workdir, "tokens.css")
    if not os.path.isdir(cards_dir) or not os.path.isfile(tokens_path):
        print(f"FEHLER: {workdir} braucht cards/ und tokens.css")
        return 2

    tokens = parse_tokens(open(tokens_path, encoding="utf-8").read())
    cards = collect_cards(cards_dir)
    if not namespace:
        namespace = re.sub(r"[^A-Za-z0-9]", "", os.path.basename(os.path.abspath(workdir))) or "DesignSystem"

    manifest = {
        "namespace": namespace,
        "components": [],
        "startingPoints": [],
        "cards": cards,
        "templates": [],
        "hasThumbnailHtml": False,
        "globalCssPaths": ["tokens.css"],
        "tokens": tokens,
        "themes": [],
        "fonts": [],
        "brandFonts": brand_fonts(tokens),
        "source": "spa",
    }
    out_path = os.path.join(workdir, "_ds_manifest.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)

    groups = {}
    for c in cards:
        groups[c["group"]] = groups.get(c["group"], 0) + 1
    print(f"OK — {len(cards)} Karten ({groups}), {len(tokens)} Tokens, "
          f"{len(manifest['brandFonts'])} Brand-Fonts → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
