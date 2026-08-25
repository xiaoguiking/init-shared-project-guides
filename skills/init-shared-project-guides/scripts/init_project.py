#!/usr/bin/env python3
"""Safely initialize shared project guidance without overwriting files."""

from __future__ import annotations

import argparse
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"


def plan(target: Path) -> list[tuple[str, Path, Path | None]]:
    """Return actions as (kind, destination, source)."""
    actions: list[tuple[str, Path, Path | None]] = []
    files = {
        target / "AGENTS.md": ASSETS_DIR / "AGENTS.md",
        target / "CLAUDE.md": None,
        target / "docs" / "knowledge" / "README.md": ASSETS_DIR / "knowledge-README.md",
    }
    for destination, source in files.items():
        actions.append(("skip" if destination.exists() else "create", destination, source))
    decisions = target / "docs" / "knowledge" / "decisions"
    actions.append(("skip-dir" if decisions.is_dir() else "mkdir", decisions, None))
    return actions


def write_file(destination: Path, source: Path | None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source is None:
        destination.write_text("@AGENTS.md\n", encoding="utf-8")
    else:
        destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize shared AGENTS.md, CLAUDE.md, and docs/knowledge safely."
    )
    parser.add_argument("--target", default=".", help="Target project directory (default: current directory).")
    parser.add_argument("--apply", action="store_true", help="Create missing files and directories.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        parser.error(f"target is not a directory: {target}")

    actions = plan(target)
    for kind, destination, source in actions:
        label = "CREATE" if kind == "create" else "MKDIR" if kind == "mkdir" else "KEEP"
        relative = destination.relative_to(target)
        detail = f" from {source.name}" if source and kind == "create" else ""
        print(f"{label:6} {relative}{detail}")

    if not args.apply:
        print("Dry run only. Re-run with --apply to create missing paths.")
        return 0

    for kind, destination, source in actions:
        if kind == "create":
            write_file(destination, source)
        elif kind == "mkdir":
            destination.mkdir(parents=True, exist_ok=True)

    print("Initialization complete. Existing files were preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
