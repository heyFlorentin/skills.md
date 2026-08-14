# Business Use Case Rubric (L3 Reference)

Load this reference only when scoring findings for commercial potential. Keep it out of the L2
SKILL.md body to preserve context budget.

## Scoring a Business Use Case Finding

Rate each finding on four axes (0–3 each), then sum to a 0–12 score.

| Axis | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Strategic fit | No mapping to Florentin One products | Adjacent, requires new product | Extends an existing product/MCP server | Directly fills a named product gap |
| Market pull | No evidence of demand | Speculative demand | Documented niche demand | Documented broad or German-market demand |
| Effort to exploit | Architectural (10+ person-days) | Structural (2–10) | Quick win (< 2) | Zero-build (adopt/config only) |
| Risk | Blocking GDPR/EU AI Act risk | Material compliance risk | Minor risk, mitigable | No material risk |

## Contextualization Checklist

Every finding MUST answer:

- [ ] Which Florentin One product / MCP server / skill does this extend or complement?
- [ ] What GDPR Art. 28 or EU AI Act obligation does it trigger, if any?
- [ ] Is it operable by a solo developer on free/hobby tiers?
- [ ] What is the single first next action to validate it?

## Confidence Rules

- A finding backed only by `unmeasured` inputs MUST cap its confidence at 0.5.
- A finding with no traceability reference MUST NOT be scored — mark it `unreviewable` or
  `fabrication-risk` and exclude it from the opportunity map.

## Non-Fabrication Hard Rules

- Do NOT invent demand figures, market sizes, or adoption numbers.
- Do NOT claim a capability exists in a resource unless a read/URL proves it.
- Do NOT recommend enterprise-only or paid-tier tooling.
