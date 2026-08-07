---
name: create-skill
description: Use when the user wants to create, design, or generate a new AI agent skill (SKILL.md) from a problem description. This skill autonomously elicits the real problem, decomposes it, designs the skill architecture, and generates a production-grade SKILL.md that is goal-oriented, efficient, reliable, and scalable. Triggered by phrases like "create a skill for...", "design a SKILL.md that...", "I need an agent skill that...", "turn this problem into a skill", "build a skill to...", "generate a skill...". Do NOT use for editing existing skills, reviewing skills, or generating non-skill artifacts.
version: 0.1.0
allowed-tools: Read, Write, WebSearch, WebFetch
---

# create-skill — The Meta-Skill for Autonomous SKILL.md Generation

## When to Use

- The user describes a task, workflow, or problem they want an AI agent to handle reliably.
- The user asks for a skill, SKILL.md, or agent capability to be created from a description.
- The user wants to encode domain knowledge, team conventions, or procedural expertise into a reusable agent skill.

## When NOT to Use

- The user is editing, reviewing, or debugging an existing SKILL.md — this skill generates new skills, it does not modify existing ones.
- The user wants a non-skill artifact (a report, a script, a document, a presentation) — this skill only produces SKILL.md files and their scaffold.
- The user has already fully specified the skill and just needs formatting — this skill does elicitation and architecture, not just syntax.

## Prerequisites

- A workspace where files can be written (local directory or skills.md runtime).
- The user must be available to answer up to 2 clarifying questions (Phase 0).

## Workflow: The 5-Phase Autonomous Pipeline

This skill executes a strict 5-phase pipeline. No phase may be skipped. Each phase gates the next.

---

### Phase 0: Problem Elicitation (Self-Discovery)

The invoker may not articulate their real problem. Your first job is to discover it. The surface request ("build a skill for code review") often masks the real need ("stop junior devs from merging without tests").

**Step 0.1 — Read and infer.** Parse the user's initial description. Identify:

- What they *said* (surface request)
- What they *meant* (inferred need — the real outcome they want)

**Step 0.2 — Ask exactly 2 clarifying questions.** No more, no less. Use these exact templates:

> **Q1:** "What specific outcome does this skill need to produce? Describe the artifact or state change that means 'done.'"
>
> **Q2:** "What must the skill NEVER do? What's the worst possible wrong output or action?"

ENSURE both questions are answered before proceeding. If the user answers only one, re-ask the unanswered one.

**Step 0.3 — Summarize the elicitation.** Echo back to the user in this exact format:

> "I understand the problem as: [concise 2-sentence synthesis of the real need].
>
> The skill will: [1-2 sentence description of the outcome it produces].
>
> It will never: [1 sentence capturing the worst-case constraint from Q2].
>
> Proceeding."

DO NOT proceed past Phase 0 until Step 0.3 is complete and the user confirms the summary.

> **Why Phase 0 exists:** Single-task scoping demands outcome-first definition. The negative constraint question (Q2) surfaces the failure boundary before any design work begins — this prevents scope creep by anchoring the design in what must NOT happen. Two questions max prevents analysis paralysis while capturing the essential axis: goal + anti-goal.

---

### Phase 1: Skill Architecture Design

Based on the elicited problem, produce an internal architecture before writing any SKILL.md content. This phase produces no user-visible output — it builds the design that Phase 2 will render.

**Step 1.1 — Classify the skill type.** Choose exactly one:

| Type | Definition | Example |
| ------ | ----------- | --------- |
| `capability-uplift` | Teaches the agent something it cannot do natively — a new tool, protocol, domain procedure | A skill that integrates with a specific API, file format, or database |
| `preference-encoding` | Encodes existing capabilities into a specific workflow, convention, or quality bar | A skill that enforces code review checklist, deployment gates, or style conventions |
| `hybrid` | Mix of both — flag as requiring extra validation in Phase 3 | A skill that both uses a new tool AND enforces a specific workflow around it |

**Step 1.2 — Define the output contract.** Answer these three questions:

1. **Artifact:** What concrete thing does the skill produce? (file, report, code change, decision, record, etc.)
2. **Success criterion:** What objectively signals "done"? (test passes, human approves, schema validates, file exists with correct content, etc.)
3. **Format/Schema:** What structure must the output satisfy? (JSON with specific keys, Markdown with specific sections, code that passes linting, etc.)

**Step 1.3 — Classify every action the skill will perform.** Complete this table internally:

| Action | Type | Blast Radius | Human Approval? |
|--------|------|-------------|------------------|
| [action description] | Read-only / Pure / Reversible / Compensatable / Irreversible | Low / Medium / High | Yes / No |

*Action type definitions:*

