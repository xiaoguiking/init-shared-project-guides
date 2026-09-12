---
name: init-shared-project-guides
description: Initialize portable, Chinese-first shared project guidance and a knowledge-base structure. Use when starting a repository or standardizing an existing repository for Codex, Claude Code, and Cursor, including safely creating or merging AGENTS.md, CLAUDE.md, and docs/knowledge.
metadata:
  version: "0.1.3"
---

# 初始化共享项目指引

为 Codex、Claude Code 和 Cursor 建立一份可维护的共享项目指引，并创建便于人工阅读的中文知识库骨架。

## 语言与可读性

- 新建的指引和知识库默认使用简体中文；保留文件名、命令、代码标识符和 `@AGENTS.md` 导入语法。
- 若仓库已有明确的文档语言约定，遵循该约定；合并既有英文文档时，不要擅自翻译用户已有内容。
- 模板只提供跨项目通用的最小规则。根据仓库已验证的信息补充具体命令、架构边界、目录入口和安全要求，不要留下泛泛的占位段落。

## 修改前检查

1. 确认目标仓库，检查 `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/`、`README.md`、`ARCHITECTURE.md` 及其他项目指引文件。
2. 遵循仓库已有规则，保留用户编写的内容和无关的工作区改动。
3. 说明将变更的文件；除非用户明确要求，不创建提交、推送、远程仓库或软链接。

## 初始化或合并

1. 新项目可运行 `python3 scripts/init_project.py --target <project> --apply`。非空仓库先不带 `--apply` 预览；脚本只创建缺失文件，绝不覆盖已有文件。
2. 已有指引时，先用脚本补齐缺失文件，再仅向 `AGENTS.md` 合并缺失的共享规则或知识库说明，并保留原有语言和内容。
3. 以 `AGENTS.md` 作为跨工具规则的唯一完整来源。仅在仓库中已确认时写入项目命令、架构边界、安全规则、文档语言约定和知识库入口。
4. `CLAUDE.md` 缺失时，创建内容严格为 `@AGENTS.md`；已存在时保留项目专有指令，只在不会冲突时补充该导入。
5. 根目录 `AGENTS.md` 同时作为 Cursor 的共享项目指引。仅在用户授权且规则与 `AGENTS.md` 重复时，删除或精简 `.cursor/rules/`；保留真正仅适用于 Cursor 的范围规则。
6. 仅在缺失时由 `assets/knowledge-README.md` 创建 `docs/knowledge/README.md`，并按需创建 `docs/knowledge/decisions/`。
7. 在 `AGENTS.md` 写明知识库入口：领域工作前阅读相关条目，新增长期有效信息后同步更新索引。

## 验证与交付

1. 确认 `AGENTS.md` 是唯一完整的共享规则文档，`CLAUDE.md` 仅作薄导入层。
2. 列出新建和修改的文件，以及刻意保留的已有文件。
3. 提示首批值得补充的项目专有信息：常用命令、架构约束、安全边界、文档语言约定，以及一条带日期的决策记录。
