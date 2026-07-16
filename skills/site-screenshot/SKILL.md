---
name: site-screenshot
description: Capture website screenshots for competitive analysis, previews, and UI reference. Use when asked to take a screenshot of a URL, snapshot a competitor site, generate homepage thumbnails, or embed site previews in a UI.
triggers:
  - "take a screenshot of"
  - "screenshot the site"
  - "capture the homepage"
  - "screenshot competitor"
  - "site preview"
  - "thumbnail of"
  - "/screenshot"
---

# Site Screenshot

Capture screenshots of any public URL and save them locally, or produce a live-preview URL that can be embedded in UI components.

## Decision: live URL vs. saved file

| Use case                                        | Pick                                        |
| ----------------------------------------------- | ------------------------------------------- |
| Embed in a React/Next.js UI, cards, thumbnails  | **Live URL** (mshots / thum.io)             |
| Need a deterministic file committed to the repo | **Saved file** (Playwright)                 |
| Competitive analysis report, one-off capture    | **Saved file**                              |
| High-volume production traffic                  | **Paid API** (screenshotone.com, urlbox.io) |

## Option A — Live URL (no dependencies)

### WordPress mshots (free, no auth)

```
https://s.wordpress.com/mshots/v1/{encoded_url}?w={width}&h={height}
```

- Free, public, widely used (Jetpack powers this).
- First request may return a placeholder while the screenshot renders — subsequent loads return the real image.
- Renders desktop viewport. No custom viewport, no cookies, no auth.

Example TypeScript helper:

```ts
export function screenshotUrl(
  domain: string,
  opts: { width?: number; height?: number } = {},
): string {
  const { width = 1280, height = 800 } = opts;
  const bare = domain.replace(/^https?:\/\//, "").replace(/\/$/, "");
  const target = `https://${bare}`;
  const params = new URLSearchParams({ w: String(width), h: String(height) });
  return `https://s.wordpress.com/mshots/v1/${encodeURIComponent(target)}?${params.toString()}`;
}
```

Use in JSX:

```tsx
<img
  src={screenshotUrl("example.com", { width: 960, height: 600 })}
  alt="example.com homepage"
  loading="lazy"
/>
```

### thum.io (free tier, watermark)

```
https://image.thum.io/get/width/{w}/crop/{h}/https://{domain}
```

- Free tier embeds a watermark.
- Paid tier unlocks no-watermark + auth.

## Option B — Saved file via Playwright

When you need a deterministic image committed to the repo, use Playwright.

### One-off via npx (no install)

```bash
npx -y playwright@latest install chromium --with-deps
npx -y playwright screenshot \
  --viewport-size=1280,800 \
  --full-page \
  https://example.com \
  ./public/screenshots/example.png
```

### Scripted (better for batches)

```ts
// scripts/screenshot.ts
import { chromium } from "playwright";

const targets = [
  { domain: "example.com", slug: "example" },
  { domain: "another.com", slug: "another" },
];

const browser = await chromium.launch();
try {
  for (const { domain, slug } of targets) {
    const ctx = await browser.newContext({
      viewport: { width: 1280, height: 800 },
    });
    const page = await ctx.newPage();
    await page.goto(`https://${domain}`, {
      waitUntil: "networkidle",
      timeout: 30_000,
    });
    await page.screenshot({ path: `public/screenshots/${slug}.png` });
    await ctx.close();
  }
} finally {
  await browser.close();
}
```

Run with: `pnpm tsx scripts/screenshot.ts`

### Tips for reliable Playwright captures

- Use `waitUntil: 'networkidle'` for SPA-heavy sites, `domcontentloaded` otherwise.
- Set a retina viewport only if needed: `deviceScaleFactor: 2` doubles file size.
- For pages with cookie banners, add `page.evaluate()` or `page.click()` to dismiss before the shot.
- Set `User-Agent` to a common desktop browser to avoid minimal/bot layouts.
- Fail soft: wrap each target in try/catch so one bad domain doesn't break the batch.

## Option C — Paid APIs (for production)

- [screenshotone.com](https://screenshotone.com) — generous free tier, cookie-banner blocker, ad blocker, dark-mode emulation.
- [urlbox.io](https://urlbox.io) — mature, full-page, PDF export.
- [microlink.io](https://microlink.io) — screenshot + metadata in one call.

## Embedding in this repo

For the lab app (`apps/lab`), the helper lives at
`apps/lab/lib/lab/screenshot.ts` — import and use `screenshotUrl(domain)`.
No Next.js Image configuration needed because we use a plain `<img>` element.

## Output checklist

When delivering a screenshot task, confirm:

- [ ] Correct viewport / aspect ratio for the consumer (card, hero, thumb).
- [ ] `alt` text describes the captured site.
- [ ] `loading="lazy"` on non-critical images.
- [ ] No hotlinking against a service's ToS.
- [ ] If committed to the repo, image is compressed (`pngquant`, `oxipng`, or run through `sharp`).
