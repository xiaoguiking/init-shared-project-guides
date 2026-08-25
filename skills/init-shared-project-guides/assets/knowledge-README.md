# Project Knowledge Base

Store reusable project context, important decisions, integration notes, and troubleshooting guidance here. Keep each document focused on one topic and update it when the underlying facts change.

## Suggested layout

| Path | Purpose |
| --- | --- |
| `architecture.md` | Decision background and architecture evolution; the repository's main architecture document remains authoritative for the current state. |
| `integrations.md` | External-service and tool integration notes. |
| `debugging.md` | Reproducible failures, root causes, and fixes. |
| `decisions/` | One durable decision per `YYYY-MM-DD-topic.md` file. |

## Writing rules

- Record facts, constraints, tradeoffs, and validation steps.
- Do not present an unimplemented design as current behavior.
- Update this index when adding a significant topic.
- Keep per-session change summaries in the repository's session log, not here.
