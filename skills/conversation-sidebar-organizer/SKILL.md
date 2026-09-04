---
name: conversation-sidebar-organizer
description: "Standardize Codex task titles and organize sidebar sections when the user asks to name, rename, classify, or clean up conversations. Do not use for ordinary task work that does not involve sidebar organization."
---

# 对话命名与侧边栏整理

Use this skill to maintain a small, understandable Codex sidebar. Treat a project as a workspace and a sidebar section as a visual category: do not move or rename projects unless the user explicitly asks.

## Naming a task

When naming or renaming a task, infer its primary deliverable and use:

```text
领域｜对象｜目标
```

Keep titles concise (normally 12-24 Chinese characters), searchable, and focused on one outcome. Remove dates, greetings, full questions, and vague phrasing. Prefer the user's vocabulary for project and technical names.

Typical domains:

- `求职` — resume, interviews, job applications, salary, career planning.
- `AI客服` — AI customer-service or Agent product requirements, learning, design, and implementation.
- `开发` — code, architecture, MCP, skills, tooling, and engineering workflows not specific to the AI customer-service product.
- `工具` — software, devices, or general troubleshooting.
- `副业` or `财务` — income, content creation, investing, and financial decisions.

Examples:

- `求职｜React｜面试题准备`
- `AI客服｜Agent前端｜功能开发`
- `开发｜MCP｜接入方案`
- `工具｜Movist Pro｜播放排障`

For an overlap, classify by the result the user wants from this conversation. For example, an AI customer-service project discussed for resume wording belongs to `求职`; an implementation plan belongs to `AI客服` or `开发`.

If the primary outcome is unclear, do not invent a new category. Use `探索与待归类` and choose a provisional concise title.

## Organizing the sidebar

Keep no more than 4-6 durable sections. Use `探索与待归类` for uncertain or one-off subjects. Create a new long-lived section only after the same theme appears at least three times or the user identifies it as ongoing.

When asked to clean up existing conversations:

1. Inspect the available titles and project associations first.
2. Create an inventory with four columns: current title, proposed title, proposed section, and confidence (`clear` or `needs review`).
3. Put mixed-purpose, title-only, or context-poor items in `needs review`; propose `探索与待归类` rather than guessing their intent.
4. Apply clear renames and moves only within the requested scope. Ask for a single confirmation before applying a batch that includes more than one conversation.
5. Do not archive, delete, or rename a project without explicit approval.

Use three modes:

- **盘点模式**: read-only. Report the inventory and identify duplicate, vague, and ambiguous titles.
- **整理模式**: after the user approves the proposed batch, rename and move only the approved items; preserve all conversation content.
- **新对话模式**: after the primary deliverable becomes clear, name the current task and place it in the best existing section. Do not create a new long-lived section for a single task.

## New-conversation behavior

If this skill is activated while handling a new task and task-title controls are available, update the current task title after the primary deliverable is clear. This is best-effort: a skill is not a guaranteed pre-creation hook, so never claim that every system-generated title will be replaced automatically.

When a user explicitly invokes this skill, first ask whether they want to organize the current task, a specific project, or the whole visible sidebar only if that scope is not already clear. For repeatable use, recognize these prompts:

- `盘点历史对话` — use 盘点模式.
- `按建议整理历史对话` — use 整理模式 after presenting and receiving approval for the batch.
- `规范当前对话标题` — use 新对话模式 for the current task.
