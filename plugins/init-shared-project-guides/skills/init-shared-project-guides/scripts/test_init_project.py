#!/usr/bin/env python3
"""Test the initializer's language, preservation, and audit invariants."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("init_project.py")


def run_initializer(target: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), "--target", str(target), *args],
        check=True,
        capture_output=True,
        text=True,
    )


class InitProjectTests(unittest.TestCase):
    def test_default_language_is_chinese(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            run_initializer(target, "--apply")
            self.assertIn("# 项目 Agent 共享指引", (target / "AGENTS.md").read_text())
            self.assertIn(
                "# 项目知识库",
                (target / "docs" / "knowledge" / "README.md").read_text(),
            )

    def test_english_language_uses_english_templates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            run_initializer(target, "--language", "en", "--apply")
            self.assertIn("# Project Agent Guide", (target / "AGENTS.md").read_text())
            self.assertIn(
                "# Project Knowledge Base",
                (target / "docs" / "knowledge" / "README.md").read_text(),
            )

    def test_existing_file_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            guide = target / "AGENTS.md"
            guide.write_text("# User-owned guide\n", encoding="utf-8")
            run_initializer(target, "--apply")
            self.assertEqual(guide.read_text(encoding="utf-8"), "# User-owned guide\n")

    def test_audit_does_not_create_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            output = run_initializer(target, "--audit").stdout
            self.assertIn("只读审计", output)
            self.assertFalse((target / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