- **Read-only:** No state change. Safe to retry infinitely.
- **Pure:** Produces output without side effects. Retry-safe.
- **Reversible:** Changes state but can be undone by a matching reverse action.
- **Compensatable:** Changes state; undoing requires a compensating transaction (saga pattern).
- **Irreversible:** State change cannot be undone. REQUIRES human approval for any that are Medium or High blast radius.

**Step 1.4 — Define the verification gate.** What assertion, test, or validation must pass before the skill can declare "done"? This must be a check the agent can execute autonomously (a test suite, a schema validator, a file existence check, a lint pass). It must NOT be "the user says it's good" — that is a separate human approval, not a verification gate.

> **Why Phase 1 exists:** Architecture-first prevents the "kitchen sink" anti-pattern — skills that try to do everything and trigger unpredictably. Side-effect classification (Meta-Study Principle 4) is enforced at design time, not runtime. The verification gate ensures every generated skill has an objective definition of success.

---

### Phase 2: SKILL.md Generation

Generate the complete SKILL.md from the architecture defined in Phase 1. Every section, instruction, and constraint must be traceable to a Phase 1 decision.

**Rule 2.1 — Name.** Derive from the problem, not the solution. Format: `kebab-case`, ≤64 chars, must match parent directory name. Prefer verb-noun pairs: `migrate-database`, `review-security`, `generate-report`. Avoid solution-specific names: prefer `validate-config` over `use-ajv-schema`.

**Rule 2.2 — Description (L1).** Follow the Trigger Triad pattern. Maximum 1,024 characters.

Format:

```
[Capability — what the skill produces, verb-noun]
[Trigger conditions — when to activate, specific scenarios]
[User vocabulary — literal phrases the user will type, in quotes]
[Negative trigger — "Do NOT use for..." explicit exclusions]
```

**Rule 2.3 — L2 Body structure.** Under 500 lines / 5,000 tokens. Every section below is mandatory:

```markdown
## When to Use
## When NOT to Use
## Prerequisites
## Workflow
   ### Step 1: ...
   ### Step 2: ...
## Failure Modes
## Output Contract
## Verification Gate
## Side Effects
```

**Rule 2.4 — Writing style.**

- **Imperative.** Write "Run the test suite" not "The test suite can be run."
- **Include the Why.** For every non-obvious instruction, append a `> **Why:** [rationale]` blockquote.
- **Negative constraints over positive directives.** Write "Do NOT refactor unrelated code" not "Focus on the relevant code." The meta-study shows negative constraints statistically outperform positive directives — they prune the action space precisely when the agent is about to make a costly error.

**Rule 2.5 — Recovery strategy.** Embed a 3-level escalation in the Failure Modes section:

1. **Level 1 (Local Retry):** For transient failures (timeouts, rate limits). Exponential backoff with jitter. Max 3 retries.
2. **Level 2 (Local Patch):** For fixable errors (schema violations, missing arguments). Attempt repair without changing the plan.
3. **Level 3 (Replan/Escalate):** For structural failures. Halt execution. Report to the user with diagnostic context. Do NOT loop.

**Rule 2.6 — Version.** Set to `0.1.0` — pre-stable, ready for evaluation. All generated skills start here.

> **Why Phase 2 rules exist:** The Trigger Triad description format (Rule 2.2) is the single highest-leverage text in the skill — it controls whether the skill activates at all. The 500-line / 5,000-token threshold (Rule 2.3) is validated by research showing performance degradation beyond this limit. Imperative style (Rule 2.4) produces measurably higher compliance than descriptive style. The 3-level escalation (Rule 2.5) prevents the most common production failure mode: infinite retry loops.

---

### Phase 3: Self-Validation

Before presenting the output, validate the generated SKILL.md against every meta-study design principle. This is an anti-rationalization gate — DO NOT present a skill that fails any check.

Complete this validation table:

| Principle | Check | Must Pass? |
| ----------- | ------- | ------------- |
| Progressive Disclosure | Description ≤ 1,024 chars. Body ≤ 5,000 tokens (≈500 lines). L3 resources gated behind on-demand loading. | YES |
| Goal-Oriented | Single task scoped. Trigger Triad in description. Negative triggers defined. No "kitchen sink." | YES |
| Efficiency | Scripts only for mechanical work (fetching, formatting, validation). LLM for reasoning only. No redundant instruction between L2 and L3. | YES |
| Reliability | Output contract defined. Failure modes enumerated with recovery paths. Verification gate specified. | YES |
| Scalability | No harness-specific features hardcoded (no `model`, `disable-model-invocation`, Claude-Code-only fields). Portability notes included. | YES |
| Side-Effect Classification | Every action typed (Read-only/Pure/Reversible/Compensatable/Irreversible). High-blast Irreversible actions gated behind human approval. | YES |
| SemVer | Version set to 0.1.0. | YES |

