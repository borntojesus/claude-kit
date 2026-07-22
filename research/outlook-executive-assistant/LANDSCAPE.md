# Landscape and product choices

## Short answer

Для self-hosted Hermes найкращий стартовий варіант зараз:

```text
Hermes
  -> local stdio @softeria/ms-365-mcp-server
  -> delegated Microsoft Graph OAuth
  -> signed-in user's Outlook mailbox
```

Це не означає, що community MCP варто використовувати для завантаження receipt files. Він добре підходить для read-only mail triage. Binary receipt collection краще винести у вузький deterministic worker.

## Варіанти

| Варіант | Сильна сторона | Обмеження | Рішення |
|---|---|---|---|
| Microsoft Work IQ Mail MCP | Офіційний Outlook MCP та Microsoft governance | Agent 365 Frontier Preview, tenant setup, admin dependency | Стежити, але не робити основою загального VPS runbook |
| Softeria Microsoft 365 MCP | Активний package, headless OAuth, exact filters, permission report, audit log | Community code, широкий tool catalog, token має реальний mailbox access | Використовувати для read-only brief із pinned version і exact allowlist |
| `ryaker/outlook-mcp` | Mail, folders, rules і calendar | Client secret, token file, ширший write surface, немає package release discipline | Не брати для executive mailbox |
| Hermes email gateway | Простий IMAP та SMTP path | Документація згадує Outlook app password, а Exchange Online Basic Auth вимкнено | Не використовувати для основної Microsoft 365 пошти |
| Custom Graph MCP | Найвужчий policy surface | Треба підтримувати власний код | Доречно для controlled sending або вузьких attachment operations |
| Deterministic Graph worker | Idempotency, file gates, predictable output | Потрібна невелика реалізація | Рекомендований для receipt collection |
| Microsoft Power Automate | Native Microsoft 365 connectors | Додаткова платформа, classification і memory треба проєктувати окремо | Добре для простого save-to-SharePoint workflow |
| Dext | Email ingestion, extraction, duplicates, accounting export | Paid third-party SaaS отримує фінансові документи | Найшвидший шлях, якщо бухгалтер уже використовує Dext |

## Чому не IMAP та SMTP

Microsoft вимкнула Basic Authentication в Exchange Online. Блокування Basic Auth також блокує app passwords. IMAP і SMTP можуть працювати через OAuth 2.0, але Microsoft Graph дає зрозуміліший permission model для message search, metadata, attachments і drafts.

Вбудований Hermes email gateway залишається корисним для окремої технічної скриньки, якщо provider підтримує сучасну auth model. Для executive Outlook mailbox цей пакет рекомендує Graph.

## Microsoft Work IQ Mail MCP

Офіційний Outlook Mail MCP входить до Microsoft Agent 365. На дату перевірки він належить до Frontier Preview. Це сильний enterprise напрямок, але не універсальна інструкція для приватного Hermes на VPS. Tenant має бути допущений до preview, а адміністратор повинен виконати Microsoft setup.

Коли Work IQ стане generally available, рішення треба переглянути. Офіційний MCP може зменшити supply-chain risk community package, але permission і prompt-injection boundaries все одно залишаться потрібними.

## Softeria Microsoft 365 MCP

Перевірена версія:

```text
package: @softeria/ms-365-mcp-server
version: 0.132.0
published: 2026-07-21
node: >=18
license: MIT
repository commit: bd8ef4999e2e4eef4b0616d3836e5e0df21f5094
```

Корисні controls:

1. Device Code Flow для headless Linux.
2. `--expected-username` для account pinning.
3. `--read-only` для write-tool filtering.
4. `--allowed-scopes` для scope boundary.
5. Exact tool regex через `ENABLED_TOOLS`.
6. Token cache paths і зовнішній auth-cache command.
7. Audit log.
8. Pagination і item caps.

### Preset filtering gotcha

У `0.132.0` `--preset` перезаписує CLI `--enabled-tools` під час argument parsing. Environment `ENABLED_TOOLS` застосовується після preset і знову перезаписує pattern.

Безпечний config у цій папці взагалі не використовує preset. MCP-side regex і Hermes-side `tools.include` містять однаковий exact allowlist.

### Production dependency audit

Fresh install із `npm install --omit=dev --ignore-scripts` та `npm audit --omit=dev` 22 липня 2026 року показав одну moderate transitive advisory у `@hono/node-server`. Advisory описує Windows path traversal у static serving. Рекомендований deployment працює через Linux stdio, не HTTP static serving.

Це не причина автоматично відмовлятися від package. Це причина pin version, запускати audit перед update і не відкривати MCP HTTP endpoint без потреби.

## Чому universal attachment tool не підходить

Softeria має `download-bytes`, який приймає відносний Graph path. Для mail attachment path виглядає так:

```text
/me/messages/{message-id}/attachments/{attachment-id}/$value
```

Tool зручний, але широкий. Model може побудувати інший path у межах дозволів token. Крім того, binary content повертається як base64 у model context. Для receipt workflow це зайвий exposure.

Вузький collector повинен сам перевіряти, що message ID походить із поточного run, attachment ID належить цьому message, MIME дозволений, файл не inline, size не перевищує limit, а hash ще не оброблявся.

## SaaS path

Якщо основна мета полягає у передачі документів бухгалтеру, Dext може бути простішим за custom collector. Кожний account отримує unique email-in address. Outlook rule пересилає supplier receipts, Dext витягує дані й дозволяє export.

Цей шлях погано підходить, якщо вимога полягає у self-hosting або забороняє передачу фінансових документів сторонньому SaaS.

## Рішення за контекстом

| Контекст | Вибір |
|---|---|
| Private executive assistant на VPS | Softeria read-only MCP плюс deterministic collector |
| Accountant already uses Dext | Outlook forwarding rule до Dext, Hermes контролює пропуски |
| Усе має залишатися у Microsoft 365 | Power Automate плюс SharePoint або OneDrive |
| Потрібне automatic sending | Окремий custom policy proxy, не universal community MCP |
| Потрібен тільки morning brief | Read-only MCP без attachment tools |
