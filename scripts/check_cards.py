#!/usr/bin/env python3
"""Static-Check für Design-System-Karten (Gate vor dem Rendern/Pushen).

Prüft jede cards/*.html im Arbeitsordner:
  1. Erste Zeile ist byte-genau der @dsCard-Marker (kein BOM, kein Leerzeichen davor).
  2. Schriften lokal eingebettet (../fonts/*.woff2), KEIN Font-CDN (googleapis/gstatic/typekit).
  3. Jede genutzte var(--token) ist in der Karte definiert (Karten sind eigenständig).
  4. Dünn-Schutz: Karte hat substanziellen Inhalt (>2500 Bytes).
  5. Asset-Referenzen zeigen lokal auf ../assets/ (kein Hotlink auf fremde Hosts).

Aufruf:  python3 check_cards.py <arbeitsordner>
Exit 0 = alles grün · Exit 1 = Fehler (Details auf stdout)
"""
import os
import re
import sys

MARKER_RE = re.compile(r'^<!-- @dsCard group="[^"]+" -->')
CDN_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "use.typekit.net", "kit.fontawesome.com")
MIN_BYTES = 2500


def check_card(path: str) -> list:
    errs = []
    raw = open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        errs.append("BOM am Dateianfang (Marker muss Byte 0 sein)")
    text = raw.decode("utf-8", errors="replace")

    first_line = text.split("\n", 1)[0]
    if not MARKER_RE.match(first_line):
        errs.append(f"Zeile 1 ist nicht der @dsCard-Marker: {first_line[:60]!r}")

    for host in CDN_HOSTS:
        if host in text:
            errs.append(f"Font-CDN-Link gefunden ({host}) — Schriften müssen lokal liegen")

    if "../fonts/" not in text and "@font-face" in text:
        errs.append("@font-face vorhanden, aber keine lokale ../fonts/-Quelle")
    if "@font-face" not in text:
        errs.append("keine @font-face-Einbettung (Karte fällt auf Ersatzschrift zurück)")

    defined = set(re.findall(r"(--[\w-]+)\s*:", text))
    used = set(re.findall(r"var\((--[\w-]+)[,)]", text))
    missing = used - defined
    if missing:
        errs.append(f"undefinierte Tokens: {sorted(missing)}")

    if len(raw) < MIN_BYTES:
        errs.append(f"dünn ({len(raw)} Bytes < {MIN_BYTES})")

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

    bad = 0
    for name in cards:
        errs = check_card(os.path.join(cards_dir, name))
        size = os.path.getsize(os.path.join(cards_dir, name))
        if errs:
            bad += 1
            print(f"FAIL {name} ({size} B)")
            for e in errs:
                print(f"     - {e}")
        else:
            print(f"pass {name} ({size} B)")

    print(f"\ntotal: {len(cards)} · bad: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
