#!/usr/bin/env python3
"""安全初始化共享项目指引，支持中文或英文模板且不覆盖已有文件。"""

from __future__ import annotations

import argparse
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
LANGUAGE_ASSETS = {
    "zh-CN": {
        "agents": ASSETS_DIR / "AGENTS.md",
        "knowledge": ASSETS_DIR / "knowledge-README.md",
    },
    "en": {
        "agents": ASSETS_DIR / "AGENTS.en.md",
        "knowledge": ASSETS_DIR / "knowledge-README.en.md",
    },
}


def plan(target: Path, language: str) -> list[tuple[str, Path, Path | None]]:
    """返回操作列表：(kind, destination, source)。"""
    actions: list[tuple[str, Path, Path | None]] = []
    assets = LANGUAGE_ASSETS[language]
    files = {
        target / "AGENTS.md": assets["agents"],
        target / "CLAUDE.md": None,
        target / "docs" / "knowledge" / "README.md": assets["knowledge"],
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


def audit(target: Path) -> None:
    """报告共享指引初始化前需要人工判断的现状，不写入任何文件。"""
    checks = [
        ("AGENTS.md", target / "AGENTS.md"),
        ("CLAUDE.md", target / "CLAUDE.md"),
        ("知识库首页", target / "docs" / "knowledge" / "README.md"),
        ("Cursor 规则目录", target / ".cursor" / "rules"),
    ]
    candidates = [
        "README.md",
        "ARCHITECTURE.md",
        "package.json",
        "pnpm-workspace.yaml",
        "pyproject.toml",
        "go.mod",
        ".github/workflows",
    ]

    print(f"只读审计：{target}")
    print("现有共享指引：")
    for label, path in checks:
        state = "已存在" if path.exists() else "缺失"
        print(f"- {label}：{state}")

    claude = target / "CLAUDE.md"
    if claude.exists():
        content = claude.read_text(encoding="utf-8")
        state = "是" if content == "@AGENTS.md\n" else "否，需要人工检查"
        print(f"- CLAUDE.md 是否为薄导入：{state}")

    found = [candidate for candidate in candidates if (target / candidate).exists()]
    print("可人工查阅的项目入口：")
    if found:
        for candidate in found:
            print(f"- {candidate}")
    else:
        print("- 未发现常见入口；初始化后应由维护者补充项目专有信息。")
    print("提示：审计只反映文件存在情况，不推断命令、架构或语言约定。")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="安全初始化共享的 AGENTS.md、CLAUDE.md 和 docs/knowledge（默认中文模板）。"
    )
    parser.add_argument("--target", default=".", help="目标项目目录（默认：当前目录）。")
    parser.add_argument("--apply", action="store_true", help="创建缺失的文件和目录。")
    parser.add_argument(
        "--audit",
        action="store_true",
        help="只读报告已有指引和候选项目入口，不创建或修改文件。",
    )
    parser.add_argument(
        "--language",
        choices=LANGUAGE_ASSETS,
        default="zh-CN",
        help="新建模板语言（默认：zh-CN）。已有文件不会被改写。",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        parser.error(f"目标路径不是目录：{target}")
    if args.audit and args.apply:
        parser.error("--audit 和 --apply 不能同时使用")

    if args.audit:
        audit(target)
        return 0

    actions = plan(target, args.language)
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
