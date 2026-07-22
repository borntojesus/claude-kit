# Deployment runbook

## Assumptions

```text
OS: current Debian or Ubuntu LTS
service user: hermes
Node.js: 22 or newer
Hermes: current reviewed release
mailbox: Microsoft 365 work account
delivery: Telegram home channel or explicit topic
```

Node 22 satisfies both current packages. Microsoft 365 MCP requires Node 18 or newer. Obsidian Headless `0.0.13` requires Node 22 or newer.

## 1. Create the Entra application

1. Open Microsoft Entra admin center.
2. Create an app registration named `Hermes Outlook Read Assistant`.
3. Select accounts in the current organizational directory only.
4. Enable public client flow.
5. Add Microsoft Graph delegated permission `Mail.Read`.
6. Do not create a client secret for Device Code Flow.
7. Record Client ID and Tenant ID in a password manager.
8. If tenant policy blocks user consent, request admin consent for `Mail.Read` only.

Do not reuse a broad internal app registration. A dedicated app makes consent and revocation easier to audit.

## 2. Install the MCP package

Create a dedicated installation directory:

```bash
sudo install -d -o hermes -g hermes /opt/hermes-outlook-mcp
sudo -u hermes npm install \
  --prefix /opt/hermes-outlook-mcp \
  --omit=dev \
  --ignore-scripts \
  @softeria/ms-365-mcp-server@0.132.0
```

Snapshot integrity:

```text
sha512-3SiXgGumTrUQpGlXWkvUwar5ZBvcYVy2zaWVyYOS4l6Ou7pO02wSxrGAXKHlMc4F2Yg0AM2w6WELamEHhr/FjA==
```

Verify:

```bash
/opt/hermes-outlook-mcp/node_modules/.bin/ms-365-mcp-server --version
npm audit --prefix /opt/hermes-outlook-mcp --omit=dev
```

Do not use `npx -y` at runtime. It can fetch a new version during service start.

## 3. Create runtime directories

```bash
sudo -u hermes install -d -m 700 /home/hermes/.config/ms365-mcp-read
sudo -u hermes install -d -m 700 /home/hermes/.local/state/ms365-mcp-read/logs
sudo -u hermes install -d -m 700 /srv/hermes-receipts
sudo -u hermes install -d -m 700 /srv/hermes-memory
```

Create archive subdirectories from [ARCHITECTURE.md](ARCHITECTURE.md). Keep archive and database on a backed-up filesystem.

## 4. Verify permissions before login

```bash
export ENABLED_TOOLS='^(list-mail-messages|list-mail-folders|list-mail-folder-messages|get-mail-message)$'
export MS365_MCP_CLIENT_ID='<client-id>'
export MS365_MCP_TENANT_ID='<tenant-id>'

/opt/hermes-outlook-mcp/node_modules/.bin/ms-365-mcp-server \
  --read-only \
  --allowed-scopes 'Mail.Read' \
  --list-permissions
```

Expected values:

```json
{
  "readOnly": true,
  "permissions": ["Mail.Read"],
  "toolPermissions": ["Mail.Read"],
  "effectivePermissions": ["Mail.Read"],
  "allowedScopes": ["Mail.Read"],
  "disabledTools": [],
  "missingAllowedScopesForTools": [],
  "extraAllowedScopesNotUsedByTools": []
}
```

Stop if another scope appears.

Do not use `--preset mail` with a CLI `--enabled-tools` filter in version `0.132.0`. The preset overwrites the CLI pattern. This package uses environment `ENABLED_TOOLS` and no preset.

## 5. Complete Device Code login

Set the same environment used by Hermes runtime:

```bash
export MS365_MCP_EXPECTED_USERNAME='<mailbox-address>'
export MS365_MCP_AUTH_CACHE_COMMAND='/usr/local/bin/ms365-auth-cache-store'
export MS365_MCP_AUTH_CACHE_COMMAND_TIMEOUT_MS='10000'

/opt/hermes-outlook-mcp/node_modules/.bin/ms-365-mcp-server \
  --read-only \
  --allowed-scopes 'Mail.Read' \
  --expected-username '<mailbox-address>' \
  --login
```

Open the Microsoft URL on a trusted device, enter the code and inspect the consent screen. It must request read access without send or write permissions.

The cache wrapper is deployment-specific. It must implement the load, save and delete contract documented by the MCP package and use the organization's approved credential store. Do not replace it with a token embedded in YAML or shell arguments.

Verify:

```bash
/opt/hermes-outlook-mcp/node_modules/.bin/ms-365-mcp-server \
  --expected-username '<mailbox-address>' \
  --verify-login
```

## 6. Configure Hermes

