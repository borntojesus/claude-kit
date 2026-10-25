# Claude to Codex audit, 2026-10-25

Prepared from the active local configuration. No secrets, auth stores, transcripts or permission allowlists are included.

## Skills

| Claude source | Codex target | Result |
| --- | --- | --- |
| alpina-recruiter | alpina-recruiter | adapted-copy |
| claude-context-picker | codex-context-picker | adapted-copy |
| consilium | consilium | adapted-copy |
| cowork | cowork | adapted-copy |
| denon-avr | denon-avr | adapted-copy |
| design-system | design-system | adapted-copy |
| design-variants | design-variants | adapted-copy |
| docx | docx | adapted-copy |
| frontend-design | frontend-design | adapted-copy |
| global-todo | global-todo | adapted-copy |
| homelab-build | homelab-build | adapted-copy |
| homelab-deploy | homelab-deploy | adapted-copy |
| homelab-service-restore | homelab-service-restore | adapted-copy |
| homelab-services | homelab-services | adapted-copy |
| homelab-status | homelab-status | adapted-copy |
| humanizer | humanizer | adapted-copy |
| icon-library | icon-library | adapted-copy |
| inbox-process | inbox-process | adapted-copy |
| karpathy-method | karpathy-method | adapted-copy |
| learn | learn | adapted-copy |
| market-research | market-research | adapted-copy |
| maya-design | maya-design | adapted-copy |
| mcp-builder | mcp-builder | adapted-copy |
| nas-card-offload | nas-card-offload | adapted-copy |
| nas-torrent-download | nas-torrent-download | adapted-copy |
| obsidian | obsidian | adapted-copy |
| org-audit | org-audit | adapted-copy; recovered old link |
| org-hiring-plan | org-hiring-plan | adapted-copy; recovered old link |
| org-jd | org-jd | adapted-copy; recovered old link |
| org-merge | org-merge | adapted-copy; recovered old link |
| org-reorg | org-reorg | adapted-copy; recovered old link |
| pdf | pdf | adapted-copy |
| pptx | pptx | adapted-copy |
| project-new | project-new | adapted-copy |
| session-order | session-order | adapted-copy |
| ship | ship | adapted-copy |
| sidebar-nav-shell | sidebar-nav-shell | adapted-copy |
| skill-creator | native skill-creator | use-native-codex-skill-creator |
| talk-prep | talk-prep | adapted-copy |
| torrentX | torrentx | adapted-copy |
| web-design-guidelines | web-design-guidelines | adapted-copy |
| xlsx | xlsx | adapted-copy |

41 source skills adapted, 4 commands converted and 2 native maintenance skills added: 47 installed skill entries. Native Codex skill-creator and existing GSD remain available. Shared duplicate skill entries are disabled only in the Codex configuration; their original files are untouched.

## Agents

15 active Claude personas adapted with inherited Codex models. Existing persona files with invalid ~/.Codex paths are redirected to the actual shared ~/.claude documents. Existing registered persona names are preserved.

## MCP

| Server | Result |
| --- | --- |
| 1password | preserved-existing |
| hermes | preserved-existing |
| homelab | preserved-existing |
| telegram-intel | imported |
| analytics | imported |
| telegram-readonly | imported |
| mail | imported |
| monobank | imported |
| context7 | imported-plugin-equivalent; optional existing CONTEXT7_API_KEY environment |

The homelab definition differs between the two applications. The existing Codex command wins; this migration does not touch either runtime. New local executables were checked for existence, HTTP services were not contacted.

## Settings

