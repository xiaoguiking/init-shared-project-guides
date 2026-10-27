# Project Agent Guide

This file is the single maintenance source for shared guidance across Codex, Claude Code, Cursor, GitHub Copilot, and Google Antigravity. Tool-specific files may retain or add tool-specific rules; do not maintain duplicate copies of shared rules.

## Project context

- Read `README.md` and the current architecture documentation before making material changes.
- Treat implemented code and verified documentation as the source of truth; do not describe plans or placeholders as completed functionality.
- Preserve unrelated changes in the working tree.

## Changes and safety

- Use the project's documented validation commands after relevant changes.
- Keep secrets in environment variables. Do not commit, print, or hard-code credentials.
- Ask before destructive actions or external side effects outside the requested scope.

## Documentation language

- Follow the repository's established documentation language. Preserve filenames, commands, and code identifiers.
- Do not rewrite existing user-authored documents merely to make their language uniform.

## Tool compatibility

AGENTS.md loading scope, feature coverage, and rule precedence differ by tool. Some Copilot surfaces do not read AGENTS.md; do not assume every tool loads this file. Verify the actual clients used by the project.

## Knowledge base

Long-lived project knowledge lives in `docs/knowledge/`; start with `docs/knowledge/README.md`. Read relevant entries before domain work, and update the index when adding durable knowledge. Keep this guide concise and do not use it as a session log.
