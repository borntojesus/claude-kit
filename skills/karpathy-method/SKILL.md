---
name: karpathy-method
description: Use when starting any non-trivial task in the ~/github repo fleet (or any repo carrying a wiki/ Obsidian vault). Establishes the spec-first, decompose → build-one-unit → verify-for-real → write-back operating loop and the memory layers (session journal, agent memory, wiki vault). Invoke before planning or writing code so the working method and durable memory are in context.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: "[task or goal]"
---

# The Karpathy Method

Operating manual for working in the `~/github` repo fleet. Named after Andrej
Karpathy's way of working with LLMs: small verifiable steps, the spec leads, and
the context (the "vault") is durable memory rather than chat that evaporates.

The full manual ships beside this skill at `KARPATHY-METHOD.md` — read it when you need the
long form. This skill is the short, always-loadable version.

## Before doing anything: read memory (fastest → slowest)

1. **Session journal** — injected by the SessionStart hook (recent per-project
   entries). Already in context; skim it.
2. **Agent memory** — `<project>/memory/MEMORY.md` + the linked fact files.
3. **Wiki vault** — if the repo has `wiki/`, start at `wiki/Home.md`. For the
   fleet root, that is `~/github/wiki/Home.md`.
4. **Repo `CLAUDE.md`** — repo-specific conventions.

## The loop

```
Spec  →  Decompose  →  Implement ONE unit  →  Verify (run it)  →  Write back  →  ↺
```

1. **Spec before code.** State the goal, acceptance criteria, and how you'll
   verify it — even one paragraph. If you can't say how you'll know it works,
   you're not ready to write it. Capture it as a note in `wiki/specs/`.
2. **Decompose into minimal, independently-testable units.** If a step can't be
   tested alone, split it further. Smallest unit wins.
3. **Implement one unit.** Match local idiom, naming, comment density. Minimum
   viable diff — fix only what the unit needs; no unrequested refactors.
4. **Verify for real.** Run the app/test, observe behaviour. `tsc --noEmit`, the
   dev server, a curl, a screenshot, a click. Evidence over hope.
5. **Write back.** Capture what was learned/decided/built as a durable, linked
   note (`[[name]]`) in the vault or agent memory — not in the chat. Then commit
   the unit as one logical Conventional-Commits change.

## Write-back targets

- **Durable fact a future session needs** (one per file) → agent `memory/` +
  index line in `MEMORY.md`.
- **Spec / decision / design reasoning** → `wiki/` note, linked from `Home.md`.
- **Don't duplicate** what code, git history, or `CLAUDE.md` already record. Save
  only the non-obvious.

## Per-task checklist (make one todo per item)

- [ ] Located/wrote the **spec** + acceptance criteria.
- [ ] **Decomposed** into minimal independently-testable units.
- [ ] Read the relevant memory layers first.
- [ ] Built **one unit**, matched local idiom, minimal diff.
- [ ] **Verified by running it** (not just editing).
- [ ] **Wrote back** the result as a linked note + committed the unit.
