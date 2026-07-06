# Generator-Gerüst: baut alle Design-System-Karten aus EINEM kanonischen Token-Block.
#
# SO WIRD ES BENUTZT (durch den Agenten, nicht den User):
#   1. Diese Datei in den Arbeitsordner kopieren (z.B. ./claude-design-build/gen_cards.py).
#   2. TOKENS_CSS mit den ECHTEN extrahierten Werten füllen (nichts erfinden!).
#   3. FONT_FACE an die tatsächlich geladenen fonts/*.woff2 anpassen.
#   4. Pro Karte einen cards["cards/<name>.html"] = page(...)-Block schreiben
#      (Karten-Satz und Muster: references/cards.md des Skills).
#   5. python3 gen_cards.py  → schreibt cards/*.html + tokens.css in den Arbeitsordner.
#
# REGELN:
#   - Der Token-Block wird NIE pro Karte von Hand editiert. Token ändern → alles neu generieren.
#   - Abgeleitete (nicht extrahierte) Werte tragen /* derived */.
#   - Erste Zeile jeder Karte ist der @dsCard-Marker — page() erledigt das, nicht anfassen.
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- WCAG-Kontrast (für die Colors-/Typography-Karte — echte Zahlen, nie geraten) ----------
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
    ok = "PASS" if r >= (3.0 if large else 4.5) else "FAIL"
    return r, ok

# ---------- 1) KANONISCHE TOKENS — MIT ECHTEN WERTEN FÜLLEN ----------
# Einheitliche Namen: --color-* / --font-* / --text-* / --leading-* / --space-* /
# --radius-* / --shadow-* / --dur-* / --ease-* / --gradient-*
TOKENS_CSS = """:root {
  /* === HIER die extrahierten Werte eintragen — Beispiele löschen === */
  --color-bg: #ffffff;
  --color-surface: #ffffff;
  --color-text: #111111;
  --color-text-secondary: #555555;
  --color-muted: #999999;
  --color-border: #e5e5e5;
  --color-accent: #0000ee;

  --font-sans: "Beispiel Sans", sans-serif;
  --font-heading: "Beispiel Sans", sans-serif;

  --text-heading-l: 32px;
  --text-body-s: 16px;
  --text-body-xs: 14px;
  --text-body-2xs: 12px;
  --text-label-m: 12px;
  --leading-l: 40px;
  --leading-xs: 24px;

  --space-2xs: 12px;
  --space-xs: 16px;
  --space-md: 24px;
  --space-lg: 32px;
  --space-2xl: 48px;

  --radius-sm: 8px;
  --shadow-sm: none; /* nur eintragen, was die Seite wirklich nutzt */
}
"""

# ---------- 2) FONT-FACE — an die geladenen fonts/*.woff2 anpassen ----------
# Pro Familie/Gewicht/Stil eine echte Datei. Lizenzierte, nicht ladbare Schriften:
# KEINE Datei erfinden — Fallback-Stack + Hinweis auf der Karte (siehe extraction.md).
FONT_FACE = """@font-face { font-family: "Beispiel Sans"; font-weight: 400; font-style: normal; font-display: swap; src: url("../fonts/beispiel-sans-400.woff2") format("woff2"); }
@font-face { font-family: "Beispiel Sans"; font-weight: 700; font-style: normal; font-display: swap; src: url("../fonts/beispiel-sans-700.woff2") format("woff2"); }
"""

# ---------- 3) ATMOSPHÄRE — die Karten-Fläche IST die Marke, keine weiße Doku-Seite ----------
# HIER das echte Flächen-Finish der Marke eintragen (aus der Extraktion, nie erfunden):
#   - Dunkle Premium-Marke mit Verläufen/Grain: den echten Canvas-Radial-Verlauf als
#     body-background + den Grain-Layer (body::before) aktivieren.
#   - Helle Flat-Marke: einfarbige Fläche, KEIN Grain, Trennung über Border — Flat ist
#     dann das Handwerk. Den ::before-Block einfach leer lassen.
# Ein Lichtmodell, eine Fläche, für ALLE Karten gleich.
ATMOSPHERE_CSS = """body {
  /* Beispiel flat/hell — ersetzen durch das echte Finish der Marke: */
  background: var(--color-bg);
  /* Beispiel dunkle Premium-Marke (nur bei Evidenz):
  background: radial-gradient(125% 92% at 50% -8%, #0c0c12 0%, #07070a 58%);
  background-color: #07070a; */
}
/* Grain-Layer — NUR aktivieren, wenn die echte Seite Grain/Noise zeigt:
body::before {
  content: ""; position: fixed; inset: 0; z-index: 3; pointer-events: none;
  opacity: 0.045; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
} */
"""

