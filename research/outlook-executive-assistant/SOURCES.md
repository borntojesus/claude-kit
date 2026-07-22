# Sources and version snapshot

Перевірено 22 липня 2026 року. Технічні твердження спираються на офіційну документацію та первинні repositories.

## Hermes

- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>
- Verified repository commit: `3e953ed815ffb1e35277a77eb3e764d39dcf36f7`
- MCP documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/>
- MCP config reference: <https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference/>
- Cron documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/>
- Skills documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/>
- Hermes email gateway: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/email/>

## Microsoft 365 MCP

- Softeria repository: <https://github.com/Softeria/ms-365-mcp-server>
- Verified repository commit: `bd8ef4999e2e4eef4b0616d3836e5e0df21f5094`
- npm package: <https://www.npmjs.com/package/@softeria/ms-365-mcp-server>
- Verified package version: `0.132.0`
- Package publish timestamp: `2026-07-21T16:19:28.996Z`
- Node requirement: `>=18`
- License: MIT
- npm integrity: `sha512-3SiXgGumTrUQpGlXWkvUwar5ZBvcYVy2zaWVyYOS4l6Ou7pO02wSxrGAXKHlMc4F2Yg0AM2w6WELamEHhr/FjA==`
- Audit advisory: <https://github.com/advisories/GHSA-frvp-7c67-39w9>

Fresh production install audit command:

```bash
npm install --omit=dev --ignore-scripts @softeria/ms-365-mcp-server@0.132.0
npm audit --omit=dev
```

Snapshot result: one moderate transitive advisory, zero high and zero critical advisories.

## Microsoft Graph and Entra

- Outlook Mail API overview: <https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview?view=graph-rest-1.0>
- Graph permissions reference: <https://learn.microsoft.com/en-us/graph/permissions-reference>
- Get message: <https://learn.microsoft.com/en-us/graph/api/message-get?view=graph-rest-1.0>
- List attachments: <https://learn.microsoft.com/en-us/graph/api/message-list-attachments?view=graph-rest-1.0>
- Get attachment and raw `$value`: <https://learn.microsoft.com/en-us/graph/api/attachment-get?view=graph-rest-1.0>
- Message search query parameter: <https://learn.microsoft.com/en-us/graph/search-query-parameter>
- Search Outlook messages: <https://learn.microsoft.com/en-us/graph/search-concept-messages>
- Message delta query: <https://learn.microsoft.com/en-us/graph/delta-query-messages>
- Outlook change notifications: <https://learn.microsoft.com/en-us/graph/outlook-change-notifications-overview>
- Device Authorization Grant: <https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code>
- Conditional Access authentication flows: <https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-authentication-flows>
- Exchange Online Basic Auth deprecation: <https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/deprecation-of-basic-authentication-exchange-online>
- Revoke user access: <https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access>

## Official Microsoft MCP direction

- Microsoft Agent 365 overview: <https://learn.microsoft.com/en-us/microsoft-agent-365/use>
- Work IQ Mail MCP reference: <https://learn.microsoft.com/en-us/connectors/a365outlookmailmcp/>

The official Mail MCP is part of Agent 365 Frontier Preview on the research date. Recheck status before a new deployment.

## Prompt injection

- Microsoft Defender prompt injection protection for email: <https://learn.microsoft.com/en-us/defender-office-365/step-by-step-guides/prompt-injection-protection-defender-for-office-365>
- OWASP LLM01 Prompt Injection: <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>

## Obsidian

- Obsidian Sync: <https://obsidian.md/sync>
- Headless Sync: <https://obsidian.md/help/sync/headless>
- Obsidian Headless: <https://obsidian.md/help/headless>
- Verified npm package: `obsidian-headless@0.0.13`
- Package publish timestamp: `2026-07-11T15:09:46.917Z`
- Node requirement: `>=22.0.0`

Obsidian Headless is open beta on the research date. The npm metadata reports `UNLICENSED`. This repository does not copy its code.

## Alternatives

- Dext email forwarding: <https://help.dext.com/en/articles/416678-set-up-email-forwarding-rules-to-dext>
- Dext Extract by email: <https://help.dext.com/en/articles/416754-how-to-submit-documents-to-dext-with-extract-by-email>
- Microsoft Power Automate Outlook actions: <https://learn.microsoft.com/en-us/power-automate/desktop-flows/actions-reference/office365outlook>

## Snapshot warning

Versions, advisories and preview status can change. Before installation, repeat npm metadata, audit, permission and license checks. Do not treat this dated snapshot as an automatic update approval.
