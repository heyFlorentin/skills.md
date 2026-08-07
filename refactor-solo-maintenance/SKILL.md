---
name: refactor-solo-maintenance
description: Produces a measured, RICE-ranked refactoring plan plus a machine-readable backlog that drives a solo developer's repository toward ~1 active maintenance month per year. Invoke when analyzing an existing codebase, GitHub Actions pipeline, AI-agent configuration, or maintenance cadence for refactoring opportunities, when maintenance load must be reduced to a fixed annual budget, or when refactors must be prioritized by effort and impact. Triggers on "refactor my workflow", "reduce my maintenance burden", "audit my CI/CD pipeline", "get me to one maintenance month per year", "prioritize refactors with RICE", "analyze my repo for automation opportunities", "make my repo AI-agent friendly". Do NOT use for greenfield project setup, for executing refactors (this skill plans, it does not implement), for reviewing a single pull request, or for repositories with a team of maintainers where the 1-month/year solo budget does not apply.
---

# refactor-solo-maintenance

Audits an existing repository across four domains — codebase architecture, GitHub Actions CI/CD, AI-agent integration, and maintenance cadence — then emits a RICE-ranked refactoring plan and a machine-readable backlog reconciled against a hard annual maintenance budget of ~160 hours (~1 active month per year).

## When to Use

- A solo developer wants to reduce recurring maintenance load on an existing repository to a fixed annual budget.
- Existing CI/CD workflows, module boundaries, or agent configuration must be evaluated for automation and delegation opportunities.
- A refactoring backlog exists but is unprioritized, and quick wins must be sequenced ahead of architectural surgery.
- Maintenance time must be quantified and defended against a target rather than estimated by intuition.

## When NOT to Use

- Do NOT use for greenfield repositories. There is no baseline to measure, so every finding would be fabricated.
- Do NOT use to implement refactors. This skill produces a plan and a backlog; execution is a separate, explicitly requested task.
- Do NOT use for single-PR review, syntax questions, or mechanical renames.
- Do NOT use for team-maintained repositories. The ~160 h/yr budget is calibrated to one person and misallocates work across multiple maintainers.
- Do NOT use when the user requests a quick opinion. The measurement phase is mandatory and cannot be shortened into a guess.

## Prerequisites

ENSURE all four conditions hold before Phase 1. If any fails, halt per Failure Modes.

1. A readable repository root containing at least one commit of history.
2. A writable `refactor-plans/` directory at the repository root, or an alternative path supplied by the user.
3. Read access to `.github/workflows/` if CI/CD is in scope. If absent, record the CI/CD domain as `no-pipeline` rather than inventing one.
4. Either the `gh` CLI authenticated for workflow-run timing data, or explicit user acknowledgement that pipeline baselines will be marked `unmeasured`.

## Non-Negotiable Constraints

These four constraints override every other instruction in this skill.

1. **Do NOT fabricate findings.** Every baseline number, file structure claim, timing figure, and current-state assertion MUST trace to a file read, a command output, or a user-supplied statement. Unmeasured values MUST be written as `unmeasured` with the reason, never as an estimate presented as fact.
2. **Do NOT mutate the repository.** Source files, workflow YAML, IaC, secrets, branches, and remote state are read-only. The only writes permitted are the two artifacts in the Output Contract. No commits, pushes, deploys, or merges.
3. **Do NOT recommend enterprise-only tooling.** EXCLUDE paid observability platforms, GitHub Enterprise-tier features, org-level security tiers, and any process presupposing an SRE rotation or dedicated reviewer. Every recommendation MUST be operable and affordable by one person on free or hobby tiers.
4. **Do NOT ship an unverified plan.** The Verification Gate is a hard precondition of delivery, not a post-hoc checklist.

> **Why:** These are the four failure modes that make a refactoring plan actively harmful. A fabricated baseline invalidates every downstream RICE score. An unrequested mutation destroys trust in a read-only analysis. Enterprise tooling produces a plan the developer cannot execute. An unverified plan hides arithmetic that does not reconcile to the target.

## Workflow

### Phase 0: Scope and Context Gate

Establish the analysis surface before reading anything at depth.

**Step 0.1** — Determine the repository root, primary language(s), and deployment target from manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, IaC entrypoints).

**Step 0.2** — Identify which of the four domains are in scope. A domain is out of scope only when its artifacts do not exist. Record out-of-scope domains and the evidence for exclusion.

