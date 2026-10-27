---
name: init-shared-project-guides
description: Initialize portable shared project guidance and a knowledge-base structure for coding agents. Use when starting a repository or auditing existing agent instructions before safely creating shared AGENTS.md guidance and optional compatibility entries.
metadata:
  version: "0.2.0"
---

# 初始化共享项目指引

为 Codex、Claude Code、Cursor、GitHub Copilot 和 Google Antigravity 建立共享项目指引，并创建便于人工阅读的知识库骨架。完整共享规则只在 `AGENTS.md` 中维护；工具专属文件可以保留或补充该工具特有规则。

## 语言与可读性

- 新建的指引和知识库默认使用简体中文。对已有明确语言约定的仓库，初始化时显式传入 `--language en` 或 `--language zh-CN`；不依赖不可靠的自动语言猜测。
- 保留文件名、命令和代码标识符。不要把某个工具的文件导入语法描述为其他工具的通用语法；合并既有文档时，不要擅自翻译用户已有内容。
- 模板只提供跨项目通用的最小规则。根据仓库已验证的信息补充具体命令、架构边界、目录入口和安全要求，不要留下泛泛的占位段落。

## 修改前检查

1. 确认目标仓库，检查 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.cursor/rules/`、`.github/`、`.claude/rules/`、`.agents/rules/`、`.agent/rules/`、`README.md`、`ARCHITECTURE.md` 及其他项目指引文件。
2. 遵循仓库已有规则，保留用户编写的内容和无关的工作区改动。
3. 说明将变更的文件；除非用户明确要求，不创建提交、推送、远程仓库或软链接。

## 初始化或合并

1. 运行 `python3 scripts/init_project.py --target <project> --tools codex claude-code cursor copilot antigravity`；默认工具为这五项，`gemini-cli` 可显式加入。非空仓库先运行 `--audit`，再不带 `--apply` 预览；脚本只创建缺失路径，绝不覆盖已有文件。
2. `--audit` 是只读检查：报告各工具入口、规则目录及候选项目入口，并提示人工合并；它不推断项目命令，也不写入文件。
3. 已有指引时，先用脚本补齐缺失文件，再仅向 `AGENTS.md` 合并缺失的共享规则或知识库说明，并保留原有语言和内容。
4. 以 `AGENTS.md` 作为共享规则的唯一维护来源。Codex、Claude Code、Cursor、Copilot 与 Antigravity 的加载范围和优先级并不相同；Copilot 的部分界面不读取 `AGENTS.md`。不要生成未经用户要求的 `.github/copilot-instructions.md` 桥接文件。
5. 只为所选工具创建入口：选择 `claude-code` 时，缺失的 `CLAUDE.md` 写入 `@AGENTS.md`；选择 `gemini-cli` 时，缺失的 `GEMINI.md` 写入 `@./AGENTS.md`。其他已存在入口和专属规则保持不变。
6. 不自动删除或合并 `.cursor/rules/`、`.claude/rules/`、`.github/`、`.agents/rules/`、`.agent/rules/` 中的规则；存在时提示维护者人工核对冲突与适用范围。
7. 仅在缺失时由对应语言的知识库模板创建 `docs/knowledge/README.md`，并按需创建 `docs/knowledge/decisions/`。
8. 在 `AGENTS.md` 写明知识库入口：领域工作前阅读相关条目，新增长期有效信息后同步更新索引。

## 验证与交付

1. 确认共享规则只在 `AGENTS.md` 维护；检查本次所选工具的入口是否指向共享正文，同时保留其专属内容。
2. 列出新建和修改的文件，以及刻意保留的已有文件。
3. 提示首批值得补充的项目专有信息：常用命令、架构约束、安全边界、文档语言约定，以及一条带日期的决策记录。
4. 根据目标客户端逐一验证指引是否载入，并记录客户端/版本、打开的项目目录、验证提示和实际可观察结果。官方机制与验证步骤见 [references/tool-compatibility.md](references/tool-compatibility.md)。不要声称仅靠文件存在即可证明客户端已载入。
5. 修改初始化脚本后，运行 `python3 scripts/test_init_project.py`；测试不依赖第三方 Python 包。
