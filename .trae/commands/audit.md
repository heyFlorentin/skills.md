---
name: audit
description: Validate the newest reasoning record against the output contract and report gaps.
---

Audit the harness's reasoning trail.

1. Locate the newest `reasoning-records/*.md` file.
2. Validate its frontmatter: `monitoring_id`, `query`, `timestamp`, `overall_confidence`, `knowledge_level`, `steps_executed`, `steps_skipped`.
3. Validate the Step Trace JSON block: `steps_executed` equals the count of `status: "ok"` entries; every non-`ok` step has a non-null `skip_reason`.
4. Check the response against the 7-element output spec (identity, reasoning transparency, confidence, multi-perspective insight, technical precision, regulatory compliance, edge case).
5. Check for forbidden vague terms ("consider", "might", "could", "perhaps", "feel free to").

Report a pass/fail per check, and list any gaps with the exact violation. Do NOT fabricate a record if none exists — state that no reasoning record is present.
