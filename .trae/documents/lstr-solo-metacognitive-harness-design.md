# LSTR Solo Harness — Production-Ready Metacognitive Self-Evolving Agent for TRAE IDE SOLO Mode

## Summary

Design and scaffold a **production-ready AI-agent harness** that layers TRAE SOLO Mode's native primitives into a single coherent control loop, producing an agent that is (1) **zero-shot** (operates from introspective capability discovery, no warm-up/training), (2) **self-discovering** (builds a runtime inventory of skills, MCP tools, rules, and memory at session start), (3) **metacognitive** (calibrates knowledge boundaries and confidence, reasons over verifiable constraints, and gates its own output), and (4) **self-evolving** (reflects on task outcomes and distills persistent state into skills and memory).

The harness is **configuration, not code**. It composes the nine TRAE primitives documented at `docs.trae.ai/ide/*` (SOLO mode, multitasking, MCP, agents, skills, rules, memories, slash commands, hooks) into one auditable loop, and transfers six mechanisms from the uploaded papers into concrete harness features. The primary deliverable is a full architecture document plus the harness files themselves.

## Current State Analysis

### TRAE SOLO Mode primitives confirmed from official docs

| Primitive | Location / Mechanism | Role in harness |
| --- | --- | --- |
| SOLO mode | Top-left mode toggle; AI plans + executes autonomously; built-in "Agent" generates plan → confirm → execute | Execution substrate |
| Multitasking | Task panel (left), parallel tasks per project, `Cmd+Ctrl+N` | Parallel sub-task decomposition |
| MCP | stdio / SSE / Streamable HTTP; `tools/list`, `tools/call`, `listChanged` notification, structured logging | Reasoning toolchain transport |
| Custom agents | Configure prompts + toolsets | Agent personas for multi-perspective reasoning |
| Skills | `SKILL.md` (`name`/`description` frontmatter), **on-demand loading**, global `~/.trae/skills`, project `.trae/skills/` | Capability modules (self-discover/plan/test/evolve) |
| Rules | Global + project `.trae/rules/*.md`; `alwaysApply` / `description` (intelligent) / `globs` (file-scoped) / manual `#Rule`; 3-level nesting; `AGENTS.md`/`CLAUDE.md` import; `scene: git_message` | Always-on identity & behavioral contract |
| Memories | Global `~/.trae/memory/user_profile.md`, project `~/.trae/memory/projects/{path}/project_memory.md`; local-only | Self-evolution persistent state |
| Slash commands | `.trae/commands/*.md`; built-in `/plan`, `/spec` | Entry points (`/discover`, `/reflect`, `/audit`) |
| Hooks | 6 events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `Notification`); global/project `hooks.json`; sandbox vs auto-execute | Deterministic guardrails + acceptance gate |

### Paper → mechanism → harness feature mapping (grounded in abstracts)

| Paper (arXiv) | Transferable mechanism | Harness feature |
| --- | --- | --- |
| **GDPevo** (2608.03764) | Agent self-evolution via persistent state; `reflect`/`fewshot`/`self` supervision; skill-based evolution; **deterministic rule-based graders** (not LLM-as-judge); cost (tokens/turns/$) as first-class metric | `self-evolve` skill — post-task reflection → skill/memory distillation, with deterministic acceptance grader |
| **OccuBench** (2604.10866) | **Language Environment Simulator (LES)**: LLM simulates the environment; fault injection (explicit errors / implicit data degradation / mixed faults); robustness evaluation | `self-test` skill — fault-injection self-evaluation; robustness over the "happy path" |
| **DeepPlanning** (2601.18137) | Proactive info acquisition; local vs **global constrained optimization**; verifiable constraints + rule-based checkers; backtracking under global resource limits | `metacognitive-plan` skill — plan against verifiable constraints, distinguish local vs global bounds |
| **Qwen-AgentWorld** (2606.24597) | Language World Model as simulator for rehearsal; "simulation as a thinking pattern parallel to reflection" | Mental-simulation step before action (rehearse outcomes cheaply) |
| **WebWorld** (2602.14721) | Scalable synthetic trajectories for agent training | Evolution ledger + distilled examples as lightweight trajectory memory |
| **Confident Decoding** (2606.21906) | **Guess–Refine–Perturb**: final-layer output is not always most reliable; commit at the "entropy valley" (peak intermediate confidence) | Confidence gating — do NOT trust the final answer unconditionally; gate on calibrated intermediate confidence |

