---
name: conversation-sidebar-organizer
description: "Create consistent, searchable conversation titles for Cursor, Codex, Grok, Claude, and similar AI tools. When host controls are available, safely rename tasks and organize Codex sidebar sections."
metadata:
  version: "0.2.0"
---

# Chat Naming / 对话命名助手

Use this skill to create consistent, searchable conversation titles across AI tools. The naming format and decision rules are portable; actual title changes and sidebar operations depend on the host's available controls. In Codex, a project is a workspace and a sidebar section is a visual category. Never rename, move, archive, or delete a project unless the user explicitly asks.

## 跨工具边界

- **通用部分**：在 Cursor、Codex、Grok、Claude 或其他 Agent 工具中，按 `领域｜对象｜目标` 生成清晰、可搜索的对话标题。
- **Codex 专属部分**：只有宿主提供任务改名、历史对话读取或侧边栏操作工具时，才能执行自动改名、盘点、批量重命名和分类；没有这些工具时，只输出建议标题或可复制的操作说明，不声称已修改。
- **工具适配**：不要假设不同工具共享标题、历史记录或侧边栏；只操作当前宿主明确暴露的对话和项目。

## 先判定范围与模式

Map the request before taking any mutation:

| User intent | Mode | Default scope | Action |
| --- | --- | --- | --- |
| `规范当前对话标题` / `给这个对话命名` | 新对话模式 | current task only | Rename the current task once its deliverable is clear. |
| `盘点历史对话` / `看看侧边栏` | 盘点模式 | visible sidebar | Read only; return an inventory. |
| `按建议整理历史对话` | 整理模式 | previously approved items | Apply only the approved batch. |
| `整理这个项目的对话` | 盘点模式 first | named project | Inspect, propose, then wait for approval. |

For explicit organization requests with no identifiable scope, ask one concise scope question. Automatic naming always targets only the current task and needs no scope question. A title-only request never authorizes sidebar moves.

## 自动命名模式（需常驻指令启用）

安装 Skill 本身不等于启用每个新对话的自动命名。只有用户或常驻指令明确启用时采用此模式。

- 新对话首轮只要有可概括的内容，就在最终答复前按 `领域｜对象｜目标` 命名一次；信息少或需求仍需澄清不是跳过理由。只依据已知内容保守概括，不虚构项目或技术。仅纯问候、空内容或完全没有可概括信息时等待下一轮。
- “测试一个对话的内容，简单测试下”应命名为 `工具｜对话功能｜简单测试`；“帮我看看 React 面试题”可命名为 `求职｜React｜面试题准备`；仅“你好”则等待。不要因为“简单测试”没有业务需求而跳过，也不要只输出标题建议而不调用可用的改名工具。
- 仅使用当前对话上下文，不扫描其他对话；只改当前标题，不移动、归档或创建分类。
- 历史中已有成功命名记录（自动或显式）则跳过。后续追问、报错、主题扩展不再自动改名；用户明确要求重新命名时才更新。
- 用户说“这个对话不要自动命名”时停止；“标题固定为……”按用户原文执行，并停止后续自动命名。
- 无法确定是否为新对话，或压缩后的上下文无法判断此前是否命名时，跳过。标题格式不代表命名来源；没有来源信息时不能可靠识别界面手动改名。
- 使用宿主任务改名工具，例如 `set_thread_title`；支持省略 ID 时直接定位当前任务。不猜测任务 ID，不写应用数据库或会话文件。
- 成功后在最终答复末尾简短记录“本对话已命名：标题”，作为后续判断依据；上下文摘要应保留成功记录及停用/固定标题选择。
- 工具不可用或失败时继续原任务，不宣称成功或反复重试，必要时说明一次未能自动命名。这是模型执行的规则，不保证每次必定触发。

## 命名任务

Infer the primary deliverable, then use this pattern:

```text
领域｜对象｜目标
```

Titles should normally be 12–24 Chinese characters, searchable, and focused on one outcome. Use the user's vocabulary for project and technical names. Remove dates, greetings, filler, whole questions, and vague verbs such as `帮忙`, `看看`, or `处理一下`.

Choose the three parts in this order:

1. **目标优先** — identify the concrete result the user expects: implementation, troubleshooting, review, preparation, comparison, or planning.
2. **领域归类** — classify by that result, not merely by a term mentioned in the conversation.
3. **对象收束** — retain the smallest useful product, feature, technology, or artifact name; omit redundant words already conveyed by the domain or goal.

Typical domains:

- `求职` — resume, interviews, job applications, salary, career planning.
- `AI客服` — AI customer-service or Agent product requirements, learning, design, and implementation.
- `开发` — code, architecture, MCP, skills, tooling, and engineering workflows not specific to the AI customer-service product.
- `工具` — software, devices, or general troubleshooting.
- `副业` or `财务` — income, content creation, investing, and financial decisions.

Examples:

| Conversation outcome | Title |
| --- | --- |
| Prepare React interview answers | `求职｜React｜面试题准备` |
| Implement an Agent frontend for the customer-service product | `AI客服｜Agent前端｜功能开发` |
| Design an MCP integration outside that product | `开发｜MCP｜接入方案` |
| Fix a Movist Pro playback problem | `工具｜Movist Pro｜播放排障` |
| Improve this skill's title rules | `开发｜对话命名 Skill｜优化` |

For overlaps, use the result the user wants: customer-service implementation is `AI客服`; wording that presents the project in a job search is `求职`; general reusable tooling is `开发`. If the primary outcome is genuinely unclear, do not invent a new category: use `探索与待归类｜对象｜待明确` and state that it is provisional.

Before saving, verify that the title has exactly two `｜` separators, does not repeat the same meaning in adjacent parts, and is not a full sentence. If a title cannot fit cleanly, prefer a specific shorter noun over abbreviating it into something unsearchable.

## 整理侧边栏

Keep 4–6 durable sections. Use `探索与待归类` for uncertain or one-off subjects. Create a new long-lived section only when the theme appears at least three times or the user explicitly identifies it as ongoing.

For a requested cleanup:

1. Inspect task titles, task status, and project associations first.
2. Create an inventory with: current title, proposed title, proposed section, rationale, and confidence (`clear` or `needs review`).
3. Mark mixed-purpose, title-only, and context-poor tasks as `needs review`; propose `探索与待归类` rather than guessing intent.
4. Report the proposed batch before any change. A batch affecting more than one conversation requires one explicit confirmation; do not treat silence or a new unrelated question as approval.
5. After confirmation, rename and move only the approved tasks. Preserve task content and leave projects unchanged unless explicitly included.
6. Report successes and any individual failures. Do not silently retry a failed move with a different section.

## 操作规则

- **盘点模式** is read-only: report duplicates, vague titles, ambiguous items, and the proposed inventory.
- **整理模式** is write-enabled only after the required approval. Prefer updating an existing section over creating a near-duplicate.
- **新对话模式** changes the current title once the deliverable is clear. If title controls are unavailable, say it could not be applied; never claim an automatic rename.
- For a title-only request, do not inspect or modify other conversations. For a move-only request, preserve the existing title unless the user also approves a rename.
- When only one unambiguous task is explicitly named, rename or move it directly; summarize the exact change afterward.
- If a task is archived, do not unarchive it just to rename or classify it unless the user specifically asks.

## Completion messages

For a current-title request, state the exact final title. For a cleanup, state the number of renamed and moved tasks, list any `needs review` items, and surface failures or skipped items. Keep the response concise; the inventory is the detailed artifact.
