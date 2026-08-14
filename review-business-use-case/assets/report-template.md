# Business Use Case Report Template

Copy this skeleton into `business-use-case-reports/<ISO-8601>-<slug>.md`. Replace bracketed
placeholders with review output. Do NOT present a report that omits a section.

```markdown
# Business Use Case Review: <slug>

Generated: <ISO-8601 timestamp>
Invoker: LSTR by Florentin One (Hannover, Germany)

## 1. Executive Summary

<verdict in ≤ 5 sentences>

## 2. Resource Inventory

| Path | Type | Status | Reviewed |
|---|---|---|---|
| <path-or-url> | file / directory / url | readable / unreviewable | yes / no |

## 3. Business Use Case Analysis

### Finding: <title>

- **Resource:** <traceability reference: path#L or URL>
- **What it is:** <description>
- **Potential use case:** <claim, grounded in the reference>

## 4. Contextualized Opportunity Map

| Finding | Florentin One product / MCP server / skill | GDPR / EU AI Act flag |
|---|---|---|
| <finding> | <mapping> | <flag or none> |

## 5. Risks & Gaps

- <compliance / technical / maintenance risk>
- <unmeasured values stated as `unmeasured` with reason>

## 6. Confidence Calibration

- **Score:** <0.0–1.0, from metacognitiveMonitoring.overallConfidence>
- **Rationale:** <factors raising or lowering confidence>

## Usability Consultation

| # | Recommendation | Effort/Impact | First next action |
|---|---|---|---|
| 1 | <highest priority, solo-operable, free/hobby tier> | Quick win / Structural / Architectural | <single action> |
```

## Rules

- Every finding in section 3 MUST carry a non-empty traceability reference.
- Section 5 MUST state unmeasured values as `unmeasured`, never as estimates presented as fact.
- The top recommendation in the consultation MUST be operable by a solo developer on free or
  hobby tiers.