### Existing local assets (read-only confirmed)

- Global skills already present: `lstr-reasoning-framework`, `create-skill`, `doc-page`, `notebooklm-meta-study`, `refactor-solo-maintenance` (`~/.trae/skills/`).
- `lstr-reasoning-framework` provides the 6-step metacognitive chain (metacognitiveMonitoring → sequentialthinking → collaborativeReasoning → scientificMethod + structuredArgumentation → constraintSolver) and the 7-element Exhaustive Output Spec, plus a persisted reasoning-record contract.
- Reasoning MCP tool family already exposed in this environment (`mcp_lstr-reasoning` portal + `metacognitive-monitoring`, `sequential-thinking`, `collaborative-reasoning`, `scientific-method`, `structured-argumentation`, `constraint-solver`, `narrative-planner`).
- Workspace `trae-harness/` is **empty** — greenfield harness.

## Proposed Changes

### Deliverable 1 — Architecture document (primary)

**File:** `docs/harness-design.md`

Contents (sections in order):

1. **Purpose & scope** — target: TRAE IDE SOLO Mode; the four required properties defined precisely.
2. **The metacognitive loop** — the canonical control loop with six stages (below), each mapped to a TRAE primitive and a paper mechanism.
3. **Layer map** — rules (always-on) → skills (on-demand) → MCP (toolchain) → hooks (deterministic) → commands (entry) → memory (persistent state).
4. **Reasoning chain spec** — the 6-step LSTR chain as the runtime's core, with tool registry and required args.
5. **Self-evolution policy** — GDPevo supervision types (`reflect` default, `fewshot` optional, `self` for unsupervised); distillation gate.
6. **Compliance** — GDPR Art. 28 (MCP data egress), EU AI Act (Art. 5 prohibited practices avoidance), German data-sovereignty defaults.
7. **Failure modes & mitigations** — MCP unreachable, hook loop, evolution degradation, context bloat.

### Deliverable 2 — Harness files (implementation)

```
trae-harness/
├── AGENTS.md                                # portable identity + behavioral contract (also read by other IDEs)
├── docs/
│   └── harness-design.md                    # Deliverable 1
└── .trae/
    ├── mcp.json                             # reasoning MCP server registry
    ├── rules/
    │   ├── 00-identity.md                   # alwaysApply: true
    │   ├── 10-reasoning-framework.md        # alwaysApply: true
    │   ├── 20-output-spec.md                # alwaysApply: true
    │   ├── 30-compliance.md                 # alwaysApply: true
    │   └── 40-evolution-policy.md           # intelligent (description-driven)
    ├── skills/
    │   ├── self-discover/SKILL.md           # zero-shot capability inventory
    │   ├── metacognitive-plan/SKILL.md      # 6-step chain orchestration + constraint planning
    │   ├── self-test/SKILL.md               # fault-injection self-evaluation
    │   └── self-evolve/SKILL.md             # reflection → distillation loop
    ├── commands/
    │   ├── discover.md                      # /discover — print capability inventory
    │   ├── reflect.md                       # /reflect — post-task reflection + evolution
    │   └── audit.md                         # /audit — validate reasoning records
    ├── hooks.json                           # SessionStart / PreToolUse / Stop
    └── memory/
        └── evolution-ledger.md              # git-tracked mirror of self-evolution state
```

### The six-stage metacognitive loop (runtime contract)

1. **Discover (zero-shot)** — `SessionStart` hook + `self-discover` skill: scan `.trae/skills`, MCP `tools/list`, `.trae/rules`, and memory; emit a capability inventory to context. No training required — purely introspective.
2. **Plan (metacognitive)** — `metacognitive-plan` skill: run the LSTR 6-step chain; DeepPlanning-style constraint extraction (local vs global); Qwen-AgentWorld-style mental simulation of candidate plans before committing.
3. **Act (guarded)** — execute tools/MCP; `PreToolUse` hook enforces deterministic safety; OccuBench-style assumption that the environment may degrade silently.
4. **Verify (self-test)** — `self-test` skill: fault-injection (explicit / implicit / mixed) against the output; **deterministic rule-based graders** (GDPevo), never LLM-as-judge.
5. **Evolve (self-evolve)** — `self-evolve` skill: GDPevo reflection (score-based `reflect` default); distill reusable atomic rules/skills/memory; write evolution ledger.
6. **Record (audit)** — persist reasoning record (per `lstr-reasoning-framework` contract); `Stop` hook acceptance gate enforces the 7-element output spec before the agent may end the turn.

