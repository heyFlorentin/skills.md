# Tasks

- [x] Task 1: Create skill directory scaffold
  - [x] Create `research-to-feature/` directory
  - [x] Create `research-to-feature/SKILL.md` with valid YAML frontmatter
  - [x] Create `research-to-feature/scripts/.gitkeep`
  - [x] Create `research-to-feature/references/.gitkeep`
  - [x] Create `research-to-feature/assets/.gitkeep`

- [x] Task 2: Write SKILL.md — frontmatter and description
  - [x] Write `name: research-to-feature`
  - [x] Write Trigger Triad description (capability, trigger conditions, user vocabulary, negative triggers)
  - [x] Set `version: 0.1.0`
  - [x] Set `allowed-tools: Read, Write, LS, Glob, Grep, WebSearch, WebFetch, run_mcp, Skill, Task`

- [x] Task 3: Write SKILL.md — When to Use / When NOT to Use
  - [x] Define positive triggers: research-to-feature pipeline, evidence-backed feature proposals
  - [x] Define negative triggers: trivial lookups, single-skill tasks, non-research feature ideas

- [x] Task 4: Write SKILL.md — Prerequisites section
  - [x] List required skills: `self-discover`, `notebooklm-meta-study`, `review-business-use-case`
  - [x] List required MCP servers: `mcp_NotebookLM`, `mcp_lstr-reasoning`
  - [x] Document prerequisite verification via `self-discover`

- [x] Task 5: Write SKILL.md — Workflow (4-phase pipeline)
  - [x] Phase 1: Capability Discovery — invoke `self-discover`, verify prerequisites, halt if missing
  - [x] Phase 2: Meta-Study — invoke `notebooklm-meta-study` on the user's topic, capture output
  - [x] Phase 3: Business-Use-Case Review — invoke `review-business-use-case` on the meta-study output
  - [x] Phase 4: RICE Scoring & Feature Spec — score candidates, select top, write implementation-ready spec

- [x] Task 6: Write SKILL.md — RICE Scoring Framework section
  - [x] Define Reach (1–5), Impact (1–5), Confidence (0.0–1.0), Effort (1–20 person-days)
  - [x] Define formula: `(Reach × Impact × Confidence) / Effort`
  - [x] Define scoring rules: evidence-backed, no fabrication, LOW-CONFIDENCE flag below 0.5

- [x] Task 7: Write SKILL.md — Output Contract section
  - [x] Define report path: `research-to-feature-reports/<ISO-8601>-<topic-slug>.md`
  - [x] Define 7 mandatory report sections
  - [x] Define feature specification subsections (user story, acceptance criteria, technical approach, affected components, first-actionable-task)

- [x] Task 8: Write SKILL.md — Failure Modes section
  - [x] Level 1: transient MCP errors — retry with backoff, max 3
  - [x] Level 2: missing skill — report with install instructions
  - [x] Level 3: meta-study or review failure — flag degraded, offer partial output

- [x] Task 9: Write SKILL.md — Verification Gate and Side Effects
  - [x] Define verification checks: all 4 phases completed, report file exists, all 7 sections non-empty, RICE score computed, confidence sourced from metacognitiveMonitoring
  - [x] Define side effects table: all actions classified by type and blast radius

- [x] Task 10: Self-validate against create-skill Phase 3 checklist
  - [x] Progressive Disclosure: description ≤ 1,024 chars, body ≤ 500 lines
  - [x] Goal-Oriented: single task scoped, Trigger Triad present, negative triggers defined
  - [x] Efficiency: no redundant instruction, scripts only for mechanical work
  - [x] Reliability: output contract defined, failure modes enumerated, verification gate specified
  - [x] Scalability: no harness-specific frontmatter, portability notes included
  - [x] Side-Effect Classification: every action typed
  - [x] SemVer: version 0.1.0

# Task Dependencies
- Tasks 2–9 depend on Task 1 (scaffold must exist)
- Tasks 3–9 depend on Task 2 (frontmatter anchors the file)
- Tasks 5–9 depend on Task 4 (prerequisites inform workflow)
- Task 10 depends on Tasks 1–9 (full SKILL.md must exist to validate)
- Tasks 2, 3, 4 can be written in parallel (independent sections)
- Tasks 6, 7, 8, 9 can be written in parallel after Task 5 (workflow defines the core logic)