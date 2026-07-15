# Generator-Gerüst (Enterprise-Niveau): baut alle Karten aus EINEM Token- + EINEM Komponenten-Block.
#
# SO WIRD ES BENUTZT (durch den Agenten, nicht den User):
#   1. Diese Datei in den Arbeitsordner kopieren (z.B. ./claude-design-build/gen_cards.py).
#   2. TOKENS_CSS mit den ECHTEN extrahierten Werten füllen (nichts erfinden; Abgeleitetes /* derived */).
#   3. FONT_FACE an die tatsächlich geladenen fonts/*.woff2 anpassen.
#   4. ATMOSPHERE auf das echte Flächen-Finish der Marke setzen (dunkel = Verlauf/Grain, hell = flat).
#   5. Pro Karte einen cards["cards/<name>.html"] = page(...)-Block schreiben.
#      Karten-Kanon + Content-Contracts: references/cards.md · Struktur-Niveau: assets/example-card.html
#   6. python3 gen_cards.py  → schreibt cards/*.html + tokens.css + components.css in den Arbeitsordner.
#
# REGELN:
#   - COMPONENTS_CSS ist der GETEILTE Komponenten-/Chrome-Block. NIE pro Karte umdefinieren — er wird
#     byte-identisch in jede Karte injiziert (Konsistenz-Beweis) und als components.css geschrieben.
#     Marken-Werte kommen über var(--token), die Klassen selbst bleiben gleich → EIN System-Gefühl.
#   - Token ändern → alle Karten neu generieren. Erste Zeile jeder Karte = @dsCard-Marker (page() macht das).
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- WCAG-Kontrast (echte Zahlen, nie geraten) ----------
def lum(hexc):
    hexc = hexc.lstrip("#")
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)

def wcag(fg, bg, large=False):
    r = ratio(fg, bg)
    return r, ("PASS" if r >= (3.0 if large else 4.5) else "FAIL")

# ---------- 1) KANONISCHE TOKENS — MIT ECHTEN WERTEN FÜLLEN ----------
TOKENS_CSS = """:root {
  /* === echte extrahierte Werte eintragen; Abgeleitetes /* derived */ markieren === */
  --color-bg: #ffffff;
  --color-surface: #ffffff;
  --color-surface-alt: #f6f6f6;
  --color-text: #111111;
  --color-text-secondary: #555555;
  --color-muted: #999999;
  --color-border: #e5e5e5;
  --color-accent: #0000ee;
  --color-accent-hover: #0000cc;      /* derived: Basis -8% */
  --color-on-accent: #ffffff;
  --color-success: #027a48;
  --color-warning: #a15c07;
  --color-error: #b42318;
  --color-ring: #0000ee;              /* derived: Focus-Ring aus Akzent */

  --font-sans: "Beispiel Sans", sans-serif;
  --font-heading: "Beispiel Sans", sans-serif;

  --text-display: 48px;
  --text-heading-l: 30px;
  --text-heading-m: 22px;
  --text-body-l: 18px;
  --text-body-s: 15px;
  --text-body-xs: 13px;
  --text-body-2xs: 12px;
  --text-label-m: 11px;
  --leading-l: 38px;

  --space-2xs: 12px;
  --space-xs: 16px;
  --space-md: 24px;
  --space-lg: 32px;
  --space-2xl: 48px;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-pill: 999px;
  --border-width: 1px;
  --shadow-sm: none;                  /* nur eintragen, was die Seite wirklich nutzt */
  --focus-ring: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-ring);
}
"""

# ---------- 2) FONT-FACE — an die geladenen fonts/*.woff2 anpassen ----------
FONT_FACE = """@font-face { font-family: "Beispiel Sans"; font-weight: 400; font-style: normal; font-display: swap; src: url("../fonts/beispiel-sans-400.woff2") format("woff2"); }
@font-face { font-family: "Beispiel Sans"; font-weight: 700; font-style: normal; font-display: swap; src: url("../fonts/beispiel-sans-700.woff2") format("woff2"); }
"""

# ---------- 3) ATMOSPHÄRE — die Karte IST die Marke (an das echte Finish anpassen) ----------
ATMOSPHERE_CSS = """body {
  background: var(--color-bg);
  /* Dunkle Premium-Marke (nur bei Evidenz):
  background: radial-gradient(125% 92% at 50% -8%, #0c0c12 0%, #07070a 58%);
  background-color: #07070a; */
}
/* Grain-Layer nur bei echtem Grain aktivieren:
body::before { content:""; position:fixed; inset:0; z-index:3; pointer-events:none;
  opacity:0.045; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); } */
"""

