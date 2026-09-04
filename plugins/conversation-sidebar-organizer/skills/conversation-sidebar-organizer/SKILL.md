---
name: conversation-sidebar-organizer
description: "Standardize Codex task titles and organize sidebar sections. Use when the user asks to name, rename, classify, inventory, or clean up Codex conversations or sidebar sections; do not use for ordinary task work."
---

# 对话命名与侧边栏整理

Use this skill to keep a small, understandable Codex sidebar. A project is a workspace; a sidebar section is a visual category. Never rename, move, archive, or delete a project unless the user explicitly asks.

## 先判定范围与模式

Map the request before taking any mutation:

| User intent | Mode | Default scope | Action |
| --- | --- | --- | --- |
| `规范当前对话标题` / `给这个对话命名` | 新对话模式 | current task only | Rename the current task once its deliverable is clear. |
| `盘点历史对话` / `看看侧边栏` | 盘点模式 | visible sidebar | Read only; return an inventory. |
| `按建议整理历史对话` | 整理模式 | previously approved items | Apply only the approved batch. |
| `整理这个项目的对话` | 盘点模式 first | named project | Inspect, propose, then wait for approval. |

If the user did not identify a current task, a project, or the visible sidebar, ask one concise scope question before inspecting or changing anything. A request that only concerns the current title never authorizes sidebar moves.

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
