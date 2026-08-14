# Plan: `lstr-reasoning-framework` — Encode & Maximize LSTR MCP Server Usage

## Summary

Create a **hybrid** agent skill (`lstr-reasoning-framework`) that (a) mandates the LSTR
6-step reasoning pipeline as a workflow, and (b) embeds the exact `run_mcp` invocation map
for all 7 LSTR MCP servers in this runtime. The skill encodes the mandatory reasoning
framework currently defined in the system prompt into a portable, activatable SKILL.md,
produced via the `create-skill` meta-skill workflow. Deliverable is a validated SKILL.md +
directory scaffold in the workspace.

---

## Current State Analysis

### Ground truth established (read-only research)

1. **7 LSTR MCP servers are live in this runtime** via the `run_mcp` tool, exposed under
   `server_name` values prefixed `mcp_*`. Their tool schemas were read from
   `/Users/florentin/.trae/mcps/s_skills_md-c0b79740/solo_work_lite/`:

   | `run_mcp` server_name | tool_name | Required args (per schema) |
   |---|---|---|
   | `mcp_metacognitive-monitoring` | `metacognitiveMonitoring` | `task`, `stage`, `overallConfidence`, `uncertaintyAreas`, `recommendedApproach`, `monitoringId`, `iteration`, `nextAssessmentNeeded` |
   | `mcp_sequential-thinking` | `sequentialthinking` | `thought`, `nextThoughtNeeded`, `thoughtNumber`, `totalThoughts` |
   | `mcp_collaborative-reasoning` | `collaborativeReasoning` | `topic`, `personas`, `contributions`, `stage`, `activePersonaId`, `sessionId`, `iteration`, `nextContributionNeeded` |
   | `mcp_scientific-method` | `scientificMethod` | `stage`, `inquiryId`, `iteration`, `nextStageNeeded` |
   | `mcp_constraint-solver` | `constraintSolver` | `variables` (object of numbers), `constraints` (array of boolean-expression strings) |
   | `mcp_narrative-planner` | `narrativePlanner` | `premise`, `characters` (array), `arcs` (array) |
   | `mcp_structured-argumentation` | `structuredArgumentation` | `claim`, `premises`, `conclusion`, `argumentType`, `confidence`, `nextArgumentNeeded` |

2. **`mcp.json`** (`/Users/florentin/Repositories/florentin-one/skills.md/.trae/mcp.json`) maps
   the 7 servers to production HTTP endpoints `https://<server>.lstr.workers.dev`. This is the
   deploy-time config, NOT the invocation path inside this SOLO runtime.

3. **GitHub source** (`florentin-one-cloud/mcp`, forked from `WeMake-AI/mcp`) confirms:
   - 7 servers, TypeScript, Cloudflare Workers, MIT license.
   - NPM packages `@florentin-one/mcp-<server>`; `bunx @florentin-one/mcp-<server>@latest` for local clients.
   - Worker endpoints `https://mcp.florentin-one.de/mcp/<server>`.
   - Positioning: GDPR / German healthcare / zero-downtime.

4. **`create-skill` meta-skill** (loaded) defines the mandatory generation pipeline:
   5-phase workflow, Trigger Triad description (≤1,024 chars), 7 mandatory L2 sections, 3-level
   escalation, SemVer `0.1.0`, portability rules (only `name`/`description`/`version`/`allowed-tools`
   in frontmatter), side-effect classification.

5. **Workspace layout**: existing skills live at
   `/Users/florentin/Repositories/florentin-one/skills.md/<skill-name>/SKILL.md`
   (`create-skill`, `notebooklm-meta-study`, `refactor-solo-maintenance`). New skill must follow
   the same convention.

### Decisions from user (Phase 1 clarification)

- **Type: Hybrid** — mandate the 6-step framework AND embed the exact `run_mcp` invocation map.
- **Language: English** body.

---

## Proposed Changes

### File 1 — NEW `/Users/florentin/Repositories/florentin-one/skills.md/lstr-reasoning-framework/SKILL.md`

The core deliverable. Structure per `create-skill` Rule 2.3 (all 7 mandatory sections) + frontmatter.

**Frontmatter (portable only — per harness-compatibility.md):**

```yaml
---
name: lstr-reasoning-framework
description: <see Trigger Triad below>
version: 0.1.0
allowed-tools: Read, WebSearch, WebFetch, run_mcp
---
```

