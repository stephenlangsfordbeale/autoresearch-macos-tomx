"""Codex CLI discovery and command construction for the local dashboard."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Callable, Mapping


DEFAULT_BUNDLED_CODEX = Path("/Applications/ChatGPT.app/Contents/Resources/codex")
CODEX_ENV_VARS = ("AUTORESEARCH_CODEX_CLI", "CODEX_CLI_PATH")


def _resolve_candidate(candidate: str, which: Callable[[str], str | None]) -> Path | None:
    value = candidate.strip()
    if not value:
        return None
    path = Path(value).expanduser()
    if path.is_file() and path.stat().st_mode & 0o111:
        return path
    resolved = which(value)
    if resolved:
        resolved_path = Path(resolved)
        if resolved_path.is_file() and resolved_path.stat().st_mode & 0o111:
            return resolved_path
    return None


def resolve_codex_executable(
    environ: Mapping[str, str] | None = None,
    which: Callable[[str], str | None] | None = None,
    bundled_path: Path = DEFAULT_BUNDLED_CODEX,
) -> Path | None:
    """Resolve the executable without requiring a GUI Codex application."""

    env = os.environ if environ is None else environ
    lookup = shutil.which if which is None else which
    for name in CODEX_ENV_VARS:
        configured = env.get(name)
        if configured:
            resolved = _resolve_candidate(configured, lookup)
            if resolved:
                return resolved
    resolved = _resolve_candidate("codex", lookup)
    if resolved:
        return resolved
    if bundled_path.is_file() and bundled_path.stat().st_mode & 0o111:
        return bundled_path
    return None


def build_codex_exec_command(executable: Path, working_directory: Path) -> list[str]:
    """Build a non-interactive command that reads its prompt from stdin."""

    return [
        str(executable),
        "exec",
        "--ephemeral",
        "--json",
        "-C",
        str(working_directory),
        "-",
    ]
