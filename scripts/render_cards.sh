#!/usr/bin/env bash
# Render-Verifikation für Design-System-Karten.
#
# Erkennt den besten verfügbaren Render-Pfad und screenshottet jede Karte:
#   1. agent-browser (CLI)          → bevorzugt
#   2. vorhandenes Playwright       → npx playwright screenshot (nichts wird installiert)
#   3. nichts verfügbar             → Exit 3 + ehrliche Meldung (nur Static-Check möglich)
#
# Aufruf:
#   render_cards.sh --detect            nur Pfad-Erkennung (Ausgabe: agent-browser|playwright|none)
#   render_cards.sh <arbeitsordner>     rendert cards/*.html nach <arbeitsordner>/shots/
set -euo pipefail

detect() {
  if command -v agent-browser >/dev/null 2>&1; then echo "agent-browser"; return; fi
  if npx --no-install playwright --version >/dev/null 2>&1; then echo "playwright"; return; fi
  echo "none"
}

if [[ "${1:-}" == "--detect" ]]; then
  detect
  exit 0
fi

WORKDIR="${1:?Aufruf: render_cards.sh <arbeitsordner> | --detect}"
CARDS_DIR="$WORKDIR/cards"
SHOTS_DIR="$WORKDIR/shots"
[[ -d "$CARDS_DIR" ]] || { echo "FEHLER: $CARDS_DIR existiert nicht"; exit 2; }
mkdir -p "$SHOTS_DIR"

MODE="$(detect)"
case "$MODE" in
  agent-browser)
    echo "Render-Pfad: agent-browser"
    for f in "$CARDS_DIR"/*.html; do
      name="$(basename "$f" .html)"
      agent-browser open "file://$(cd "$(dirname "$f")" && pwd)/$(basename "$f")" >/dev/null
      agent-browser wait 500 >/dev/null
      agent-browser screenshot "$(cd "$SHOTS_DIR" && pwd)/$name.png" >/dev/null
      echo "  shot: $name.png"
    done
    ;;
  playwright)
    echo "Render-Pfad: playwright (vorhandene Installation)"
    for f in "$CARDS_DIR"/*.html; do
      name="$(basename "$f" .html)"
      npx --no-install playwright screenshot --wait-for-timeout=500 \
        "file://$(cd "$(dirname "$f")" && pwd)/$(basename "$f")" \
        "$SHOTS_DIR/$name.png" >/dev/null
      echo "  shot: $name.png"
    done
    ;;
  none)
    echo "KEIN Browser verfügbar (weder agent-browser noch Playwright)."
    echo "Es wurde NICHT gerendert — nur der Static-Check (check_cards.py) ist gelaufen."
    echo "Das im Bericht ehrlich ausweisen. Nichts installieren, nur um zu rendern."
    exit 3
    ;;
esac

COUNT="$(ls "$SHOTS_DIR"/*.png 2>/dev/null | wc -l | tr -d ' ')"
echo "OK — $COUNT Screenshots in $SHOTS_DIR — jetzt mit dem Read-Tool ANSEHEN."
