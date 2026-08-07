# Meta-Study Design Principles — Full Reference

> **L3 Reference for `create-skill`.** Loaded on demand when the invoker asks "why" a design decision was made or requests the evidence behind the principles. NOT needed for normal skill generation.

## Study Overview

**Source:** Meta-Study: "Designing the Perfect SKILL.md for Goal-Oriented, Efficient, Reliable, and Scalable AI Agent Use" (2026-07-31)
**Confidence:** 0.95 / 1.0
**Sources:** 113 across 6 research dimensions
**Master Notebook:** `8dd95a5c-6beb-44b0-8de3-f8e825f31aff`

---

## Principle 1: Progressive Disclosure & Directory Boundaries

### Source Consensus

The three-tier progressive disclosure model (L1 metadata, L2 instructions, L3 resources) is universally adopted across 30+ agent products. It keeps base context footprint at ~50-100 tokens per skill. The 500-line / 5,000-token threshold for L2 body is widely validated — performance degrades measurably beyond this limit.

### Key Citations

- agentskills.io specification (December 2025)
- Anthropic Claude Platform Docs — three-level loading system
- Microsoft Agent Framework — progressive disclosure implementation
- arXiv:2603.29919 — three-level loading and skill compression research
- Red Hat ACE Team (Jul 2026) — production validation of L1/L2/L3 gating

### Implication for Generated Skills

Every generated skill MUST gate L3 resources behind on-demand loading. L2 body must stay under 500 lines. L1 description must be the highest-leverage text — it controls activation.

---

## Principle 2: Process-Driven Lifecycles

### Source Consensus

Agents left to their own devices default to the shortest execution path, skipping testing, security checks, and review. The 6-stage lifecycle (Define→Plan→Build→Verify→Review→Ship) with anti-rationalization gates is validated by production deployments at Red Hat and NVIDIA.

### Key Citations

- Red Hat ACE Team (Jul 2026) — RCA skill lifecycle lessons
- NVIDIA-Verified Agent Skills — capability governance framework
- AWS Security Blog — "Balancing speed and safety: A control framework for AI coding agents"

### Implication for Generated Skills

Every generated skill must have explicit phase gates. No phase may be skipped. The verification gate must be an objective, automatable check — not "trust the agent."

---

## Principle 3: SemVer Compatibility Contracts

### Source Consensus

Semantic Versioning (MAJOR.MINOR.PATCH) is the dominant versioning pattern. MAJOR for breaking schema changes, MINOR for backward-compatible additions, PATCH for internal compression. The 4-phase deprecation lifecycle (soft deprecation → warning → hard deprecation → sunset) is the community standard.

### Key Citations

- AIQuinta — "Versioning Agent Skills: SemVer, Compatibility, Deprecation"
- Addy Osmani's agent-skills repository — version-control-as-code approach
- OpenClaw issue #43260 — mid-session model swap risks

### Implication for Generated Skills

All generated skills start at 0.1.0 (pre-stable). The SKILL.md output contract defines what constitutes MAJOR vs MINOR vs PATCH for that specific skill.

---

## Principle 4: Side-Effect Classification

### Source Consensus

Every action an agent performs must be classified by type (Read-only / Pure / Reversible / Compensatable / Irreversible) and blast radius (Low / Medium / High). Irreversible actions with Medium or High blast radius REQUIRE human approval. The idempotent saga pattern (compensating transactions for multi-step workflows) is the consensus recovery mechanism.

### Key Citations

- "5 AI Agent Error Handling Patterns That Keep Your Agent Running at 3 AM" — idempotency keys, saga patterns
- arXiv: "From Agent Loops to Structured Graphs" — DAG compilation with compensation chains
- MLflow — tool behavior annotations (readOnlyHint, destructiveHint, idempotentHint)
- LangChain — idempotence tool wrapping patterns

### Implication for Generated Skills

Every generated skill MUST include a Side Effects table classifying all actions. High-blast Irreversible actions MUST be gated behind human approval. The Failure Modes section must include saga compensation paths.

---

## Principle 5: Bounded Recovery & Separated Diagnostic Contexts

### Source Consensus

Unbounded retry loops ("retry storms") are the #1 production failure mode. The 3-level bounded escalation (Local Retry → Local Patch → Replan/Escalate) prevents infinite loops. Separating execution context ($C_{exec}) from diagnostic context ($C_{diag}) prevents reasoning degradation from error noise.

### Key Citations

- arXiv: "Self-Healing Agentic Orchestrators" — 18,000 controlled executions, 94.0% success under budget constraints
- arXiv: "From Agent Loops to Structured Graphs" — context partitioning and scheduler-theoretic framework
- Sentry Blog — "AI agent observability: The developer's guide to agent tracing"
- "AI Agent Error Handling Best Practices" — defense-in-depth error architecture

