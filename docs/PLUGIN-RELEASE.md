# 发布清单

当前仓库采用“一 Skill 一版本、插件可选”的发布模型。已有插件的 Skill 同步校验插件版本；没有插件的 Skill 直接发布裸 Skill。

1. 选择并添加开源许可证；许可证会决定他人是否可以修改、再发布或商业使用此插件。
2. 在一台干净的 Codex 环境中，从仓库根目录添加市场并安装插件；使用三条代表性提示词验证当前标题、历史盘点和确认后的批量整理。
3. 更新对应 `skills/<skill-name>/SKILL.md` 的 `metadata.version`，如果存在插件则同步插件副本和 `plugins/<skill-name>/.codex-plugin/plugin.json` 的版本，并在该 Skill 的 `CHANGELOG.md` 写明行为变化。正式发布使用纯 `x.y.z` 版本；本地调试缓存版本不用于 GitHub Release。
4. 提交、推送并打上对应 Skill 的 Git 标签，例如 `conversation-sidebar-organizer` 的 `0.2.0` 使用 `skill/conversation-sidebar-organizer/v0.2.0`。发布工作流只校验并发布这个 Skill，不会要求其他 Skill 同步升级。
5. 在 GitHub Release 中附上 README 的效果图、安装步骤、三条触发提示词和反馈入口。

## 本地验收

首次使用官方校验脚本时，先确认 Python 环境具备 `PyYAML`：

```bash
python3 -c "import yaml"
# 若上一条报错，只需安装一次：
python3 -m pip install --user PyYAML
```

```bash
python3 /Users/sakura/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/conversation-sidebar-organizer
```

还应确保源码 Skill 和插件内 Skill 完全一致：

```bash
diff -u skills/conversation-sidebar-organizer/SKILL.md \
  plugins/conversation-sidebar-organizer/skills/conversation-sidebar-organizer/SKILL.md
```

## 完整发布流程

```bash
# 1. 验证插件、JSON 和源码/插件副本一致性
python3 /Users/sakura/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/conversation-sidebar-organizer  # 仅对有插件的 Skill 执行
diff -u skills/conversation-sidebar-organizer/SKILL.md \
  plugins/conversation-sidebar-organizer/skills/conversation-sidebar-organizer/SKILL.md

# 2. 提交版本与变更记录（裸 Skill 不需要加入插件目录）
git add skills/conversation-sidebar-organizer plugins/conversation-sidebar-organizer CHANGELOG.md
git commit -m "chore(release): prepare conversation-sidebar-organizer v0.2.0"
git push origin main

# 3. 创建标签，触发 GitHub Release 校验和自动 Release
git tag skill/conversation-sidebar-organizer/v0.2.0
git push origin skill/conversation-sidebar-organizer/v0.2.0
```

完成后在新的 Codex 对话中安装或重新安装插件，并用“纯问候、简单测试、具体任务、历史盘点”四类请求验收。发布失败时先修正版本、市场路径或 Skill 副本不一致问题，再创建新的版本标签；不要移动已发布标签。旧的 `v0.x.y` 标签属于仓库级历史发布，不作为新的 Skill 发布格式。

## 发布后反馈模板

请提供：Codex 版本、使用环境（桌面版/CLI/IDE）、实际提示词、期望结果、实际结果，以及是否涉及标题、移动、归档或项目操作。不要附带不必要的对话敏感内容。
