---
name: inbox-process
description: Weekly append-and-review inbox processing for second-brain vaults. Use when the user says "process inbox", "розбери інбокс", "розклади нотатки", or at weekly review time. Files inbox items into PARA folders, updates MOCs, rescues still-relevant items to the top, refreshes the hot cache. Pass a vault name to target a specific vault.
---

# Inbox process — append-and-review weekly pass

Processes the single capture note of a second-brain vault into its PARA
structure (Projects / Areas / Resources / Archive).

## Configure your vaults

Before first use, fill this table in with your own vaults. The argument passed
to the skill (`/inbox-process <arg>`) selects the row; no argument uses the
first one.

| Arg               | Vault root              | Inbox              | Hot cache |
| ----------------- | ----------------------- | ------------------ | --------- |
| _(none)_ / `main` | `~/Vaults/<your-vault>` | `0 INBOX/inbox.md` | `hot.md`  |
| `work`            | `~/vaults/<work-vault>` | `0 INBOX/inbox.md` | `hot.md`  |

If the vault uses localized folder names (e.g. `10 Проекти` instead of
`10 Projects`), note the mapping here too — step 2 refers to these folders.

## Procedure

1. **Read** the vault's hot cache, then `inbox.md` top-to-bottom. Items are
   separated by blank lines or bullets; newest on top. Also list any loose
   files sitting in `0 INBOX/` beside `inbox.md` — they are items too.
2. **Classify each item** (append-and-review + PARA):
   - **Actionable, tied to an outcome** → note in `10 Projects/<project>/`.
     Create the project folder only if ≥2 items point at it; otherwise file
     under the closest area.
   - **Standing responsibility / interest** → `20 Areas`.
   - **Reference (article, tool, idea-for-later)** → `30 Resources`.
   - **Task, not knowledge** (do X, call Y) → do NOT create a note; route it to
     your task layer (todo app, project board). Leave a one-line pointer in the
     filed summary.
   - **Still hot but unfileable** → RESCUE: move the line back to the top of
     `inbox.md` (this is the attention-ranking mechanism — not a failure).
   - **Dead / no longer interesting** → drop silently. Don't archive noise.
3. **Filing rules:** one idea per note, kebab-case filename, `[[link]]` to the
   nearest MOC/map and to related notes. Match the vault's language
   conventions.
4. **Update maps:** add the new note to the relevant MOC (`mocs/`, `Home.md`,
   or the closest MOC note).
5. **Write back:**
   - Rewrite `inbox.md`: header intact, rescued items on top, everything else
     removed.
   - Append one line to the vault log (e.g. `log.md`) if the vault keeps one.
   - Update the hot cache "Active" section if a new project emerged.
6. **Report** (in chat): N items → filed X, rescued Y, dropped Z, tasks
   routed T, with links to created notes. Never claim "processed" without
   showing the per-item disposition.

## Guardrails

- Never delete or rewrite notes outside `0 INBOX/`, MOC link-sections, the hot
  cache, and the log.
- If an item is ambiguous between two homes, prefer the PARA folder closer to
  action (Projects > Areas > Resources) and link from both MOCs.
- If the inbox has >30 items, process the top 30 and say so — don't silently
  truncate.
