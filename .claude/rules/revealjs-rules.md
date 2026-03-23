---
paths:
  - "presentations/**/*.html"
  - "review/**/*.html"
---

# Reveal.js Rules

- RevealNotes plugin: import `notes.esm.js` and include `plugins: [RevealNotes]` in `Reveal.initialize()`
- Speaker notes: `<aside class="notes">full script here</aside>` inside each `<section>`
- Print-to-PDF: append `?print-pdf` to the URL, print in Chrome with background graphics on
- Self-contained: CDN links only, no local file dependencies
- Images: use `<!-- IMAGE_PLACEHOLDER: description -->` comment + CSS gradient fallback — never broken img tags

```html
<script type="module">
import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.esm.js';
import RevealNotes from 'https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.esm.js';
Reveal.initialize({ hash: true, plugins: [ RevealNotes ] });
</script>
```
