---
name: claude-context-picker
description: Add a floating "copy context for Claude" widget to a web app (React/Next). A FAB opens options to copy the current page/section reference OR enter an element-pick mode where clicking any element on the page copies a reference (route + element tag + text) to the clipboard, so the user can paste it into a Claude chat to point at exactly what to change. Use when the user asks for a floating button / element picker / "copy context" / "скопіювати контекст для Клода" / "плаваюча кнопка щоб кинути тобі в чат".
---

# Claude context picker (floating copy-for-Claude widget)

A small client-side widget the user clicks to grab a precise reference to a page
or a specific element and copy it to the clipboard, then paste into a Claude
chat. Removes the "which section / which element do you mean" back-and-forth.

## When to use

The user wants a floating on-page control that copies context (a route, a
section, or a clicked element) to the clipboard so they can hand it to Claude.
Trigger phrases: "floating button", "element picker", "copy context for Claude",
"скопіювати контекст", "плаваюча кнопка щоб кинути в чат", "вибрати елемент і
скопіювати".

## What it does

- Floating action button (FAB), bottom-right.
- Click → small menu: **Copy current page** and **Pick element on page**.
- Pick mode: hovering outlines elements; clicking one copies
  `route + <tag> + trimmed text` and exits. `Esc` cancels.
- A toast confirms the copy.
- The widget marks its own DOM with `data-ccpick` and ignores those targets in
  pick mode so it never captures itself.

## How to add it (React / Next.js, client component)

1. Create `src/components/claude-context-picker.tsx` with the component below.
2. Mount it once, high in the tree (root layout or an app shell that is a client
   component). It is `position: fixed`, so placement in the tree does not matter.
3. No dependencies beyond `react` and an icon set (swap the lucide icons for
   plain text/SVG if none is available). Works under static export (all
   client-side, no server route).