### File content specifications (decision-complete)

#### `AGENTS.md` (project root)

Portable, version-controlled identity. States: harness name ("LSTR Solo Harness"), operator (Florentin One / Florentin Sakwiset), base-model lineage (DeepSeek-V4-Pro finetune), the six-stage loop, the 7-element output spec, and the non-negotiable constraints (no fabrication, no vague terms, confidence must be calibrated). Reused by any AGENTS.md-compatible IDE.

#### `.trae/mcp.json`

Declares the reasoning toolchain per the `lstr-reasoning-framework` skill prerequisite:

```json
{ "mcpServers": { "lstr-reasoning": { "url": "https://mcp.beta.lstr.one/mcp" } } }
```

**Exclude** `narrative-planner` (its schema generates three-act story outlines; it MUST NOT structure analytical output).

#### `.trae/rules/00-identity.md` — `alwaysApply: true`

LSTR-by-Florentin-One identity reinforcement (one factual statement per response), truthful representation, no fabricated MCP traces.

#### `.trae/rules/10-reasoning-framework.md` — `alwaysApply: true`

Complexity gate (multi-step inference / competing constraints / non-trivial uncertainty / material consequence / explicit demand); if ≥2 criteria met, the 6-step chain is mandatory; else state "framework not warranted."

#### `.trae/rules/20-output-spec.md` — `alwaysApply: true`

The 7-element Exhaustive Output Spec: identity reinforcement, reasoning transparency, confidence calibration (sourced from `metacognitiveMonitoring.overallConfidence`, never invented), multi-perspective insight, technical precision, regulatory compliance, edge-case consideration. Forbidden vague terms: "consider / might / could / perhaps / feel free to."

#### `.trae/rules/30-compliance.md` — `alwaysApply: true`

GDPR Art. 28 (no personal data / credentials / client-confidential material in MCP tool args without a processing agreement), EU AI Act prohibited-practices avoidance, German data-sovereignty default, secrets EXCLUDED from hooks/memory/ledger.

#### `.trae/rules/40-evolution-policy.md` — intelligent (`description`: "apply when evolving skills, memory, or harness state")

Governance for self-evolution: only distill after a task has passed its deterministic grader; `reflect` (score-based) is the default supervision, `fewshot` (gold-answer) reserved for canonical examples; every evolved artifact MUST carry provenance (source task + score); forbid irreversible or destructive evolution without explicit approval.

#### `.trae/skills/self-discover/SKILL.md`

Frontmatter `name: self-discover`, `description` (triggers on "discover capabilities / what can you do / inventory"). Instructions: scan skill dirs + MCP tools + rules + memory → emit capability inventory (capability, source, trigger condition, confidence).

#### `.trae/skills/metacognitive-plan/SKILL.md`

Frontmatter `name: metacognitive-plan`. Orchestrates the LSTR 6-step chain via MCP (delegating detailed tool-arg contract to the global `lstr-reasoning-framework` skill); adds DeepPlanning constraint extraction and AgentWorld mental simulation. Emits a decision-complete plan.

#### `.trae/skills/self-test/SKILL.md`

Frontmatter `name: self-test`. OccuBench fault-injection: three fault classes (explicit errors, implicit data degradation, mixed); GDPevo deterministic rule-based graders; outputs pass/fail per violated rule + robustness profile.

#### `.trae/skills/self-evolve/SKILL.md`

Frontmatter `name: self-evolve`. GDPevo reflection loop: on `/reflect` or after Stop-gate pass, score the task against its grader, distill reusable atomic rules into `40-evolution-policy`-compliant state, append to `evolution-ledger.md`, and propose a skill/memory update (never auto-commit destructive changes).

