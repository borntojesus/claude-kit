# Codex adaptation of the local Claude setup

The source remains the active `~/.claude` installation. This tool stages adapted user skills, command equivalents, agents, global guidance, lifecycle hook adapters and compatible missing MCP definitions. See [AUDIT.md](AUDIT.md) for the full per-item disposition.

```sh
python3 codex/sync.py --stage /private/tmp/codex-claude-parity
python3 codex/test_migration.py
python3 codex/sync.py --stage /private/tmp/codex-claude-parity --apply
```

Run from this repository. The stage contains a private copy of existing configuration and stays outside Git. Applying requires filesystem permission to write `~/.codex`. Every changed file is backed up first under `~/.codex/backups/claude-parity-<timestamp>/`, with a ledger identifying newly added files. Repeating the same installation makes no changes. Restage to pick up source edits; stale config merges are rejected.

No authentication, literal secrets, Claude permissions, model selection, plugin enablement or hook trust hashes are imported. Review newly added hooks through `/hooks` in Codex before they can run. Restart Codex or open a new chat to refresh the discovered setup. Existing Claude and shared `~/.agents` skill files are preserved. Native Codex skill-creator is retained.

The adapters deliberately reuse the maintained source hooks in `~/.claude/hooks`. Keep that installation available. Stop records bounded, filtered final messages in `~/.codex/journals`, with no additional model calls. Recall reads those outcomes plus the existing canonical Claude journal. This is not a full transcript archive or an assurance that arbitrary sensitive prose can be automatically detected.

To undo, inspect the backup ledger, restore previously existing files from that backup and remove only the listed newly created paths after reviewing them. Do not replace the entire Codex directory or restore authentication from unrelated backups.