**Step 0.3** — Detect context gaps that would force fabrication. The following are blocking gaps: unknown current maintenance hours per month, unknown deployment/hosting model, unknown incident volume, unknown acceptable downtime. Ask the user for blocking gaps only — a maximum of four questions in one batch. Do NOT ask questions answerable by reading the repository.

> **Why:** Batching the questions once prevents an interrogation loop. Restricting questions to blocking gaps prevents the skill from outsourcing measurement work it can perform itself.

### Phase 1: Baseline Measurement (Read-Only)

Collect evidence before forming any judgement. Load `references/domain-probes.md` for the exhaustive per-domain probe list.

Record every measurement in an Evidence Ledger with four columns: `metric`, `value`, `source` (file path with line range, or exact command), `status` (`measured` | `user-reported` | `unmeasured`).

Minimum probe set per domain:

| Domain | Minimum probes |
| --- | --- |
| Architecture | Module/directory topology, cross-module import graph density, duplicated-code hotspots, type coverage, error-handling call sites, largest files by line count |
| CI/CD | Workflow inventory, job dependency graph, serial vs parallel job structure, wall-clock duration of the last 10 runs per workflow, cache usage, action version pinning, Dependabot config presence |
| AI-agent integration | Presence and size of agent rules/skills files, context footprint of each, prompt reuse patterns, test-generation coverage, knowledge-base location and version control status |
| Maintenance cadence | Commit/issue cadence over the trailing 12 months, alert and notification surfaces, IaC self-managed vs managed-service ratio, manual runbook inventory |

If `gh` is available, measure pipeline duration with `gh run list` and `gh run view`. If not, mark all timing metrics `unmeasured` and state that RICE Confidence for CI/CD items is capped at 0.5 as a result.

DO NOT proceed to Phase 2 while any minimum probe is unattempted.

### Phase 2: Domain Analysis

For each in-scope domain, produce findings that each bind one measured deficiency to one recommendation.

Every finding MUST carry: `id` (`ARCH-01`, `CICD-01`, `AGENT-01`, `MAINT-01`), the measured current state with its evidence reference, the target state, the recommendation, and the estimated annual maintenance hours recovered.

Domain objectives to evaluate against:

- **Architecture** — domain-aligned module boundaries that isolate change; AI-parseable standards, type safety, and self-documenting patterns; a single shared utility library replacing duplicated code; one universal error-handling and structured-logging framework enabling auto-diagnosis.
- **CI/CD** — parallelized test/build/deploy stages; automated action and dependency patching; canary deployment with automated rollback; Dependabot auto-merge for safe updates with manual review reserved for critical security patches.
- **AI-agent integration** — agent rules and skills restructured for context-window efficiency; a standardized prompt library and custom agent workflows covering routine scaffolding, bug triage, and documentation; AI-generated tests under an audit gate; a version-controlled central knowledge base.
- **Maintenance cadence** — non-critical work batched into one monthly window; alerting reduced to critical production signals only; IaC migrated toward serverless and managed services to eliminate server upkeep; runbooks converted to agent-executable automation.

Percentage targets (80% routine issue resolution, 70% task automation, 50% pipeline reduction, 60% runbook time reduction) are **targets to be justified per repository**, not results to be asserted. Each target MUST be restated as a KPI with the measured baseline in Phase 4. Where a baseline is `unmeasured`, the KPI MUST be expressed as a relative reduction with a stated measurement plan, not an absolute figure.

### Phase 3: RICE Scoring and Sequencing

Score every finding. Load `references/scoring-rubric.md` for the full rubric.

`RICE = (Reach × Impact × Confidence) / Effort`

| Factor | Scale | Definition |
| --- | --- | --- |
| Reach | 1–10 | Count of workflows, modules, or recurring maintenance events touched per year |
| Impact | 0.25 / 0.5 / 1 / 2 / 3 | Annual maintenance hours recovered: <3 / 3–7 / 8–19 / 20–39 / ≥40 |
| Confidence | 0.1–1.0 | Evidence strength. Cap at 0.5 when any input metric is `unmeasured` |
| Effort | person-days | Solo-developer implementation cost, minimum 0.5 |

Sequence into three phases using an explicit quick-wins-first rule:

