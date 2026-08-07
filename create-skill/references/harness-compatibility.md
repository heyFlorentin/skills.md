# Harness Compatibility Reference

> **L3 Reference for `create-skill`.** Loaded on demand when the invoker targets a specific agent harness (Claude Code, Codex, Cursor, etc.) or asks about portability. NOT needed for normal skill generation.

## Discovery Paths by Harness

| Harness | Project Scope | User Scope | Discovery Model |
| --------- | -------------- | ------------ | ----------------- |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | Automatic (description matching) + manual (`/skill-name`) |
| **GitHub Copilot** | `.github/skills/` (also reads `.claude/skills/`) | — | Automatic (three-level progressive disclosure) |
| **Codex CLI** | `.agents/skills/` | `~/.agents/skills/` or `~/.codex/skills/` | Automatic (description matching) |
| **Cursor** | `.cursorrules` (project root) or `chat.agentSkillsLocations` | — | Always-on — no selective discovery, rules apply to every interaction |
| **Gemini CLI** | `.gemini/skills/` | — | Automatic |
| **OpenCode** | `.opencodeai/skills/` | — | Automatic |
| **OpenClaw** | — | `~/.openclaw/skills/` | Automatic |
| **skills.md (hasna)** | Remote via MCP — no local skill source | `.skills/pins/` for preferences | Remote registry, MCP-based discovery |

## Frontmatter Extensions by Harness

### Standard (Portable — Use These)

| Field | Spec | Notes |
| ------- | ------ | ------- |
| `name` | Required | kebab-case, ≤64 chars, must match directory |
| `description` | Required | ≤1,024 chars |
| `version` | Optional | SemVer recommended |
| `license` | Optional | SPDX identifier |
| `tags` | Optional | Comma-separated |
| `allowed-tools` | Optional | Restrict agent tool access |

### Claude Code Only (AVOID — Breaks Portability)

| Field | Effect |
| ------- | -------- |
| `model` | Model override — rejected by other harnesses |
| `disable-model-invocation` | Requires manual triggering |
| `user-invocable` | Hides from CLI menu |
| `effort` | Reasoning depth |
| `context: fork` | Isolated subagent context |
| `hooks` | Lifecycle hooks |
| `paths` | File path restrictions |
| `shell` | Shell integration |

### OpenAI Codex Only (AVOID — Breaks Portability)

Sidecar file: `agents/openai.yaml` for UI display names, policies, and MCP tool dependencies. Not part of the SKILL.md spec.

### OpenClaw Only (AVOID — Breaks Portability)

Nested `metadata.openclaw` blocks for preflight gating (verifying local binaries, env variables before exposing skill).

## Portability Best Practices for Generated Skills

1. **Use only `name`, `description`, `version`, `allowed-tools` in frontmatter.** Everything else is harness-specific.
2. **If the user explicitly requests a harness-specific feature**, add it in a `## Harness Notes` section in the body — not in frontmatter — with a clear label: "Claude Code only: ..."
3. **Test on at least two harnesses before promoting from 0.1.0 to 1.0.0.**
4. **Document tool dependencies.** If the skill requires `Read`, `Write`, `Bash`, or any MCP tool, list them under `## Prerequisites`.
5. **Avoid model- or temperature-specific instructions.** Do not write "Use Opus for this step" or "Set temperature to 0" — these are harness/operator decisions, not skill concerns.

## Cursor-Specific Warning

Cursor's skills system treats all skills as always-on context. This is fundamentally different from Claude Code/Codex progressive disclosure. Skills with large L2 bodies (>2,000 tokens) may significantly impact Cursor's context budget. If the user targets Cursor, consider:

- Keeping L2 body under 2,000 tokens
- Moving more content to L3 references
- Using shorter, denser writing style

## skills.md Platform-Specific Notes

- Skills on skills.md are remote-execution by default — the skill source stays on the platform, not local.
- Generated SKILL.md files can be published to skills.md following their publishing guide (`skills.md/docs/publishing`).
- Premium pricing and approval gates are set at the platform level, not in the SKILL.md.
- The `skills validate <name>` command checks frontmatter, manifest, and directory structure before publishing.

## Registry Compatibility

Generated skills should be compatible with these registries:

- **skills.md** (`@hasna/skills`) — requires `skills validate <name>` pass
- **Agensi** — 8-point security scan and review before listing
- **skills.sh** — one-command installation, telemetry rankings
- **mdskills.ai** — GitHub-based, requires `agent-skills` topic on repo
- **agentskills.io** — open standard, any compliant runtime
- **SkillsMD** (`npx skillsmd`) — requires `skill.md` naming (note: lowercase `s`)
