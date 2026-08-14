# LSTR MCP Tool Argument Reference (L3)

> On-demand reference for the exact `run_mcp` invocation schema of all 7 LSTR MCP servers.
> Load this file only when the agent needs the full required-arg contract per tool.

## Invocation Map (`run_mcp` → this runtime)

| `server_name` | `tool_name` | Required args (per schema) |
| --- | --- | --- |
| `mcp_metacognitive-monitoring` | `metacognitiveMonitoring` | `task`, `stage`, `overallConfidence`, `uncertaintyAreas`, `recommendedApproach`, `monitoringId`, `iteration`, `nextAssessmentNeeded` |
| `mcp_sequential-thinking` | `sequentialthinking` | `thought`, `nextThoughtNeeded`, `thoughtNumber`, `totalThoughts` |
| `mcp_collaborative-reasoning` | `collaborativeReasoning` | `topic`, `personas`, `contributions`, `stage`, `activePersonaId`, `sessionId`, `iteration`, `nextContributionNeeded` |
| `mcp_scientific-method` | `scientificMethod` | `stage`, `inquiryId`, `iteration`, `nextStageNeeded` |
| `mcp_constraint-solver` | `constraintSolver` | `variables` (object of numbers), `constraints` (array of boolean-expression strings) |
| `mcp_narrative-planner` | `narrativePlanner` | `premise`, `characters` (array), `arcs` (array) |
| `mcp_structured-argumentation` | `structuredArgumentation` | `claim`, `premises`, `conclusion`, `argumentType`, `confidence`, `nextArgumentNeeded` |

## Per-Tool Detail

### 1. metacognitiveMonitoring

- `stage` enum: `knowledge-assessment`, `planning`, `execution`, `monitoring`, `evaluation`, `reflection`.
- `knowledgeAssessment` (optional object): `domain`, `knowledgeLevel`
  (expert/proficient/familiar/basic/minimal/none), `confidenceScore` (0–1),
  `supportingEvidence`, `knownLimitations`, `relevantTrainingCutoff`.
- `claims` (optional array): each `{claim, status(fact|inference|speculation|uncertain),
  confidenceScore, evidenceBasis, alternativeInterpretations, falsifiabilityCriteria}`.
- `reasoningSteps` (optional array): each `{step, potentialBiases, assumptions, logicalValidity,
  inferenceStrength}`.
- Required: `task`, `stage`, `overallConfidence`, `uncertaintyAreas`, `recommendedApproach`,
  `monitoringId`, `iteration`, `nextAssessmentNeeded`.

### 2. sequentialthinking

- Required: `thought`, `nextThoughtNeeded`, `thoughtNumber`, `totalThoughts`.
- Optional: `isRevision`, `revisesThought`, `branchFromThought`, `branchId`, `needsMoreThoughts`.
- Terminate when `nextThoughtNeeded:false` with a single final answer.

### 3. collaborativeReasoning

- `stage` enum: `problem-definition`, `ideation`, `critique`, `integration`, `decision`, `reflection`.
- `personas[]`: each requires `id`, `name`, `expertise[]`, `background`, `perspective`, `biases[]`,
  `communication{style, tone}`.
- `contributions[]`: each requires `personaId`, `content`, `type`
  (observation/question/insight/concern/suggestion/challenge/synthesis), `confidence`.
- Required: `topic`, `personas`, `contributions`, `stage`, `activePersonaId`, `sessionId`,
  `iteration`, `nextContributionNeeded`.

### 4. scientificMethod

- `stage` enum: `observation`, `question`, `hypothesis`, `experiment`, `analysis`, `conclusion`,
  `iteration`.
- `hypothesis` (optional object): `statement`, `variables[]`, `assumptions[]`, `hypothesisId`,
  `confidence`, `domain`, `iteration`, `status(proposed/testing/supported/refuted/refined)`.
- `experiment` (optional object): `design`, `methodology`, `predictions[]`, `experimentId`,
  `hypothesisId`, `controlMeasures[]`.
- Required: `stage`, `inquiryId`, `iteration`, `nextStageNeeded`.

### 5. constraintSolver

- `variables`: object mapping name → **number**.
- `constraints`: array of **single** boolean-expression strings; allowed charset
  `A-Za-z0-9_ \s<>=!()+*/.%|&^`. Use `&`/`|` (not `&&`/`||`), no commas.
- Required: `variables`, `constraints` (minItems 1).

### 6. narrativePlanner

- Required: `premise` (minLength 1), `characters` (array, minItems 1), `arcs` (array, minItems 1).
- Three-act story tool; repurposed by the framework for output structuring.

### 7. structuredArgumentation

- `argumentType` enum: `thesis`, `antithesis`, `synthesis`, `objection`, `rebuttal`.
- Optional linkage: `argumentId`, `respondsTo`, `supports[]`, `contradicts[]`,
  `strengths[]`, `weaknesses[]`, `suggestedNextTypes[]`.
- Required: `claim`, `premises`, `conclusion`, `argumentType`, `confidence`, `nextArgumentNeeded`.
