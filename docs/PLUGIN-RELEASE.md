# 发布清单

`conversation-sidebar-organizer` 已具备仓库级插件市场结构。发布前按以下顺序执行。

1. 选择并添加开源许可证；许可证会决定他人是否可以修改、再发布或商业使用此插件。
2. 在一台干净的 Codex 环境中，从仓库根目录添加市场并安装插件；使用三条代表性提示词验证当前标题、历史盘点和确认后的批量整理。
3. 更新 `plugins/conversation-sidebar-organizer/.codex-plugin/plugin.json` 的 `version`，并在 README 的变更记录写明行为变化。
4. 提交、推送并打上与 `version` 一致的 Git 标签。
5. 在 GitHub Release 中附上 README 的效果图、安装步骤、三条触发提示词和反馈入口。

## 本地验收

```bash
python3 /Users/sakura/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/conversation-sidebar-organizer
```

还应确保源码 Skill 和插件内 Skill 完全一致：

```bash
diff -u skills/conversation-sidebar-organizer/SKILL.md \
  plugins/conversation-sidebar-organizer/skills/conversation-sidebar-organizer/SKILL.md
```

## 发布后反馈模板

请提供：Codex 版本、使用环境（桌面版/CLI/IDE）、实际提示词、期望结果、实际结果，以及是否涉及标题、移动、归档或项目操作。不要附带不必要的对话敏感内容。