Merge [config/hermes-outlook-readonly.example.yaml](config/hermes-outlook-readonly.example.yaml) into `~/.hermes/config.yaml`. Preserve unrelated settings.

Then run:

```bash
hermes mcp list
hermes mcp test microsoft365_mail_read
```

Reload an active session with:

```text
/reload-mcp
```

Exactly four Outlook tools should be visible. No attachment, send, reply, delete, move or mailbox rule tool should appear.

## 7. Install the skill

```bash
sudo -u hermes install -d -m 700 /home/hermes/.hermes/skills/executive-mail-operations
sudo -u hermes install -m 600 \
  skill/executive-mail-operations/SKILL.md \
  /home/hermes/.hermes/skills/executive-mail-operations/SKILL.md
```

Run the Hermes skill inspection or listing command available in the installed release and confirm the frontmatter parses.

## 8. Create Obsidian operational memory

Copy the contents of [templates/obsidian/](templates/obsidian/) to `/srv/hermes-memory`. Fill in `brief.md` and `context.md` manually before cron is enabled.

Do not store credentials or raw receipts in the vault.

### Official Headless Sync

Back up the local and remote vault first.

```bash
sudo npm install -g obsidian-headless@0.0.13
sudo -u hermes ob login
sudo -u hermes ob sync-setup \
  --vault 'Hermes Memory' \
  --path /srv/hermes-memory \
  --device-name 'hermes-server'
sudo -u hermes ob sync-config \
  --path /srv/hermes-memory \
  --mode bidirectional \
  --conflict-strategy conflict \
  --configs '' \
  --file-types ''
sudo -u hermes ob sync --path /srv/hermes-memory
```

After a successful round-trip test, run `ob sync --continuous` under a reviewed systemd user service. The Headless client is open beta on the research date. Monitor logs and keep an independent backup.

Do not run desktop Sync and Headless Sync on the same local path.

## 9. Configure the receipt collector

Copy [config/receipt-collector.example.yaml](config/receipt-collector.example.yaml) outside the repository:

```bash
sudo -u hermes install -m 600 \
  config/receipt-collector.example.yaml \
  /home/hermes/.config/receipt-collector.yaml
```

Replace placeholders. Start with:

```yaml
runtime:
  dry_run: true
```

The collector implementation must conform to [RECEIPT-COLLECTOR-CONTRACT.md](RECEIPT-COLLECTOR-CONTRACT.md) and both JSON schemas. Place the executable script under `~/.hermes/scripts/`, because Hermes cron restricts pre-run scripts to that directory.

## 10. Create cron jobs

### Weekly receipts

```bash
hermes cron create '0 7 * * 1' \
  'Validate the collector JSON, read only the approved manifest, write the weekly receipt report, and return a compact Telegram summary. Follow the executive-mail-operations skill.' \
  --script receipt-collector.py \
  --skill executive-mail-operations \
  --workdir /srv/hermes-memory \
  --deliver telegram \
  --name weekly-work-card-receipts
```

### Morning brief

```bash
hermes cron create '0 8 * * 1-5' \
  'Read the operational memory files, inspect Outlook for the last 48 hours, write today brief, and return a compact Telegram summary. Do not open attachments or modify the mailbox. Follow the executive-mail-operations skill.' \
  --skill executive-mail-operations \
  --workdir /srv/hermes-memory \
  --deliver telegram \
  --name outlook-morning-priorities
```

For the cron platform, enable only `file` and `microsoft365_mail_read`. Disable terminal, browser, code execution, delegation and write-capable mail processes.

## 11. Test manually

```bash
hermes cron run weekly-work-card-receipts
hermes cron run outlook-morning-priorities
hermes cron runs weekly-work-card-receipts --limit 5
hermes cron runs outlook-morning-priorities --limit 5
```

Do not enable the schedules until [TEST-PLAN.md](TEST-PLAN.md) passes on a test mailbox or isolated folder.

## 12. Operations

Daily checks:

```text
last cron status
authentication status
Obsidian sync status
collector error count
quarantine count
archive free space
```

Weekly checks:

```text
manifest exists
run time range is correct
duplicates are stable
candidates were reviewed
backup completed
no new MCP tools appeared
```

Before package update:

1. Install into staging directory.
2. Run fresh production audit.
3. Re-run permission report with production filters.
4. Compare tool schemas.
5. Run capability and injection fixtures.
6. Record new version and integrity.
7. Update production in a planned window.

## Rollback

1. Pause both cron jobs.
2. Set `enabled: false` for the MCP server.
3. Reload MCP or restart Hermes.
4. Disable the Entra enterprise application or revoke consent.
5. Stop collector and Obsidian sync services.
6. Preserve logs, manifest and database for review.
7. Remove runtime token cache only after processes stop.
