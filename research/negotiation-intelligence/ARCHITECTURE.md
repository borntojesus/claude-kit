# Claude Code architecture

## Packaging

Під час розробки компоненти доцільно тримати в `.claude/skills/` і `.claude/agents/` тестового проєкту. Після стабілізації їх треба перенести до plugin structure цього репозиторію.

```text
negotiation-intelligence/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── audience-intelligence/
│   ├── negotiation-prep/
│   ├── evidence-ledger/
│   ├── data-analysis-workflow/
│   ├── chart-selection/
│   ├── decision-narrative/
│   └── presentation-audit/
├── agents/
│   ├── audience-researcher.md
│   ├── data-analyst.md
│   ├── visualization-critic.md
│   ├── counterparty-simulator.md
│   └── evidence-red-team.md
└── bin/
    ├── profile-data
    ├── analyze-data
    ├── render-chart
    └── validate-evidence
```

Офіційний Claude Code plugin layout вимагає, щоб `.claude-plugin/` містив лише `plugin.json`. Папки `skills/`, `agents/`, `hooks/` і `bin/` мають лежати в корені plugin.

## Межа між skills та agents

### Skill

Використовувати для:

- чекліста
- послідовності дій
- output schema
- правил вибору методу
- завантаження references
- виклику deterministic script

Skill має бути коротким. Довгі методики розміщуються в `references/`. Script виконується, а не завантажується в prompt.

### Subagent

Використовувати для:

- незалежного дослідження
- ізоляції великого контексту
- альтернативної інтерпретації
- симуляції іншої сторони
- adversarial review

Для `audience-researcher`, `counterparty-simulator` і `evidence-red-team` рекомендовано `memory: project`. У memory дозволено зберігати лише перевірені повторювані факти, патерни та рішення. Не можна переносити непідтверджені психологічні припущення як факти.

## Оркестрація

Основний Claude process залишається оркестратором. Він не делегує один і той самий аналіз кільком агентам без чіткої причини. Кожен subagent отримує:

- обмежене питання
- список дозволених джерел
- очікуваний output schema
- каталог для результату
- правило не змінювати source data

## Контракти артефактів

### `findings.json`

```json
[
  {
    "id": "F-001",
    "claim": "Activation decreased after the onboarding change",
    "metric": "seven_day_activation_rate",
    "baseline": 0.48,
    "current": 0.37,
    "effect": -0.11,
    "method": "cohort comparison",
    "confidence": "medium",
    "evidence_ids": ["E-003", "E-004"],
    "limitations": ["No randomized control group"],
    "decision_implication": "Do not increase acquisition spend before fixing onboarding"
  }
]
```

### `evidence-ledger.csv`

```csv
evidence_id,claim_id,source_type,source,location,observed_at,confidence,notes
E-003,F-001,dataset,data/events.parquet,query.sql,2026-07-22,high,Reproducible from raw events
E-004,F-001,document,research/interviews.md,lines 42-58,2026-07-22,medium,Qualitative support only
```

### `audience-map.csv`

```csv
person,role,decision_role,influence,stance,interests,risks,metrics,evidence_preference,expected_action,confidence
Jane Doe,CFO,economic_buyer,5,neutral,cash efficiency,implementation risk,free cash flow,scenario model,approve budget,medium
```

`confidence` описує якість нашого знання про учасника. Воно не є оцінкою характеру людини.

### Chart specification

Кожен графік повинен мати:

- `question`
- `finding_id`
- `data_source`
- `transform`
- `chart_type`
- `vega_lite_spec`
- `annotation`
- `uncertainty`
- `accessibility_note`

Графік без `finding_id` не потрапляє до presentation outline.

## Negotiation model

`negotiation-prep` має розділяти:

- positions: заявлені вимоги
- interests: причини вимог
- BATNA: найкраща альтернатива без угоди
- reservation point: межа прийнятності
- aspiration point: обґрунтована ціль
- ZOPA: можлива зона угоди
- objective criteria: зовнішні стандарти й порівняння
- issues: параметри, якими можна торгувати
- packages: кілька еквівалентних пропозицій
- concessions: умовні поступки з reciprocation

Числа, яких немає у джерелах, позначаються як hypotheses. Модель не повинна видавати припущення про BATNA іншої сторони як факт.

## Guardrails

1. Raw data залишається незмінним.
2. Трансформації зберігаються як code або SQL.
3. Кожне число у narrative має trace до finding та evidence.
4. Відсутні дані не заповнюються без явного правила imputation.
5. Візуалізація не обрізає вісь без обґрунтування.
6. Кореляція не описується як причинність.
7. Forecast завжди відділяється від historical data.
8. Sensitive personal data не копіюється в agent memory.
9. Red-team agent працює read-only.
10. PPTX generation починається тільки після audit pass.

## Invocation model

Skills, що змінюють або генерують багато артефактів, краще запускати вручну через `/skill-name` з `disable-model-invocation: true`. Reference skills можуть залишатися model-invoked.

Для важких досліджень доцільно використовувати:

```yaml
context: fork
agent: Explore
```

Data analysis не треба повністю переносити у fork, якщо головний контекст повинен бачити проміжні перевірки. Краще делегувати exploration, а фінальну валідацію залишити оркестратору.

## Reproducibility

Кожен engagement має фіксувати:

- timestamp
- Claude Code version
- git commit
- input file hashes
- package versions
- executed commands
- random seeds
- SQL queries
- chart specifications
- known limitations
