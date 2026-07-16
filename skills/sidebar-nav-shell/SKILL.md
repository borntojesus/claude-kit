---
name: sidebar-nav-shell
description: Scaffold a collapsible sidebar navigation shell for a React/Next.js app. Left sidebar grouped into hubs (accordion), collapses to an icon rail with a burger toggle, off-canvas drawer on mobile, sticky topbar with breadcrumbs and an optional complexity badge, theme-aware via CSS tokens, state persisted in localStorage. Use when the user asks for a "sidebar", "side menu", "collapsible menu", "hub navigation", "burger nav", "бокове меню", "меню з хабами", or wants app navigation moved from top tabs into a proper dashboard shell.
---

# Sidebar navigation shell

A drop-in app shell: grouped collapsible sidebar + mobile drawer + topbar with
breadcrumbs. Two files plus a mount. No component library required (icons via
lucide-react; swap for any set). Works under Next.js App Router and static export.

## When to use

The user wants real app navigation: a left sidebar organized into sections
("hubs"), that collapses to an icon rail (burger), becomes a drawer on mobile,
and shows where you are (breadcrumbs). Trigger phrases: "sidebar", "side menu",
"collapsible menu", "hub navigation", "бокове меню", "меню з хабами", "бургер".

## Pieces

1. `nav-items.ts` — the nav data (a `HOME` link + `NAV_GROUPS` of hubs), plus
   helpers: `getNavGroups`, `getFlatNav`, `findTrail` (for breadcrumbs). Optional
   `EXTERNAL` flag to hide internal-only items in a public build.
2. `app-shell.tsx` — the client shell: desktop sidebar (accordion hubs, collapse
   to rail), mobile drawer + burger, sticky topbar (breadcrumbs + complexity
   badge + your toggles), main content. Persists collapse + open-hubs to
   localStorage.
3. Mount `<AppShell>{children}</AppShell>` in the root layout, wrapping the page.

## Styling / tokens

Uses shadcn-style CSS custom properties: `--sidebar`, `--sidebar-foreground`,
`--sidebar-accent`, `--sidebar-accent-foreground`, `--sidebar-border`,
`--primary`, `--muted`, `--muted-foreground`, `--background`, `--border`,
`--foreground`. If the project has shadcn, they exist. Otherwise define them once
for `:root` and `.dark`. Keep accent chroma modest so thin icons do not vibrate
on dark backgrounds.

## `src/components/nav-items.ts`

```ts
import type { LucideIcon } from "lucide-react";
import { Gauge, FileText, Settings, Users } from "lucide-react"; // pick real icons

export type NavItem = {
  href: string;
  label: string;
  icon: LucideIcon;
  complexity?: number; // optional 1..10 badge; drop if not needed
};
export type NavGroup = { id: string; label: string; items: NavItem[] };

export const HOME: NavItem = { href: "/", label: "Overview", icon: Gauge };

export const NAV_GROUPS: NavGroup[] = [
  {
    id: "group-a",
    label: "Section A",
    items: [
      { href: "/docs", label: "Docs", icon: FileText },
      { href: "/team", label: "Team", icon: Users },
    ],
  },
  {
    id: "group-b",
    label: "Section B",
    items: [{ href: "/settings", label: "Settings", icon: Settings }],
  },
];

// Optional: hide internal-only routes in a public build (set NEXT_PUBLIC_EXTERNAL=1).
export const EXTERNAL = process.env.NEXT_PUBLIC_EXTERNAL === "1";
const EXTERNAL_ALLOW = new Set<string>(["/", "/docs"]);

export function getNavGroups(): NavGroup[] {
  if (!EXTERNAL) return NAV_GROUPS;
  return NAV_GROUPS.map((g) => ({
    ...g,
    items: g.items.filter((i) => EXTERNAL_ALLOW.has(i.href)),
  })).filter((g) => g.items.length > 0);
}

export const NAV: NavItem[] = [HOME, ...NAV_GROUPS.flatMap((g) => g.items)];
export function getFlatNav(): NavItem[] {
  if (!EXTERNAL) return NAV;
  return [HOME, ...getNavGroups().flatMap((g) => g.items)];
}

// Resolve a route to { group, item } for breadcrumbs (matches sub-routes too).
export function findTrail(pathname: string): {
  group?: NavGroup;
  item?: NavItem;
} {
  if (pathname === "/") return { item: HOME };
  for (const g of NAV_GROUPS)
    for (const it of g.items)
      if (pathname === it.href || pathname.startsWith(it.href + "/"))
        return { group: g, item: it };
  return {};
}
```

