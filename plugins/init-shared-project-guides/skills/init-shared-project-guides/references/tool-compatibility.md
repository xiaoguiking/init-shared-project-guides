# 工具兼容性与加载验证

官方文档核对日期：2026-10-27。下表仅概述官方文档明确说明的加载能力；文件存在不等于当前客户端已加载，实际范围还会受客户端、功能区、版本和项目打开方式影响。此仓库尚未对每种客户端进行实机验证。

| 工具 | 官方文档所述机制 | 本 Skill 的处理 |
| --- | --- | --- |
| Codex | 项目规则使用 `AGENTS.md`，可按目录层级发现。 | 始终生成共享正文。 |
| Claude Code | 当前支持 `AGENTS.md`；也支持 `CLAUDE.md` 和文件导入。版本或功能不支持 AGENTS 时可使用 CLAUDE 入口。 | 仅选择 `claude-code` 时，在缺失的 `CLAUDE.md` 写入 `@AGENTS.md`。已有文件保留。 |
| Cursor | 支持根目录及子目录 `AGENTS.md`，并与其他规则组合；`.cursor/rules/*.mdc` 仍可提供范围专属规则，更具体规则可能优先。 | 始终生成共享正文，不自动改写 `.cursor/rules/`。 |
| GitHub Copilot | 支持因产品和功能区而异。VS Code Chat、CLI及部分 agent/review 场景支持 agent instructions；GitHub.com Copilot Chat、VS Code code review、Visual Studio 和其他场景可能要求 `.github/copilot-instructions.md` 或路径规则。 | 使用 `AGENTS.md` 作为共享来源；不生成 Copilot 桥接文件。需要该文件的 Copilot 功能区需由维护者另行适配，并避免复制共享规则。 |
| Google Antigravity | App、CLI 和 IDE 支持根目录与子目录的 `AGENTS.md`、`GEMINI.md`。 | 始终生成共享正文，不生成额外入口。 |
| Gemini CLI（可选） | 项目上下文默认从 `GEMINI.md` 加载，支持 `@file` 导入。 | 仅选择 `gemini-cli` 时，在缺失的 `GEMINI.md` 写入 `@./AGENTS.md`。 |

## 验证步骤

对每个实际使用的客户端分别验证，记录客户端名称与版本、打开的仓库根目录、检查的规则文件和观察到的行为：

1. 使用该产品官方文档列出的项目指令文件位置，确认本仓库的 `AGENTS.md` 或适配入口位于已打开的项目范围内。
2. 在新会话中提出一个只由项目规则决定、可安全观察的请求，例如询问项目文档中指定的验证命令；检查回答是否遵循该规则。
3. 切换到受子目录规则覆盖的文件时，验证该工具是否加载预期范围内的规则。不要假设工具间具有相同的层级或优先级。
4. 如果客户端提供上下文/规则查看界面，可将其作为辅助证据；没有此界面时，记录对照提示和回答，不把单次行为当作普遍保证。
5. Copilot 应按具体功能区单独核实。依赖 `.github/copilot-instructions.md` 的界面需要维护者明确决定是否增加该文件及其同步方式。

## 官方来源

- [OpenAI：AGENTS.md 自定义指令](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code：Project memory and instruction files](https://code.claude.com/docs/en/memory)
- [Cursor：Rules](https://cursor.com/docs/rules)
- [GitHub Copilot：Custom instructions support by environment](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- [Google Antigravity：Rules](https://www.antigravity.google/docs/rules/)
- [Gemini CLI：Project context (GEMINI.md)](https://geminicli.com/docs/cli/gemini-md/)
