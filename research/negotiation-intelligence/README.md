# Negotiation intelligence for Claude Code

Дата дослідження: 22 липня 2026 року.

Ця папка описує систему підготовки до переговорів, управлінських презентацій і складних зустрічей у Claude Code. Фокус системи: аналіз аудиторії, переговорна стратегія, перевірка даних, статистичний аналіз, вибір візуалізації, побудова аргументації та репетиція запитань. Візуальний дизайн слайдів свідомо не входить у ядро.

## Рекомендація

Один універсальний presentation agent змішує забагато різних задач. Надійніший підхід має три рівні:

1. Skills задають повторювані процедури, формати результатів і правила перевірки.
2. Subagents виконують незалежне дослідження, аналізують позиції сторін і критикують висновки в окремому контексті.
3. Deterministic scripts рахують метрики, виконують статистичні тести та будують графіки, щоб модель не обчислювала значення вільним текстом.

Фінальний PPTX має бути downstream артефактом. Він отримує вже перевірені `findings.json`, `evidence-ledger.csv`, `charts/`, `narrative.md` і `qa.md`. Генератор презентації не повинен самостійно вигадувати аналіз або джерела.

## Що вже є в claude-kit

Корисні агенти, які можна перевикористати:

| Агент | Поточна сильна сторона | Роль у новому workflow |
|---|---|---|
| `sales-deal-strategist` | MEDDPICC, win planning, competitive positioning | Комерційні переговори та карта впливу |
| `sales-discovery-coach` | SPIN, Gap Selling, Pain Funnel | Підготовка запитань і виявлення інтересів |
| `sales-proposal-strategist` | Win themes і proposal narrative | Аргументація пропозиції |
| `sales-account-strategist` | Stakeholder mapping і multi-threading | Карта учасників та коаліцій |
| `finance-financial-analyst` | Сценарії, sensitivity analysis, unit economics | Кількісна модель рішення |
| `support-analytics-reporter` | Переклад даних у бізнес-висновки | Аналітичний звіт |
| `support-executive-summary-generator` | Стислі управлінські висновки | Decision memo та executive narrative |
| `specialized-model-qa` | Перевірка моделей і припущень | Аудит статистичних висновків |
| `testing-reality-checker` | Незалежна критика готовності | Red-team перевірка |
| `design-visual-storyteller` | Візуальна розповідь | Лише після затвердження змісту |

Поточні skills `market-research`, `competitor-analysis`, `product-manager` і `humanizer` корисні як допоміжні. Вони не закривають повний переговорний та аналітичний цикл.

## Що треба додати

Рекомендований мінімальний набір нових skills:

| Skill | Результат |
|---|---|
| `meeting-brief` | Ціль рішення, контекст, обмеження, відомі факти та прогалини |
| `audience-intelligence` | Stakeholder map, мотиви, ризики, критерії рішення, доказові потреби |
| `negotiation-prep` | BATNA, reservation point, aspiration point, ZOPA, issue matrix, concessions |
| `evidence-ledger` | Реєстр тверджень, джерел, рівня впевненості та обмежень |
| `data-analysis-workflow` | Data dictionary, quality report, аналіз, findings і reproducibility log |
| `chart-selection` | Семантичний вибір графіка та machine-readable chart specification |
| `decision-narrative` | SCQA, Pyramid Principle, Claim-Evidence-Implication і decision ask |
| `presentation-audit` | Фактична, логічна, аудиторна та переговорна перевірка |
| `qa-rehearsal` | Питання, короткі відповіді, глибокі відповіді та межі розкриття |

Рекомендовані нові subagents:

| Subagent | Навіщо потрібний окремий контекст |
|---|---|
| `audience-researcher` | Незалежно реконструює інтереси й політичну карту аудиторії |
| `data-analyst` | Працює з даними та повертає тільки відтворювані результати |
| `visualization-critic` | Перевіряє, чи відповідає графік питанню та чи не вводить в оману |
| `counterparty-simulator` | Симулює позицію іншої сторони, її BATNA та заперечення |
| `evidence-red-team` | Шукає слабкі джерела, стрибки логіки та альтернативні пояснення |

## Робочий процес

```text
Source documents and data
  -> meeting brief
  -> audience map
  -> negotiation map
  -> data quality and analysis
  -> evidence ledger
  -> verified findings
  -> chart specifications
  -> decision narrative
  -> red-team review
  -> Q&A rehearsal
  -> presentation outline
  -> optional PPTX generation
```

## Артефакти

Кожен запуск має створювати окрему папку:

```text
work/<engagement-id>/
├── 00-brief.md
├── 01-audience-map.csv
├── 02-negotiation-map.md
├── 03-data-dictionary.csv
├── 04-data-quality.json
├── 05-analysis/
├── 06-findings.json
├── 07-evidence-ledger.csv
├── 08-charts/
├── 09-narrative.md
├── 10-red-team.md
├── 11-qa.md
└── 12-sources.md
```

Ця структура відділяє факти від інтерпретацій і дозволяє повторно побудувати графіки після зміни даних.

## Рекомендоване рішення

Першу версію варто реалізувати прямо в `claude-kit` як skills і agents. Окремий runtime framework не потрібний. Claude Code вже підтримує project skills, plugin skills, subagents, `context: fork`, persistent agent memory, hooks і deterministic scripts.

Початковий обсяг:

1. `audience-intelligence`
2. `negotiation-prep`
3. `data-analysis-workflow`
4. `chart-selection`
5. `evidence-red-team`

Ці п'ять компонентів закриють найбільші прогалини, не дублюючи наявні sales agents і вбудовані document skills.

## Документи дослідження

- [LANDSCAPE.md](LANDSCAPE.md): оцінка репозиторіїв і правила запозичення.
- [ARCHITECTURE.md](ARCHITECTURE.md): структура Claude Code plugin та контракти між компонентами.
- [DATA-ANALYSIS-AND-VISUALIZATION.md](DATA-ANALYSIS-AND-VISUALIZATION.md): аналітичний і візуалізаційний pipeline.
- [IMPLEMENTATION-ROADMAP.md](IMPLEMENTATION-ROADMAP.md): план реалізації та evals.
- [SOURCES.md](SOURCES.md): первинні джерела та дата перевірки.
