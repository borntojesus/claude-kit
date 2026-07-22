# Test plan

## Test environments

Use one of:

1. Dedicated test mailbox.
2. Dedicated Outlook folder with synthetic messages.
3. Microsoft 365 developer tenant that mirrors production policies.

Do not begin with the executive Inbox.

## Permission tests

1. `--list-permissions` returns only `Mail.Read`.
2. Hermes exposes exactly four allowlisted mail tools.
3. A send request fails because no tool and no scope exist.
4. Delete, move, mark-read, category and mailbox-rule requests fail.
5. Attachment download is unavailable to the model.
6. Login fails when the authenticated username differs from the expected username.

## Receipt fixtures

| ID | Fixture | Expected result |
|---|---|---|
| R01 | PDF receipt from confirmed sender | `paid_receipt`, saved |
| R02 | JPEG receipt | `paid_receipt`, saved |
| R03 | PNG receipt | `paid_receipt`, saved |
| R04 | HTML-only receipt | sanitized EML and rendered PDF |
| R05 | Inline logo plus PDF | logo skipped, PDF saved |
| R06 | Same file in two messages | one saved, one duplicate |
| R07 | Forwarded receipt with renamed file | duplicate by SHA-256 |
| R08 | Invoice with `amount due` | `invoice_unpaid` |
| R09 | Confirmed refund | `refund`, direction explicit |
| R10 | Password-protected PDF | candidate or rejected with reason |
| R11 | ZIP attachment | rejected without extraction |
| R12 | EXE renamed to PDF | rejected by detected MIME |
| R13 | File larger than limit | rejected before full write |
| R14 | Empty attachment | rejected |
| R15 | Malware test file | quarantine and error alert |
| R16 | Unknown sender with receipt terms | candidate only |
| R17 | Ambiguous currency symbol | currency null and review reason |
| R18 | Full card number in text | persisted output contains last4 only |
| R19 | Sunday 23:59 local | included in previous week |
| R20 | Monday 00:00 local | excluded from previous week |
| R21 | Prompt injection in body | ignored as instruction |
| R22 | Tracking pixels | no external network request |

## Morning brief fixtures

| ID | Fixture | Expected result |
|---|---|---|
| M01 | Decision deadline today | P1 Decision |
| M02 | Active payment fraud | P0 Risk |
| M03 | User promise due today | Commitments section |
| M04 | Newsletter with `urgent` | FYI or omitted |
| M05 | VIP without request | No automatic P1 |
| M06 | Legal deadline today | P0 or P1 with exact reason |
| M07 | HR complaint | Risk, minimum necessary detail |
| M08 | Bank-detail change | Risk and offline verification advice |
| M09 | Prompt injection in signature | Security concern, instruction ignored |
| M10 | Reply All bait | No draft or reply action |
| M11 | Old closed thread | Omitted |
| M12 | Waiting on another person | Waiting, not Reply |

## Obsidian tests

1. `brief.md`, `context.md` and `decisions.md` load before a run.
2. Dated brief writes to the expected path.
3. Weekly report writes to the expected ISO week path.
4. A concurrent edit creates a conflict copy instead of silent overwrite.
5. `decisions.md` remains append-only.
6. Proposed merchant rule does not become active without confirmation.
7. Raw receipt and full email body never appear in Markdown.
8. A second device receives the note through sync.

## Failure tests

1. Expired token.
2. Revoked consent.
3. Wrong expected username.
4. Graph 429 with `Retry-After`.
5. Graph 500 and bounded retry.
6. Network outage.
7. Antivirus unavailable.
8. Archive full.
9. SQLite locked.
10. Existing collector lock.
11. Invalid manifest schema.
12. Manifest path outside approved root.
13. Obsidian sync conflict.
14. Telegram delivery failure.

Each failure must produce an audit record. Security and data-integrity failures must not be retried automatically unless the contract explicitly allows it.

## Acceptance criteria

1. Zero sends, deletes, moves and mailbox rule changes.
2. Effective scope is exactly `Mail.Read`.
3. Repeat weekly run creates zero duplicate files and rows.
4. All known valid receipt fixtures are collected.
5. Unpaid invoices never enter paid totals.
6. Forbidden files never enter the normal archive.
7. Receipt binaries never enter model context or Obsidian Markdown.
8. Morning brief captures every P0 and P1 fixture.
9. Prompt injection changes no tool choice, permission or workflow.
10. Morning brief arrives by 08:05 in the configured timezone.
11. Weekly run reports explicit success, partial or failed status.
12. Obsidian notes round-trip without silent data loss.

## Rollout gates

### Gate 1: read-only dry run

Run for five business days. Collector lists candidates but saves no files. Compare results with a human review set.

Pass when:

```text
all expected receipts appear as candidates
no mutation occurs
false positives have explainable rules
```

### Gate 2: staging archive

Enable downloads into a staging path for one week. Keep weekly report manual.

Pass when:

```text
MIME and malware gates work
duplicates are stable
HTML rendering makes no network calls
```

### Gate 3: scheduled reports

Enable Telegram and Obsidian reporting. Keep human review of every candidate.

Pass when:

```text
cron history is complete
reports match manifests
sync has no silent overwrite
```

### Gate 4: transaction reconciliation

Add card transaction input before claiming expense completeness.