## `src/components/app-shell.tsx`

```tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  ChevronDown,
  Menu,
  PanelLeftClose,
  PanelLeftOpen,
  X,
} from "lucide-react";
import {
  findTrail,
  getFlatNav,
  getNavGroups,
  HOME,
  type NavItem,
} from "@/components/nav-items";
import { cn } from "@/lib/utils"; // or: const cn = (...a) => a.filter(Boolean).join(" ")

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const groups = getNavGroups();
  const flat = getFlatNav();
  const trail = findTrail(pathname);
  const complexity = trail.item?.complexity;

  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openGroups, setOpenGroups] = useState<string[]>(() =>
    groups.map((g) => g.id),
  );

  useEffect(() => {
    try {
      setCollapsed(localStorage.getItem("nav-collapsed") === "1");
      const raw = localStorage.getItem("nav-groups");
      if (raw) setOpenGroups(JSON.parse(raw));
    } catch {}
  }, []);
  useEffect(() => {
    try {
      localStorage.setItem("nav-collapsed", collapsed ? "1" : "0");
    } catch {}
  }, [collapsed]);
  useEffect(() => {
    try {
      localStorage.setItem("nav-groups", JSON.stringify(openGroups));
    } catch {}
  }, [openGroups]);
  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  const toggleGroup = (id: string) =>
    setOpenGroups((p) =>
      p.includes(id) ? p.filter((x) => x !== id) : [...p, id],
    );
  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  function link(item: NavItem, compact: boolean, onNav?: () => void) {
    const active = isActive(item.href);
    return (
      <Link
        key={item.href}
        href={item.href}
        onClick={onNav}
        title={compact ? item.label : undefined}
        aria-current={active ? "page" : undefined}
        className={cn(
          "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
          compact && "justify-center px-0",
          active
            ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
            : "text-sidebar-foreground/70 hover:bg-sidebar-accent/60 hover:text-sidebar-foreground",
        )}
      >
        <item.icon className="h-4 w-4 shrink-0" aria-hidden />
        {!compact && <span className="truncate">{item.label}</span>}
      </Link>
    );
  }

  const expandedNav = (onNav?: () => void) => (
    <nav className="flex flex-1 flex-col gap-1 overflow-y-auto px-2 py-2">
      {link(HOME, false, onNav)}
      {groups.map((g) => {
        const open = openGroups.includes(g.id);
        return (
          <div key={g.id} className="mt-1">
            <button
              type="button"
              onClick={() => toggleGroup(g.id)}
              aria-expanded={open}
              className="flex w-full items-center justify-between rounded-lg px-3 py-1.5 font-mono text-[0.65rem] tracking-widest text-sidebar-foreground/50 uppercase transition-colors hover:text-sidebar-foreground"
            >
              {g.label}
              <ChevronDown
                className={cn(
                  "h-3.5 w-3.5 transition-transform",
                  open && "rotate-180",
                )}
              />
            </button>
            {open && (
              <div className="mt-0.5 flex flex-col gap-0.5">
                {g.items.map((it) => link(it, false, onNav))}
              </div>
            )}
          </div>
        );
      })}
    </nav>
  );

  const railNav = () => (
    <nav className="flex flex-1 flex-col gap-0.5 overflow-y-auto px-2 py-2">
      {flat.map((it) => link(it, true))}
    </nav>
  );

  return (
    <div className="flex min-h-full">
      {/* Desktop sidebar */}
      <aside
        className={cn(
          "sticky top-0 hidden h-svh shrink-0 flex-col border-r border-sidebar-border bg-sidebar transition-[width] duration-200 md:flex",
          collapsed ? "w-[64px]" : "w-60",
        )}
      >
        <div
          className={cn(
            "flex items-center gap-2 px-3 py-3",
            collapsed && "justify-center px-0",
          )}
        >
          <span className="h-2 w-2 shrink-0 rounded-full bg-primary" />
          {!collapsed && (
            <span className="truncate font-mono text-[0.7rem] tracking-[0.2em] text-sidebar-foreground/80 uppercase">
              App
            </span>
          )}
        </div>
        {collapsed ? railNav() : expandedNav()}
        <div
          className={cn(
            "border-t border-sidebar-border p-2",
            collapsed && "flex justify-center",
          )}
        >
          <button
            type="button"
            onClick={() => setCollapsed((v) => !v)}
            aria-label={collapsed ? "Expand menu" : "Collapse menu"}
            className="flex h-8 w-full items-center justify-center gap-2 rounded-lg text-sm text-sidebar-foreground/70 transition-colors hover:bg-sidebar-accent hover:text-sidebar-foreground"
          >
            {collapsed ? (
              <PanelLeftOpen className="h-4 w-4" />
            ) : (
              <>
                <PanelLeftClose className="h-4 w-4" />
                <span>Collapse</span>
              </>
            )}
          </button>
        </div>
      </aside>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div
            className="absolute inset-0 bg-black/50"
            aria-hidden
            onClick={() => setMobileOpen(false)}
          />
          <aside className="absolute inset-y-0 left-0 flex w-64 flex-col border-r border-sidebar-border bg-sidebar">
            <div className="flex items-center justify-between px-3 py-3">
              <span className="font-mono text-[0.7rem] tracking-[0.2em] text-sidebar-foreground/80 uppercase">
                App
              </span>
              <button
                type="button"
                onClick={() => setMobileOpen(false)}
                aria-label="Close menu"
                className="text-sidebar-foreground/70 hover:text-sidebar-foreground"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            {expandedNav(() => setMobileOpen(false))}
          </aside>
        </div>
      )}

      {/* Main column */}
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-30 flex h-14 items-center gap-2 border-b border-border bg-background/80 px-4 backdrop-blur sm:px-6">
          <button
            type="button"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
            className="-ml-1 flex h-9 w-9 items-center justify-center rounded-lg hover:bg-muted md:hidden"
          >
            <Menu className="h-5 w-5" />
          </button>
          <nav
            aria-label="Breadcrumb"
            className="flex min-w-0 items-center gap-1.5 font-mono text-[0.65rem] tracking-wider text-muted-foreground uppercase sm:text-xs"
          >
            {trail.group && (
              <>
                <span className="truncate">{trail.group.label}</span>
                <span aria-hidden className="opacity-50">
                  /
                </span>
              </>
            )}
            <span className="truncate text-foreground">
              {trail.item?.label ?? "Overview"}
            </span>
            {typeof complexity === "number" && (
              <span className="ml-1.5 hidden shrink-0 rounded-full border border-border px-1.5 py-0.5 text-[0.6rem] sm:inline">
                {complexity}/10
              </span>
            )}
          </nav>
          <div className="ml-auto flex items-center gap-2">
            {/* ThemeToggle, actions */}
          </div>
        </header>
        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

## Mount (root layout)

```tsx
// app/layout.tsx
import { AppShell } from "@/components/app-shell";
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-full">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
```

## Adapt checklist

- Replace `NAV_GROUPS` / `HOME` with the project's real routes and icons.
- Drop `complexity` and the badge if not wanted; drop `EXTERNAL` if there is no
  public/internal split.
- `cn` is shadcn's `clsx`+`tailwind-merge` helper; inline a trivial join if the
  project lacks it.
- If not Tailwind, port classes to the project's styling; keep the structure:
  collapse state, accordion hubs, rail when collapsed, mobile drawer, breadcrumbs.
- Keep accent chroma modest so icons/text do not shimmer on dark.
