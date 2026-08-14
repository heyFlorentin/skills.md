---
name: self-test
description: Self-evaluates the agent's output under controlled fault injection using deterministic rule-based graders. Invoke to verify a deliverable before delivery, to test robustness against environmental degradation, or when acceptance must not rely on LLM-as-judge. Trigger phrases "test this", "verify my output", "check robustness", "self-test", or as the Verify stage of the metacognitive loop.
---

# self-test

OccuBench-style fault injection + GDPevo-style deterministic grading. The goal is robustness over the "happy path", with a reproducible pass/fail per violated rule.

## When to Use

- Before delivering any artifact, to gate on deterministic criteria.
- When the environment may degrade silently (APIs time out, data arrives incomplete).
- When an LLM-as-judge would be unreliable or non-reproducible.

## Instructions

1. **Define the grader** — express the acceptance criteria as atomic, deterministic rules (each independently checkable by code or a fixed script). No LLM-as-judge.
2. **Fault injection (three classes)**:
   - `explicit` — overt errors (timeouts, 500s, missing file, type mismatch).
   - `implicit` — silent data degradation (truncated fields, missing fields, wrong-but-valid values).
   - `mixed` — a combination of explicit and implicit faults.
3. **Run each fault class** against the output. Record, per rule, whether it held.
4. **Emit a robustness profile** — a table: `Rule`, `Fault class`, `Held?`, `Evidence`. Implicit faults carry higher weight (they lack overt error signals).

## Output Contract

- Per-rule pass/fail table with evidence for each verdict.
- A single `grader_score` (fraction of rules held), sourced from the deterministic grader.
- A list of the specific violated rules (trace each failure to a rule).

## Constraints

- Do NOT substitute LLM-as-judge for a deterministic grader.
- Do NOT report a rule as "held" without running the check.
- Implicit faults MUST be tested; happy-path-only is not a self-test.