# ---------- 3b) Basis-CSS — Doku-Gerüst + Tiefen-Klassen (Doktrin, Rezept, Demo-Meta) ----------
BASE_CSS = """* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  color: var(--color-text);
  font-family: var(--font-sans);
  font-size: var(--text-body-s);
  line-height: 1.5;
  padding: var(--space-2xl);
  position: relative;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 960px; margin: 0 auto; position: relative; z-index: 1; }
.kicker {
  font-weight: 700; font-size: var(--text-label-m);
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--color-muted); margin-bottom: var(--space-2xs);
}
/* These, kein Label: "Tiefe wird gebaut, nicht behauptet" statt "Shadows" */
.card-title {
  font-family: var(--font-heading); font-weight: 700;
  font-size: var(--text-heading-l); line-height: var(--leading-l);
  margin: 0 0 8px 0;
}
/* Doktrin-Absatz: erklärt das SYSTEM (warum die Marke so aussieht), aus der Evidenz */
.doctrine { color: var(--color-text-secondary); font-size: var(--text-body-xs); line-height: 1.65; margin: 0 0 var(--space-lg) 0; max-width: 640px; }
.section-label {
  font-weight: 700; font-size: var(--text-body-2xs); letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--color-text-secondary);
  margin: var(--space-lg) 0 var(--space-2xs) 0;
}
/* Rezept: WIE ein Wert gebaut/eingesetzt wird — an jeder Demonstration */
.recipe { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 9.5px; color: var(--color-muted); line-height: 1.6; margin-top: 6px; }
/* Demo-Meta: Name + Einsatz unter jeder Demo-Kachel */
.demo-name { font-size: 13px; font-weight: 600; margin-top: 12px; }
.demo-use { font-size: 11px; color: var(--color-muted); font-family: ui-monospace, "SF Mono", Menlo, monospace; margin-top: 2px; }
.note { font-size: var(--text-body-2xs); color: var(--color-muted); }
.mono { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 11px; color: var(--color-text-secondary); }
"""


def page(group, kicker, title, sub, body, extra_css=""):
    """Baut eine eigenständige Karten-HTML. Erste Zeile = @dsCard-Marker (byte-genau)."""
    return f"""<!-- @dsCard group="{group}" -->
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{kicker} — {title}</title>
<style>
{FONT_FACE}
{TOKENS_CSS}
{BASE_CSS}
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

# ---------- 4) KARTEN — Beispiel ersetzen, Standard-Satz + Tiefen-Standard: references/cards.md ----------
# Gruppen: "Brand" | "Foundations" | "Components"
# Struktur-Referenz (Pflicht-Niveau): assets/example-card.html im Skill-Ordner.
# Jede Karte: These-Titel · Doktrin · >=3 Sektionen · Rezepte (.recipe) · Nutzungsregeln · Token-Labels.
cards["cards/overview.html"] = page(
    "Brand", "MARKE — Design System", "Titel als These, nicht als Label",
    "Doktrin-Absatz: erklärt in 2-3 Sätzen das SYSTEM der Marke (was trägt die Fläche, was der "
    "Akzent, welche Regel steckt dahinter) — aus der Extraktions-Evidenz, nicht erfunden.",
    """
  <div class="section-label">Demonstration mit Rezept</div>
  <div style="display:flex; gap:8px;">
    <div style="flex:2;">
      <div style="height:56px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);"></div>
      <div class="demo-name">Fläche</div>
      <div class="demo-use">--color-bg · trägt alles</div>
      <div class="recipe">Rezept: wie die Fläche gebaut ist (Verlauf? flat? Grain?)</div>
    </div>
    <div style="flex:1;">
      <div style="height:56px; background:var(--color-accent); border-radius:var(--radius-sm);"></div>
      <div class="demo-name">Akzent</div>
      <div class="demo-use">--color-accent · sparsam</div>
      <div class="recipe">Rezept: wo der Akzent erlaubt ist</div>
    </div>
    <div style="flex:1;">
      <div style="height:56px; background:var(--color-border); border-radius:var(--radius-sm);"></div>
      <div class="demo-name">Trennung</div>
      <div class="demo-use">--color-border</div>
      <div class="recipe">Rezept: Border statt Schatten? Warum?</div>
    </div>
  </div>
  <div class="section-label">Nutzungsregeln</div>
  <ul style="font-size:var(--text-body-xs); color:var(--color-text-secondary); margin:0; padding-left:18px;">
    <li>Regel 1 aus der Evidenz (z.B. „Akzentfarbe nur am Haupt-CTA, nie für Navigation").</li>
    <li>Regel 2 — auch Verbote sind Regeln, oft die wertvollsten.</li>
  </ul>
  <div class="section-label">Hinweis für den Bau</div>
  <p class="note">Diesen Beispiel-Block komplett durch echten Marken-Inhalt ersetzen. Das Gate
  verlangt ≥6 KB Substanz und ≥3 Sektionen pro Karte — eine echte Karte erreicht das durch
  Inhalt, nie durch Fülltext. Struktur-Niveau: assets/example-card.html.</p>
""")

# ---------- 5) Schreiben + Selbst-Assert ----------
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
with open(os.path.join(OUT, "tokens.css"), "w", encoding="utf-8") as f:
    f.write(TOKENS_CSS)
for path, content in cards.items():
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(content)
    assert content.startswith('<!-- @dsCard group="'), f"Marker fehlt: {path}"
    used = set(re.findall(r"var\((--[\w-]+)[,)]", content))
    defined = set(re.findall(r"(--[\w-]+)\s*:", content))
    assert used <= defined, f"undefinierte Tokens in {path}: {used - defined}"
print(f"OK — {len(cards)} Karten + tokens.css geschrieben nach {OUT}")
print("Nächster Schritt: check_cards.py (Gate), dann render_cards.sh, dann Push.")
