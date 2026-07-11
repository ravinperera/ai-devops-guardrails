# Agent Portability

AI DevOps Guardrails starts with portable instruction files rather than a vendor-specific plugin.

The core behaviour should live in `AGENTS.md` and the skill files. Agent-specific adapters should stay thin and point back to the same rules.

## Current support

| Agent/tool | File | Support level |
|---|---|---|
| Generic agents | `AGENTS.md` | Always-on project instructions where supported |
| Claude Code | `CLAUDE.md` and `AGENTS.md` | Project instructions |
| GitHub Copilot | `.github/copilot-instructions.md` | Repository instructions |
| Cursor | Copy `AGENTS.md` or create Cursor rules | Instruction-tier |
| Windsurf | Copy `AGENTS.md` or create Windsurf rules | Instruction-tier |
| Cline | Copy `AGENTS.md` or `.clinerules` equivalent | Instruction-tier |
| Codex | `AGENTS.md` | Project instructions |

## Future adapters

Future versions may add:

- Claude Code plugin manifest
- Codex plugin manifest
- OpenCode plugin adapter
- Cursor rules file
- Windsurf rules file
- slash-command wrappers for each skill
- lifecycle hooks for review mode activation

## Adapter rule

Keep adapters thin.

The DevOps safety model should remain in:

- `AGENTS.md`
- `skills/*/SKILL.md`
- documentation under `docs/`

Adapters should only load, expose or route to those rules. They should not fork the behaviour into multiple conflicting versions.
