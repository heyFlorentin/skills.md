---
name: self-evolve
description: Reflects on a completed task's outcome and distills reusable atomic rules into persistent state (skills and memory), governed by the self-evolution policy. Invoke after a task passes its deterministic grader, on "/reflect", or as the Evolve stage of the metacognitive loop. Trigger phrases "reflect on this task", "/reflect", "learn from this", "distill a rule".
---

# self-evolve

GDPevo reflection loop. Converts a passed task's outcome into persistent, provenance-tracked state, without destructive mutation.

## When to Use

- After a task has been graded and passed its deterministic grader.
- When a reusable rule was exercised and should persist across future tasks.
- On `/reflect` to close the Evolve stage of the metacognitive loop.

## When NOT to Use

- Do NOT use when the task failed its grader (evolving from a failed task propagates error).
- Do NOT use for one-time or temporary instructions.

## Instructions

1. **Score the task** — obtain `grader_score` from the deterministic grader (`self-test`). If no grader ran, do NOT distil; report the gap.
2. **Select supervision type** per `40-evolution-policy.md`: `reflect` (default), `fewshot` (canonical only), `self` (exploratory).
3. **Distil atomic rules** — extract the smallest reusable rule(s) the task exercised. Record provenance: `task_slug`, `grader_score`, `supervision_type`.
4. **Propose, do not auto-commit** — write the proposal to `.trae/memory/evolution-ledger.md` with `status: proposed`. Apply to a skill or memory only on approval.
5. **Record cost** — tokens, turns, and tool calls, alongside accuracy (cost is a first-class metric).

## Output Contract

- One ledger entry appended with full schema: `timestamp`, `task_slug`, `supervision_type`, `grader_score`, `distilled_rule`, `provenance`, `status`.
- An explicit proposal (skill update / memory update / no-op) with the reason.

## Constraints

- No destructive or irreversible evolution without explicit approval.
- No secrets or personal data in any distilled artifact (GDPR Art. 28).
- MUST NOT evolve away from `00-identity.md` or `20-output-spec.md`.
