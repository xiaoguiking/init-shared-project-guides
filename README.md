# Agent Skills

可由 CC Switch 管理的个人 Agent Skills 集合。

## Skills

| Skill | 用途 |
| --- | --- |
| `init-shared-project-guides` | 为项目初始化或合并 Codex、Claude Code、Cursor 共用的 `AGENTS.md`、`CLAUDE.md` 与 `docs/knowledge/`。 |

## CC Switch 使用方式

1. 将本仓库推送到 GitHub（可以是私有仓库）。
2. 在 CC Switch 的 Skills 面板添加仓库，选择本仓库的 `skills/` 子目录。
3. 将 Skills 源存储位置设为 `~/.agents/skills/`，以便受支持的 Agent 工具共享同一份源文件。
4. 在目标项目中调用 `$init-shared-project-guides`。

Skill 源码使用目录式 `SKILL.md` 格式。更新后提交并推送本仓库，再通过 CC Switch 的更新检测同步到本机。

## 本地验证

初始化器默认只预览：

```bash
python3 skills/init-shared-project-guides/scripts/init_project.py --target /path/to/project
```

确认输出后，显式写入缺失文件：

```bash
python3 skills/init-shared-project-guides/scripts/init_project.py --target /path/to/project --apply
```

它只创建缺失的 `AGENTS.md`、`CLAUDE.md`、`docs/knowledge/README.md` 和 `docs/knowledge/decisions/`，不会覆盖已有文件。
