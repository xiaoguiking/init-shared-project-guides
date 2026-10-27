#!/usr/bin/env python3
"""Test tool selection, safe initialization, and read-only audit behavior."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("init_project.py")
DEFAULT_TOOLS = ("codex", "claude-code", "cursor", "copilot", "antigravity")


def run_initializer(target: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), "--target", str(target), *args],
        check=check,
        capture_output=True,
        text=True,
    )


class InitProjectTests(unittest.TestCase):
    def test_default_tools_create_shared_files_and_claude_bridge_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            run_initializer(target, "--apply")
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / "docs/knowledge/README.md").is_file())
            self.assertEqual((target / "CLAUDE.md").read_text(), "@AGENTS.md\n")
            self.assertFalse((target / "GEMINI.md").exists())
            self.assertFalse((target / ".github/copilot-instructions.md").exists())

    def test_explicit_gemini_only_selection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            run_initializer(target, "--tools", "gemini-cli", "--apply")
            self.assertEqual((target / "GEMINI.md").read_text(), "@./AGENTS.md\n")
            self.assertFalse((target / "CLAUDE.md").exists())

    def test_codex_only_does_not_create_compatibility_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            run_initializer(target, "--tools", "codex", "--apply")
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertFalse((target / "CLAUDE.md").exists())
            self.assertFalse((target / "GEMINI.md").exists())

    def test_invalid_tool_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_initializer(Path(directory), "--tools", "unknown", check=False)
            self.assertNotEqual(result.returncode, 0)

    def test_preview_and_audit_do_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            preview = run_initializer(target)
            audit = run_initializer(target, "--audit").stdout
            self.assertIn("Copilot", audit)
            self.assertIn("人工", audit)
            self.assertIn("antigravity", audit)
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertIn("预览", preview.stdout)

    def test_existing_bridge_and_tool_rules_are_preserved_and_audited(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            claude = target / "CLAUDE.md"
            claude.write_text("# Existing Claude-only rule\nKeep this text.\n", encoding="utf-8")
            gemini = target / "GEMINI.md"
            gemini.write_text("# Existing Gemini-only rule\nKeep this too.\n", encoding="utf-8")
            rule = target / ".cursor/rules/custom.mdc"
            rule.parent.mkdir(parents=True)
            rule.write_text("cursor-specific", encoding="utf-8")
            result = run_initializer(target, "--audit")
            self.assertIn("人工比较", result.stdout)
            run_initializer(target, "--tools", "codex", "claude-code", "gemini-cli", "--apply")
            self.assertEqual(claude.read_text(), "# Existing Claude-only rule\nKeep this text.\n")
            self.assertEqual(gemini.read_text(), "# Existing Gemini-only rule\nKeep this too.\n")
            self.assertEqual(rule.read_text(encoding="utf-8"), "cursor-specific")

    def test_apply_is_idempotent_and_preserves_user_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "AGENTS.md").write_text("user guide", encoding="utf-8")
            run_initializer(target, "--apply")
            run_initializer(target, "--apply")
            self.assertEqual((target / "AGENTS.md").read_text(), "user guide")
            self.assertEqual((target / "CLAUDE.md").read_text(), "@AGENTS.md\n")

    def test_language_selection_and_gemini_bridge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            run_initializer(target, "--language", "en", "--tools", "codex", "gemini-cli", "--apply")
            self.assertIn("# Project Agent Guide", (target / "AGENTS.md").read_text())
            self.assertIn("# Project Knowledge Base", (target / "docs/knowledge/README.md").read_text())
            self.assertEqual((target / "GEMINI.md").read_text(), "@./AGENTS.md\n")

    def test_dangling_symlink_is_not_treated_as_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "AGENTS.md").symlink_to(target / "missing-target")
            result = run_initializer(target, "--apply", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue((target / "AGENTS.md").is_symlink())
            self.assertFalse((target / "CLAUDE.md").exists())

    def test_guide_directory_collision_fails_before_other_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "AGENTS.md").mkdir()
            result = run_initializer(target, "--apply", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((target / "CLAUDE.md").exists())
            self.assertFalse((target / "docs").exists())

    def test_path_collisions_fail_before_any_partial_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "docs/knowledge").mkdir(parents=True)
            (target / "docs/knowledge/decisions").write_text("collision", encoding="utf-8")
            result = run_initializer(target, "--apply", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((target / "AGENTS.md").exists())

    def test_audit_handles_invalid_entry_encoding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "CLAUDE.md").write_bytes(b"\xff")
            result = run_initializer(target, "--audit")
            self.assertEqual(result.returncode, 0)
            self.assertIn("无法安全读取", result.stdout)

    def test_symlinked_output_parent_blocks_all_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "repo"
            outside = root / "outside"
            target.mkdir()
            outside.mkdir()
            (target / "docs").symlink_to(outside, target_is_directory=True)
            result = run_initializer(target, "--apply", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse(list(outside.iterdir()))


if __name__ == "__main__":
    unittest.main()
