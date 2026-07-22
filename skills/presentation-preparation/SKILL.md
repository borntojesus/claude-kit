---
name: presentation-preparation
description: Build or improve a research backed presentation workspace with a grouped sidebar, live deck, evidence and speaker notes under each slide, reusable research documents, public and internal views, and validation gates. Use for presentation preparation hubs, speaker press centers, slide research systems, pitch workspaces, deck review tools, or requests for a side menu with a presentation and detailed supporting data below it.
---

# Presentation preparation

Build the presentation as a traceable working system, not as a loose slide file.

## Workflow

1. Write a brief with audience, decision, duration, venue, constraints, source boundary, and definition of done.
2. Create separate `public` and `internal` visibility levels before adding content.
3. Store projects, presentations, research, slides, sources, and assets as files in Git.
4. Build a grouped sidebar from content metadata. Reuse the `sidebar-nav-shell` skill when implementing a React or Next.js interface.
5. Render the live deck in the main column. Support previous, next, fullscreen, black screen, Home, End, and presenter clicker keys.
6. Render the current slide's internal preparation data immediately below the deck.
7. Link every factual claim to a research document or source ledger entry.
8. Keep raw source material in research files. Put only the minimum audience facing text on the slide.
9. Generate the public build from `visibility`, then scan its output for internal markers.
10. Validate content and rehearse before calling the deck ready.

## Required slide kitchen

Each slide may contain these internal sections:

```text
Goal
Voice
Research
Claims
Sources
Objections
Timing
Audience response
Verification
```

Keep `Goal`, `Voice`, `Research`, and `Sources` available on every slide. Add the other sections when useful. Unknown section names must fail validation instead of disappearing silently.

## Interface contract

Use three stable regions:

```text
left sidebar | deck canvas
             | slide controls
             | current slide kitchen
             | related research and source details
```

The sidebar contains project research and presentation research. The deck stays in the main column. Fullscreen contains only the slide canvas. Internal preparation data never appears in fullscreen or the public build.

## Content rules

Use Markdown plus YAML frontmatter. Folder names define stable slugs. Numeric filename prefixes define slide order. Keep project research and presentation research in separate folders. A presentation document with the same slug overrides the project document. `excludeResearch` removes inherited research explicitly.

Read [references/content-model.md](references/content-model.md) when creating or validating files. Read [references/workspace-architecture.md](references/workspace-architecture.md) when designing routes, modules, visibility, or the interface.

Copy starter files from `assets/` when scaffolding a new workspace.

## Release gates

Require all of the following:

1. YAML and frontmatter schemas pass.
2. Slide and research slugs are unique in their scope.
3. Media files and internal links resolve.
4. Every numeric or factual claim has a source or an explicit hypothesis label.
5. Keyboard controls work without trapping focus or hijacking form inputs.
6. The sidebar works as a desktop rail and mobile drawer.
7. Internal routes and markers are absent from the public artifact.
8. The deck has a rehearsed full, normal, and compressed timing path.
9. Public copy passes the humanizer review.

Do not generate a PPTX until the narrative, claims, evidence, and slide order pass review.