**If any check fails:** Return to Phase 2 and fix the generation. Identify which rule was violated and regenerate that section. DO NOT present a failed skill.

**If all checks pass:** Proceed to Phase 4.

> **Why Phase 3 exists:** This is the anti-rationalization gate. Without it, the agent will ship skills with obvious flaws — missing failure modes, bloated descriptions, harness-specific lock-in. The self-validation table forces the agent to confront its own output quality before the user sees it. This is Meta-Study Principle 2 (Process-Driven Lifecycles) applied to skill creation itself.

---

### Phase 4: Delivery

**Step 4.1 — Write the SKILL.md.** Save to `./<skill-name>/SKILL.md` (or the path specified by the invoker).

**Step 4.2 — Generate the directory scaffold:**

```
<skill-name>/
├── SKILL.md
├── scripts/          # Create if the skill uses scripts; leave a .gitkeep otherwise
├── references/       # Create if the skill uses L3 reference files
└── assets/           # Create if the skill uses templates or static assets
```

If no files exist in a directory, place an empty `.gitkeep` so the scaffold is complete.

**Step 4.3 — Output the skill manifest.** Print this summary:

```
## Skill Generated: <skill-name>

- **Type:** <capability-uplift | preference-encoding | hybrid>
- **Version:** 0.1.0
- **Description:** <one-line from the SKILL.md description>
- **Output:** <what the skill produces>
- **Verification:** <how success is verified>
- **Side Effects:** <summary of actions classified>
```

**Step 4.4 — Close with the activation test.** Add this line to the output:

> "To test this skill, invoke it with: '`[example user query that should trigger it]`'"

The activation test must use a phrase from the User Vocabulary section of the Trigger Triad.

---

## Failure Modes

### Phase 0: User gives vague answers to clarifying questions

**Recovery (Level 1):** Re-ask the unanswered question with a concrete example: "For example, if you asked for a code review skill, the outcome might be 'a Markdown file with found issues, severity, and suggested fixes in the PR comments section.' What would the equivalent be for your use case?"

### Phase 3: Validation fails on one or more checks

**Recovery (Level 2):** Return to Phase 2. Identify the specific section that caused the failure. Regenerate only that section. Re-run Phase 3. If the same check fails twice, flag the conflict to the user rather than looping: "I'm unable to satisfy the [principle] constraint because [reason]. Here's the trade-off. How should I proceed?"

### Phase 4: Output path is not writable

**Recovery (Level 1):** Report the error with the attempted path. Ask the user for an alternative path. Do NOT write to a fallback location without asking.

### Generated skill would require tools the agent doesn't have

**Recovery (Level 3):** Halt. Report: "This skill requires [tool], which may not be available in all agent environments. Options: (1) Add the tool to your agent configuration, (2) I can redesign the skill to avoid this dependency, (3) I can add a prerequisite check that gracefully fails if the tool is absent."

---

## Output Contract

This skill produces:

1. **`<skill-name>/SKILL.md`** — A complete, validated, production-grade agent skill with YAML frontmatter and Markdown instructions.
2. **Directory scaffold** — `scripts/`, `references/`, `assets/` subdirectories.
3. **Skill manifest** — A structured summary printed to output.

The SKILL.md MUST:

- Have valid YAML frontmatter with `name` and `description` at minimum.
- Have a body under 500 lines / 5,000 tokens.
- Include all 7 mandatory sections: When to Use, When NOT to Use, Prerequisites, Workflow, Failure Modes, Output Contract, Verification Gate, Side Effects.
- Pass all 7 self-validation checks in Phase 3.

---

## Verification Gate

Before declaring a generation complete, ALL of these must be true:

- [ ] Phase 0 completed with both clarifying questions answered and summary confirmed.
- [ ] Phase 1 architecture documented (type, output contract, action classification, verification gate).
- [ ] Phase 2 SKILL.md written with all 7 mandatory sections.
- [ ] Phase 3 self-validation table completed with all 7 checks passing.
- [ ] Phase 4 scaffold written to disk.
- [ ] Phase 4 manifest printed to output.
- [ ] Activation test line included in output.

---

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| -------- | ------ | ------------- | ------------------ |
| Read user's problem description | Read-only | Low | No |
| Ask clarifying questions | Pure | Low | No |
| Design skill architecture (internal) | Pure | Low | No |
| Generate SKILL.md content (internal) | Pure | Low | No |
| Self-validate against principles (internal) | Pure | Low | No |
| Write SKILL.md to disk | Reversible | Medium | No — user can delete or modify |
| Create directory scaffold | Reversible | Low | No — empty directories are harmless |
| Print manifest to output | Pure | Low | No |
