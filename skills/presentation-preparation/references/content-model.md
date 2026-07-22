# Content model

## Folder layout

```text
content/projects/<project>/
  project.yml
  research/
    <topic>.md
  assets/
  presentations/<presentation>/
    presentation.yml
    research/
      <topic>.md
    slides/
      01-intro.md
      02-problem.md
```

The folder name is the slug. Do not repeat a mutable slug inside YAML.

## Project

```yaml
title: Quarterly strategy review
description: Presentation workspace for leadership reviews.
tags: [strategy, leadership]
order: 10
visibility: internal
```

## Presentation

```yaml
title: Growth plan
description: Decision deck for the next operating cycle.
event: Leadership review
date: 2026-08-15
durationMin: 30
status: draft
visibility: internal
excludeResearch: []
```

## Slide

```markdown
---
title: Retention limits growth
section: Problem
kicker: Current state
visibility: public
points:
  - Activation improved
  - Retention did not
claimIds: [C-001]
---

## Goal

Secure agreement that retention is the first constraint to fix.

## Voice

Pause after the cohort chart and ask which segment deserves attention first.

## Research

See the research document `research/retention`.

## Claims

`C-001`: Week eight retention fell from 31% to 24%.

## Sources

`E-004`: `analysis/cohorts.sql`, result captured 2026-08-01.

## Objections

Acquisition volume changed during the same period.

## Timing

90 seconds.

## Audience response

The owner names the segment to investigate.

## Verification

Rebuild the chart from `analysis/cohorts.sql`.
```

## Research document

```markdown
---
title: Retention analysis
summary: Cohort evidence behind the retention section.
order: 20
visibility: internal
---

State the question, method, evidence, limits, and decision implication.
```

## Evidence ledger

Use one row per evidence item:

```csv
evidence_id,claim_id,source,location,observed_at,confidence,notes
E-004,C-001,warehouse,analysis/cohorts.sql,2026-08-01,high,Reproducible query
```

Claims without evidence must carry `status: hypothesis` and stay out of the public deck until confirmed.
