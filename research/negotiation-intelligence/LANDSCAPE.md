# Repository and skill landscape

## Метод оцінювання

Репозиторії оцінювалися за шістьма критеріями:

1. Сумісність із Claude Code або відкритим Agent Skills standard.
2. Якість процедур, а не краса фінального документа.
3. Відтворюваність аналізу.
4. Наявність scripts, templates, references та eval patterns.
5. Активність і відсутність archive status станом на 22 липня 2026 року.
6. Ліцензія та можливість безпечного запозичення.

Кількість stars не використовувалась як показник якості. Вона враховувалась лише як сигнал поширеності.

## Tier A: базові джерела

### anthropics/skills

URL: <https://github.com/anthropics/skills>

Використати для:

- формату `SKILL.md`
- progressive disclosure
- структури `scripts/`, `references/`, `assets/` і `examples/`
- `skill-creator` та eval workflow
- вбудованих document skills як архітектурного прикладу

Не копіювати document skills без перевірки їхніх окремих ліцензій. Репозиторій прямо вказує, що частина document skills є source-available, а не open source.

### anthropics/financial-services

URL: <https://github.com/anthropics/financial-services>

Використати як приклад business workflow, де upstream data переходить у downstream deliverables. Особливо корисні:

- `competitive-analysis`
- `dd-meeting-prep`
- `client-review`
- `unit-economics`
- `portfolio-monitoring`
- `clean-data-xls`
- `audit-xls`
- `ib-check-deck`

Репозиторій має Apache-2.0. Перед перенесенням конкретного skill треба зберегти атрибуцію і перевірити локальний LICENSE у його папці.

### anthropics/claude-cookbooks

URL: <https://github.com/anthropics/claude-cookbooks>

Використати для:

- композиції кількох skills
- data analysis і financial reporting examples
- cross-format workflow
- container reuse і progressive disclosure

Ліцензія MIT. Це референс, а не готовий переговорний plugin.

### K-Dense-AI/scientific-agent-skills

URL: <https://github.com/K-Dense-AI/scientific-agent-skills>

Вибірково використати:

- `exploratory-data-analysis`
- `statistical-analysis`
- `scientific-critical-thinking`
- `scientific-visualization`
- `literature-review`
- `peer-review`
- `market-research-reports`

Не встановлювати весь набір у ядро `claude-kit`. Велика кількість вузьких наукових skills збільшує шум discovery і не потрібна для бізнесових переговорів. Ліцензія MIT, репозиторій активно оновлювався напередодні дослідження.

## Tier B: data and visualization engines

| Репозиторій | Роль | Ліцензія | Рекомендація |
|---|---|---|---|
| [duckdb/duckdb](https://github.com/duckdb/duckdb) | Локальний OLAP для CSV, JSON і Parquet | MIT | Основний query engine |
| [pola-rs/polars](https://github.com/pola-rs/polars) | Швидкі DataFrame transformations | MIT | Для великих табличних наборів |
| [Data-Centric-AI-Community/fg-data-profiling](https://github.com/Data-Centric-AI-Community/fg-data-profiling) | Автоматичне EDA і data quality profiling | MIT | Опційний перший прохід |
| [vega/vega-lite](https://github.com/vega/vega-lite) | Декларативна граматика візуалізацій | BSD-3-Clause | Канонічний chart spec |
| [vega/altair](https://github.com/vega/altair) | Python API для Vega-Lite | BSD-3-Clause | Основний Python renderer |
| [observablehq/plot](https://github.com/observablehq/plot) | Exploratory visualization у JavaScript | ISC | Для interactive exploration |
| [plotly/plotly.py](https://github.com/plotly/plotly.py) | Інтерактивні Python charts | MIT | Для hover і сценарних графіків |
| [evidence-dev/evidence](https://github.com/evidence-dev/evidence) | SQL і Markdown reports as code | MIT | Для live decision reports |
| [Financial-Times/chart-doctor](https://github.com/Financial-Times/chart-doctor) | Visual Vocabulary і chart selection | MIT | Методика вибору графіка |

Рекомендований стандарт обміну між аналізом і рендерингом: Vega-Lite JSON. Він declarative, diff-friendly і достатньо структурований для автоматичної перевірки осей, шкал, агрегування й джерел.

## Tier C: приклади, які треба читати критично

### anthropics/claude-quickstarts

URL: <https://github.com/anthropics/claude-quickstarts>

`financial-data-analyst` показує інтерактивний аналіз фінансових даних. Корисний як UI та tool-use референс. Для локального Claude Code plugin він важчий, ніж потрібно.

### markdown-viewer/skills

URL: <https://github.com/markdown-viewer/skills>

Корисний для Mermaid і Vega-Lite previews у Markdown. Перед копіюванням треба окремо перевірити ліцензію кожного компонента та стабільність renderer setup.

## Що не рекомендується брати як основу

### Універсальні slide generators

Причина відмови:

- змішують дослідження, аргументацію і layout
- часто не мають evidence contract
- можуть генерувати графіки без data lineage
- оцінюють результат за зовнішнім виглядом, а не за якістю рішення

PPTX skill доречний лише після завершення research workflow.

### Важкі multi-agent frameworks

OpenAI Agents SDK, LangGraph, AutoGen і CrewAI є сильними runtime frameworks, але для першої версії вони створять зайву інфраструктуру. Claude Code вже має skills, subagents, agent teams, hooks, memory і plugin packaging.

Окремий framework стане виправданим, якщо з'являться:

- зовнішній API або scheduled service
- довготривалий state machine поза Claude Code session
- централізований tracing багатьох користувачів
- queue, retries і service-level guarantees

## Gap analysis для claude-kit

| Capability | Поточне покриття | Прогалина |
|---|---|---|
| Sales qualification | Сильне | Надто прив'язане до B2B sales |
| Discovery questions | Сильне | Немає універсальної audience evidence map |
| Negotiation strategy | Часткове | Немає BATNA, ZOPA, concession і package workflow |
| Stakeholder analysis | Часткове | Немає стандартного output schema |
| Data profiling | Відсутнє | Потрібний deterministic workflow |
| Statistical analysis | Часткове в agents | Немає reusable skill і test protocol |
| Chart selection | Слабке | Немає semantic chart decision tree |
| Visualization generation | Загальне | Немає Vega-Lite contract і validation |
| Evidence management | Відсутнє | Потрібний claim-source-confidence ledger |
| Presentation audit | Часткове | Потрібна factual і audience-fit перевірка |
| Q&A simulation | Часткове | Немає disclosure boundaries і answer tiers |

## Ліцензійна політика запозичення

Для кожного перенесеного компонента:

1. Перевірити LICENSE у конкретній папці.
2. Зберегти copyright notice.
3. Додати джерело до кореневого `NOTICE.md`.
4. Зафіксувати commit SHA upstream.
5. Не копіювати source-available компоненти як MIT.
6. Власні адаптації позначити окремо від upstream тексту.
