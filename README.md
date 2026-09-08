# Agent Skills

可由 CC Switch 或 Codex 使用的个人 Agent Skills 集合。

## 推荐：对话命名与侧边栏整理

`conversation-sidebar-organizer` 把 Codex 对话统一命名为 `领域｜对象｜目标`，并以“先盘点、后确认”的方式整理侧边栏。它不会因一次标题请求而移动其他对话，也不会自动归档或修改项目。

### 适用场景

- 让当前对话更易搜索，例如 `开发｜MCP｜接入方案`。
- 盘点历史对话，找出重复、模糊或缺少上下文的标题。
- 在确认候选清单后，批量重命名和分类历史对话。

### 触发方式

在 Codex 消息中显式输入以下任一提示词：

```text
$conversation-sidebar-organizer 规范当前对话标题
$conversation-sidebar-organizer 盘点历史对话
$conversation-sidebar-organizer 整理这个项目的对话
$conversation-sidebar-organizer 按刚才建议整理历史对话
```

也可以直接使用自然语言；清晰的 Skill 描述会帮助 Codex 自动匹配。但涉及批量修改时，建议始终显式使用 `$conversation-sidebar-organizer`。

### 新对话自动命名（可选）

安装 Skill 后，将下面这段规则合并到全局 `~/.codex/AGENTS.md`，保留已有内容：

```markdown
## 新对话自动命名

对新建的 Codex 对话，首轮只要有可概括内容，就在最终答复前使用
conversation-sidebar-organizer 调用宿主改名工具，按 `领域｜对象｜目标` 命名一次，无需额外询问。
简单测试也必须命名，例如“测试一个对话的内容，简单测试下” → `工具｜对话功能｜简单测试`。
信息少或需求待澄清时按已知内容保守概括，不虚构项目或技术；仅纯问候、空内容或完全无可概括信息时等待。
历史中已有成功命名记录则跳过；只有工具成功才记录“本对话已命名：标题”。
后续追问不自动改名。用户要求停用、固定标题或重新命名时遵循其选择。
无法判断是否为新对话时跳过。仅使用宿主的任务改名工具，不扫描其他任务。
Skill 或工具不可用时继续原任务，不宣称命名成功。
```

新建对话并发送具体需求或“简单测试下”即可试用，无需再输入命名提示词。成功后答复会简短记录标题，
供后续判断是否已命名。需要宿主提供任务改名工具；此方式由模型执行，不是保证触发的系统 Hook。
界面手动改名的来源不可见时不能可靠识别，需要固定标题时请在对话里明确说明。
裸 Skill 与插件副本选择一种安装，避免同名版本混淆。

### 效果示例

| 输入意图 | 处理结果 |
| --- | --- |
| “帮我看看 React 面试题” | `求职｜React｜面试题准备` |
| “为 AI 客服实现 Agent 前端” | `AI客服｜Agent前端｜功能开发` |
| “整理以前的对话” | 先输出盘点表；多条对话必须等待确认后才会修改。 |

## 安装插件

仓库已包含可安装插件和仓库级市场清单：

```text
.agents/plugins/marketplace.json
plugins/conversation-sidebar-organizer/
```

克隆本仓库后，在 Codex 的插件界面选择 **Add Marketplace**，并选择该仓库根目录；随后安装 **对话命名与侧边栏整理**。在 CLI 中，可将仓库根目录添加为市场来源：

```bash
codex plugin marketplace add /absolute/path/to/Skill
```

安装后新建一个对话，用“规范当前对话标题”验证即可。

若只希望让某个项目团队使用，请将 `.agents/plugins/marketplace.json` 和 `plugins/` 一并提交到那个项目仓库。若只想使用裸 Skill 而非插件，则将 `skills/conversation-sidebar-organizer/` 放入项目的 `.agents/skills/`。

## Skills

| Skill | 用途 |
| --- | --- |
| `conversation-sidebar-organizer` | 规范 Codex 对话标题，并以可确认的批次安全整理侧边栏分类。 |
| `controlled-change-workflow` | 通过受控流程执行可验证的代码与配置变更。 |
| `init-shared-project-guides` | 为项目初始化或合并 Codex、Claude Code、Cursor 共用的 `AGENTS.md`、`CLAUDE.md` 与 `docs/knowledge/`。 |

## 推广与发布

发布前先在 5–10 位重度 Codex 用户中试用，重点收集自动触发准确性、标题可搜索性，以及批量整理的安全感。GitHub Release 建议包含：30 秒效果图、上方三条提示词、安装方式、变更记录和反馈入口。完整发布步骤见 [发布清单](docs/PLUGIN-RELEASE.md)。

要在多个团队或多个代码库间分发时，优先发布插件；插件是可安装的分发单元，Skill 则保留为其中可复用的工作流。详见 [OpenAI Docs：构建插件](https://learn.chatgpt.com/zh-Hant/docs/build-plugins)。

## CC Switch 使用方式

1. 将本仓库推送到 GitHub（可以是私有仓库）。
2. 在 CC Switch 的 Skills 面板添加仓库，选择本仓库的 `skills/` 子目录。
3. 将 Skills 源存储位置设为 `~/.agents/skills/`，以便受支持的 Agent 工具共享同一份源文件。
4. 在目标项目中调用对应的 `$skill-name`。

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

## 发布版本

推送符合 `v*` 的 Git 标签会自动校验所有 `skills/*/SKILL.md`，并创建带自动生成说明的 GitHub Release：

```bash
git tag v0.1.0
git push origin v0.1.0
```

常规代码提交推送到 `main` 后，CC Switch 即可通过“检查更新”发现更新；不需要等待 Release。