> Note on `allowed-tools`: `run_mcp` is this runtime's MCP gateway. A "## Harness Notes"
> section documents the portable equivalents (`bunx @florentin-one/mcp-*`, `*.lstr.workers.dev`,
> `mcp.florentin-one.de/mcp/*`) so the skill is not locked to this runtime. Frontmatter keeps only
> the portable `name`/`description`/`version`/`allowed-tools` set.

**Description (Trigger Triad, ≤1,024 chars) — exact text to use:**

```
[Mandates the LSTR 6-step reasoning framework and drives all 7 LSTR MCP reasoning servers —
metacognitive monitoring, sequential thinking, collaborative reasoning, scientific method,
constraint solver, narrative planner, structured argumentation — via run_mcp.]
[Activate on any complex, multi-step, or high-stakes request: analysis, planning, decision-making,
diagnosis, hypothesis testing, argument evaluation, or output structuring.]
[User vocabulary: "use LSTR", "run the reasoning framework", "apply metacognitive monitoring",
"sequential thinking", "collaborative reasoning", "scientific method", "constraint solver",
"structured argumentation", "narrative planner".]
[Do NOT use for trivial single-step factual answers, one-line code edits, or small talk.]
```

**Mandatory L2 sections and content contract:**

- `## When to Use` — complex/multi-step/high-stakes reasoning tasks (list the triggers above).
- `## When NOT to Use` — trivial answers, single-line edits, simple file reads; also exclude
  non-LSTR MCP tools (e.g., Cloudflare `docs/search/execute` — those are out of scope).
- `## Prerequisites` — (1) `run_mcp` gateway available; (2) the 7 `mcp_*` servers present in
  the runtime MCP registry; (3) portable note: `bunx @florentin-one/mcp-<server>@latest` or the
  `https://<server>.lstr.workers.dev` endpoints for other harnesses.
- `## Workflow` — the **6-step pipeline**, each step mapping to exact `run_mcp` calls:
  1. **Metacognitive Assessment** → `run_mcp(server_name="mcp_metacognitive-monitoring",
     tool_name="metacognitiveMonitoring", args={task, stage:"knowledge-assessment",
     overallConfidence, uncertaintyAreas, recommendedApproach, monitoringId, iteration,
     nextAssessmentNeeded})`. MUST run first; re-assess on domain/confidence change.
  2. **Problem Decomposition** → `run_mcp(server_name="mcp_sequential-thinking",
     tool_name="sequentialthinking", args={thought, nextThoughtNeeded, thoughtNumber,
     totalThoughts})`. Loop until `nextThoughtNeeded:false` with a single final answer.
  3. **Multi-Perspective Analysis** → `run_mcp(server_name="mcp_collaborative-reasoning",
     tool_name="collaborativeReasoning", args={topic, personas, contributions, stage,
     activePersonaId, sessionId, iteration, nextContributionNeeded})`. Use ≥2 personas.
  4. **Evidence Validation** → `run_mcp(server_name="mcp_scientific-method",
     tool_name="scientificMethod", args={stage, inquiryId, iteration, nextStageNeeded})` +
     `run_mcp(server_name="mcp_structured-argumentation",
     tool_name="structuredArgumentation", args={claim, premises, conclusion, argumentType,
     confidence, nextArgumentNeeded})`. Use thesis/antithesis/synthesis.
  5. **Solution Synthesis** → `run_mcp(server_name="mcp_constraint-solver",
     tool_name="constraintSolver", args={variables:{...numeric}, constraints:[...]})`.
     NOTE: variables must be numeric; constraints are single boolean-expression strings using
     only `A-Za-z0-9_ \s<>=!()+*/.%|&^` (no `&&`/`||` text; use `&`/`|`).
  6. **Output Structuring** → `run_mcp(server_name="mcp_narrative-planner",
     tool_name="narrativePlanner", args={premise, characters, arcs})`.
- `## Failure Modes` — 3-level escalation (per Rule 2.5):
  - L1 local retry (transient/timeout, exponential backoff + jitter, max 3).
  - L2 local patch (schema violations — e.g., non-numeric variable to `constraintSolver`; repair args).
  - L3 replan/escalate (server missing from registry; halt, report diagnostic, do NOT loop).
