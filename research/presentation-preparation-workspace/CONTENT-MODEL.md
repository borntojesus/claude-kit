# Контент модель

## Структура

```text
content/projects/
  <project>/
    project.yml
    research/
      audience.md
      market.md
    assets/
    evidence-ledger.csv
    presentations/
      <presentation>/
        presentation.yml
        research/
          objections.md
        slides/
          01-intro.md
          02-problem.md
```

Folder name є стабільним slug. Slide order визначає numeric prefix. Постійне посилання використовує решту filename.

## Project і presentation

Project містить shared research та assets. Presentation додає event, date, duration, status, visibility і `excludeResearch`.

Research inheritance має два рівні:

1. Project research доступний усім presentation цього project.
2. Presentation research із тим самим slug замінює project document.
3. `excludeResearch` явно видаляє непотрібний inherited document.

Глибший cascade не потрібний. Два рівні легко пояснити та перевірити.

## Slide frontmatter

Audience facing fields:

```yaml
title: Retention limits growth
section: Problem
kicker: Current state
visibility: public
points:
  - Activation improved
  - Retention did not
claimIds: [C-001]
media: retention-chart.svg
mediaFit: contain
```

## Slide kitchen

Markdown body використовує дозволені H2 секції:

| Section | Питання |
|---|---|
| `Goal` | Що має змінитися в кімнаті після слайда? |
| `Voice` | Що сказати, спитати або зробити? |
| `Research` | Який аналіз підтримує слайд? |
| `Claims` | Які твердження та числа використані? |
| `Sources` | Де лежить точний доказ? |
| `Objections` | Яке сильне заперечення очікувати? |
| `Timing` | Скільки секунд витратити? |
| `Audience response` | Яка спостережувана реакція потрібна? |
| `Verification` | Як відтворити факт або графік? |

Невідома H2 секція зупиняє validation. Мовчазне ігнорування створює втрату даних.

## Evidence trace

```text
slide point
  -> claim ID
  -> evidence ID
  -> exact source and location
  -> reproducible query or document excerpt
```

Claim без evidence залишається hypothesis. Він не переходить у public deck як факт.

## Templates

Starter files лежать у [templates/](templates/). Ті самі assets входять до installable skill у `skills/presentation-preparation/assets/`.
