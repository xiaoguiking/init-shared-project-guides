# Project Agent Guide

This file is the single complete source of shared guidance for Codex, Claude Code, and Cursor. Maintain shared rules here; do not copy them into tool-specific files.

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

## Knowledge base

Long-lived project knowledge lives in `docs/knowledge/`; start with `docs/knowledge/README.md`. Read relevant entries before domain work, and update the index when adding durable knowledge. Keep this guide concise and do not use it as a session log.