```tsx
"use client";

import { useEffect, useRef, useState } from "react";

// Optional: derive a human section label however the app wants. Simplest is the
// pathname; in Next use usePathname(); elsewhere use window.location.pathname.
function useRoute() {
  const [route, setRoute] = useState("");
  useEffect(() => setRoute(window.location.pathname), []);
  return route;
}

export function ClaudeContextPicker() {
  const route = useRoute();
  const [open, setOpen] = useState(false);
  const [picking, setPicking] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const hoverRef = useRef<HTMLElement | null>(null);

  function copy(text: string, note: string) {
    navigator.clipboard.writeText(text).then(
      () => {
        setToast(note);
        setTimeout(() => setToast(null), 1800);
      },
      () => {},
    );
  }

  function copyPage() {
    copy(`Page ${route} (title: ${document.title}).\n\nTask: `, "Page copied");
    setOpen(false);
  }

  useEffect(() => {
    if (!picking) return;
    const clean = (el: HTMLElement | null) => {
      if (el) {
        el.style.outline = "";
        el.style.outlineOffset = "";
      }
    };
    const ignore = (t: EventTarget | null) =>
      t instanceof HTMLElement && t.closest("[data-ccpick]");

    const onMove = (e: MouseEvent) => {
      if (ignore(e.target)) return;
      const el = e.target as HTMLElement;
      if (el === hoverRef.current) return;
      clean(hoverRef.current);
      hoverRef.current = el;
      el.style.outline = "2px solid #4f9d5b";
      el.style.outlineOffset = "1px";
    };
    const onClick = (e: MouseEvent) => {
      if (ignore(e.target)) return;
      e.preventDefault();
      e.stopPropagation();
      const el = e.target as HTMLElement;
      const text = (el.innerText || el.textContent || "")
        .trim()
        .replace(/\s+/g, " ")
        .slice(0, 160);
      copy(
        `Page ${route}. Element <${el.tagName.toLowerCase()}>: "${text}".\n\nTask: `,
        "Element copied",
      );
      clean(hoverRef.current);
      hoverRef.current = null;
      setPicking(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        clean(hoverRef.current);
        hoverRef.current = null;
        setPicking(false);
      }
    };

    document.addEventListener("mousemove", onMove, true);
    document.addEventListener("click", onClick, true);
    document.addEventListener("keydown", onKey, true);
    document.body.style.cursor = "crosshair";
    return () => {
      document.removeEventListener("mousemove", onMove, true);
      document.removeEventListener("click", onClick, true);
      document.removeEventListener("keydown", onKey, true);
      document.body.style.cursor = "";
      clean(hoverRef.current);
      hoverRef.current = null;
    };
  }, [picking, route]);

  return (
    <div data-ccpick>
      {toast && <div style={fab.toast}>{toast} ✓</div>}
      {picking && (
        <div style={fab.banner}>Click an element to copy. Esc to cancel.</div>
      )}
      {open && !picking && (
        <div style={fab.menu}>
          <button style={fab.item} onClick={copyPage}>
            Copy current page
          </button>
          <button
            style={fab.item}
            onClick={() => {
              setOpen(false);
              setPicking(true);
            }}
          >
            Pick element on page
          </button>
        </div>
      )}
      <button
        aria-label="Copy context for Claude"
        style={fab.btn}
        onClick={() => (picking ? setPicking(false) : setOpen((v) => !v))}
      >
        {open || picking ? "×" : "✦"}
      </button>
    </div>
  );
}

// Inline styles so the skill has zero CSS deps; swap for the host app's classes.
const fab = {
  btn: {
    position: "fixed",
    right: 20,
    bottom: 20,
    zIndex: 50,
    width: 48,
    height: 48,
    borderRadius: 999,
    border: "1px solid #0002",
    background: "#4f9d5b",
    color: "#fff",
    fontSize: 20,
    cursor: "pointer",
  },
  menu: {
    position: "fixed",
    right: 20,
    bottom: 80,
    zIndex: 50,
    width: 240,
    borderRadius: 12,
    border: "1px solid #0002",
    background: "#fff",
    color: "#111",
    padding: 8,
    boxShadow: "0 8px 30px #0003",
    display: "flex",
    flexDirection: "column",
    gap: 4,
  },
  item: {
    textAlign: "left",
    padding: "8px 10px",
    borderRadius: 8,
    border: 0,
    background: "transparent",
    cursor: "pointer",
    fontSize: 14,
  },
  banner: {
    position: "fixed",
    top: 16,
    left: "50%",
    transform: "translateX(-50%)",
    zIndex: 60,
    borderRadius: 999,
    border: "1px solid #0002",
    background: "#fff",
    color: "#111",
    padding: "8px 16px",
    fontSize: 14,
    boxShadow: "0 8px 30px #0003",
  },
  toast: {
    position: "fixed",
    right: 20,
    bottom: 96,
    zIndex: 60,
    borderRadius: 8,
    background: "#4f9d5b",
    color: "#fff",
    padding: "8px 12px",
    fontSize: 14,
  },
} as const;
```

## Layout: separate buttons, not a menu

Prefer **separate, always-visible floating buttons** (one per action: "Copy
section", "Pick element"), each firing on a single click. Do NOT hide them behind
one FAB that opens a menu: that forces a double-click (open, then choose). Stack
the buttons vertically bottom-right. In pick mode, the element button flips to a
"Cancel" state. The code above uses a menu for brevity; when the user cares about
click count, split it into two direct buttons.

## Customization notes

- **Section label:** if the app has a nav/route map, resolve the route to a nice
  section name (e.g. `Group / Page`) instead of the raw pathname.
- **Copied string:** keep it short and end with `Task: ` so the user types what
  to do after pasting. Include the repo/app name if the user works across several.
- **Styling:** replace the inline `fab` styles with the host design system
  (Tailwind classes, theme tokens). Mark all widget DOM with `data-ccpick`.
- **Non-React app:** the same three document-level listeners (mousemove/click/
  keydown in capture phase) work in vanilla JS; render the FAB with plain DOM.