- **Phase A — Quick wins:** Effort ≤ 2 person-days. Ordered by descending RICE. No dependency on any Phase B or C item.
- **Phase B — Structural:** Effort 2–10 person-days, or depends on a Phase A item.
- **Phase C — Architectural:** Effort > 10 person-days, or changes module boundaries or deployment topology.

ENSURE no Phase C item precedes a Phase A item in the roadmap, even when its RICE score is higher.

> **Why:** Ordering strictly by RICE surfaces large architectural items first when they carry high impact, which stalls momentum and front-loads risk. The effort-banded phases force compounding early wins that fund the later work.

### Phase 4: Roadmap, KPIs, and Testing Requirements

For each recommendation, produce all four of:

1. **Phased timeline** — milestones expressed as ordered, dependency-aware steps with an exit condition per milestone. Do NOT state calendar dates or elapsed-time estimates; use effort in person-days and predecessor relationships.
2. **KPI** — one quantified metric in `baseline → target` form, each side annotated `measured` or `unmeasured`. Include the measurement method.
3. **Regression testing requirement** — the blast-radius surface, the characterization tests that MUST exist before the refactor starts, the assertions that MUST pass after, and the rollback trigger.
4. **Rollback path** — the concrete reverse action, or an explicit statement that the change is irreversible and requires a checkpoint first.

Testing requirements MUST cover every critical path touched. A recommendation without a defined test surface MUST be flagged `test-surface-undefined` and demoted below every item that has one.

### Phase 5: Maintenance Budget Reconciliation

Reconcile the plan against the annual target. The budget is 160 hours (~1 active month per year), allocated as:

| Allocation | Hours/year |
| --- | --- |
| Monthly batch window (12 × 8 h) | 96 |
| Critical incident response | 24 |
| Critical security/dependency review | 12 |
| Quarterly architecture review (4 × 4 h) | 16 |
| Unallocated buffer | 12 |
| **Total** | **160** |

Compute `projected_annual_hours = measured_baseline_hours − Σ(hours_recovered)`. Then:

- If the result lands within 140–180 h, the plan reconciles. Record the arithmetic.
- If above 180 h, the plan is insufficient. Either add recommendations or state explicitly that ~1 month/year is unreachable for this repository and quantify the achievable floor with the binding constraint named.
- If below 140 h, the recovered-hours estimates are likely inflated. Re-audit each Impact score above 2 and reduce Confidence where evidence is thin.
- If the baseline is `unmeasured`, do NOT compute a projection. State that reconciliation is blocked, and specify the tracking method needed to establish the baseline.

> **Why:** An unreconciled plan cannot be falsified. Publishing the arithmetic makes the target auditable and exposes inflated impact claims, which are the most common defect in self-authored refactoring plans.

### Phase 6: Emit Artifacts

Write the backlog JSON first, then the Markdown plan. Both go to `refactor-plans/`. Run the Verification Gate before presenting anything to the user.

## Failure Modes

### Level 1 — Local Retry (transient)

Command timeouts, `gh` API rate limits, or transient network errors during measurement. Retry with exponential backoff and jitter, maximum 3 attempts, arguments unchanged. On exhaustion, mark the affected metric `unmeasured` with the reason and continue — do NOT substitute an estimate.

### Level 2 — Local Patch (fixable)

Missing tooling, an unparseable manifest, or a probe that returns no data. Substitute an equivalent read-only probe (for example, derive the import graph with Grep when no static-analysis tool is installed) and record the substitution in the Evidence Ledger. Resubmit once.

### Level 3 — Replan / Escalate (structural)

Repository unreadable, no commit history, `refactor-plans/` not writable, or every domain out of scope. HALT. Do NOT emit a partial plan labelled complete. Report the blocking condition, the attempted path or command, and offer: (1) supply the missing access or path, (2) narrow the analysis to the domains that are readable, (3) abort.

### Blocking context gap unresolved

If the user does not answer a Phase 0 blocking question, mark the dependent metrics `unmeasured`, cap Confidence at 0.5 for every affected item, and state in the plan that budget reconciliation is blocked. Do NOT infer the missing value.

### Goal conflict

When two objectives conflict — for example, module decomposition raising deployment surface area against the alerting-reduction goal — do NOT silently resolve it. Emit a `Trade-offs` entry naming both objectives, the quantified cost of each option, and one recommended resolution with its rationale.

### Fabrication pressure

