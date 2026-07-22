# Test plan

## Content parser

1. Valid project, presentation, research і slide files parse.
2. Unknown frontmatter key produces a useful file and line error.
3. Unknown slide kitchen H2 fails validation.
4. Duplicate slide slug fails validation.
5. Missing media fails validation.
6. Broken internal research link fails validation.
7. Missing `excludeResearch` target fails validation.

## Research inheritance

1. Project document appears in every presentation by default.
2. Presentation document with the same slug replaces it.
3. `excludeResearch` removes it.
4. Sort order remains stable.

## Evidence

1. Every `claimId` exists in the ledger.
2. Every evidence row points to a source location.
3. A hypothesis cannot be rendered as a confirmed public claim.
4. Reproducible claims regenerate the same result from a fixture.

## Deck

1. Previous and next controls stop at boundaries.
2. Presenter keys work.
3. Form input focus disables shortcuts.
4. Black screen exits on the next key without advancing.
5. Fullscreen excludes sidebar and kitchen.
6. Shared slide slug opens the correct slide after reordering.

## Sidebar

1. Active route and breadcrumb match.
2. Project and presentation research are separated visibly.
3. Desktop collapse state persists.
4. Mobile drawer opens, traps focus correctly, closes on navigation and Escape.
5. Icon rail has accessible names and tooltips.

## Public boundary

1. Internal routes are absent.
2. Internal navigation labels are absent.
3. Sentinel scan finds no internal fixture text in any output file.
4. Speaker notes, objections and research paths are absent.
5. Public slide links remain stable.

## Rehearsal gates

1. Full, normal and compressed paths are documented.
2. Normal path fits the slot in a timed run.
3. Each slide has a timing target.
4. Top objections have prepared answers.
5. Every slide earns its place through a stated Goal.
