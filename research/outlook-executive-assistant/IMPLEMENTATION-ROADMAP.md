# Implementation roadmap

## Recommended collector stack

Use Node.js 22 for the first collector implementation. The server already needs Node 22 for Obsidian Headless, and `@azure/msal-node` matches the authentication stack used by the selected Microsoft 365 MCP.

Suggested dependencies:

```text
@azure/msal-node
undici
yaml
ajv
file-type
mailparser
sanitize-html
better-sqlite3 or node:sqlite when the deployed Node release supports it reliably
```

External programs:

```text
clamdscan
Chromium or Playwright for network-blocked HTML rendering
pdftotext or another reviewed PDF text extractor
OCRmyPDF or Tesseract for image-only documents
```

Do not add an LLM framework to the collector. Classification starts with deterministic rules. Optional model extraction can process redacted text later, behind a feature flag and a separate test gate.

Hermes cron runs `.sh` and `.bash` scripts with Bash. Use a small `receipt-collector.sh` wrapper that invokes the pinned Node entrypoint. Do not give the report agent terminal access.

## Unit 1: configuration and validation

Deliver:

```text
src/config.ts
src/paths.ts
test/config.test.ts
```

Requirements:

1. Parse YAML against a strict schema.
2. Reject unknown fields.
3. Reject relative or world-writable config paths.
4. Validate IANA timezone.
5. Validate archive containment.
6. Validate sender and domain rules.
7. Refuse full card numbers.

Verification:

```text
valid example loads
unknown field fails
unsafe path fails
invalid last4 fails
```

## Unit 2: authentication and account pinning

Deliver:

```text
src/auth.ts
src/token-store.ts
bin/collector-login.ts
test/auth.test.ts
```

Requirements:

1. Device Code Flow.
2. Delegated `Mail.Read` only.
3. Tenant and username pinning.
4. External credential-store adapter.
5. Fail closed when cache storage fails.
6. Separate login and runtime commands.

Verification:

```text
wrong username fails
scope expansion fails
missing cache backend fails
token never appears in logs
```

## Unit 3: bounded Graph reader

Deliver:

```text
src/graph.ts
src/message-search.ts
src/attachments.ts
test/graph.test.ts
```

Requirements:

1. Use fixed Graph host and version.
2. Calculate UTC range from local calendar week.
3. Fetch minimal message fields first.
4. Cap pages, messages and attachment sizes.
5. Honor `Retry-After` for 429.
6. Reject absolute or non-Graph attachment URLs.
7. Bind attachment ID to the current message.

Verification uses recorded fixtures or a mock Graph server. Tests must prove that caller-provided arbitrary paths cannot reach the request layer.

## Unit 4: file safety pipeline

Deliver:

```text
src/quarantine.ts
src/mime.ts
src/antivirus.ts
src/archive.ts
test/file-safety.test.ts
```

Requirements:

1. Exclusive file creation with mode `0600`.
2. Streaming hard size limit.
3. Byte-based MIME detection.
4. SHA-256.
5. ClamAV gate.
6. Filename normalization.
7. Atomic archive move.
8. Recovery path on database failure.

Use the EICAR test file only inside the isolated fixture directory. Never commit it as a raw executable fixture if repository security tooling blocks it. A generated-at-test-time string is safer.

## Unit 5: receipt parsing and classification

Deliver:

```text
src/extract/pdf.ts
src/extract/image.ts
src/extract/html.ts
src/classify.ts
test/classify.test.ts
```

Start with deterministic extraction:

```text
merchant aliases
ISO date patterns
amount and currency patterns
paid and unpaid markers
refund markers
last4 patterns with immediate redaction
```

Every extracted field carries confidence and source span internally. The manifest may omit raw spans to avoid leaking sensitive text.

HTML rendering runs with network disabled. Tests must fail if any request leaves the renderer.

## Unit 6: state and manifest

Deliver:

```text
src/db.ts
src/manifest.ts
schemas migrations
test/idempotency.test.ts
```

Requirements:

1. SQLite transaction per document.
2. Unique constraints for message, attachment and SHA-256 identities.
3. Immutable completed manifest.
4. Resume after interrupted run.
5. Separate human review decisions.
6. JSON output validated against both schemas in this package.

Run the same fixture week twice. The second run must add zero files and zero document rows.

## Unit 7: Hermes integration

Deliver:

```text
~/.hermes/scripts/receipt-collector.sh
~/.hermes/scripts/receipt-collector.mjs
cron definitions
```

The Bash wrapper sets a minimal environment and invokes Node by absolute path. It emits no token or raw document content.

The weekly report job receives only the final context object. The job's enabled toolsets are `file` only. The morning job receives `file` and `microsoft365_mail_read`.

## Unit 8: transaction reconciliation

Add only after email collection passes its rollout gates.

Deliver:

```text
src/reconcile.ts
schemas/card-transactions.schema.json
test/reconcile.test.ts
```

Requirements:

1. CSV import starts read-only.
2. Currency is never inferred.
3. Date tolerance is explicit.
4. Merchant normalization is versioned.
5. Missing receipts remain visible.
6. Human overrides are auditable.

## Release gates

### Alpha

```text
test mailbox
dry-run only
no file writes outside fixture path
```

### Beta

```text
staging archive
known senders
manual weekly execution
all receipt fixtures pass
```

### Production candidate

```text
scheduled read-only brief
scheduled weekly collection
backups verified
token revocation tested
Obsidian conflict test passed
```

### Production completeness

```text
card transaction reconciliation
accountant export accepted
four weeks of measured false-positive and false-negative rates
```

## Metrics

Track:

```text
known receipt recall
candidate precision
unpaid invoice false positives
duplicate rate
manual review count
collector error rate
morning P0/P1 recall
brief delivery latency
Obsidian conflict count
```

Do not report success from aggregate accuracy alone. Missing one legal deadline or payment-fraud message matters more than classifying several newsletters correctly.
