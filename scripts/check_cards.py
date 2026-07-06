#!/usr/bin/env python3
"""Static-Check für Design-System-Karten (Gate vor Rendern/QA-Rubric/Push).

Prüft jede cards/*.html im Arbeitsordner:
  1. Erste Zeile byte-genau der @dsCard-Marker (kein BOM, kein Leerzeichen davor).
  2. Schriften lokal (../fonts/*.woff2) in Karte ODER geteilter CSS; KEIN Font-CDN.
  3. Jede var(--token) ist in Karte ODER tokens.css/components.css definiert (Shared-CSS-Isolation).
  4. TIEFEN-Gate: >=6000 Bytes und >=3 Sektionen (section-label).
  5. Colors-Karte: berechnete WCAG-Ratios (Muster "n:1").
  6. KONSISTENZ: der geteilte /* @components:start..end */-Block ist in ALLEN Karten byte-identisch
     (beweist EIN System). Fehlt der Block, ist die Karte nicht aus dem Generator.
  7. SPECIMEN: Typography-Karte enthält einen echten Fließtext-Absatz (kein reines Label-Grid).
  8. A11Y: Motion-Karte muss prefers-reduced-motion erwähnen; interaktive Komponenten-Karten
     (buttons/inputs/nav/table/modal/tabs) müssen einen :focus/focus-visible-State zeigen.
  9. Asset-Referenzen lokal auf ../assets/ (kein Hotlink).

Aufruf:  python3 check_cards.py <arbeitsordner>
Exit 0 = grün · 1 = Fehler · 2 = Aufruf-/Struktur-Fehler
"""
import hashlib
import os
import re
import sys

MARKER_RE = re.compile(r'^<!-- @dsCard group="[^"]+" -->')
CDN_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "use.typekit.net", "kit.fontawesome.com")
COMPONENTS_RE = re.compile(r"/\* @components:start \*/.*?/\* @components:end \*/", re.S)
WCAG_RE = re.compile(r"\d[\d,.]*\s*:\s*1")
FOCUS_RE = re.compile(r":focus(-visible)?|focus-visible|--focus-ring|box-shadow[^;]*ring", re.I)
MIN_BYTES = 6000
MIN_SECTIONS = 3
INTERACTIVE = ("buttons", "inputs", "forms", "nav", "navigation", "tabs", "table",
               "modal", "drawer", "toast", "pagination")


def load_shared_defs(workdir: str) -> set:
    """Token-Namen, die in tokens.css / components.css definiert sind."""
    defs = set()
    for name in ("tokens.css", "components.css"):
        p = os.path.join(workdir, name)
        if os.path.isfile(p):
            defs |= set(re.findall(r"(--[\w-]+)\s*:", open(p, encoding="utf-8").read()))
    return defs


def check_card(path: str, shared_defs: set, shared_has_fontface: bool) -> list:
    errs = []
    raw = open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        errs.append("BOM am Dateianfang (Marker muss Byte 0 sein)")
    text = raw.decode("utf-8", errors="replace")
    base = os.path.basename(path).lower()

    if not MARKER_RE.match(text.split("\n", 1)[0]):
        errs.append(f"Zeile 1 ist nicht der @dsCard-Marker: {text.splitlines()[0][:60]!r}")

    for host in CDN_HOSTS:
        if host in text:
            errs.append(f"Font-CDN-Link ({host}) — Schriften müssen lokal liegen")

    has_face = "@font-face" in text or shared_has_fontface
    if not has_face:
        errs.append("keine @font-face-Einbettung (Karte fällt auf Ersatzschrift zurück)")
    if "@font-face" in text and "../fonts/" not in text:
        errs.append("@font-face vorhanden, aber keine lokale ../fonts/-Quelle")

    defined = set(re.findall(r"(--[\w-]+)\s*:", text)) | shared_defs
    used = set(re.findall(r"var\((--[\w-]+)[,)]", text))
    missing = used - defined
    if missing:
        errs.append(f"undefinierte Tokens (weder Karte noch tokens/components.css): {sorted(missing)}")

    if len(raw) < MIN_BYTES:
        errs.append(f"zu dünn ({len(raw)} B < {MIN_BYTES}) — Tiefen-Standard (references/cards.md)")

    sections = len(re.findall(r'class="[^"]*section-label', text))
    if sections < MIN_SECTIONS:
        errs.append(f"nur {sections} Sektion(en) < {MIN_SECTIONS} — erklärtes System, keine Token-Liste")

    if "colors" in base and not WCAG_RE.search(text):
        errs.append("Colors-Karte ohne berechnete WCAG-Ratios (Muster 4.5:1)")

    if "typography" in base:
        # echter Fliesstext-Absatz: ein <p> mit >120 Zeichen Text (Specimen statt Label-Grid)
        paras = [re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<p[^>]*>(.*?)</p>", text, re.S)]
        if not any(len(p.strip()) > 120 for p in paras):
            errs.append("Typography-Karte ohne echten Fließtext-Absatz (Specimen fehlt)")

    if "motion" in base and "prefers-reduced-motion" not in text:
        errs.append("Motion-Karte ohne prefers-reduced-motion (A11y)")

    if any(k in base for k in INTERACTIVE) and not FOCUS_RE.search(text):
        errs.append("interaktive Komponenten-Karte ohne sichtbaren Focus-State (A11y)")

    for src in re.findall(r'src="([^"]+)"', text):
        if src.startswith(("http://", "https://", "//")):
            errs.append(f"externes Asset gehotlinkt: {src[:80]} — nach assets/ laden")

    return errs


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    workdir = sys.argv[1]
    cards_dir = os.path.join(workdir, "cards")
    if not os.path.isdir(cards_dir):
        print(f"FEHLER: {cards_dir} existiert nicht")
        return 2
    cards = sorted(f for f in os.listdir(cards_dir) if f.endswith(".html"))
    if not cards:
        print(f"FEHLER: keine *.html in {cards_dir}")
        return 2

    shared_defs = load_shared_defs(workdir)
    comp_css = os.path.join(workdir, "components.css")
    shared_has_fontface = any(
        "@font-face" in open(os.path.join(workdir, n), encoding="utf-8").read()
        for n in ("components.css", "tokens.css") if os.path.isfile(os.path.join(workdir, n))
    )

    bad = 0
    comp_hashes = {}
    for name in cards:
        path = os.path.join(cards_dir, name)
        text = open(path, encoding="utf-8").read()
        errs = check_card(path, shared_defs, shared_has_fontface)

        m = COMPONENTS_RE.search(text)
        if not m:
            errs.append("kein geteilter /* @components */-Block — nicht aus dem Generator (Konsistenz)")
        else:
            comp_hashes[name] = hashlib.sha1(m.group(0).encode()).hexdigest()

        size = os.path.getsize(path)
        if errs:
            bad += 1
            print(f"FAIL {name} ({size} B)")
            for e in errs:
                print(f"     - {e}")
        else:
            print(f"pass {name} ({size} B)")

    # Konsistenz: alle Komponenten-Blöcke byte-identisch?
    uniq = set(comp_hashes.values())
    if len(uniq) > 1:
        bad += 1
        print("\nFAIL Konsistenz: der geteilte Komponenten-Block ist NICHT in allen Karten identisch")
        for h in uniq:
            names = [n for n, hh in comp_hashes.items() if hh == h]
            print(f"     Variante {h[:8]}: {names}")

    print(f"\ntotal: {len(cards)} · bad: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
