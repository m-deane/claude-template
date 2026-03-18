---
applyTo: "presentations/**/*.html"
description: "reveal.js v5 rules for HTML presentation files"
---

# Reveal.js v5 Presentation Rules

## CDN Links

All reveal.js assets must be loaded from CDN. No local file dependencies.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/black.css">
```

## RevealNotes Plugin Setup

Import `notes.esm.js` and include `RevealNotes` in the plugins array:

```html
<script type="module">
import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.esm.js';
import RevealNotes from 'https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.esm.js';
Reveal.initialize({ hash: true, plugins: [ RevealNotes ] });
</script>
```

## Speaker Notes Format

Every `<section>` (slide) must contain speaker notes using `<aside class="notes">` tags.
Speaker notes must be full sentences, not bullet points.

```html
<section>
  <h2>Slide Title</h2>
  <p>Visible slide content (max 40 words)</p>
  <aside class="notes">
    Full speaker script goes here. Write in complete sentences at a pace of
    130 words per minute. Include transition cues to the next slide.
  </aside>
</section>
```

## Print-to-PDF

Append `?print-pdf` to the presentation URL, then print in Chrome with background graphics enabled.

## Image Placeholders

Never use broken `<img>` tags. Use the placeholder comment pattern with a CSS gradient fallback:

```html
<!-- IMAGE_PLACEHOLDER: description of the intended image -->
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 100%; height: 300px; border-radius: 8px;">
</div>
```

## Content Rules

- Max 40 words visible on any slide body
- One key assertion per slide — not a list of facts
- 100% of slides must have speaker notes in `<aside class="notes">` tags
- 0 slides with >50 words of visible body text

## Self-Contained Files

- CDN links only — no local file dependencies
- All CSS should be inline or in a `<style>` block within the HTML file
- All JavaScript should be in `<script>` tags within the HTML file

## Validation

- HTML must open in Chrome without console errors
- `S` key must open the speaker notes view
- Slide count within +/-2 of duration target (1 slide per 1.5-2 min)
- Narrative arc traceable: hook, 3 MECE pillars, specific CTA
