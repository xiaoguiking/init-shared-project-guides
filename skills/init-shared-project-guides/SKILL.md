---
name: init-shared-project-guides
description: Initialize portable shared project guidance and a knowledge-base structure. Use when starting a repository or standardizing an existing repository for Codex, Claude Code, and Cursor, including safely creating or merging AGENTS.md, CLAUDE.md, and docs/knowledge.
---

# Initialize Shared Project Guides

Create one maintainable source of project guidance that Codex, Claude Code, and Cursor can use.

## Inspect before changing

1. Identify the target repository and inspect `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `README.md`, `ARCHITECTURE.md`, and any repository instruction files.
2. Follow existing repository instructions. Preserve user-authored content and unrelated working-tree changes.
3. Explain the files that will change. Do not create a commit, push, remote repository, or symlinks unless the user explicitly requests it.

## Initialize or merge

1. For a new project, run `python3 scripts/init_project.py --target <project> --apply`. Run it without `--apply` first when the target is not empty. The script creates only missing files and never overwrites existing ones.
2. If the project already has instructions, use the script for missing files, then manually preserve and merge only missing shared-guidance or knowledge-base sections into `AGENTS.md`.
3. Make `AGENTS.md` the single source for cross-tool rules. Include project-specific commands, architecture boundaries, security rules, and the knowledge-base reference only when they are known from the repository.
4. If `CLAUDE.md` is absent, create it with exactly `@AGENTS.md`. If it exists, preserve its project-specific instructions and add that import only when it does not create a conflict.
5. Treat root `AGENTS.md` as Cursor's shared project instruction file. Remove or shrink `.cursor/rules/` only when the user authorizes it and a rule duplicates `AGENTS.md`. Retain genuinely Cursor-specific scoped rules.
6. Create `docs/knowledge/README.md` from `assets/knowledge-README.md` only when absent. Create `docs/knowledge/decisions/` as needed.
7. Add the knowledge-base reference to `AGENTS.md`: read the relevant entry before domain work, and update the index after adding lasting knowledge.

## Verify and hand off

1. Confirm that `AGENTS.md` is the only full shared-rule document and `CLAUDE.md` is a thin import.
2. List created and modified files, plus any existing files intentionally preserved.
3. Suggest the first project-specific entries to add: commands, architecture constraints, security boundaries, and a dated decision record.
