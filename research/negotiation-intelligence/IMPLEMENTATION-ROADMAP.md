# Implementation roadmap

## Phase 0: conventions

Результат:

- зафіксовані artifact schemas
- naming convention
- sample engagement
- ліцензійні правила
- test fixtures без конфіденційних даних

Exit criteria:

- усі JSON і CSV schemas проходять validation
- один sample engagement можна прочитати без усних пояснень

## Phase 1: audience and negotiation

Створити:

- `skills/audience-intelligence`
- `skills/negotiation-prep`
- `agents/audience-researcher.md`
- `agents/counterparty-simulator.md`

Eval cases:

1. B2B renewal із ризиком підвищення ціни.
2. Salary negotiation.
3. Vendor procurement із кількома stakeholders.
4. Internal budget approval.
5. Partnership negotiation із невідомою BATNA іншої сторони.

Критерії:

- positions не змішані з interests
- unknowns позначені
- BATNA не вигадана
- decision roles визначені
- issue matrix містить tradable variables

## Phase 2: evidence and data analysis

Створити:

- `skills/evidence-ledger`
- `skills/data-analysis-workflow`
- `agents/data-analyst.md`
- scripts для profiling, hashing і validation

Test datasets:

- clean SaaS metrics
- duplicate events
- missing denominator
- mixed currencies
- timezone boundary
- Simpson's paradox case
- correlation without causation case

Критерії:

- raw data не змінена
- кожен finding відтворюється
- metric definition явна
- limitations присутні
- confidence не завищений

## Phase 3: visualization

Створити:

- `skills/chart-selection`
- `agents/visualization-critic.md`
- Vega-Lite schema validator
- SVG і PNG renderer

Eval cases:

- category comparison
- time trend
- cohort retention
- distribution
- uncertainty
- scenario sensitivity
- misleading truncated axis

Критерії:

- chart відповідає analytical question
- source і transformation записані
- spec валідний
- accessibility check пройдений
- title не сильніший за finding

## Phase 4: narrative and red team

Створити:

- `skills/decision-narrative`
- `skills/presentation-audit`
- `skills/qa-rehearsal`
- `agents/evidence-red-team.md`

Audit dimensions:

- factual accuracy
- logical validity
- audience fit
- negotiation risk
- missing counterargument
- overclaiming
- disclosure boundaries
- action clarity

## Phase 5: packaging

Після стабілізації:

1. Додати skills та agents до основного plugin.
2. Оновити `.claude-plugin/plugin.json` за потреби.
3. Оновити README counts.
4. Додати upstream attribution до `NOTICE.md`.
5. Протестувати через `claude --plugin-dir`.
6. Запустити `/doctor` і skill evals.
7. Перевірити чисту інсталяцію з marketplace.

## Перевірка skills

Для кожного skill потрібні:

- trigger tests
- non-trigger tests
- golden structure checks
- adversarial input
- incomplete input
- conflicting sources
- sensitive data case
- deterministic schema validation

Scorecard:

| Dimension | Weight |
|---|---:|
| Factual grounding | 25% |
| Completeness | 15% |
| Correct uncertainty | 15% |
| Reproducibility | 15% |
| Decision usefulness | 15% |
| Audience fit | 10% |
| Format compliance | 5% |

Автоматична перевірка не замінює blind human review. `skill-creator` рекомендує порівнювати варіанти на реальних test prompts і генерувати review artifact для людини.

## Порядок реалізації

Якщо ресурс обмежений, порядок такий:

1. `evidence-ledger`
2. `audience-intelligence`
3. `negotiation-prep`
4. `data-analysis-workflow`
5. `chart-selection`
6. `presentation-audit`
7. `qa-rehearsal`

`evidence-ledger` стоїть першим, бо він створює спільний контракт для дослідження, аналізу, графіків і narrative.

## Умови готовності

Перша production-ready версія готова, коли:

- три різні типи переговорів проходять end-to-end workflow
- кожне число в narrative має evidence trace
- усі графіки відтворюються з source data
- red team знаходить planted defects у test fixtures
- skill trigger tests стабільні
- немає ліцензійних прогалин
- clean install працює без ручного копіювання файлів
