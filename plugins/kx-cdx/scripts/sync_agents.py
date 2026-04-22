from __future__ import annotations

import shutil
from pathlib import Path


AGENTS = {
    "planner": "Interactive planning agent for KX workflows.",
    "backend-dev": "Backend development agent for APIs, services, and data models.",
    "frontend-web-dev": "Web frontend development agent for React and Next.js applications.",
    "frontend-app-dev": "Mobile app development agent for React Native applications.",
    "debugger": "Debugging agent for root cause analysis and verified fixes.",
    "code-reviewer": "Code review agent focused on correctness, security, performance, and quality.",
    "back-tester": "Backend testing agent for API, service, and integration tests.",
    "web-tester": "Web E2E testing agent for Playwright-based validation.",
    "app-tester": "Mobile UI testing agent for Maestro-based app validation.",
}

MARKER_START = "# BEGIN KX-CDX AGENTS"
MARKER_END = "# END KX-CDX AGENTS"


def build_config_block() -> str:
    lines = [MARKER_START]
    for name, description in AGENTS.items():
        lines.append(f'[agents.{name}]')
        lines.append(f'description = "{description}"')
        lines.append(f'config_file = "agents/{name}.toml"')
        lines.append("")
    lines.append(MARKER_END)
    return "\n".join(lines)


def sync_agent_files(plugin_root: Path, codex_home: Path) -> None:
    source_dir = plugin_root / "agents-src"
    target_dir = codex_home / "agents"
    target_dir.mkdir(parents=True, exist_ok=True)

    for path in source_dir.glob("*.toml"):
        shutil.copy2(path, target_dir / path.name)


def sync_config(codex_home: Path) -> None:
    config_path = codex_home / "config.toml"
    original = config_path.read_text() if config_path.exists() else ""
    block = build_config_block()

    if MARKER_START in original and MARKER_END in original:
        start = original.index(MARKER_START)
        end = original.index(MARKER_END) + len(MARKER_END)
        updated = original[:start].rstrip() + "\n\n" + block + "\n" + original[end:].lstrip()
    else:
        updated = original.rstrip() + "\n\n" + block + "\n"

    config_path.write_text(updated)


def main() -> None:
    plugin_root = Path(__file__).resolve().parent.parent
    codex_home = Path.home() / ".codex"
    sync_agent_files(plugin_root, codex_home)
    sync_config(codex_home)
    print("Synced KX-CDX agents to ~/.codex/agents and updated ~/.codex/config.toml")


if __name__ == "__main__":
    main()