# ---------- 3b) GETEILTER Komponenten-/Chrome-Block — byte-identisch in JEDE Karte ----------
# Marker /* @components:start/end */ ist für den Konsistenz-Hash im Gate. NICHT pro Karte ändern.
# Klassen nutzen var(--token) → passen sich pro Marke an, bleiben aber überall gleich.
COMPONENTS_CSS = """/* @components:start */
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { color: var(--color-text); font-family: var(--font-sans); font-size: var(--text-body-s); line-height: 1.55; padding: var(--space-2xl); position: relative; -webkit-font-smoothing: antialiased; }
.wrap { max-width: 980px; margin: 0 auto; position: relative; z-index: 1; }
.kicker { font-weight: 700; font-size: var(--text-label-m); letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-muted); margin-bottom: var(--space-2xs); }
.card-title { font-family: var(--font-heading); font-weight: 700; font-size: var(--text-heading-l); line-height: var(--leading-l); margin: 0 0 8px 0; }
.doctrine { color: var(--color-text-secondary); font-size: var(--text-body-s); line-height: 1.7; margin: 0 0 var(--space-lg) 0; max-width: 640px; }
.section-label { font-weight: 700; font-size: var(--text-body-2xs); letter-spacing: 0.1em; text-transform: uppercase; color: var(--color-text-secondary); margin: var(--space-lg) 0 var(--space-2xs) 0; }
.recipe { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 9.5px; color: var(--color-muted); line-height: 1.6; margin-top: 8px; }
.demo-name { font-size: 13px; font-weight: 700; margin-top: 12px; }
.demo-use { font-size: 11px; color: var(--color-muted); font-family: ui-monospace, "SF Mono", Menlo, monospace; margin-top: 2px; }
.note { font-size: var(--text-body-2xs); color: var(--color-muted); line-height: 1.6; }
.mono { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 11px; color: var(--color-text-secondary); }
.rules { font-size: var(--text-body-xs); color: var(--color-text-secondary); margin: 0; padding-left: 18px; line-height: 1.8; }
.rules b { color: var(--color-text); }
.derived { display: inline-block; font-family: ui-monospace, monospace; font-size: 9px; letter-spacing: .06em; text-transform: uppercase; color: var(--color-muted); border: 1px solid var(--color-border); border-radius: 4px; padding: 1px 5px; vertical-align: middle; }
/* Geteilte Komponenten — Marken-Werte via Tokens, Klassen überall gleich */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-family: var(--font-sans); font-weight: 600; font-size: 14px; padding: 11px 22px; border-radius: var(--radius-pill); border: 1px solid transparent; cursor: pointer; min-height: 44px; }
.btn--primary { background: var(--color-accent); color: var(--color-on-accent); }
.btn--primary:hover { background: var(--color-accent-hover); }
.btn--secondary { background: transparent; color: var(--color-text); border-color: var(--color-border); }
.btn--ghost { background: transparent; color: var(--color-text-secondary); }
.btn:focus-visible { outline: none; box-shadow: var(--focus-ring); }
.btn[disabled], .btn--disabled { opacity: .4; pointer-events: none; }
.input { display: block; width: 100%; font-family: var(--font-sans); font-size: var(--text-body-xs); padding: 11px 14px; border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: var(--color-surface); color: var(--color-text); min-height: 44px; }
.input:focus-visible { outline: none; border-color: var(--color-accent); box-shadow: var(--focus-ring); }
.input--error { border-color: var(--color-error); }
.badge { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: var(--radius-pill); }
.swatch { border: 1px solid var(--color-border); border-radius: var(--radius-sm); overflow: hidden; }
.swatch__chip { height: 52px; }
.swatch__meta { padding: 8px 10px; }
.swatch__meta .name { font-size: 12px; font-weight: 700; }
.state-row { display: flex; gap: 14px; flex-wrap: wrap; align-items: center; }
.state-row > div { text-align: center; }
.ctx { border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; background: var(--color-surface); }
.anatomy { position: relative; }
.redline { font-family: ui-monospace, monospace; font-size: 9px; color: var(--color-accent); }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-2xs); }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-2xs); }
/* @components:end */
"""


