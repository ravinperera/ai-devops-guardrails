# Agent Portability

AI DevOps Guardrails starts with portable instruction files rather than a vendor-specific plugin.

The core behaviour should live in `AGENTS.md` and the skill files. Agent-specific adapters should stay thin and point back to the same rules.

For the planned integration sequence and adapter acceptance requirements, see the [agent integration roadmap](roadmap.md).

## Support levels

- **Instruction tier:** project context loaded from files such as `AGENTS.md`, `CLAUDE.md`, or repository-specific instruction files.
- **Skill tier:** focused workflows from `skills/*/SKILL.md` loaded by a compatible agent or copied into its skill directory.
- **Plugin tier:** a tested host adapter with installation metadata, commands, hooks, or lifecycle integration.

Instruction and skill files are available now. Plugin-tier support remains planned unless a tested adapter is present in this repository.

## Current support

| Agent/tool | File | Support level |
|---|---|---|
| Generic agents | `AGENTS.md` | Instruction tier where supported |
| Claude Code | `CLAUDE.md` and `AGENTS.md` | Instruction tier |
| GitHub Copilot | `.github/copilot-instructions.md` | Instruction tier |
| Cursor | Copy `AGENTS.md` or create Cursor rules | Instruction tier |
| Windsurf | Copy `AGENTS.md` or create Windsurf rules | Instruction tier |
| Cline | Copy `AGENTS.md` or `.clinerules` equivalent | Instruction tier |
| Codex | `AGENTS.md` | Instruction tier |
| Compatible skill hosts | `skills/*/SKILL.md` | Skill tier when manually loaded or copied |

## Planned adapters

The roadmap currently considers:

- Claude Code plugin manifest and review commands
- Codex plugin manifest and shared skill discovery
- Cursor rules adapter
- OpenCode adapter
- GitHub Copilot CLI command wrappers, subject to a stable interface
- Windsurf and Cline project-rule adapters

These are plans, not current support claims. Each adapter must be implemented, tested, and documented before the README describes it as available.

## Adapter rule

Keep adapters thin.

The DevOps safety model should remain in:

- `AGENTS.md`
- `skills/*/SKILL.md`
- documentation under `docs/`

Adapters should only load, expose, or route to those rules. They should not fork the behaviour into multiple conflicting versions.

## Minimum adapter evidence

Before an adapter is marked supported, it should include:

- documented installation and removal steps
- declared permissions and network behaviour
- a smoke test proving that shared instructions load
- a safe high-risk-request example that demonstrates escalation
- documented limitations and supported host versions
- no requirement for cloud credentials merely to activate the guardrails
