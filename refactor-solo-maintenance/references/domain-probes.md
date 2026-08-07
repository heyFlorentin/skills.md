# Domain Probes — Full Reference

> **L3 reference for `refactor-solo-maintenance`.** Loaded on demand during Phase 1 when the minimum probe set is insufficient or a substitute probe is needed. NOT required for a standard run.

Every probe below is read-only. Do NOT run any command that writes, commits, pushes, or deploys.

## Domain 1 — Codebase Architecture

| Probe | Method | Yields |
| --- | --- | --- |
| Directory topology | `Glob` on `**/*` scoped to source roots | Module boundaries, nesting depth |
| Largest files | `find`-free: list source files, sort by line count | Refactor candidates, god-objects |
| Cross-module imports | `Grep` for import/require/use statements, group by source and target module | Coupling density, cycle candidates |
| Duplicate code hotspots | `Grep` for repeated function signatures and literal blocks; check for existing `jscpd`/`ruff`/`clippy` config | Shared-utility extraction targets |
| Type coverage | Presence and strictness of `tsconfig.json` (`strict`, `noImplicitAny`), `mypy.ini`, type annotation density | AI-parseability baseline |
| Error handling | `Grep` for `catch`, `except`, `Result`, `panic`, `console.error`, bare re-throws | Fragmentation count, silent-failure sites |
| Logging | `Grep` for logger imports and raw `print`/`console.log` | Structured-logging gap |
| Public API surface | Exported symbols per module | Blast radius per module change |

Coupling heuristic: a module importing from more than 3 sibling modules is a decomposition candidate. Record the count, not a verdict.

## Domain 2 — GitHub Actions CI/CD

| Probe | Method | Yields |
| --- | --- | --- |
| Workflow inventory | `Glob` `.github/workflows/*.{yml,yaml}` | Pipeline count |
| Job graph | Read each workflow, map `needs:` edges | Serial chains that could parallelize |
| Matrix usage | `Grep` for `strategy:`/`matrix:` | Existing fan-out |
| Wall-clock duration | `gh run list --limit 10 --json databaseId,workflowName,createdAt,updatedAt,conclusion` | Baseline pipeline time |
| Per-job timing | `gh run view <id> --json jobs` | Critical path, longest job |
| Cache usage | `Grep` for `actions/cache`, `cache:` in setup actions | Cold-install waste |
| Action pinning | `Grep` for `uses:` and inspect ref format | Supply-chain and drift exposure |
| Dependabot | Read `.github/dependabot.yml` | Update automation baseline |
| Auto-merge | `Grep` for `gh pr merge --auto`, `dependabot` automerge workflows | Manual review load |
| Deploy strategy | `Grep` for `environment:`, canary/blue-green/rollback steps | Deployment risk baseline |
| Concurrency | `Grep` for `concurrency:` | Wasted duplicate runs |

Critical path: the longest `needs:` chain by summed job duration. Parallelization potential is total job time minus critical path time. Report both.

If `gh` is unavailable or unauthenticated, mark every timing metric `unmeasured`, state the reason, and cap CI/CD item Confidence at 0.5.

## Domain 3 — AI-Agent Integration

| Probe | Method | Yields |
| --- | --- | --- |
| Agent rules | `Glob` `.trae/rules/*`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*` | Always-loaded context footprint |
| Rule size | Line and approximate token count per file | Context budget consumption |
| Skills inventory | `Glob` `*/SKILL.md` | Existing delegation coverage |
| Skill body size | Line count per SKILL.md against the 500-line limit | Progressive-disclosure violations |
| L3 gating | Presence of `references/` and on-demand load instructions | Wasted always-on context |
| Prompt reuse | `Grep` for prompt/template directories | Prompt-library gap |
| Test generation | Test file count vs source file count; CI test job presence | AI-test-audit baseline |
| Knowledge base | Location of docs/ADRs; whether version-controlled | Consistency-of-execution baseline |
| MCP config | Read `.trae/mcp.json` or equivalent | Tool availability for agent workflows |

Always-loaded context footprint is the sum of agent rules plus every skill description. Report it in approximate tokens. A footprint above ~2,000 tokens before any task begins is a reduction candidate.

## Domain 4 — Maintenance Cadence

| Probe | Method | Yields |
| --- | --- | --- |
| Commit cadence | `git log --since='12 months ago' --date=format:'%Y-%m' --pretty=%ad` grouped by month | Activity distribution, batching feasibility |
| Hotspot churn | `git log --since='12 months ago' --name-only --pretty=format:` frequency count | Files driving repeat maintenance |
| Issue cadence | `gh issue list --state all --limit 100 --json createdAt,labels` | Incident and routine-task volume |
| Alert surfaces | `Grep` for webhook/notification config, monitoring SDK imports | Noise inventory |
| IaC inventory | `Glob` Terraform/Pulumi/CDK/Compose/Dockerfile/k8s manifests | Self-managed vs managed ratio |
| Server-managed resources | `Grep` IaC for VM/instance/node-group/autoscaling resources | Patch and upkeep burden |
| Runbooks | `Glob` `**/runbook*`, `**/RUNBOOK*`, `docs/ops/**` | Automation candidates |
| Scheduled jobs | `Grep` for `schedule:`/`cron:` in workflows | Existing unattended automation |

Self-managed ratio: count of IaC resources requiring OS/runtime patching divided by total compute resources. Every self-managed compute resource is a recurring maintenance line item — quantify its hours from the user-reported baseline, do NOT assume an industry figure.

## Substitute Probes

When the primary method is unavailable, use these and record the substitution in the Evidence Ledger.

| Unavailable | Substitute | Confidence impact |
| --- | --- | --- |
| `gh` CLI | Workflow YAML structural analysis only | Cap at 0.5 |
| Static analysis tool | `Grep` pattern counting | Cap at 0.7 |
| Coverage report | Test-file-to-source-file ratio | Cap at 0.6 |
| Issue tracker access | `git log` message classification | Cap at 0.5 |
| User maintenance baseline | None — reconciliation blocked | Do NOT project |
