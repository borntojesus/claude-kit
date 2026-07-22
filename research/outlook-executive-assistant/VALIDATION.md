# Validation record

Date: 22 July 2026

## Source snapshots

```text
Hermes commit:
3e953ed815ffb1e35277a77eb3e764d39dcf36f7

Softeria Microsoft 365 MCP commit:
bd8ef4999e2e4eef4b0616d3836e5e0df21f5094

Published MCP package:
@softeria/ms-365-mcp-server@0.132.0
```

## Effective permission check

Command:

```bash
ENABLED_TOOLS='^(list-mail-messages|list-mail-folders|list-mail-folder-messages|get-mail-message)$' \
  ms-365-mcp-server \
  --read-only \
  --allowed-scopes Mail.Read \
  --list-permissions
```

Observed result:

```json
{
  "mode": "personal",
  "readOnly": true,
  "filter": "^(list-mail-messages|list-mail-folders|list-mail-folder-messages|get-mail-message)$",
  "permissions": ["Mail.Read"],
  "toolPermissions": ["Mail.Read"],
  "effectivePermissions": ["Mail.Read"],
  "allowedScopes": ["Mail.Read"],
  "disabledTools": [],
  "missingAllowedScopesForTools": [],
  "extraAllowedScopesNotUsedByTools": []
}
```

## Production dependency audit

Test method:

1. Create an empty temporary directory.
2. Install `@softeria/ms-365-mcp-server@0.132.0` with `--omit=dev --ignore-scripts`.
3. Run `npm audit --omit=dev --json`.

Observed result:

```text
production dependencies: 155
optional dependencies: 50
moderate advisories: 1
high advisories: 0
critical advisories: 0
```

The advisory is `GHSA-frvp-7c67-39w9` in the transitive `@hono/node-server` dependency. It concerns Windows static serving. The proposed runtime uses Linux stdio.

## Package checks

Passed:

```text
both YAML examples parsed
both JSON files parsed
both JSON Schemas compiled with AJV draft 2020-12 and ajv-formats
all local Markdown links resolved
git diff whitespace check
scan for private email, domain, IP and key material
scan for dash punctuation and curly quotes in new public prose
read-only config scan for Mail.ReadWrite, Mail.Send and attachment tools
```

## Humanizer review

The public docs were checked for promotional wording, inflated claims, repetitive negative parallelism, fake significance, em dash punctuation, decorative emphasis and chatbot filler. Technical lists were kept where they define complete contracts or tests.

## Not validated

The following items require a real deployment and are not claimed as complete:

```text
Entra registration and consent
OAuth token-cache wrapper
live mailbox behavior
receipt collector implementation
ClamAV and HTML renderer integration
Telegram delivery
Obsidian round-trip sync
accountant export
card transaction reconciliation
```

Use [TEST-PLAN.md](TEST-PLAN.md) before production.
