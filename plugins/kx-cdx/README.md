# KX Codex Plugin

KX spec-driven workflow plugin for Codex.

## Contents

- `skills/`: KX workflow skills aligned with `plugins/kx/skills`
- `agents-src/`: Codex custom agent source files
- `references/`: shared review and workflow references
- `scripts/sync_agents.py`: installs the custom agents into `~/.codex`

## Install

Codex에 바로 시키려면 이렇게 요청해도 된다:

```text
kx-cdx 플러그인 설치해줘. marketplace 설정하고, agent sync까지 하고, 끝나면 설치 결과 보고해줘.
```

### 1. Clone or update the source repo

```bash
cd ~/buzzni/projects
git clone https://github.com/ryanBuzzni/kx-spec-plugins.git
cd kx-spec-plugins
```

If the repo already exists:

```bash
cd ~/buzzni/projects/kx-spec-plugins
git pull origin main
```

### 2. Link the plugin into the local Codex plugin directory

```bash
mkdir -p ~/plugins
ln -sfn ~/buzzni/projects/kx-spec-plugins/plugins/kx-cdx ~/plugins/kx-cdx
```

### 3. Register the local marketplace

Create or update `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "kx-codex-marketplace",
  "interface": {
    "displayName": "KX Codex Plugins"
  },
  "plugins": [
    {
      "name": "kx-cdx",
      "source": {
        "source": "local",
        "path": "./plugins/kx-cdx"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Development"
    }
  ]
}
```

### 4. Enable the plugin in Codex config

Add this block to `~/.codex/config.toml` if it is not already present:

```toml
[plugins."kx-cdx@kx-codex-marketplace"]
enabled = true
```

### 5. Sync the custom agents

```bash
python3 ~/plugins/kx-cdx/scripts/sync_agents.py
```

This copies the KX agent definitions into `~/.codex/agents/` and updates `~/.codex/config.toml`.

### 6. Restart Codex

Restart Codex so refreshed plugin skills and agent registrations are loaded.

## Update

When the plugin changes:

```bash
cd ~/buzzni/projects/kx-spec-plugins
git pull origin main
python3 ~/plugins/kx-cdx/scripts/sync_agents.py
```

Then restart Codex.

Codex에 바로 시키려면:

```text
kx-cdx 최신으로 반영해줘. git pull 하고, sync_agents.py 실행하고, 바뀐 내용까지 보고해줘.
```

## Verify

Check that these are present:

- `~/plugins/kx-cdx`
- `~/.codex/agents/planner.toml`
- `~/.codex/agents/backend-dev.toml`
- `~/.codex/agents/frontend-web-dev.toml`
- `~/.codex/agents/frontend-app-dev.toml`
- `~/.codex/agents/debugger.toml`
- `~/.codex/agents/code-reviewer.toml`
- `~/.codex/agents/back-tester.toml`
- `~/.codex/agents/web-tester.toml`
- `~/.codex/agents/app-tester.toml`

Codex에 확인을 맡기려면:

```text
kx-cdx 설치 상태 확인해줘. plugin, marketplace, agents 등록 상태를 점검하고 결과를 보고해줘.
```

## Notes

- This plugin is the Codex counterpart to `plugins/kx`.
- Do not edit `plugins/kx` or `.claude-plugin` when updating Codex-only behavior.
