---
name: lstr-reasoning-framework
description: >
  Mandates the LSTR 6-step reasoning framework and drives all 7 LSTR MCP reasoning servers —
  metacognitive monitoring, sequential thinking, collaborative reasoning, scientific method,
  constraint solver, narrative planner, structured argumentation — via run_mcp. Activate on any
  complex, multi-step, or high-stakes request: analysis, planning, decision-making, diagnosis,
  hypothesis testing, argument evaluation, or output structuring. User vocabulary: "use LSTR",
  "run the reasoning framework", "apply metacognitive monitoring", "sequential thinking",
  "collaborative reasoning", "scientific method", "constraint solver", "structured argumentation",
  "narrative planner". Do NOT use for trivial single-step factual answers, one-line code edits,
  or small talk.
version: 0.1.0
allowed-tools: Read, WebSearch, WebFetch, run_mcp
---

# lstr-reasoning-framework

Encode and maximize the use of the 7 LSTR MCP reasoning servers by mandating the 6-step
reasoning pipeline and supplying the exact `run_mcp` invocation map.

## When to Use

- Any complex, multi-step, or high-stakes request requiring structured reasoning.
- Analysis, planning, decision-making, diagnosis, hypothesis testing, argument evaluation, or
  output structuring.
- Requests where the user explicitly names LSTR reasoning tools or the framework
  (see User Vocabulary in the description).
- Requests that would benefit from calibrated confidence, multi-perspective analysis, or
  constraint validation before producing a final answer.

## When NOT to Use

- Trivial single-step factual answers, one-line code edits, simple file reads, or small talk.
- Any task that does not require reasoning across multiple perspectives or evidence validation.
- Non-LSTR MCP tools. The Cloudflare `mcp_plugin_Cloudflare_cloudflare-api` server
  (`docs`/`search`/`execute`) is EXCLUDED from scope. Do NOT route it through this skill.

## Prerequisites

