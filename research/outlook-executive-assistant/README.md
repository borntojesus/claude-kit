# Outlook executive assistant for Hermes

Дата перевірки: 22 липня 2026 року.

Ця папка описує приватного поштового асистента для Hermes на Linux VPS. Він працює без n8n, читає Outlook через Microsoft Graph, щодня готує короткий бриф, раз на тиждень збирає чеки робочих карток і зберігає операційну пам'ять в Obsidian.

Пакет є implementation-ready design, а не заявою про готовий production deployment. Receipt collector має окремий контракт, schema і тест-план. Його код треба реалізувати та перевірити на тестовій скриньці перед доступом до реальної пошти.

## Рекомендація

Система має три ізольовані контури:

```text
Outlook
  |
  +--> read-only MCP --> Hermes --> morning brief --> Telegram
  |
  +--> receipt collector --> private archive + SQLite manifest
                              |
                              +--> weekly report --> Telegram

Obsidian Headless Sync <--> Hermes operational memory
```

Morning brief використовує локальний stdio MCP з чотирма read-only mail tools. Collector працює як детермінований pre-run script. LLM не отримує binary attachments і не має Outlook send, delete, move або rule tools.

## Два робочі процеси

### Morning brief

У робочі дні о 08:00 Hermes:

1. Читає точні operational memory files.
2. Перевіряє до 30 листів за останні 48 годин.
3. Повністю читає тільки можливі Decision, Reply, Risk або листи з дедлайном сьогодні.
4. Показує рішення, відповіді, ризики, обіцянки та максимум три корисні FYI.
5. Записує повний brief у dated Obsidian note.
6. Надсилає коротку версію в Telegram.

### Weekly receipts

Щопонеділка о 07:00 collector:

1. Обробляє попередній календарний тиждень у `Europe/Kyiv`.
2. Шукає known senders, merchant domains і receipt keywords.
3. Приймає PDF, JPG, PNG та HTML-only receipts.
4. Перевіряє MIME, розмір, SHA-256 і ClamAV.
5. Відрізняє paid receipt, unpaid invoice, refund, statement і candidate.
6. Зберігає original file у private archive.
7. Записує idempotent manifest у SQLite та JSON.
8. Передає Hermes тільки counts і manifest path.

Email-only collection не доводить повноту обліку. Для цього receipt manifest треба звіряти з card transaction CSV або bank API. Такий reconciliation layer описаний у [RECEIPT-COLLECTOR-CONTRACT.md](RECEIPT-COLLECTOR-CONTRACT.md).

## Permission model

Read-only workflows використовують окрему single-tenant Entra public client application:

```text
Delegated scope: Mail.Read
OAuth flow: Device Code Flow
Expected account: pinned by username
```

Не додавайте `Mail.ReadWrite`, `Mail.Send`, shared mailbox scopes або Files scopes. Якщо потрібні drafts, створіть іншу Entra application і окремий MCP process. Не розширюйте read-only process.

## Що є в папці

| Файл | Призначення |
|---|---|
| [LANDSCAPE.md](LANDSCAPE.md) | Порівняння готових рішень і rationale |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Компоненти, data flow, state і Obsidian memory |
| [SECURITY.md](SECURITY.md) | Threat model, prompt injection, permissions і privacy |
| [RECEIPT-COLLECTOR-CONTRACT.md](RECEIPT-COLLECTOR-CONTRACT.md) | Детермінований контракт collector |
| [IMPLEMENTATION-ROADMAP.md](IMPLEMENTATION-ROADMAP.md) | Мінімальні кодові units і release gates |
| [RUNBOOK.md](RUNBOOK.md) | Entra, MCP, Obsidian, cron, audit, rollback |
| [TEST-PLAN.md](TEST-PLAN.md) | Fixtures, acceptance criteria і rollout gates |
| [VALIDATION.md](VALIDATION.md) | Виконані перевірки й чесні межі готовності |
| [SOURCES.md](SOURCES.md) | Первинні джерела і version snapshot |
| [config/](config/) | Sanitized YAML examples |
| [schemas/](schemas/) | JSON Schema для manifest і pre-run output |
| [skill/](skill/) | Hermes skill із trust boundary |
| [prompts/](prompts/) | Morning та weekly prompts |
| [templates/obsidian/](templates/obsidian/) | Operational vault skeleton |

## Quick start

1. Прочитайте [SECURITY.md](SECURITY.md).
2. Створіть test mailbox або test folder.
3. Зареєструйте single-tenant Entra public client із delegated `Mail.Read`.
4. Встановіть pinned Microsoft 365 MCP package.
5. Об'єднайте [config/hermes-outlook-readonly.example.yaml](config/hermes-outlook-readonly.example.yaml) з Hermes config.
6. Перевірте `effectivePermissions` через `--list-permissions`.
7. Скопіюйте skill у `~/.hermes/skills/executive-mail-operations/`.
8. Створіть operational Obsidian vault із [templates/obsidian/](templates/obsidian/).
9. Реалізуйте collector за його контрактом і почніть із `dry_run: true`.
10. Пройдіть [TEST-PLAN.md](TEST-PLAN.md) до ввімкнення cron.

## Межа готовності

Готовими є architecture, permissions, MCP configuration, prompt policy, schemas, Obsidian structure, cron design і test plan.

Не готовими без deployment context є OAuth login, token cache wrapper, receipt collector implementation, merchant rules, card aliases, Telegram target і accountant export. Ці частини залежать від конкретного tenant та business process.