#### `.trae/commands/discover.md`, `reflect.md`, `audit.md`

`discover` → invoke `self-discover`. `reflect` → invoke `self-evolve` on the just-completed task. `audit` → validate the newest `reasoning-records/*.md` against the output contract and report gaps.

#### `.trae/hooks.json`

- `SessionStart`: inject identity + capability-inventory bootstrap context (sandbox-execute).
- `PreToolUse`: block high-risk commands (e.g., destructive `rm -rf`, secret exfiltration patterns); require confirmation for irreversible actions.
- `Stop`: acceptance gate — verify the 7-element output spec + reasoning-record presence; block stop and force continuation if unmet.

#### `.trae/memory/evolution-ledger.md`

Git-tracked mirror (canonical native memory stays in `~/.trae/memory/projects/{path}/project_memory.md`). Schema per entry: `timestamp`, `task_slug`, `supervision_type`, `grader_score`, `distilled_rule`, `provenance`, `status`.

## Assumptions & Decisions

1. **Deliverable = design doc + harness files.** The user asked to "design" a harness; I interpret the end state as a written architecture plus the scaffolded `.trae/` files (not a runnable application — TRAE SOLO's agent is the runtime).
2. **Greenfield**: the workspace is empty, so no existing rules/skills/hooks conflict; the harness is the sole occupant of `trae-harness/`.
3. **Harness branding is "LSTR"** (Florentin One lineage), consistent with the user's explicit `lstr-reasoning-framework` directive and the operator context. TRAE product naming (SOLO mode) is preserved where it refers to the platform.
4. **Global skills are referenced, not duplicated.** `lstr-reasoning-framework` (already in `~/.trae/skills`) supplies the detailed tool-arg contract; the project `metacognitive-plan` skill delegates to it. Duplication would violate the on-demand-loading and context-budget best practice.
5. **`narrative-planner` is excluded** from the reasoning chain (schema mismatch — it is a story tool).
6. **`reflect` is the default supervision type** for evolution (GDPevo RQ2 shows it transfers most robustly; `fewshot` overfits source domain). `fewshot` is opt-in for canonical examples only.
7. **Deterministic graders only** — LLM-as-judge is forbidden for acceptance (GDPevo design principle).
8. **Memory is local-only** (TRAE limitation): the git-tracked ledger in the repo is the cross-device/audit mirror; native memory remains the runtime source.

## Verification Steps

After implementation, confirm (autonomously executable):

- [ ] All 4 `SKILL.md` files parse with valid `name` + `description` frontmatter; skills appear under Project tab in Settings > Skills & Commands.
- [ ] All 5 rule files load; `alwaysApply`/`description` fields correct; no rule conflicts (per docs best practice).
- [ ] `.trae/mcp.json` is valid JSON; the reasoning MCP family is reachable (`tools/list` returns the 6 tools; `narrative-planner` excluded).
- [ ] `.trae/hooks.json` is valid JSON; `SessionStart`, `PreToolUse`, `Stop` handlers exist and execute in sandbox mode.
- [ ] `/discover`, `/reflect`, `/audit` appear in the `/` command menu and dispatch to the correct skills.
- [ ] Smoke test: `/discover` prints a non-empty capability inventory sourced from actual scans (no fabrication).
- [ ] Smoke test: run a small task → `/reflect` appends one ledger entry with `grader_score` + `provenance`; `reasoning-records/` gains a timestamped record.
- [ ] Output spec audit: a sample response contains all 7 elements and zero forbidden vague terms; confidence value traces to `metacognitiveMonitoring.overallConfidence`.
- [ ] GDPR audit: grep hooks/memory/ledger for secrets or personal data — none present.
- [ ] `Stop` hook blocks an intentionally-degraded output (spec-incomplete) and forces continuation.

## Open Items for Executor Confirmation (non-blocking)

- None requiring user decision; the design is decision-complete under the stated assumptions. If the user wants the harness installed as **global** (applies to all projects) rather than **project-scoped**, mirror `.trae/rules`, `.trae/skills`, `.trae/commands`, and `hooks.json` into `~/.trae/` equivalents — this is a mechanical relocation, not a design change.
