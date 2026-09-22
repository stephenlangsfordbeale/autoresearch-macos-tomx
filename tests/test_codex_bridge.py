from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parents[1] / ".codex" / "skills" / "autoresearch-lab" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from codex_bridge import build_codex_exec_command, resolve_codex_executable  # noqa: E402


class CodexBridgeTests(unittest.TestCase):
    def test_dashboard_uses_cli_bridge_not_gui_automation(self) -> None:
        source = (SCRIPT_DIR / "dashboard_server.py").read_text(encoding="utf-8")

        self.assertIn("codex_cli_available", source)
        self.assertIn("make_codex_job", source)
        self.assertNotIn("send_prompt_to_codex_app", source)
        self.assertNotIn("osascript", source)
        self.assertNotIn('"pbcopy"', source)

    def test_explicit_environment_path_wins(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            executable = Path(temp_dir) / "configured-codex"
            executable.write_text("#!/bin/sh\n", encoding="utf-8")
            executable.chmod(executable.stat().st_mode | 0o111)

            resolved = resolve_codex_executable(
                environ={"AUTORESEARCH_CODEX_CLI": str(executable)},
                which=lambda _: None,
                bundled_path=Path(temp_dir) / "missing-bundled-codex",
            )

            self.assertEqual(resolved, executable)

    def test_path_lookup_is_used_before_bundled_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path_executable = Path(temp_dir) / "path-codex"
            path_executable.write_text("#!/bin/sh\n", encoding="utf-8")
            path_executable.chmod(path_executable.stat().st_mode | 0o111)
            bundled_executable = Path(temp_dir) / "bundled-codex"

            resolved = resolve_codex_executable(
                environ={},
                which=lambda name: str(path_executable) if name == "codex" else None,
                bundled_path=bundled_executable,
            )

            self.assertEqual(resolved, path_executable)

    def test_bundled_fallback_is_used_when_path_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            bundled = Path(temp_dir) / "codex"
            bundled.write_text("#!/bin/sh\n", encoding="utf-8")
            bundled.chmod(bundled.stat().st_mode | 0o111)

            resolved = resolve_codex_executable(environ={}, which=lambda _: None, bundled_path=bundled)

            self.assertEqual(resolved, bundled)

    def test_missing_executable_returns_none(self) -> None:
        resolved = resolve_codex_executable(
            environ={},
            which=lambda _: None,
            bundled_path=Path("/tmp/definitely-missing-codex"),
        )

        self.assertIsNone(resolved)

    def test_command_reads_prompt_from_stdin(self) -> None:
        command = build_codex_exec_command(Path("/usr/local/bin/codex"), Path("/tmp/workspace"))

        self.assertEqual(
            command,
            [
                "/usr/local/bin/codex",
                "exec",
                "--ephemeral",
                "--json",
                "-C",
                "/tmp/workspace",
                "-",
            ],
        )


if __name__ == "__main__":
    unittest.main()
