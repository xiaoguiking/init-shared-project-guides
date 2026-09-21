# Project Knowledge Base

Store reusable project context, important decisions, integration notes, and troubleshooting guidance here. Keep each document focused on one topic and update it when the underlying facts change. Follow the repository's established documentation language; preserve filenames, commands, and code identifiers.

## Suggested layout

| Path | Purpose | Create or update when |
| --- | --- | --- |
| `architecture.md` | Architecture evolution and decision background; the repository's main architecture document remains authoritative for the current state. | Architecture boundaries or key technical choices change. |
| `integrations.md` | External-service and tool integration boundaries and validation. | An external dependency is added, changed, or investigated. |
| `debugging.md` | Reproducible failures, root causes, and fixes. | A resolved issue has reusable value. |
| `decisions/` | One durable decision per `YYYY-MM-DD-topic.md` file. | A confirmed decision needs its tradeoffs preserved. |

## Index

No project-specific entries yet. Add a link and one-sentence summary here when adding a significant topic.

## Writing rules

- Record facts, constraints, tradeoffs, validation steps, and the applicable scope.
- Do not present an unimplemented design as current behavior.
- Update this index when adding a significant topic; mark obsolete content with its replacement or remove it.
- Keep per-session change summaries in the repository's session log, not here.
