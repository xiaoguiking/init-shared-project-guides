#!/usr/bin/env python3
"""安全初始化中文优先的共享项目指引，且不覆盖已有文件。"""

from __future__ import annotations

import argparse
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"


def plan(target: Path) -> list[tuple[str, Path, Path | None]]:
    """返回操作列表：(kind, destination, source)。"""
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
        description="安全初始化共享的 AGENTS.md、CLAUDE.md 和 docs/knowledge（默认中文模板）。"
    )
    parser.add_argument("--target", default=".", help="目标项目目录（默认：当前目录）。")
    parser.add_argument("--apply", action="store_true", help="创建缺失的文件和目录。")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        parser.error(f"目标路径不是目录：{target}")

    actions = plan(target)
    for kind, destination, source in actions:
        label = "新建" if kind == "create" else "建目录" if kind == "mkdir" else "保留"
        relative = destination.relative_to(target)
        detail = f"（模板：{source.name}）" if source and kind == "create" else ""
        print(f"{label:6} {relative}{detail}")

    if not args.apply:
        print("以上为预览，使用 --apply 创建缺失路径。")
        return 0

    for kind, destination, source in actions:
        if kind == "create":
            write_file(destination, source)
        elif kind == "mkdir":
            destination.mkdir(parents=True, exist_ok=True)

    print("初始化完成，已有文件均已保留。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
