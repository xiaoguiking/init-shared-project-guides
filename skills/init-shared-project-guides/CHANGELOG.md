# Changelog: init-shared-project-guides

## 0.2.0 - 2026-10-27

- 扩展共享指引到 Codex、Claude Code、Cursor、GitHub Copilot 和 Google Antigravity；Gemini CLI 可选生成兼容入口。
- 新增 `--tools` 选择，按所选工具创建薄入口；审计各工具规则目录并提醒人工合并，不自动改写既有规则。
- 增加官方加载机制说明与客户端验证步骤，明确 Copilot 各功能区的能力差异。
- 加强路径碰撞与符号链接预检，避免向目标仓库之外写入。

## 0.1.5 - 2026-09-21

- 增加可移植插件清单与仓库 marketplace 分发入口，支持公开插件目录和跨 Agent 安装。

## 0.1.4 - 2026-09-21

- 增加 `--language zh-CN|en`，支持按仓库约定选择中文或英文模板。
- 增加只读 `--audit`，初始化前报告现有指引、Cursor 规则和常见项目入口。
- 增加英文 `AGENTS.md`、知识库模板和无第三方依赖的 unittest 覆盖。

## 0.1.3 - 2026-09-11

- 建立独立 Skill 版本基线，并承接仓库此前的 `0.1.3` 变更记录。
