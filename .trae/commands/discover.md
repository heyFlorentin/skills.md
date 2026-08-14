---
name: discover
description: Build a zero-shot runtime capability inventory of the LSTR Solo Harness.
---

Invoke the `self-discover` skill.

1. Scan `~/.trae/skills/*/SKILL.md` and `.trae/skills/*/SKILL.md` for skill names, descriptions, and trigger conditions.
2. Call `tools/list` on each MCP server in `.trae/mcp.json`.
3. Read `.trae/rules/*.md` frontmatter (alwaysApply vs description-driven).
4. Read project memory and the evolution ledger.

Output a capability table with columns `Capability`, `Source`, `Trigger condition`, `Confidence`, plus a short "Gaps" list. Every row MUST trace to a real source (no fabrication).
