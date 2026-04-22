# KX Codex Plugin

KX spec-driven workflow plugin for Codex.

## Contents

- `skills/`: KX workflow skills aligned with `plugins/kx/skills`
- `agents-src/`: Codex custom agent source files
- `references/`: shared review and workflow references
- `scripts/sync_agents.py`: installs the custom agents into `~/.codex`

## Install

1. Install or enable the `kx-cdx` plugin through the local marketplace.
2. Sync the custom agents:

```bash
python3 ~/plugins/kx-cdx/scripts/sync_agents.py
```

3. Restart Codex so refreshed plugin skills and agent registrations are loaded.

## Notes

- This plugin is the Codex counterpart to `plugins/kx`.
- Do not edit `plugins/kx` or `.claude-plugin` when updating Codex-only behavior.
