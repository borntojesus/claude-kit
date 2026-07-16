# The Karpathy Method — how to work in this repo fleet

> Agent-facing operating manual. Read this when starting work in any repo under
> `~/github`. It exists so that any session — fresh or resumed — understands
> _how_ we build here, not just _what_ the code is. Named after Andrej
> Karpathy's way of working with LLMs: small verifiable steps, the spec leads,
> and the context (the "vault") is treated as durable memory rather than thrown
> away each session.

## The one-paragraph version

Before writing code, write the **spec** — what "done" looks like and how it will
be verified. Then **decompose** the goal into the smallest units that can each
be built and checked on their own. Build **one unit at a time**, **verify it for
real** (run it, observe it), then **write the result back** into long-term
memory as a linked note. Repeat. The vault/memory is the project's brain across
sessions; the chat window is not. Never let work outrun the spec, and never let
a unit grow past "one thing I can test."

## The loop

```
Spec  →  Decompose  →  Implement one unit  →  Verify (run it)  →  Write back  →  ↺
```

1. **Spec before code.** State the goal, the acceptance criteria, and the
   verification method _first_ — even one paragraph. If you can't say how you'll
   know it works, you're not ready to write it.
2. **Decompose into minimal, independently-testable units.** Each unit should be
   buildable and verifiable alone. If a step can't be tested in isolation, split
   it further. Smaller units = fewer places for a bug to hide and cheaper rework.
3. **Implement one unit.** Match the surrounding code's idiom, naming, and
   comment density. Minimum-viable diff: fix only what the unit needs; resist
   refactors that weren't asked for (see the Minimal Change discipline).
4. **Verify for real.** Run the app/test and observe the behaviour — don't assume
   a passing edit means a passing feature. `tsc --noEmit`, the dev server, a
   curl, a screenshot, an actual click. Evidence over hope.
5. **Write back to the vault.** Capture what was learned, decided, or built as a
   durable note — not in the chat, which evaporates. Link it to related notes.
   The next session reads the vault, not the transcript.

## Where memory lives (layers, fastest to slowest)

| Layer                | Location                                                               | What goes here                                                                   |
| -------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Session journal**  | injected by the SessionStart hook                                      | recent per-project session entries — read first, every session                   |
| **Agent memory**     | native per-project `memory/` dir, indexed by `MEMORY.md`               | durable facts future sessions need (one fact per file); auto-loaded each session |
| **Karpathy vault**   | repo's `wiki/` Obsidian vault (when present) — start at `wiki/Home.md` | spec notes, decisions, `[[linked]]` atomic notes; the project's long-term brain  |
| **Auto session log** | `~/Vaults/<your-vault>/sessions/<project>.md`              | written automatically by the SessionEnd hook — never hand-edit                   |

**Read order at session start:** session journal → `MEMORY.md` → `wiki/Home.md`
(if the repo has a vault) → the repo's `CLAUDE.md`.

## Principles

- **The spec leads.** Code serves the spec, not the reverse. Update the spec
  note when the goal changes; don't let code and spec silently diverge.
- **Atomic, linked notes.** One idea per note. Link liberally with `[[name]]`; a
  link to a note that doesn't exist yet marks something worth writing later.
- **Don't duplicate what the repo already records.** Code structure, git
  history, past fixes, and `CLAUDE.md` are already memory. Save only what is
  _non-obvious_ and not derivable from them.
- **Verify, then claim.** State outcomes faithfully: if a test fails, say so with
  the output; if a step was skipped, say that. "Done" means observed-working.
- **Smallest unit wins.** When unsure how far to decompose, go smaller. A unit
  you can verify in one step is always cheaper than one you can't.
- **Write back before moving on.** A finished unit isn't finished until its
  result is in durable memory and (if it's a code unit) committed as one logical
  Conventional-Commits change.

## Per-task checklist

- [ ] Wrote/located the **spec** and acceptance criteria.
- [ ] **Decomposed** into minimal independently-testable units.
- [ ] Read the relevant memory layers first.
- [ ] Built **one unit**, matched local idiom, minimal diff.
- [ ] **Verified by running it** (not just by editing).
- [ ] **Wrote back** the result/decision as a linked note + committed the unit.

## Relationship to the global rules

This expands the "Obsidian Memory Method" and "Karpathy method" notes in
`~/.claude/CLAUDE.md`. Those rules still govern; this file is the longer-form
operating manual for the `~/github` fleet. Repo-specific conventions live in each
repo's own `CLAUDE.md` and override nothing here — they specialise it.
