---
description: Apply when evolving skills, memory, or harness state — i.e. when distilling task outcomes into persistent rules, proposing a skill update, or appending to the evolution ledger.
---

# Self-Evolution Policy

## Supervision Types (GDPevo)

- `reflect` — default. Distil from the task's own scores (reinforcement-learning-like). Transfers most robustly across domains.
- `fewshot` — opt-in. Distil from gold answers (supervised-like). Reserved for canonical examples only; overfits the source domain and MUST NOT be the default.
- `self` — unsupervised. Used for exploratory tasks only; lowest confidence distillations.

## Distillation Gate

Distil a rule into skills/memory ONLY when:

1. The task passed its deterministic grader (`grader_score` recorded, never LLM-as-judge).
2. The rule is atomic (one business rule, not an entangled bundle).
3. Provenance is recorded: source `task_slug` + `grader_score` + `supervision_type`.
4. The distillation is additive and reversible.

## Constraints

- MUST NOT auto-commit destructive or irreversible evolution. Propose first; apply on approval.
- MUST NOT evolve away from the identity contract in `00-identity.md` or the output spec in `20-output-spec.md`.
- MUST append every distillation to `.trae/memory/evolution-ledger.md`.
- MUST NOT write secrets or personal data into any evolved artifact (GDPR Art. 28).

## Cost as First-Class Metric

Record tokens, turns, and elapsed tool calls alongside accuracy. A useful evolution MUST improve task success without an unbounded resource increase.
