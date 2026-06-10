---
name: frontend-slides
description: Use when the user wants a presentation as HTML slides, a web-first talk deck, or a PPTX-to-HTML conversion with strong visual design and minimal runtime dependencies.
---

# Frontend Slides

Create distinctive HTML slide decks as self-contained files. Use this when the deliverable should run in a browser, be easy to share as HTML, or complement a `.pptx` deck with a web version.

## When To Use

- The user wants a talk, pitch, tutorial, or internal deck as HTML slides.
- The user wants a web companion to an existing PowerPoint.
- The user wants a presentation that feels more designed and interactive than a standard `.pptx`.

Do not use this skill when the user only wants a native PowerPoint file. In that case prefer the `pptx` or `Presentations` workflow.

## Core Rules

- Output a single self-contained HTML file when practical.
- Keep the slide stage fixed at `1920x1080` and scale the stage to the viewport.
- Avoid generic default aesthetics. Make typography, palette, spacing, and motion feel intentional.
- Treat the HTML deck as a presentation, not a responsive article. Do not reflow slide internals for phone layouts.
- Prefer a small number of strong visual ideas over many weak ones.

## Workflow

1. Determine the mode:
   - New deck from brief or notes
   - Convert existing `.pptx`
   - Enhance existing HTML slides
2. Decide whether the deck is:
   - Speaker-led: fewer words, more slides, stronger pacing
   - Reading-first: denser but still designed and readable
3. For visual direction, review:
   - [references/STYLE_PRESETS.md](references/STYLE_PRESETS.md)
   - `assets/bold-template-pack/selection-index.json`
4. Only load deeper template files after choosing a direction:
   - short preview cards first
   - full `design.md` only for the selected bold template
5. Before generating the final deck, read:
   - [references/html-template.md](references/html-template.md)
   - [references/animation-patterns.md](references/animation-patterns.md)
   - [assets/viewport-base.css](assets/viewport-base.css)
6. Build the deck and preview it locally.
7. Check for overflow, overlap, bad contrast, weak hierarchy, and broken transitions before delivering.

## Local Conventions For Codex

- Save preview or final decks inside the active workspace, not inside the skill folder.
- When a local browser preview is useful, prefer Codex browser tooling or a local file preview.
- If the user also wants a native deck, keep HTML and PPT outputs as parallel deliverables from the same source material.

## PPTX Conversion

For `.pptx` conversion, use:

```text
python scripts/extract-pptx.py <input.pptx> <output_dir>
```

Notes:

- This script requires `python-pptx`.
- Install it only when needed:

```text
pip install python-pptx
```

- The script extracts text, notes, and images into `extracted-slides.json` plus an `assets/` folder.

## References

- `references/STYLE_PRESETS.md`: lightweight safe presets
- `references/html-template.md`: structure and expected HTML behavior
- `references/animation-patterns.md`: motion patterns by deck feeling
- `assets/viewport-base.css`: mandatory fixed-stage CSS base
- `assets/bold-template-pack/selection-index.json`: compact bold template index
- `assets/bold-template-pack/templates/*`: deeper template material, read selectively

## Common Mistakes

- Making a web page instead of a slide deck
- Reflowing slide content responsively instead of scaling the stage
- Overcrowding slides to avoid adding more slides
- Using generic AI-looking fonts, gradients, or card grids
- Reading the entire bold template pack instead of narrowing first