def page(group, kicker, title, sub, body, extra_css=""):
    """Baut eine eigenständige Karten-HTML. Erste Zeile = @dsCard-Marker (byte-genau).
    Injiziert Tokens + geteilten Komponenten-Block + Atmosphäre + kartenspezifisches extra_css."""
    return f"""<!-- @dsCard group="{group}" -->
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{kicker} — {re.sub('<[^>]+>', '', title)}</title>
<style>
{FONT_FACE}
{TOKENS_CSS}
{COMPONENTS_CSS}
{ATMOSPHERE_CSS}
{extra_css}
</style>
</head>
<body>
<div class="wrap">
  <div class="kicker">{kicker}</div>
  <h1 class="card-title">{title}</h1>
  <p class="doctrine">{sub}</p>
{body}
</div>
</body>
</html>
"""


cards = {}

# ---------- 4) KARTEN — Beispiel ersetzen. Kanon + Contracts: references/cards.md ----------
# Struktur-Referenz (Pflicht): assets/example-card.html. Jede Karte: These · Doktrin · Specimen/Kontext
# · State-Matrix (Komponenten) · Regeln · Token-Labels · A11y-Notiz (Komponenten).
cards["cards/overview.html"] = page(
    "Brand", "MARKE — Design System", "Titel als These, nicht als Label",
    "Doktrin-Absatz: erklärt das SYSTEM der Marke (was trägt die Fläche, was der Akzent, welche Regel "
    "dahinter) — aus der Extraktions-Evidenz, nicht erfunden. Ersetze diesen Beispiel-Block komplett.",
    """
  <div class="section-label">Farb-Signatur</div>
  <div style="display:flex; gap:8px;">
    <div style="flex:2; height:52px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);"></div>
    <div style="flex:1; height:52px; background:var(--color-accent); border-radius:var(--radius-sm);"></div>
    <div style="flex:1; height:52px; background:var(--color-success); border-radius:var(--radius-sm);"></div>
    <div style="flex:1; height:52px; background:var(--color-border); border-radius:var(--radius-sm);"></div>
  </div>
  <div class="section-label">Mini-UI (Specimen — Palette in Aktion)</div>
  <div class="ctx" style="max-width:320px;">
    <div style="font-family:var(--font-heading); font-weight:700; font-size:16px;">Beispiel-Karte</div>
    <p style="font-size:var(--text-body-xs); color:var(--color-text-secondary); margin:6px 0 12px;">Zeigt Fläche, Text, Badge und Button im echten Marken-Look.</p>
    <span class="badge" style="background:var(--color-surface-alt); color:var(--color-text);">Label</span>
    <div style="margin-top:12px;"><span class="btn btn--primary">Aktion</span></div>
  </div>
  <div class="section-label">Grundsätze</div>
  <ul class="rules">
    <li><b>Grundsatz 1</b> aus der Evidenz (z.B. „Akzentfarbe nur am Haupt-CTA").</li>
    <li><b>Grundsatz 2</b> — auch Verbote sind Regeln, oft die wertvollsten.</li>
  </ul>
  <p class="note" style="margin-top:var(--space-md);">Struktur-Niveau: assets/example-card.html. Gate:
  ≥6 KB, ≥3 Sektionen. Tiefe kommt aus Inhalt, nie aus Fülltext.</p>
""")

# ---------- 5) Schreiben (cards + tokens.css + components.css) + Selbst-Assert ----------
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
with open(os.path.join(OUT, "tokens.css"), "w", encoding="utf-8") as f:
    f.write(TOKENS_CSS)
# components.css = der geteilte Block ohne Marker-Kommentare (für globalCssPaths)
comp = COMPONENTS_CSS.replace("/* @components:start */\n", "").replace("/* @components:end */\n", "")
with open(os.path.join(OUT, "components.css"), "w", encoding="utf-8") as f:
    f.write(comp)
for path, content in cards.items():
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(content)
    assert content.startswith('<!-- @dsCard group="'), f"Marker fehlt: {path}"
    assert "/* @components:start */" in content, f"Komponenten-Block fehlt: {path}"
print(f"OK — {len(cards)} Karten + tokens.css + components.css → {OUT}")
print("Nächster Schritt: check_cards.py (Gate), render_cards.sh + Design-QA-Rubric, dann Push.")
