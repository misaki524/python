---
name: portfolio-build
description: Rebuild the portfolio's deployable HTML (portfolio/dist/index.html) from portfolio/index.html. Use after editing the portfolio's index.html or anything under portfolio/assets/, so the published version with embedded images stays in sync — or whenever asked to build, regenerate, or publish the portfolio.
---

# Portfolio build

The portfolio lives in `portfolio/`. **`portfolio/index.html` is the single source of truth** (CSS + JS are inlined; images are referenced from `portfolio/assets/`).

`portfolio/build-standalone.py` regenerates the deployable file with images downscaled and base64-embedded, so it opens with no folder and no network:

- **`portfolio/dist/index.html`** — for web hosting (e.g. drag the `portfolio/dist/` folder onto Netlify Drop). Self-contained; can also be opened locally by double-click.

## When to run

Run this whenever `portfolio/index.html` or anything under `portfolio/assets/` changes, so `dist/index.html` doesn't go stale.

## Steps

1. From the repository root, run the build (the script resolves paths from its own location, so no `cd` is needed):

   ```bash
   python3 portfolio/build-standalone.py
   ```

   Requires macOS `sips` for image conversion (already used by the script).

2. Confirm the output was written and report its size:

   ```bash
   ls -la portfolio/dist/index.html
   ```

## Notes

- **Do not hand-edit** `portfolio/dist/index.html` — it is generated. Edit `portfolio/index.html` and rebuild.
- New images added under `assets/` are picked up automatically: the script rewrites every `src="assets/..."` to an embedded data URI.
- Images are downscaled to max 1280px, JPEG quality 82, before embedding (tunable via `MAX_PX` / `JPEG_QUALITY` in the script).
- The script previously also emitted a root-level `ポートフォリオ.html`; that output was removed on purpose. Only `dist/index.html` is generated now.
