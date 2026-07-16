---
name: icon-library
description: Set up and use an SVG icon library (lucide-react by default) consistently in a React/Next app. Covers install, the named-import pattern, sizing/color/accessibility conventions, string-keyed icon maps for data-driven UI (nav, badges, cards), keeping imports sorted and unused-free, and swapping icon sets. Use when the user adds icons, asks to "add an icon", "set up icons", "icon library", "lucide", "поставити іконки", "бібліотека іконок", "додати іконку", or repeatedly wires the same icon boilerplate across projects.
---

# Icon library (lucide-react)

A consistent way to add and use icons so every project looks the same and you
never re-explain the boilerplate. Default set: **lucide-react** (tree-shakeable,
1000+ icons, matches shadcn). The conventions apply to any named-export SVG set
(react-icons, phosphor-react, @tabler/icons-react).

## When to use

The user adds icons, wants icons set up, or keeps rewiring the same icon code.
Triggers: "add an icon", "icon library", "lucide", "додати іконку", "поставити
іконки", "бібліотека іконок".

## Install

```sh
npm i lucide-react     # or: pnpm add / yarn add / bun add
```

No config, no provider. Icons are individual React components imported by name.

## Import pattern

Named imports, **alphabetically sorted**, one block. Only import what you use
(with `noUnusedLocals` an unused icon fails the build, which is the point).

```tsx
import { ArrowRight, Cpu, ShieldCheck } from "lucide-react";
```

Adding an icon = add one name to this list. Keep it sorted so diffs stay clean.

## Rendering conventions

- Size with utility classes, not props: `className="h-4 w-4"` (or `h-3.5 w-3.5`
  inline, `h-5 w-5` in buttons). Avoid the `size={}` prop so sizing lives with
  layout.
- Color inherits `currentColor`: set it on the icon or its parent
  (`text-primary`, `text-muted-foreground`).
- Always `aria-hidden` for decorative icons; give the interactive parent an
  `aria-label`. Only give the icon its own label if it is the sole content.
- `shrink-0` on icons inside flex rows so they never squish.

```tsx
<button aria-label="Next" className="flex items-center gap-2 text-primary">
  <ArrowRight className="h-4 w-4 shrink-0" aria-hidden />
  Next
</button>
```

## Data-driven UI: string-keyed icon map

For nav items, badges, or cards defined in data, do NOT put JSX in the data.
Store either the icon component or a string key and map it.

Option A — component in the data (typed):

```tsx
import type { LucideIcon } from "lucide-react";
import { Gauge, FileText } from "lucide-react";

type Item = { href: string; label: string; icon: LucideIcon };
const NAV: Item[] = [
  { href: "/", label: "Overview", icon: Gauge },
  { href: "/docs", label: "Docs", icon: FileText },
];

// render:
{
  NAV.map((it) => <it.icon key={it.href} className="h-4 w-4" aria-hidden />);
}
```

Option B — string key + map (when data is JSON / from a CMS):

```tsx
import { Gauge, FileText, type LucideIcon } from "lucide-react";

const ICONS: Record<string, LucideIcon> = { gauge: Gauge, docs: FileText };
const data = [{ id: "gauge", label: "Overview" }];

{
  data.map((d) => {
    const Icon = ICONS[d.id] ?? Gauge; // fallback icon
    return <Icon key={d.id} className="h-4 w-4" aria-hidden />;
  });
}
```

## Finding the right icon name

lucide names are PascalCase of the kebab name at lucide.dev/icons. Common picks:
navigation `ArrowRight` `ChevronDown` `Menu` `X` `PanelLeftClose`; status
`Check` `CircleAlert` `TriangleAlert` `ShieldCheck`; content `FileText` `Image`
`LayoutGrid` `Table`; actions `Copy` `Download` `Trash2` `Pencil` `Search`
`Settings`; comms `Mail` `MessageCircle` `Send`; money `Wallet` `Coins`
`TrendingDown`. If unsure, grep the package: `ls node_modules/lucide-react/dist/esm/icons | grep -i <term>`.

## Guardrails

- Keep the import list sorted and free of unused entries (run `tsc --noEmit`).
- Do not mix icon sets in one UI; pick one and stay.
- Prefer a single shared icon map per feature over scattering `<SomeIcon />`
  ad hoc, so swapping the set later is one edit.
- Keep stroke-based icons calm on dark themes: high-chroma accents make thin
  1.5px strokes shimmer.

## Swapping sets

Because usage is named imports + a map, switching to another set is: change the
import source and the names. If you used Option B, only the `ICONS` map changes.

```

```
