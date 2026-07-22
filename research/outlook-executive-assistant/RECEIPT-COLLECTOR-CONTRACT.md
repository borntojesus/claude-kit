# Receipt collector contract

## Purpose

`receipt-collector.py` is a deterministic scheduled worker. It searches a bounded Outlook time range, saves approved receipt documents, writes an idempotent manifest and emits a small JSON context for Hermes.

It is not an agent. It does not accept natural-language instructions from email, use browser automation, send mail or modify mailbox state.

## Inputs

1. Sanitized YAML config.
2. OAuth token for one expected account.
3. Explicit run range or `previous_calendar_week` mode.
4. Confirmed sender, merchant and card alias rules.
5. Private archive root.

CLI contract:

```text
receipt-collector.py
  --config <absolute-yaml-path>
  [--run-id YYYY-Www]
  [--dry-run]
  [--json]
```

The script must reject relative config paths and config files writable by group or other users.

## Time range

Default weekly behavior:

```text
timezone: Europe/Kyiv
run time: Monday 07:00
range start: previous Monday 00:00:00 inclusive
range end: current Monday 00:00:00 exclusive
```

Convert boundaries to UTC once and use those exact values for Graph queries and manifest metadata. A retry uses the same boundaries.

## Candidate discovery

Fetch minimal message properties first:

```text
id
internetMessageId
receivedDateTime
sender
subject
bodyPreview
hasAttachments
```

Candidate rules are additive:

1. Exact sender allowlist.
2. Sender domain allowlist with receipt term.
3. Confirmed merchant rule.
4. Subject or body keyword plus attachment.
5. HTML-only receipt markers.

Unknown senders remain `candidate`. Do not automatically promote a new sender to the allowlist.

## Attachment eligibility

Accept only:

```text
application/pdf
image/jpeg
image/png
```

Reject or quarantine metadata for:

```text
inline attachment
reference attachment
archive
executable
script
macro-enabled Office file
unknown MIME
size above limit
empty file
malware detection
password-protected document when text extraction is required
```

Do not trust extension or declared `contentType` alone. Detect type from bytes.

## Document classification

### `paid_receipt`

Requires at least one strong paid signal:

```text
receipt
paid
payment successful
transaction completed
authorization code
card last4
merchant rule that explicitly emits paid receipts
```

### `invoice_unpaid`

Use when document requests payment and lacks a paid signal. Common markers:

```text
amount due
payment required
due date
bank details for payment
до сплати
```

### `refund`

Use for confirmed returned funds. Store amount with explicit direction. Do not silently subtract it from a receipt with a different currency.

### `statement`

Use for card or supplier statements. A statement is evidence for reconciliation, not a replacement for every receipt.

### `candidate`

Use when evidence is incomplete, sender is unknown, amount is ambiguous or the file needs human review.

### `rejected`

Use for security, type, size or parsing failures. Preserve metadata and safe error reason. Do not place unscanned binary in the normal archive.

## Extraction

Fields:

```text
merchant
document_date
amount
currency
card_alias
card_last4
document_number
tax_amount optional
classification
confidence
review_reasons
```

Never infer currency from server locale. If the symbol is ambiguous and no country or ISO code resolves it, set currency to null and create a review reason.

Never store full card number. A detector may use it transiently to redact input, but only last4 and confirmed alias may persist.

## File handling

1. Create quarantine file with `O_CREAT | O_EXCL` and mode `0600`.
2. Stream bytes with a hard size limit.
3. Close and fsync the file.
4. Detect MIME and compute SHA-256.
5. Scan with configured antivirus command.
6. Normalize final filename.
7. Move atomically within the same filesystem.
8. Commit database row only after final path exists.

If database commit fails, leave the file in a recovery area and emit an error. Do not report it as saved.

## Deduplication

Use three keys:

```text
internetMessageId
graphMessageId + attachmentId
sha256
```

SHA-256 is the final document identity. The same receipt forwarded under another filename must be a duplicate.

Idempotency rules:

1. Repeating a completed run does not create files or rows.
2. A failed run can resume unfinished items.
3. A manifest is immutable after status becomes `success` or `partial`.
4. Human review changes create a separate decision record.

## HTML-only receipts

When no eligible attachment exists but the message matches a confirmed HTML receipt rule:

1. Fetch message MIME.
2. Save original `.eml` to quarantine.
3. Parse MIME without remote requests.
4. Sanitize HTML.
5. Render PDF with network disabled.
6. Scan and hash both original and rendered files.
7. Set `source_kind` to `html_email`.

## Manifest

Each run writes:

```text
/srv/hermes-receipts/manifests/<run-id>.json
```

The document follows [schemas/receipt-manifest.schema.json](schemas/receipt-manifest.schema.json).

Manifest paths must be absolute, normalized and contained under configured archive roots. Store no attachment bytes.

## Stdout for Hermes

The final stdout line follows [schemas/collector-output.schema.json](schemas/collector-output.schema.json).

Example:

```json
{
  "wakeAgent": true,
  "context": {
    "run_id": "2026-W30",
    "status": "success",
    "saved": 8,
    "duplicates": 2,
    "candidates": 1,
    "rejected": 0,
    "errors": 0,
    "manifest": "/srv/hermes-receipts/manifests/2026-W30.json"
  }
}
```

Use `wakeAgent: false` only when the run succeeded and there is no new reportable state. Errors must wake the agent or exit nonzero so cron delivers a failure.

## Locking and retries

Use a process lock under the state directory. A second run exits with a distinct already-running status.

Retry transient HTTP 429 and 5xx responses with bounded exponential backoff and Graph `Retry-After`. Do not retry authentication, permission, invalid path, malware or schema errors automatically.

## Reconciliation extension

Optional transaction input schema:

```text
transaction_id
posted_date
merchant_raw
amount
currency
card_alias
card_last4
```

Match in stages:

1. Exact amount, currency, card alias and close date.
2. Confirmed merchant alias with date tolerance.
3. Refund direction.
4. Human review.

Output statuses:

```text
matched
missing_receipt
unmatched_receipt
amount_mismatch
currency_mismatch
refund
```

Do not claim receipt completeness until every relevant card transaction has one of these statuses.