| Claude setting | Codex disposition |
| --- | --- |
| env | not copied; shared integrations use existing environment/1Password |
| attribution | global rules prohibit AI attribution |
| permissions | preserve Codex sandbox and approvals; no blanket allow import |
| model | preserve current Codex model |
| hooks | 8 adapted handlers; native trust review required; notification/status/audio and Claude transcript writer excluded |
| statusLine | Claude-specific; preserve existing Codex behavior |
| enabledPlugins | audit only; preserve Codex plugin state |
| extraKnownMarketplaces | Claude-specific; preserve existing Codex behavior |
| effortLevel | preserve current Codex effort |
| modelSettings | Claude-specific; preserve existing Codex behavior |
| skipWorkflowUsageWarning | Claude-specific; preserve existing Codex behavior |
| theme | preserve Codex app appearance; generated UI remains light per global rules |
| agentPushNotifEnabled | Claude-specific; preserve existing Codex behavior |
| skipAutoPermissionPrompt | Claude-specific; preserve existing Codex behavior |
| autoMode | preserve Codex native approval policy |
| cleanupPeriodDays | Claude-specific; preserve existing Codex behavior |

## Plugins

| Plugin | Claude enabled | Codex cache | Skill count |
| --- | --- | --- | --- |
| vercel@claude-plugins-official | False | True | 33 |
| figma@claude-plugins-official | False | True | 14 |
| superpowers@claude-plugins-official | True | True | 14 |
| ponytail@ponytail | False | False | 6 |
| homelab-ops@skills-library | True | True | 4 |
| alpina-team@alpina-plugins | False | True | 2 |
| frontend-design@claude-plugins-official | True | True | 1 |
| security-guidance@claude-plugins-official | True | False | 0 |
| typescript-lsp@claude-plugins-official | True | False | 0 |
| claude-md-management@claude-plugins-official | True | False | 1 |
| session-report@claude-plugins-official | True | False | 1 |
| context7@claude-plugins-official | True | False | 0 |
| cloudflare@claude-plugins-official | False | False | 13 |
| claude-blog@agricidaniel-blog | False | False | 32 |

Existing native frontend-design, superpowers and homelab-ops plugins are preserved. CLAUDE.md maintenance and session-report receive Codex-specific skills; Context7 receives an anonymous MCP entry; its optional API key is not required. Existing code-review/security capabilities remain. Claude TypeScript LSP, status line, notification sounds, retention and model-specific controls are not represented as working Codex features. Disabled Claude plugins are inventoried, not enabled.

## Verification

Seven behavioral and integrity tests pass. All 47 skill YAML frontmatters parse with Ruby YAML. All staged TOML and JSON parse. Codex Doctor loads the staged configuration; its auth failure is expected because authentication was deliberately not copied into the test home, and network checks were restricted. Full MCP connectivity and hook trust remain runtime checks.

## Limits

- New hooks need /hooks trust review; trust hashes are deliberately untouched.
- Stop records bounded, filtered final messages in ~/.codex/journals; this is outcome recall, not full transcript summarization.
- Existing model, effort, app appearance, approval policy and plugin enabled state are preserved.
- Existing MCP definitions win on conflicts, including the different homelab server command.
- Claude LSP/status-line/auto-mode and plugin-private services require native equivalents; no fake parity claimed.
- MCP runtime connectivity and OAuth must be verified in a fresh Codex session.

## Official references

- [Codex skills](https://developers.openai.com/codex/skills)
- [Lifecycle hooks and native trust review](https://learn.chatgpt.com/docs/hooks)
- [Codex configuration](https://developers.openai.com/codex/config-reference)

Related fleet spec: [[codex-claude-parity-2026-10-25]].

## Installed verification

Installed 277 files with backups at `~/.codex/backups/claude-parity-20261025-232022-806089/`. SHA-256 verification matched every installed file. Reapplying the exact stage returned `changed: 0`.

Codex Doctor on the actual installation confirmed configuration, authentication, app-server initialization, healthy databases and provider connectivity. Its nonzero exit comes from `TERM=dumb` in the tool terminal; it initially reported the missing optional Context7 environment variable, which was subsequently removed in favor of documented anonymous access, and an available CLI update. This task does not update the CLI. MCP service connectivity and new-hook trust have not been certified.

The Context7 follow-up changed only config.toml, with another backup at `~/.codex/backups/claude-parity-20261025-232914-616313/`. The source plugin README confirms that anonymous access is supported without an API key.
