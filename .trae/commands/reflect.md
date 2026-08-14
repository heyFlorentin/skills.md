---
name: reflect
description: Reflect on the just-completed task and distil reusable rules into persistent state (self-evolution).
---

Invoke the `self-evolve` skill on the just-completed task.

1. Obtain the `grader_score` from the deterministic grader (`self-test`). If no grader ran, report the gap and do NOT distil.
2. Select supervision type per `40-evolution-policy.md` (default `reflect`).
3. Distil atomic reusable rule(s) with provenance (`task_slug`, `grader_score`, `supervision_type`).
4. Append one entry to `.trae/memory/evolution-ledger.md` with `status: proposed`; propose the skill/memory update — do NOT auto-commit.
5. Record cost (tokens, turns, tool calls) alongside accuracy.

Do NOT evolve from a failed task, do NOT write secrets, and do NOT evolve away from `00-identity.md` or `20-output-spec.md`.
