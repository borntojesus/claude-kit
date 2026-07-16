---
name: logo-finder
description: Find and download official company / brand / tech logos as SVG (preferred) or PNG. Use when the user asks to "find a logo", "get the <company> logo", "add company logos", needs brand marks for a portfolio / deck / site / case-study / comparison page, or wants to fill a logos/ folder. Tries simple-icons → Wikipedia/Wikimedia SVG → Brandfetch → Clearbit → official press kits → favicon, prefers vector, and saves tint-ready files.
---

# Logo Finder

Locate and download a brand/company/tech logo, preferring **SVG**, falling back
to a high-res **PNG**. Save it where the project keeps logos (default
`logos/co/<slug>.svg` for companies, `logos/<slug>.svg` for tech/products).

## When to use

- "find the <X> logo" / "get me <X>'s logo" / "add logos for these companies"
- Filling a portfolio / case-study / comparison / pitch deck with brand marks
- Replacing a low-res or wrong-format logo with a clean vector

## Decision order (stop at the first that yields a clean asset)

Prefer **vector, single-path, transparent**. For UI tinting (mask to a theme
color), a monochrome SVG is ideal — note it for the caller.

1. **Tech / product / dev-tool logos → simple-icons** (huge, MIT, monochrome SVG,
   tint-ready). Slug = lowercase, no spaces/dots (`nextdotjs`, `sanity`,
   `tailwindcss`, `payloadcms`).
   - File: `https://cdn.simpleicons.org/<slug>` (current mark) or pin a color:
     `https://cdn.simpleicons.org/<slug>/<hexOrColor>`.
   - Browse/confirm slug: `https://simpleicons.org`. Source SVG on GitHub:
     `https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/<slug>.svg`.
2. **Any brand → Wikipedia / Wikimedia Commons** (often the official vector,
   freely licensed). Search Commons for "`<Company> logo`", grab the **Original
   file** (`upload.wikimedia.org/.../<File>.svg`). Best source for _full
   wordmark_ logos simple-icons doesn't carry.
3. **Brandfetch Logo API** — `https://cdn.brandfetch.io/<domain>/w/512/h/512`
   (or the typed endpoint with a client id if the user has one). Good for
   color/wordmark logos by domain. Returns SVG/PNG.
4. **Clearbit Logo API** (PNG, quick, by domain):
   `https://logo.clearbit.com/<domain>?size=256` — decent square mark, PNG only.
5. **Official press / brand kit** — search "`<Company> brand assets`" /
   "`<Company> press kit`" / "`<Company> logo svg`". Use the company's own CDN
   when licensing allows. WebSearch + WebFetch.
6. **Last resort: favicon** (low quality, only if nothing else):
   `https://www.google.com/s2/favicons?domain=<domain>&sz=128` or
   `https://icons.duckduckgo.com/ip3/<domain>.ico`.

## How to run

1. Resolve identity: get the **canonical domain** (for brandfetch/clearbit) and a
   **kebab `slug`** for the filename. If the company isn't obvious, WebSearch the
   name + "official site" first.
2. Try sources in order with the bundled helper, or `curl` directly:
   ```sh
   bash ~/.claude/skills/logo-finder/fetch-logo.sh <slug> [domain] [outdir]
   ```
   The helper attempts simple-icons → clearbit → favicon and writes the first hit
   to `<outdir>/<slug>.{svg,png}` (default outdir `./logos/co`). For Wikimedia /
   Brandfetch / press-kit hits, fetch the resolved URL yourself with `curl -L`.
3. **Validate** every download — never trust a 200:
   - SVG: `head -c 200 file.svg` must start with `<svg`/`<?xml`, not HTML/JSON.
   - PNG: `file file.png` says PNG and size > ~1 KB (Clearbit returns a tiny
     placeholder for unknown domains).
   - Open dimensions / aspect; reject 16×16 favicons unless that's all there is.
4. **Report** per logo: source used, format, whether it's monochrome
   (tint-ready) or full-color, and the saved path. Flag licensing for non-CC
   sources (press kits, brandfetch) — trademarks stay the owner's.

## Conventions (matches vacancy-portfolio-kit)

- Company logos → `logos/co/<slug>.svg`; tech/tools → `logos/<slug>.svg`.
- Prefer `.svg`; only keep `.png`/`.webp` when no usable vector exists
  (e.g. `coursebox.png`, `aem.png`).
- Monochrome marks are tinted in CSS (`filter: brightness(0) invert(1)` on dark).
  Full-color marks (e.g. `hugo-color.png`) are left untinted — say which it is.

## Notes

- Batch: when given a list, fetch concurrently and return a table
  (company · source · format · tint-ready · path).
- simple-icons covers tech/SaaS brands extremely well; reach for Wikimedia when
  you need the _wordmark_, not just the glyph.
- Respect trademarks: downloading for portfolio/comparison/editorial use is
  normal; don't imply endorsement or alter marks beyond theme-tinting.
