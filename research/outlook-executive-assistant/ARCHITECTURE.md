# Architecture

## Design goals

1. Morning brief має читати пошту без mutation permissions.
2. Receipt files не проходять через LLM context.
3. Weekly runs є idempotent і auditable.
4. Operational memory читається з точних files, а не з випадкового chat history.
5. Raw financial documents не потрапляють в Obsidian Markdown або vector index.
6. Кожен process має мінімальний tool і permission surface.

## Components

```text
Microsoft Entra ID
  |
  +--> public client registration
       delegated Mail.Read
       Device Code Flow
       pinned username
             |
             +---------------------------+
             |                           |
             v                           v
  Microsoft 365 MCP              Receipt collector
  local stdio                    deterministic script
             |                           |
             v                           v
         Hermes agent             private archive
             |                    SQLite + JSON manifest
             |                           |
             +-------------+-------------+
                           v
                  Obsidian operational vault
                           |
                           v
                    Telegram delivery
```

## Process isolation

### Mail reader process

Purpose: morning classification and user-requested search.

Allowed tools:

```text
list-mail-folders
list-mail-folder-messages
list-mail-messages
get-mail-message
```

Forbidden tools include attachments, send, reply, delete, move, categories and mailbox rules.

Runtime:

```text
transport: stdio
read-only: true
scope: Mail.Read
pagination: disabled
top cap: 30
parallel calls: false
```

### Receipt collector process

Purpose: weekly document capture.

It is a normal program, not an autonomous agent. It owns Graph calls, file validation, antivirus, deduplication and persistence. Its final stdout line follows [schemas/collector-output.schema.json](schemas/collector-output.schema.json).

Hermes sees counts and an approved manifest path. It never receives `contentBytes`.

### Report agent process

Purpose: transform an already validated manifest into a readable weekly note.

Allowed capabilities:

```text
read manifest JSON
read operational memory
write dated Markdown report
return Telegram summary
```

It does not call Outlook during weekly receipt reporting.

## Scheduled flow

### Monday 07:00

```text
Hermes cron
  -> run receipt-collector.py as pre-run script
  -> collector acquires lock
  -> calculate previous Monday through Sunday in Europe/Kyiv
  -> query messages
  -> evaluate rules
  -> collect and validate documents
  -> write SQLite transaction
  -> write immutable JSON manifest
  -> emit wakeAgent context
  -> Hermes reads manifest
  -> write receipts/YYYY-Www.md
  -> Telegram summary
```

If no state changed, collector returns `wakeAgent: false`. Hermes skips the model call.

### Weekdays 08:00

```text
Hermes cron
  -> load executive-mail-operations skill
  -> read brief.md, context.md, decisions.md, commitments/active.md
  -> list up to 30 messages from last 48 hours
  -> fetch full body only when needed
  -> classify and prioritize
  -> write briefs/YYYY-MM-DD.md
  -> Telegram summary
```

## Receipt search strategy

Do not depend on one keyword query. Use layered candidates:

1. Exact sender allowlist.
2. Sender domain plus receipt terms.
3. Confirmed merchant aliases.
4. Subject or body terms plus an acceptable attachment.
5. Unknown sender matches as `candidate_only`.

Recommended terms include `receipt`, `invoice`, `paid`, `payment`, `bill`, `чек`, `квитанція`, `оплата` and vendor-specific phrases.

Keyword presence does not prove payment. Classification rules are in [RECEIPT-COLLECTOR-CONTRACT.md](RECEIPT-COLLECTOR-CONTRACT.md).

## Archive layout

```text
/srv/hermes-receipts/
├── originals/YYYY/MM/
├── rendered/YYYY/MM/
├── quarantine/
├── manifests/
├── state/
│   ├── receipts.sqlite3
│   └── collector.lock
└── logs/
```

Recommended filename:

```text
YYYY-MM-DD__merchant__amount-currency__sha256-8.ext
```

All dynamic filename parts must be normalized. Do not trust subject, attachment name or merchant text as a path.

## State model

### `runs`

```text
run_id
range_start
range_end
timezone
started_at
finished_at
status
found_count
saved_count
duplicate_count
candidate_count
rejected_count
error_count
```

### `messages`

```text
internet_message_id unique
graph_message_id
received_at
sender_address
subject_hash
processed_at
```

Store a subject hash by default. Keep plaintext subject only when audit requirements justify it.

### `documents`

```text
document_id
message_id + attachment_id unique
sha256 unique
document_class
mime_type
size_bytes
archive_path
merchant
document_date
amount
currency
card_alias
card_last4
confidence
review_status
```

Never store full PAN, CVV, PIN, MFA code or access token.

## HTML-only receipts

Some vendors place the entire receipt in the email body. Collector should:

1. Fetch MIME message content through Graph `$value`.
2. Select the preferred HTML or text part.
3. Remove scripts, forms, iframes and active content.
4. Block all network requests.
5. Render a local PDF.
6. Save the original `.eml` and rendered PDF.
7. Record both hashes in the manifest.

Remote images must remain blocked. This prevents tracking pixels and makes rendering deterministic.

## Obsidian memory

Recommended runtime vault:

```text
/srv/hermes-memory/
├── Home.md
├── brief.md
├── context.md
├── decisions.md
├── rules/
│   ├── merchants.md
│   └── mail-priority.md
├── commitments/
│   └── active.md
├── briefs/
│   └── YYYY-MM-DD.md
├── receipts/
│   └── YYYY-Www.md
└── sessions/
```

Use exact files for operational state. Semantic search is useful for historical questions, but it should not decide today's priority from the entire vault on every run.

### Karpathy loop

```text
brief -> context -> run one workflow -> verify -> dated note -> decision write-back
```

`decisions.md` is append-only. A new merchant rule remains proposed until the user confirms it. The agent must not infer a permanent rule from one email.

## Sync model

For a public template, a dedicated `Hermes Memory` vault is safer than copying a person's full private vault to the VPS. Official Obsidian Headless Sync supports continuous Linux sync and end-to-end encryption, but the feature is open beta on the research date.

If the deployment cannot use Obsidian Sync, use another reviewed bidirectional sync method with conflict copies and backups. Do not place the same local path under two concurrent sync engines.

## Card reconciliation

Receipt collection and expense completeness are different problems.

```text
card transaction feed
      +
receipt manifest
      =
matched
missing receipt
unmatched receipt
refund
amount mismatch
currency mismatch
```

Phase one may collect email receipts only. Production bookkeeping should add transaction reconciliation before claiming full coverage.
