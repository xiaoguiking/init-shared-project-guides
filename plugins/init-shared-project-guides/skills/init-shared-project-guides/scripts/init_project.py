#!/usr/bin/env python3
"""安全初始化共享项目指引，支持中文或英文模板且不覆盖已有文件。"""

from __future__ import annotations

import argparse
import os
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
TOOLS = ("codex", "claude-code", "cursor", "copilot", "antigravity", "gemini-cli")
DEFAULT_TOOLS = TOOLS[:5]


def path_entry_exists(path: Path) -> bool:
    """Treat files, directories, and even dangling symlinks as existing entries."""
    return os.path.lexists(path)


def plan(target: Path, language: str, tools: list[str]) -> list[tuple[str, Path, Path | None]]:
    """返回操作列表：(kind, destination, source)。"""
    actions: list[tuple[str, Path, Path | None]] = []
    assets = LANGUAGE_ASSETS[language]
    files: dict[Path, Path | None] = {
        target / "AGENTS.md": assets["agents"],
        target / "docs" / "knowledge" / "README.md": assets["knowledge"],
    }
    if "claude-code" in tools:
        files[target / "CLAUDE.md"] = None
    if "gemini-cli" in tools:
        files[target / "GEMINI.md"] = None
    for destination, source in files.items():
        actions.append(("skip" if path_entry_exists(destination) else "create", destination, source))
    decisions = target / "docs" / "knowledge" / "decisions"
    actions.append(("skip-dir" if path_entry_exists(decisions) else "mkdir", decisions, None))
    return actions


def write_file(destination: Path, source: Path | None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source is None:
        import_text = "@AGENTS.md\n" if destination.name == "CLAUDE.md" else "@./AGENTS.md\n"
        destination.write_text(import_text, encoding="utf-8")
    else:
        destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def audit(target: Path, tools: list[str]) -> None:
    """报告共享指引初始化前需要人工判断的现状，不写入任何文件。"""
    checks = [
        ("共享正文 AGENTS.md", target / "AGENTS.md"),
        ("Claude Code 兼容入口 CLAUDE.md", target / "CLAUDE.md"),
        ("Gemini CLI 兼容入口 GEMINI.md", target / "GEMINI.md"),
        ("知识库首页", target / "docs" / "knowledge" / "README.md"),
        ("Cursor 专属规则 .cursor/rules/", target / ".cursor" / "rules"),
        ("Copilot 仓库指令 .github/copilot-instructions.md", target / ".github" / "copilot-instructions.md"),
        ("Copilot 路径指令 .github/instructions/", target / ".github" / "instructions"),
        ("Claude Code 专属规则 .claude/rules/", target / ".claude" / "rules"),
        ("Antigravity 专属规则 .agents/rules/", target / ".agents" / "rules"),
        ("Antigravity 旧版规则 .agent/rules/", target / ".agent" / "rules"),
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
        state = "已存在" if path_entry_exists(path) else "缺失"
        print(f"- {label}：{state}")

    print(f"本次选择工具：{', '.join(tools)}")
    print("自动创建入口仅限所选工具：Claude Code → CLAUDE.md；Gemini CLI → GEMINI.md。")
    print("Cursor 与 Antigravity 可读取 AGENTS.md。Copilot：VS Code Chat/CLI、cloud agent 与 code review 的支持范围不同；不会生成 copilot-instructions.md 桥接文件。")
    existing_rules = [label for label, path in checks[4:] if path_entry_exists(path)]
    if existing_rules:
        print("检测到工具专属规则；请人工比较共享正文与专属规则，脚本不会合并或改写：")
        for label in existing_rules:
            print(f"- {label}")

    for name, expected in (("CLAUDE.md", "@AGENTS.md\n"), ("GEMINI.md", "@./AGENTS.md\n")):
        entry = target / name
        if path_entry_exists(entry):
            if entry.is_symlink():
                state = "是符号链接，脚本保留；请人工确认目标"
            elif entry.is_file():
                try:
                    content = entry.read_text(encoding="utf-8")
                    state = "是" if content == expected else "否，需要人工检查"
                except (OSError, UnicodeError):
                    state = "无法安全读取，需要人工检查"
            else:
                state = "不是普通文件或为悬空链接，阻止自动写入；需人工检查"
            print(f"- {name} 是否为薄导入：{state}")

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
        description="安全初始化共享 AGENTS.md、所选工具入口和 docs/knowledge（默认中文模板）。"
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
    parser.add_argument(
        "--tools",
        nargs="+",
        choices=TOOLS,
        default=list(DEFAULT_TOOLS),
        metavar="TOOL",
        help="目标工具（默认：codex claude-code cursor copilot antigravity；gemini-cli 可选）。",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        parser.error(f"目标路径不是目录：{target}")
    if args.audit and args.apply:
        parser.error("--audit 和 --apply 不能同时使用")

    if args.audit:
        audit(target, args.tools)
        return 0

    actions = plan(target, args.language, args.tools)
    errors: list[str] = []
    for kind, destination, _ in actions:
        entry_exists = path_entry_exists(destination)
        if kind in ("create", "skip") and entry_exists and (destination.is_symlink() or not destination.is_file()):
            errors.append(f"{destination.relative_to(target)} 已存在但不是普通文件，无法安全作为指引文件")
        if kind in ("mkdir", "skip-dir") and entry_exists and (destination.is_symlink() or not destination.is_dir()):
            errors.append(f"{destination.relative_to(target)} 已存在但不是普通目录")
        if kind not in ("create", "mkdir"):
            continue
        relative = destination.relative_to(target)
        for parent in (target.joinpath(*relative.parts[:i]) for i in range(1, len(relative.parts))):
            if path_entry_exists(parent) and (parent.is_symlink() or not parent.is_dir()):
                errors.append(f"{parent.relative_to(target)} 是非目录或符号链接，拒绝向外写入")
                break
    if errors:
        parser.error("写入前检查失败：" + "；".join(dict.fromkeys(errors)))
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

    print("初始化完成，已有路径均已保留。工具专属规则如需统一，请人工合并；脚本不会覆盖或自动合并。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
