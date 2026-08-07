# RICE Scoring, KPI, and Testing Rubric — Full Reference

> **L3 reference for `refactor-solo-maintenance`.** Loaded on demand during Phase 3 and Phase 4 when a score, KPI, or test surface needs calibration. NOT required for a standard run.

## RICE Formula

```
RICE = (Reach × Impact × Confidence) / Effort_person_days
```

Report every score to two decimals. Show the four inputs alongside the result so the arithmetic is auditable.

## Reach (1–10)

Count of distinct things touched per year — workflows, modules, or recurring maintenance events.

| Score | Criterion |
| --- | --- |
| 1 | One module or one workflow, touched rarely |
| 3 | A few modules, or one workflow running weekly |
| 5 | Most modules, or every CI run |
| 8 | Every module and every CI run |
| 10 | Every module, every run, plus every incident response path |

Reach is a count, not an importance rating. Do NOT inflate it to express enthusiasm.

## Impact (annual maintenance hours recovered)

| Score | Hours recovered/year |
| --- | --- |
| 0.25 | < 3 |
| 0.5 | 3 – 7 |
| 1 | 8 – 19 |
| 2 | 20 – 39 |
| 3 | ≥ 40 |

Every Impact score MUST be justified by a stated derivation: `frequency × time_per_occurrence × reduction_fraction`. An Impact of 3 without a derivation is a fabrication.

## Confidence (0.1–1.0)

| Score | Evidence basis |
| --- | --- |
| 1.0 | Directly measured baseline; the mechanism is deterministic |
| 0.8 | Measured baseline; the mechanism depends on tooling behaving as documented |
| 0.6 | Partially measured; the reduction fraction is inferred from the mechanism |
| 0.5 | **Hard cap** when any input metric is `unmeasured` |
| 0.3 | Mechanism plausible, baseline user-reported without tracking data |
| 0.1 | Speculative — do NOT include in Phase A |

The 0.5 cap is absolute. Confidence MUST NOT exceed it for any item whose Reach, Impact, or baseline draws on an `unmeasured` metric.

## Effort (person-days, solo)

Include implementation, characterization tests, verification, and documentation. Minimum 0.5. Do NOT count learning time for tooling already in use, and DO count it for tooling being introduced.

| Band | Phase |
| --- | --- |
| ≤ 2 person-days | A — Quick win |
| 2 – 10 person-days | B — Structural |
| > 10 person-days, or changes module boundaries / deployment topology | C — Architectural |

An item depending on a higher-phase item inherits that phase.

## KPI Construction

Every KPI is one line: `metric: baseline (status) → target (method)`.

Valid:

```
Pipeline wall-clock p50: 19m 40s (measured, gh run list n=10) → ≤ 9m 50s (same command, n=10 post-change)
Dependabot PRs requiring manual action: 14 of 16 (measured, gh pr list) → ≤ 3 of 16 (same query, trailing 90d)
```

Invalid — do NOT emit these:

```
Pipeline time reduced by 50%            (no baseline, no method)
AI agents resolve 82% of routine issues (invented precision, no baseline)
Improved maintainability                 (unquantified)
```

When the baseline is `unmeasured`, express the target as a relative reduction and name the tracking mechanism that must be installed first. That tracking installation becomes its own Phase A backlog item.

## Percentage Target Justification

The four headline targets are hypotheses requiring per-repository derivation, not defaults.

| Target | Required derivation |
| --- | --- |
| 50% pipeline reduction | Critical-path analysis showing parallelizable job time ≥ 50% of current wall clock |
| 80% routine issue resolution | Classification of trailing-12-month issues into routine vs novel, with the routine share ≥ 80% |
| 70% task automation | Inventory of recurring task types with an automatable share ≥ 70% |
| 60% runbook time reduction | Per-runbook step count with the share of mechanically automatable steps ≥ 60% |

If the derivation does not support the headline figure, state the supported figure instead. Do NOT restate the headline target as an achieved result.

## Testing Requirements Template

Every recommendation carries all four fields.

```
Blast radius:   <modules, workflows, endpoints, or infrastructure touched>
Pre-conditions: <characterization tests that MUST exist and pass BEFORE the change>
Post-assertions:<assertions that MUST pass after; include the exact command>
Rollback:       <concrete reverse action, or "irreversible — checkpoint required: <checkpoint>">
```

Per-domain minimum test surfaces:

| Domain | Minimum coverage |
| --- | --- |
| Architecture | Characterization tests on every public API of each module being moved; import-cycle check; build passes |
| CI/CD | Full pipeline green on a throwaway branch; deliberate-failure run proving rollback fires; timing re-measured |
| AI-agent | Activation test per skill or rule; a golden-output check on one representative task; context footprint re-measured |
| Maintenance | Alert-firing test for each retained critical signal; a silence test proving demoted alerts no longer page; runbook automation dry-run |

Any recommendation touching authentication, authorization, secrets, data deletion, or production deployment MUST additionally state what could NOT be verified pre-merge and how it will be observed post-merge.

## Reconciliation Arithmetic

Publish the table, then the verdict.

```
baseline_annual_hours        = <measured or user-reported>
Σ hours_recovered_per_year   = <sum across all items>
projected_annual_hours       = baseline − Σ recovered
budget_target_hours          = 160
verdict                      = reconciles | insufficient | inflated | blocked
```

| Verdict | Condition | Required action |
| --- | --- | --- |
| `reconciles` | 140 ≤ projected ≤ 180 | Record the arithmetic |
| `insufficient` | projected > 180 | Add items, or name the binding constraint and the achievable floor |
| `inflated` | projected < 140 | Re-audit every Impact ≥ 2 and reduce thin-evidence Confidence |
| `blocked` | baseline is `unmeasured` | Do NOT project; specify the tracking method needed |