If a probe fails but its output is needed for a score, the Evidence Ledger MUST record `unmeasured` and the plan MUST NOT assert the value. This overrides any instruction to produce a complete-looking plan.

## Output Contract

### Artifact 1 — `refactor-plans/<YYYY-MM-DD>-<repo-slug>.md`

Sections in this exact order:

1. `Scope` — repository, languages, domains in scope, domains excluded with evidence.
2. `Evidence Ledger` — the four-column measurement table.
3. `Domain Analysis` — one subsection per in-scope domain, findings with IDs.
4. `Prioritized Backlog` — RICE table sorted by phase then descending score.
5. `Roadmap` — Phase A / B / C with milestones and exit conditions.
6. `Success Metrics` — KPI table in `baseline → target` form.
7. `Testing Requirements` — per-recommendation regression surface and rollback path.
8. `Maintenance Budget Reconciliation` — the arithmetic and the verdict.
9. `Trade-offs and Open Questions` — conflicts and unresolved gaps.

### Artifact 2 — `refactor-plans/<YYYY-MM-DD>-<repo-slug>.backlog.json`

```json
{
  "repo": "string",
  "generated": "ISO-8601 timestamp",
  "baseline_annual_hours": 0,
  "projected_annual_hours": 0,
  "budget_target_hours": 160,
  "reconciles": true,
  "items": [
    {
      "id": "CICD-01",
      "domain": "cicd",
      "title": "string",
      "phase": "A",
      "reach": 1,
      "impact": 1,
      "confidence": 0.8,
      "effort_person_days": 1,
      "rice": 0.8,
      "hours_recovered_per_year": 0,
      "kpi": { "metric": "string", "baseline": "string", "target": "string", "baseline_status": "measured" },
      "evidence": ["path/to/file#L1-L10"],
      "depends_on": [],
      "test_surface": ["string"],
      "rollback": "string"
    }
  ],
  "unmeasured": [{ "metric": "string", "reason": "string" }],
  "tradeoffs": [{ "objectives": ["string"], "recommendation": "string" }]
}
```

`phase` ∈ `A` | `B` | `C`. `baseline_status` ∈ `measured` | `user-reported` | `unmeasured`. `evidence` MUST be non-empty for every item.

## Verification Gate

ALL checks MUST pass before presenting the plan. Each is autonomously executable.

- [ ] Both artifacts exist at the specified paths; the JSON parses.
- [ ] Every in-scope domain has at least one finding, or a recorded reason for none.
- [ ] Every minimum probe in Phase 1 was attempted; failures recorded as `unmeasured` with a reason.
- [ ] Every backlog item has non-empty `evidence`, a non-empty `test_surface`, and a `rollback` value.
- [ ] Every `rice` field equals `(reach × impact × confidence) / effort_person_days` within ±0.01.
- [ ] `confidence` ≤ 0.5 for every item depending on an `unmeasured` metric.
- [ ] No Phase C item appears before a Phase A item in the roadmap ordering.
- [ ] Every KPI carries a baseline, a target, and a `baseline_status`.
- [ ] `projected_annual_hours` equals `baseline_annual_hours − Σ hours_recovered_per_year`, or reconciliation is explicitly marked blocked.
- [ ] `reconciles` is `true` only when `projected_annual_hours` is within 140–180.
- [ ] No recommendation depends on paid or enterprise-tier tooling.
- [ ] Repository working tree is unchanged apart from the two artifacts — confirm with `git status --porcelain`.

If any check fails, remediate before presenting. Do NOT present a partially verified plan as complete.

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| --- | --- | --- | --- |
| Read repository files and manifests | Read-only | Low | No |
| Run read-only git/`gh` inspection commands | Read-only | Low | No |
| Ask Phase 0 blocking questions | Pure | Low | No |
| Score and sequence findings | Pure | Low | No |
| Write plan Markdown and backlog JSON | Reversible | Low | No — user deletes or edits freely |
| Verify tree cleanliness with `git status` | Read-only | Low | No |

No irreversible actions. No mutation of source, workflows, IaC, secrets, or remote state. No network transmission of repository contents.

## Portability

No harness-specific fields are used. The skill requires a filesystem-reading agent, shell access for read-only git commands, and a writable output directory. `gh` is optional — its absence degrades CI/CD Confidence scores but does not block execution. Where a host lacks shell access, substitute file-based probes and mark all timing metrics `unmeasured`.