### Implication for Generated Skills

Every generated skill must include a 3-level escalation in Failure Modes. Recovery paths must be specific to each failure mode. The skill must never retry infinitely — all retry loops have bounded counters.

---

## Principle 6: Goal-Oriented Design (Trigger Accuracy)

### Source Consensus

The description field is the single most critical text — it controls activation. The Trigger Triad (Capability + Trigger Conditions + User Vocabulary) achieves highest activation accuracy. Negative constraints ("Do NOT...") statistically outperform positive directives ("Do...") by pruning the action space at decision points.

### Key Citations

- Large-scale empirical study (5,000+ Claude Code runs on SWE-bench Verified) — negative > positive constraints
- Termdock — "Good Skill Design: Principles That Work" — trigger accuracy patterns
- Multiple practitioners — "pushy" description technique (slightly aggressive, authoritative activation language)
- Negative Prompting 2026 guides — scope boundary enforcement

### Implication for Generated Skills

Every generated description must use the Trigger Triad. Every generated skill must include both "When to Use" (positive triggers) and "When NOT to Use" (negative triggers). The negative trigger section is NOT optional.

---

## Principle 7: Scalability & Portability

### Source Consensus

Harness-specific features in SKILL.md frontmatter (Claude-Code-only `model`, `disable-model-invocation`, `effort`, `hooks`) break portability. The open standard at agentskills.io guarantees that compliant agents discover skills using only `name` and `description`. Directory paths differ across harnesses (`.claude/skills/`, `.agents/skills/`, `.cursor/`, `.gemini/skills/`) but the SKILL.md format is shared.

### Key Citations

- agentskills.io — open standard, Apache-2.0/CC-BY-4.0, governed by Agentic AI Foundation (Linux Foundation)
- Multiple marketplace analyses — 7 active skill marketplaces (Agensi, skills.sh, mdskills.ai, etc.)
- Red Hat ACE Team — harness portability comparison table (Claude Code, GitHub Copilot, Codex, Cursor, Gemini CLI, OpenCode)
- arXiv:2603.02176 — AgentSkillOS ecosystem-scale orchestration
- MCP specification — Build with Agent Skills (modelcontextprotocol.io)

### Implication for Generated Skills

Generated skills MUST NOT include harness-specific frontmatter fields unless explicitly requested by the user. The skill should work on any agentskills.io-compliant runtime. Portability notes should document which tools are required and how to configure them across environments.

---

## Top-Ranked Sources (from Meta-Study)

1. **arXiv: "From Agent Loops to Structured Graphs"** — Mathematical scheduler framework, Kahn's algorithm DAG validation, static plan compilation proofs
2. **arXiv: "Self-Healing Agentic Orchestrators"** — 18,000 controlled executions, 94.0% success under budget, empirical fault-injection
3. **AIQuinta: "Versioning Agent Skills"** — SemVer lifecycle, 4-phase deprecation, compatibility contracts
4. **Agentic Integration Platform** — Production architecture: FastAPI + Temporal + NATS + MCP sidecars
5. **Confident AI: "5 Best CI/CD Tools for Testing AI Agents"** — Golden dataset curation, step-level metrics, release gates
6. **Red Hat ACE Team (Jul 28, 2026)** — Production RCA skill with 26% cost reduction, SkillOpt compression (90.4%)
7. **NVIDIA-Verified Agent Skills** — Capability governance framework, 4-tier gate-based permission model
8. **arXiv:2602.12670** — "Less is more" approach: focused skills outperform comprehensive ones
9. **arXiv:2604.04323** — Optimal 1-3 skills per task; beyond this, cognitive overhead dominates
10. **Zylos Research (May 2026)** — Typed skill registries reduce planning errors 30-50%

---

## Edge Cases & Known Limitations

- **36.82% of public skills contain at least one security flaw** (Snyk "ToxicSkills" Study, Feb 2026). 13.4% contain critical issues. Skills bundling executable scripts are 2.12x more likely to have vulnerabilities.
- **No native versioning schema** in the core specification. Versioning is an optional metadata entry — the generated 0.1.0 convention is a community practice, not a spec requirement.
- **Trigger collision** is common above 50 installed skills. 46% of marketplace listings share a name. When generating a skill name, prefer unique verb-noun combinations over generic terms.
- **Cross-platform portability is aspirational.** Skills written for one agent environment often implicitly rely on model-specific behaviors. Generated skills should be tested across at least two harnesses before promotion to 1.0.0.
