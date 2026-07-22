# Provenance

## Source snapshot

The pattern was extracted from the local `talk-scale-academy` repository at commit:

```text
72f0e0d3e3f64ed903aedf3a31ed0fa24132ab53
```

Relevant source units:

```text
app/src/components/app-shell.tsx
app/src/components/nav-items.ts
app/src/components/pitch-deck.tsx
app/src/data/pitch.ts
docs/superpowers/specs/2026-07-20-presentation-research-tool-design.md
notes/presentation-toolkit.md
```

## What was generalized

1. Hard coded navigation became content driven project and presentation navigation.
2. TypeScript slide objects became Markdown and YAML files.
3. The original `goal`, `voice`, `research` and `links` detail block became a larger slide kitchen with claim trace and rehearsal fields.
4. One presentation became a project with many presentations.
5. One public cut became a reusable visibility model and artifact leak test.

## What was excluded

No participant profile, correspondence, private business metric, customer data, credential, server address, tunnel identifier, or deployment command was copied.

The supporting demo catalog was not copied. Its role was architectural evidence that a deck can link to deeper interactive material outside the slide canvas.

## Relationship to existing research

The package complements [Negotiation Intelligence](../negotiation-intelligence/README.md). Negotiation Intelligence produces audience maps, findings, evidence ledgers and narrative. This package stores and renders those artifacts around a live deck.
