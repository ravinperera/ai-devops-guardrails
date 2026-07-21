# Agent Integration Roadmap

AI DevOps Guardrails begins as a portable set of instructions and review skills. The roadmap below separates what works today from richer integrations that may be added later.

The project should not claim plugin support until an adapter is implemented, tested, and documented for that host.

## Integration tiers

### 1. Instruction tier — available now

Instruction-tier support gives an AI coding agent the guardrail rules as repository context.

Current files:

- `AGENTS.md` for agents that support portable project instructions
- `CLAUDE.md` for Claude Code project guidance
- `.github/copilot-instructions.md` for GitHub Copilot repository guidance

Instruction files can influence agent behaviour, but they do not enforce CI checks, deployment approvals, branch protections, IAM controls, or production change management.

### 2. Skill tier — available now where supported

The `skills/` directory contains focused review workflows that can be loaded or copied into compatible agent systems:

- `devops-review`
- `terraform-audit`
- `github-actions-review`
- `aws-iam-review`
- `deployment-readiness`
- `secrets-check`

Skill-tier adapters should expose these existing files rather than duplicate their safety rules.

### 3. Plugin tier — planned

Plugin-tier support may add installation manifests, commands, and lifecycle hooks where an agent provides stable extension points.

A plugin adapter must remain thin. It should load the shared instructions and skills, not maintain a separate version of the guardrails.

## Proposed adapter sequence

| Priority | Host | Proposed work | Status |
|---|---|---|---|
| 1 | Claude Code | Plugin manifest, skill discovery, review commands, optional safe activation hook | Planned |
| 2 | Codex | Plugin manifest, shared skill discovery, review commands | Planned |
| 3 | Cursor | Repository rule file that points to the shared instruction model | Planned |
| 4 | OpenCode | Thin adapter that injects the shared rules and exposes review skills | Planned |
| 5 | GitHub Copilot CLI | Command wrappers if the plugin interface is stable and documented | Candidate |
| 6 | Windsurf and Cline | Project-rule adapters aligned with `AGENTS.md` | Candidate |

Priority does not guarantee delivery. Adapters depend on documented, stable host capabilities and safe test coverage.

## Adapter requirements

A new adapter should meet all of the following before it is described as supported:

- Reuse `AGENTS.md` and `skills/*/SKILL.md` as the source of truth.
- Avoid destructive actions or production access by default.
- Never request or store cloud credentials merely to load the guardrails.
- Clearly distinguish advisory output from enforced policy.
- Document installation, removal, permissions, and limitations.
- Include a smoke test showing that the adapter loads the intended rules.
- Include a test or example showing that high-risk requests are escalated rather than silently executed.
- Avoid telemetry or external network calls unless explicitly documented and optional.

## Suggested implementation phases

### Phase 1 — portability foundation

- Keep the instruction files aligned.
- Keep reusable safety behaviour in the existing skills.
- Add worked examples and agent-specific installation documentation.
- Add lightweight validation for Markdown, YAML, and adapter manifests.

### Phase 2 — first-party adapters

- Add a Claude Code adapter.
- Add a Codex adapter.
- Add a Cursor rules adapter.
- Document exact supported versions and limitations.

### Phase 3 — lifecycle and command support

- Add commands such as `devops-review`, `terraform-audit`, and `deployment-readiness` where supported.
- Consider opt-in hooks that activate review context before infrastructure changes.
- Keep all hooks advisory unless a separate enforcement mechanism is explicitly configured.

### Phase 4 — compatibility and release discipline

- Add adapter compatibility tests.
- Publish versioned releases and migration notes.
- Track deprecated host interfaces and remove unsupported claims promptly.

## Contributing an adapter

Before starting an adapter, open an issue describing:

1. The target agent and its documented extension mechanism.
2. Which shared instructions and skills the adapter will load.
3. Whether it requires hooks, commands, network access, or additional permissions.
4. How installation and removal will work.
5. How the adapter will be tested without cloud credentials or production access.
6. Known limitations and any behaviour that remains advisory only.

Prefer one small adapter per pull request. Do not combine a new host integration with broad changes to the core guardrail model.

## Non-goals

The roadmap does not aim to:

- replace cloud policy enforcement, CI controls, or human approval
- execute infrastructure changes automatically
- bypass agent permission prompts
- maintain different safety policies for different AI agents
- claim support based only on copying a file name without testing how the host loads it
