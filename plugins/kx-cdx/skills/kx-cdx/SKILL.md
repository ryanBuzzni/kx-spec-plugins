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

- Verify the plugin skill set matches `plugins/kx`.
- Sync KX custom agents from this plugin into `~/.codex/agents/`.
- Keep Codex-side instructions aligned with the Claude plugin without editing the Claude source.

## Working rules

- Reuse existing project patterns before introducing new ones.
- Prefer targeted verification over broad test runs.
- Keep plugin-specific instructions here, and leave repo-specific rules to project files.
