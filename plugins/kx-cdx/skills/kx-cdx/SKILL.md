---
name: kx-cdx
description: Bootstrap KX workflows in Codex. Use when the task should follow the KX Codex plugin conventions.
---

# KX Codex Bootstrap

Use this skill as the entry point for KX workflows in Codex.

## Current scope

- Confirm the user goal and restate the intended outcome succinctly.
- Inspect the relevant codebase or documents before proposing changes.
- Favor Codex-native features such as skills, subagents, and repo-local plugin configuration.
- Keep changes scoped and verifiable.

## Next build-out targets

- Port KX planning workflow into Codex-native skills.
- Port KX development agents into `.codex/agents/*.toml` or plugin-bundled workflows.
- Add shared references and optional MCP/app integrations once the base workflow is stable.

## Working rules

- Reuse existing project patterns before introducing new ones.
- Prefer targeted verification over broad test runs.
- Keep plugin-specific instructions here, and leave repo-specific rules to project files.
