---
name: self-discover
description: Builds a zero-shot runtime capability inventory for the LSTR Solo Harness. Invoke when the agent needs to discover its own capabilities — trigger phrases "discover capabilities", "what can you do", "inventory your tools", "/discover", or at SessionStart bootstrap. Produces a capability table (capability, source, trigger condition, confidence) from skills, MCP tools, rules, and memory.
---

# self-discover

Zero-shot, self-discovering capability inventory. No training or warm-up — purely introspective: the agent reads its own configuration surface and reports what it can do.

## When to Use

- Session start (bootstrap), or when explicitly asked "what can you do".
- Before planning a complex task, to know which tools and skills are available.
- When a task's required capability is uncertain.

## Instructions

1. **Scan skills** — read frontmatter `name` + `description` from `~/.trae/skills/*/SKILL.md` and `.trae/skills/*/SKILL.md`. Record each skill's trigger conditions.
2. **Scan MCP tools** — call `tools/list` on each declared MCP server in `.trae/mcp.json`. Record tool names and their one-line purpose. EXCLUDE `narrative-planner` from the analytical toolchain.
3. **Scan rules** — read frontmatter from `.trae/rules/*.md`. Record which are `alwaysApply`, which are `description`-driven (intelligent), and their activation conditions.
4. **Scan memory** — read `~/.trae/memory/projects/{project}/project_memory.md` and `.trae/memory/evolution-ledger.md` for distilled rules.
5. **Emit the inventory** — a table with columns: `Capability`, `Source` (skill/MCP/rule/memory + path), `Trigger condition`, `Confidence` (0.0–1.0 based on evidence completeness).

## Output Contract

- Non-empty capability table; every row MUST trace to a real file or `tools/list` response (no fabrication).
- A short "Gaps" list: capabilities the task may need that are NOT currently discoverable.

## Constraints

- Do NOT claim a capability whose source you did not read.
- Confidence is evidence-based; an unread source is `unverified`, not `0.9`.
