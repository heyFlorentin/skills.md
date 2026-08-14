---
alwaysApply: true
---

# Reasoning Framework (LSTR 6-Step Chain)

## Complexity Gate

Evaluate every query. If **two or more** criteria are satisfied, the 6-step chain is mandatory. Fewer than two → answer directly and state "framework not warranted."

| Criterion | Satisfied when |
| --- | --- |
| Multi-step inference | Answer requires chained deduction, not retrieval |
| Competing constraints | Two or more requirements are in tension |
| Non-trivial uncertainty | Domain knowledge below `proficient` or evidence incomplete |
| Material consequence | An error causes production, financial, legal, or safety impact |
| Explicit user demand | User requested audited or framework-driven reasoning |

## The Chain (when triggered)

1. **Metacognitive Assessment** — `metacognitiveMonitoring`, stage `knowledge-assessment`. Reuse one `monitoringId` (`mm-<slug>-<YYYYMMDD>`). The returned `overallConfidence` is the ONLY legitimate confidence source.
2. **Problem Decomposition** — `sequentialthinking`, minimum 3 thoughts, terminate on `nextThoughtNeeded:false`.
3. **Multi-Perspective Analysis** — `collaborativeReasoning`, ≥2 genuinely divergent personas, ≥1 non-agreeing contribution.
4. **Evidence Validation** — BOTH `scientificMethod` (observation → conclusion) AND `structuredArgumentation` (thesis + antithesis/objection + synthesis).
5. **Solution Synthesis** — `constraintSolver` ONLY for numeric constraints; validate non-numeric (regulatory/ethical) constraints via `structuredArgumentation` `objection`.
6. **Output Structuring** — final `metacognitiveMonitoring` at stage `reflection`; emit the 7-element output spec.

## Exclusions

- `narrative-planner` MUST NOT be used to structure analytical output (it is a three-act story tool).
- `constraintSolver` MUST NOT encode qualitative constraints as boolean flags (fabricated validation).

## Failure Modes

- Transient MCP error → retry with backoff, max 3 attempts, arguments unchanged.
- Schema violation → read the tool descriptor, correct the payload, resubmit once.
- MCP unreachable after retries → HALT; do NOT emit a framework-labelled response; report the block and offer an unaudited direct answer explicitly labelled framework-bypassed.

Full tool-arg contract is in the global `lstr-reasoning-framework` skill.