1. `run_mcp` gateway available in the runtime (this runtime's MCP invocation surface).
2. The 7 `mcp_*` servers present in the runtime MCP registry:
   `mcp_metacognitive-monitoring`, `mcp_sequential-thinking`, `mcp_collaborative-reasoning`,
   `mcp_scientific-method`, `mcp_constraint-solver`, `mcp_narrative-planner`,
   `mcp_structured-argumentation`.
3. Portable alternatives for other harnesses (documented in "## Harness Notes"): install via
   `bunx @florentin-one/mcp-<server>@latest` or point the client at
   `https://<server>.lstr.workers.dev` (or `https://https://mcp.lstr.one/mcp/<server>`).

## Workflow

MUST execute the 6 steps in order. Do NOT skip a step. Re-assess only when the domain, task
complexity, or confidence level changes (Step 1 governs).

### Step 1: Metacognitive Assessment

Run FIRST, before any analysis. Evaluate knowledge boundaries, classify claims
(fact / inference / speculation / uncertain), and calibrate confidence.

```json
run_mcp(
  server_name = "mcp_metacognitive-monitoring",
  tool_name   = "metacognitiveMonitoring",
  args = {
    "task": "<task description>",
    "stage": "knowledge-assessment",
    "overallConfidence": 0.0,
    "uncertaintyAreas": ["<area>"],
    "recommendedApproach": "<approach>",
    "monitoringId": "<unique-id>",
    "iteration": 0,
    "nextAssessmentNeeded": true
  }
)
```

> **Why:** Mandatory first-step self-monitoring establishes calibrated confidence and surfaces
> reasoning biases before any downstream step, preventing overconfident or unfounded output.

### Step 2: Problem Decomposition

Break the problem into discrete logical sub-tasks. Loop `sequentialthinking` until
`nextThoughtNeeded:false`; a single final answer MUST close the chain.

```json
run_mcp(
  server_name = "mcp_sequential-thinking",
  tool_name   = "sequentialthinking",
  args = {
    "thought": "<current step>",
    "nextThoughtNeeded": true,
    "thoughtNumber": 1,
    "totalThoughts": 5
  }
)
```

> **Why:** Sequential decomposition filters irrelevant information and yields a verified solution
> hypothesis with a single correct answer.

### Step 3: Multi-Perspective Analysis

Simulate diverse expert personas. Use at least two personas with distinct expertise and biases.

```json
run_mcp(
  server_name = "mcp_collaborative-reasoning",
  tool_name   = "collaborativeReasoning",
  args = {
    "topic": "<problem>",
    "personas": [{"id": "p1", "name": "<name>", "expertise": ["<area>"], "background": "<bg>",
                  "perspective": "<view>", "biases": ["<bias>"],
                  "communication": {"style": "direct", "tone": "neutral"}}],
    "contributions": [{"personaId": "p1", "content": "<contribution>", "type": "observation",
                        "confidence": 0.8}],
    "stage": "problem-definition",
    "activePersonaId": "p1",
    "sessionId": "<unique-id>",
    "iteration": 0,
    "nextContributionNeeded": true
  }
)
```

> **Why:** Multi-persona collaboration surfaces value trade-offs and reduces single-perspective
> bias before committing to a recommendation.

### Step 4: Evidence Validation

Test hypotheses and validate logical premises. Run `scientificMethod` for hypothesis testing and
`structuredArgumentation` for dialectical thesis/antithesis/synthesis.

```json
run_mcp(
  server_name = "mcp_scientific-method",
  tool_name   = "scientificMethod",
  args = {
    "stage": "hypothesis",
    "inquiryId": "<unique-id>",
    "iteration": 0,
    "nextStageNeeded": true
  }
)
```

```json
run_mcp(
  server_name = "mcp_structured-argumentation",
  tool_name   = "structuredArgumentation",
  args = {
    "claim": "<proposition>",
    "premises": ["<premise>"],
    "conclusion": "<consequence>",
    "argumentType": "thesis",
    "confidence": 0.8,
    "nextArgumentNeeded": true
  }
)
```

> **Why:** Formal scientific reasoning avoids confirmation bias; dialectical argumentation forces
> competing claims to be evaluated and integrated rather than asserted.

### Step 5: Solution Synthesis

Validate the synthesized solution against all known constraints. NOTE the schema: `variables`
MUST be numeric, and each `constraints` entry MUST be a single boolean-expression string using only
`A-Za-z0-9_ \s<>=!()+*/.%|&^` — do NOT use `&&`/`||` or commas; use `&`/`|` for logical operators.

```json
run_mcp(
  server_name = "mcp_constraint-solver",
  tool_name   = "constraintSolver",
  args = {
    "variables": {"v1": 1, "v2": 2},
    "constraints": ["v1 >= 0", "v2 > v1"]
  }
)
```

> **Why:** Constraint validation rejects solutions that violate regulatory, technical, or ethical
> bounds before the answer is emitted.

### Step 6: Output Structuring

Organize the final response. `narrativePlanner` is a three-act story tool; the framework repurposes
it for output structuring (premise = the core message; characters = stakeholders/entities;
arcs = section progression). Do NOT over-claim its story-generation scope.

```json
run_mcp(
  server_name = "mcp_narrative-planner",
  tool_name   = "narrativePlanner",
  args = {
    "premise": "<core message>",
    "characters": ["<stakeholder>"],
    "arcs": ["<section>"]
  }
)
```

> **Why:** A narrative structure enforces a laconic, ordered, and complete final answer.

## Failure Modes

| Mode | Escalation | Recovery |
| --- | --- | --- |
| Transient failure (timeout, rate limit) | L1 Local Retry | Exponential backoff with jitter. Max 3 retries. |
| Schema violation (e.g., non-numeric `constraintSolver` variable; missing required arg) | L2 Local Patch | Repair the args without changing the plan. Re-issue the call. |
| Server missing from registry / unknown `server_name` | L3 Replan/Escalate | Halt execution. Report diagnostic context to the user. Do NOT loop. |

> **Why:** Bounded escalation prevents unbounded retry loops ("retry storms"), the dominant
> production failure mode (Meta-Study Principle 5).

## Output Contract

The skill produces a reasoning trace plus the final answer. The final response MUST include:

1. **Reasoning transparency** — which `run_mcp` servers were used and the key insight gained from each.
2. **Calibrated confidence score** (0.0–1.0) for the primary conclusion.
3. **At least one multi-perspective insight** derived from Step 3 or Step 4.
4. **Technical precision** — domain-appropriate terminology (throughput, latency, SLA, root cause,
   idempotency, etc.).
5. **Regulatory reference** — GDPR / EU AI Act / German business culture where applicable.
6. **Edge-case analysis** — at least one failure mode or boundary condition addressed.

## Verification Gate

Before declaring the task complete, ALL of the following MUST be true:

- [ ] Every `run_mcp` call in the 6 steps returned successfully (no error response).
- [ ] All 6 steps were invoked; none skipped.
- [ ] Step 2 ended with `nextThoughtNeeded:false`.
- [ ] Final answer includes a calibrated confidence score and a reasoning-transparency note.
- [ ] At least one multi-perspective insight present.
- [ ] No non-LSTR MCP server was invoked.

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| --- | --- | --- | --- |
| Invoke `metacognitiveMonitoring` | Read-only | Low | No |
| Invoke `sequentialthinking` | Read-only | Low | No |
| Invoke `collaborativeReasoning` | Read-only | Low | No |
| Invoke `scientificMethod` | Read-only | Low | No |
| Invoke `structuredArgumentation` | Read-only | Low | No |
| Invoke `constraintSolver` | Pure | Low | No |
| Invoke `narrativePlanner` | Pure | Low | No |

All actions are Read-only or Pure — they do not mutate external state. No Irreversible actions;
no human approval required.

## Harness Notes

- **This runtime:** invoke via `run_mcp` with the `mcp_*` `server_name` values above.
- **Claude Desktop / Cursor (portable):** use `bunx @florentin-one/mcp-<server>@latest` as the
  `command`/`args`, or point the client at `https://<server>.lstr.workers.dev`.
- **Worker endpoints:** `https://https://mcp.lstr.one/mcp/<server>` (Cloudflare Workers, global edge).
- **Frontmatter** keeps only `name`/`description`/`version`/`allowed-tools` for portability across
  agentskills.io-compliant runtimes.
