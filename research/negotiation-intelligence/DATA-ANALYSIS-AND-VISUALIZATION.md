# Data analysis and visualization workflow

## Принцип

Мета аналізу полягає не у створенні максимальної кількості графіків. Мета полягає у зменшенні невизначеності перед конкретним рішенням.

Кожен analysis brief починається з п'яти питань:

1. Яке рішення треба прийняти?
2. Які твердження можуть змінити це рішення?
3. Які метрики представляють ці твердження?
4. Які дані можуть їх підтвердити або спростувати?
5. Який рівень невизначеності прийнятний?

## Pipeline

### 1. Intake

Зібрати:

- файли та джерела
- data owners
- період спостереження
- одиниці вимірювання
- business definitions
- очікувану гранулярність
- privacy constraints

### 2. Data dictionary

Для кожного поля зафіксувати:

- назву
- тип
- значення
- одиницю
- джерело
- owner
- допустимі nulls
- transformation history

### 3. Quality checks

Мінімальний набір:

- schema drift
- duplicates
- missingness
- invalid categories
- impossible values
- date gaps
- timezone consistency
- denominator mismatch
- currency mismatch
- join cardinality
- survivorship bias
- sample coverage

`fg-data-profiling` може прискорити перший прохід, але його alerts не замінюють business validation.

### 4. Analysis

Порядок:

1. Baseline.
2. Distribution.
3. Segmentation.
4. Time trend.
5. Cohort comparison.
6. Sensitivity analysis.
7. Statistical uncertainty.
8. Alternative explanations.
9. Decision implication.

Не починати з machine learning, якщо питання вирішується descriptive statistics або SQL aggregation.

### 5. Findings

Finding повинен містити:

- одне перевірюване твердження
- effect size
- baseline або comparator
- метод
- evidence
- confidence
- limitations
- business implication

P-value без effect size і business relevance не є достатнім finding.

## Рекомендований стек

### DuckDB

Основний query engine для локальних CSV, JSON і Parquet. Переваги для Claude Code:

- простий file-based workflow
- SQL легко перевіряти у diff
- немає окремого database server
- зручні window functions і aggregations
- результат можна відтворити однією командою

### Polars або pandas

Polars доцільний для великих наборів і lazy execution. Pandas доцільний, якщо ecosystem compatibility важливіша за швидкість. Skill не повинен автоматично переписувати весь аналіз з pandas на Polars.

### SciPy і statsmodels

Використовувати для:

- confidence intervals
- hypothesis tests
- regression diagnostics
- time-series models
- power analysis

Модель повинна пояснювати assumptions тесту та перевіряти, чи вони виконуються.

### Vega-Lite і Altair

Vega-Lite JSON є рекомендованим канонічним форматом графіка. Altair створює цей spec з Python. Переваги:

- declarative representation
- machine-readable encodings
- повторне рендерення
- простіший автоматичний audit
- SVG output для презентації

Plotly можна використовувати для exploratory hover і interactive reports. Фінальний статичний артефакт усе одно повинен мати export у SVG або PNG.

## Матриця вибору графіка

| Аналітичне питання | Перший вибір | Не використовувати без причини |
|---|---|---|
| Порівняння категорій | Sorted bar або dot plot | Pie chart з багатьма категоріями |
| Зміна в часі | Line chart | Stacked area для точних порівнянь |
| До та після | Slope chart | Два окремих pie charts |
| Відхилення від плану | Diverging bar або bullet chart | Gauge chart |
| Розподіл | Histogram, box plot або strip plot | Лише average bar |
| Зв'язок змінних | Scatter plot | Dual-axis chart |
| Retention | Cohort heatmap | Загальна середня retention line |
| Funnel | Stage bars із абсолютами і rates | Декоративна funnel shape |
| Scenario sensitivity | Tornado або range plot | Один point forecast |
| Part-to-whole | Stacked bar | 3D pie chart |
| Ranking change | Slope або bump chart | Незв'язані таблиці |
| Geographic pattern | Choropleth лише для rates | Raw counts by area |

Матриця базується на семантичному підході Financial Times Visual Vocabulary: спочатку визначається relationship у даних, потім chart form.

## Перевірка візуалізації

Кожен графік перевіряється за чеклістом:

### Truth

- Чи правильний denominator?
- Чи показана невизначеність?
- Чи не прихована важлива частина distribution?
- Чи коректна агрегація?
- Чи не змінює truncated axis сприйняття effect?
- Чи має annotation trace до finding?

### Audience

- Чи зрозуміє аудиторія одиниці?
- Чи потрібне пряме підписування?
- Чи видно decision threshold?
- Чи відповідає рівень деталізації ролі учасника?

### Accessibility

- Не покладатися лише на колір.
- Використовувати colorblind-safe palette.
- Мати достатній contrast.
- Додавати alt text і текстовий висновок.
- Зберігати читабельність у grayscale.

### Reproducibility

- Source path існує.
- Query або transformation збережено.
- Spec проходить schema validation.
- Export відповідає spec.
- Chart ID пов'язаний із finding ID.

## Графіки для керівників

Для переговорів графік повинен відповідати на три питання:

1. Що сталося?
2. Чому це важливо для цієї аудиторії?
3. Яке рішення або trade-off випливає?

Приклад title:

```text
Weak: Monthly activation rate
Strong: Activation fell 11 percentage points after the onboarding change
```

Strong title допустимий лише тоді, коли finding пройшов evidence audit.

## Розділення аналізу та переконання

Один і той самий dataset може підтримувати різні переговорні позиції. Тому система зберігає окремо:

- observations
- statistical findings
- interpretation
- negotiation use
- disclosure risk

Це дозволяє перевірити, чи presentation narrative не перебільшує силу доказів.
