# Phase 3 — Design-QA-Rubric & Review-Loop

> Der Mechanismus, der Top-Niveau MARKEN-UNABHÄNGIG macht. Das Byte-Gate (check_cards.py) fängt
> Dünnes und Kaputtes. Es fängt NICHT Hässliches, schwache Hierarchie, fremden Look oder
> Inkonsistenz. Dafür bewertet Claude jede gerenderte Karte adversarisch gegen diese Rubric.

## Haltung: kritischer Art-Director, nicht Autor

Bewerte NICHT als der, der die Karte gebaut hat, sondern als externer Art-Director, der abnimmt.
Default skeptisch. Die Leitfrage bei jeder Karte: **„Würde ein Kunde für dieses Design-System
zahlen? Sieht das aus wie aus einer Agentur oder wie ein Bootstrap-Template?"** Wohlwollen ist hier
der Feind. Lieber eine Runde mehr nachbessern als eine mittelmäßige Karte durchwinken.

## Die sieben Dimensionen (je 0-4, Pass ab 3)

Bewerte jede Karte anhand ihres **Screenshots** (nicht des Codes) auf allen sieben:

1. **Visuelle Hierarchie** — Führt der Blick? Titel > Sektionen > Detail klar getrennt? Oder alles
   gleich laut/flach?
2. **Spacing-Rhythmus & Ausrichtung** — Konsistente Abstände, saubere Kanten, ein Grid spürbar?
   Oder gequetscht/willkürlich/verrutscht?
3. **Specimen-Realismus** — Zeigt die Karte echte Nutzung (Pangram/Absatz, Komponente im Kontext,
   State-Matrix)? Oder nur nackte Swatches und Labels?
4. **Doktrin- & Rezept-Klarheit** — Erklärt die Karte das System (These, Warum, Rezept, Regeln)?
   Versteht ein Fremder die Regel, ohne den Code zu sehen?
5. **Atmosphäre im MARKEN-Finish** — Steht die Karte im echten Look der Marke (Fläche, Farbe,
   Bewegung)? Nicht generisch-weiß, nicht ein FREMDER Look (kein Dark-Glass auf einer Flat-Marke,
   kein Flat auf einer Premium-Marke).
6. **Kontrast & A11y** — Alles lesbar? WCAG-Paare eingehalten/ausgewiesen? Focus-Ring bei
   Komponenten sichtbar? Keine Grau-auf-Grau-Todeszonen.
7. **Konsistenz über den ganzen Satz** — Nutzt die Karte dieselbe Fläche, dieselben Button-/Badge-/
   Chrome-Klassen wie die anderen? Wirkt sie als Teil EINES Systems oder wie ein Fremdkörper?

### Score-Anker (gilt für jede Dimension)
- **0** — fehlt komplett.
- **1** — Ansatz da, grob mangelhaft.
- **2** — vorhanden, aber erkennbar schwach (Template-Niveau).
- **3** — solide, Agentur-tauglich. **Das ist die Pass-Schwelle.**
- **4** — exzellent, das Beste, was die Marke hergibt.

## Der Review-Loop

1. Nach dem Rendern (`render_cards.sh`) jede Karte per Read-Tool ansehen und die 7 Scores vergeben.
   Scores + eine kurze Begründung je Karte notieren (knapp, ehrlich).
2. **Jede Karte mit einer Dimension < 3 geht zurück in Phase 2.** Gezielt nachbessern (nicht
   blind neu bauen): die schwache Dimension benennen und im Generator genau das beheben
   (mehr Hierarchie, echtes Specimen, Kontext-Demo, Regel-Sektion, Atmosphäre nachziehen …).
3. Betroffene Karten neu generieren, neu rendern, neu bewerten.
4. **Maximal 2 Nachbesserungs-Runden.** Bleibt danach eine Karte unter 3, ehrlich im Bericht
   ausweisen (welche Karte, welche Dimension, warum) statt sie stillschweigend zu pushen.
5. **Kein Push, solange eine Karte eine Dimension < 3 hat** — außer der User winkt eine benannte
   Ausnahme ausdrücklich durch.

## Set-Level-Urteil (in den Bericht)

Nach dem Loop ein Gesamt-Urteil geben:
- Durchschnitts-Score über alle Karten und alle Dimensionen.
- Die **schwächsten zwei Karten** mit ihrem Grund benennen („das ist das Niveau, hier ist die Kante").
- Ein Satz: hält der Satz als EIN System zusammen? Konsistenz-Dimension über alle Karten.

Ehrlichkeit schlägt Schönfärben. Der User will wissen, wo die Kante ist, nicht ein „alles super".

## Häufige Abwertungs-Gründe (aktiv dagegen prüfen)
- Swatches/Labels ohne Kontext (Dim 3) — der häufigste Grund für „sieht billig aus".
- Alles gleich laut, kein Fokus (Dim 1).
- Generisch-weiße Doku-Fläche statt Marken-Finish (Dim 5).
- Ein Fremd-Look aufgezwungen (Dim 5) — z.B. der Look einer anderen Referenz-Marke.
- Eine Karte tanzt aus der Reihe (andere Button-Form, andere Fläche) (Dim 7).
- Grau-auf-Grau, unsichtbarer Focus (Dim 6).
