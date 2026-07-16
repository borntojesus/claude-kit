# claude-kit

Набір скілів, агентів і команд для [Claude Code](https://claude.com/claude-code).
Це те, чим я користуюсь щодня. Тут 64 скіли, 103 агенти та 1 команда.

## Установка

Найпростіший шлях. Відкрий Claude Code і виконай:

```
/plugin marketplace add borntojesus/claude-kit
/plugin install claude-kit@claude-kit
```

Готово. Скіли, агенти й команди підхопляться автоматично.

### Альтернатива: скрипт

Якщо хочеш просто покласти файли собі в `~/.claude`:

```sh
git clone https://github.com/borntojesus/claude-kit.git
cd claude-kit
./install.sh
```

Скрипт копіює вміст у `~/.claude/skills`, `~/.claude/agents` і `~/.claude/commands`.
Наявні файли з такими ж іменами він не чіпає, а показує список пропущених.

## Що всередині

### Скіли (64)

**SEO та GEO (~45).** Повний цикл: аудит сайту, технічне SEO, дослідження
ключових слів, аналіз SERP, схема-розмітка, локальне SEO, беклінки, контент.
Плюс окремий блок GEO, тобто оптимізація під AI-пошук (AI Overviews, ChatGPT,
Perplexity).

**Розробка.** `payload`, `cms-migration`, `vercel-react-best-practices`,
`vercel-composition-patterns`, `web-design-guidelines`, `icon-library`,
`sidebar-nav-shell`, `claude-context-picker`.

**Робочі процеси.** `karpathy-method` (спец-перший підхід до роботи з кодом),
`inbox-process` (розбір інбоксу second-brain сховища), `obsidian`, `cowork`
(генерує промпт для браузерного агента), `logo-finder`, `site-screenshot`,
`humanizer` (прибирає ознаки AI-письма), `maya-design` (UX-аудит).

### Агенти (103)

Інженерія (архітектори, ревʼюери, SRE, безпека), дизайн і UX, маркетинг і
соцмережі, платна реклама, продажі, продукт, фінанси, тестування, юридичні.

### Команди (1)

`/analis-load` показує, що навантажує твій Mac: локальні сервери, dev-сервери,
сесії Claude, з розбивкою по памʼяті та CPU.

## Що сюди свідомо не увійшло

**Скіли, вбудовані в Claude Code** (`docx`, `pdf`, `pptx`, `xlsx`,
`frontend-design`, `skill-creator`, `canvas-design`, `mcp-builder` та інші).
Вони пропрієтарні і вже стоять у тебе разом із Claude Code. Копіювати їх сюди
не можна і не треба.

**GSD** (69 скілів + 34 агенти для планування фаз проєкту). Це окремий проєкт зі
своїм інсталятором і автооновленням. Копія тут швидко б протухла і зламала вам
`/gsd-update`. Ставте з оригіналу: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core).

**Мої homelab-скіли та клієнтські агенти.** Прошиті під приватну інфраструктуру
і дані клієнтів, тому лишаються поза публічним доступом.

## Ліцензії та авторство

Тут зібрані як мої власні напрацювання, так і скіли інших авторів під
дозвільними ліцензіями. Оригінальні файли LICENSE збережені в кожній теці.
Повний перелік джерел: [NOTICE.md](NOTICE.md).

Моя частина (`karpathy-method`, `cowork`, `icon-library`, `sidebar-nav-shell`,
`claude-context-picker`, `logo-finder`, `inbox-process`, `maya-design`,
агенти й команди) поширюється під [MIT](LICENSE).

Якщо ви автор чогось із цього набору і хочете інших умов, напишіть в issues,
приберу або поправлю атрибуцію.