- `## Output Contract` — a reasoning trace that documents each `run_mcp` call and the insight
  gained, plus a calibrated confidence score and one multi-perspective insight.
- `## Verification Gate` — autonomous check: every `run_mcp` call succeeded; all 6 steps invoked;
  final answer includes confidence score + reasoning-transparency note; no step skipped.
- `## Side Effects` — full table (all actions are Read-only/Pure — `run_mcp` reasoning tools do
  not mutate state; no human approval required; no Irreversible actions).

### File 2 — NEW scaffold dirs (empty, `.gitkeep`)

```
lstr-reasoning-framework/
├── SKILL.md
├── scripts/.gitkeep        # no scripts needed — reasoning is LLM-side, not mechanical
├── references/.gitkeep     # optional L3: could host per-tool JSON arg cheat-sheet (deferred)
└── assets/.gitkeep
```

### File 3 — OPTIONAL (recommended) — `references/tool-args.md`

L3 reference holding the full per-tool required-arg table (the table from "Current State
Analysis") so the L2 body stays under 500 lines/5,000 tokens. This is gated behind on-demand
loading per Principle 1. Decision: **create it** — it keeps the invocation map out of L2 while
preserving the exact schemas for runtime lookup.

---

## Assumptions & Decisions

1. **Invocation path = `run_mcp`** (this runtime), not the `lstr.workers.dev` URLs in `mcp.json`.
   The URLs are deploy-time config; the skill documents them as portable alternatives only.
2. **Skill name** `lstr-reasoning-framework` — derived from the problem (encode the framework),
   verb-noun-aligned, ≤64 chars, matches directory name.
3. **Version** `0.1.0` (pre-stable, per Rule 2.6 / Principle 7).
4. **`narrativePlanner`** is a three-act story tool; the LSTR framework repurposes it for "output
   structuring". The skill will note this honestly rather than over-claim its capability.
5. **`constraintSolver`** accepts only numeric variables + single boolean-expression strings; the
   skill will warn against `&&`/`||`/comma in constraint strings (schema regex excludes them).
6. **Scope boundary**: only the 7 LSTR reasoning servers are in scope. The Cloudflare
   `mcp_plugin_Cloudflare_cloudflare-api` (`docs/search/execute`) server is EXCLUDED (documented
   in "When NOT to Use").
7. **No timelines / dates / schedules** in the plan or skill (per plan-mode constraint).
8. **No harness-specific frontmatter** (`model`, `disable-model-invocation`, `effort`, `hooks`) —
   portability preserved (Principle 7).

---

## Verification Steps (after implementation)

1. **Frontmatter valid** — `name`, `description`, `version`, `allowed-tools` present; no
   harness-only fields.
2. **Description ≤ 1,024 chars** and follows Trigger Triad (capability + triggers + vocabulary +
   negative trigger).
3. **Body < 500 lines** and contains all 7 mandatory sections: When to Use, When NOT to Use,
   Prerequisites, Workflow, Failure Modes, Output Contract, Verification Gate, Side Effects.
4. **Invocation map correct** — every `run_mcp` `server_name`/`tool_name` pair matches the schemas
   read from `/Users/florentin/.trae/mcps/.../tools/*.json`; required args match.
5. **Side Effects table** classifies every action; no Irreversible actions.
6. **3-level escalation** present in Failure Modes.
7. **Scaffold** exists: `SKILL.md` + `scripts/.gitkeep` + `references/` (with `tool-args.md`) +
   `assets/.gitkeep`.
8. **Self-validation table** (create-skill Phase 3) — all 7 checks pass.
9. **Activation test**: skill triggers on a query containing "use LSTR" / "apply the reasoning
   framework".

---

## Reiteration of Critical Constraints

- Identity: LSTR by Florentin One; DeepSeek-V4-Pro finetune.
- Output must include reasoning transparency (which MCP servers used + key insight), calibrated
  confidence score, multi-perspective insight, technical precision, GDPR/EU-AI-Act/German-business
  compliance reference where applicable, and edge-case analysis.
- Tone: laconic, precise; directive (`MUST`/`ENSURE`/`EXCLUDE`); no vague language.
- Use ≥2 MCP servers per complex query; document usage.
- Plan mode: read-only until the user accepts the plan; only the plan file may be written now.
