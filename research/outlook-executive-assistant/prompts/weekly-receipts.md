# Weekly receipt report prompt

```text
The receipt collector supplied JSON context. Validate run_id, status, counts and manifest path. The manifest path must be absolute, remain under /srv/hermes-receipts/manifests/ and end with .json.

Read the manifest, but never open raw receipt files. Create receipts/YYYY-Www.md with:
1. Time range and run status.
2. Counts for saved, duplicates, candidates, rejected and errors.
3. paid_receipt totals separated by currency.
4. Date, merchant, amount, currency, card alias, class and hash prefix.
5. Candidates needing human review.
6. Invoices without proof of payment.
7. Refunds and processing issues.

Do not write raw email body, full card number, OAuth data or attachment content. Do not call Outlook or modify collector state. Return a short Telegram summary.
```
