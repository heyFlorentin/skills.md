---
name: monitor-startup-dach
version: 0.1.0
description: Fetch the top-25 posts from r/StartupDACH/hot.json, classify each into six deterministic German intent clusters (co-founder, compliance, funding, feedback, visibility, hiring) using a local keyword classifier, and write an anonymized Markdown digest with per-cluster counts and summaries. Trigger on "monitor StartupDACH", "what's trending on StartupDACH", "StartupDACH intent digest", "summarize r/StartupDACH hot posts". Do NOT use for authenticated Reddit data, comment/body retrieval, sentiment scoring, LLM-based classification, or any ICU / Florentin One proprietary endpoint integration.
---

# monitor-startup-dach

## When to Use

- Fetch the current top-25 posts of `r/StartupDACH` and bucket them into intent clusters for demand discovery.
- Produce an anonymized Markdown digest of founder intent trends.
- Run the deterministic classifier (or its self-test) locally with zero external dependencies.

## When NOT to Use

- MUST NOT fetch post comments, selftext bodies, or any authenticated/OAuth Reddit data.
- MUST NOT invoke any ICU endpoint, any third-party LLM, or any Florentin One proprietary API — none is available here.
- MUST NOT use an LLM to classify intent; the classifier is deterministic keyword matching.
- MUST NOT mutate any repository file, config, environment variable, or reviewed resource.

## Prerequisites

- Python 3 standard library only (`json`, `re`, `unicodedata`, `sys`).
- NO `pip install`, NO API key, NO OAuth token, NO config or environment changes.
- Reddit JSON retrieved by the agent via WebFetch or curl (see Step 1); classification runs fully on-device.

> **Why:** Stdlib-only keeps the skill operable by a solo developer on free/hobby tiers with zero setup. Decoupling retrieval from classification keeps the script portable across environments where raw outbound HTTP to `reddit.com` is blocked (some sandboxes return HTTP 403). The deterministic classifier avoids cross-border LLM processing (GDPR Art. 5(1)(c) data minimization).

## Workflow

### Step 1: Fetch

Retrieve `https://www.reddit.com/r/StartupDACH/hot.json?limit=25` using the agent's WebFetch (or `curl`). Pipe the JSON into the classifier:

```bash
# agent retrieves the JSON, then:
cat hot.json | python3 scripts/fetch_and_classify.py
# or pass a file path:
python3 scripts/fetch_and_classify.py hot.json
```

The script filters `kind == "t3"` and takes the first 25 posts.

> **Why:** Raw outbound HTTP to `reddit.com` from a script is blocked (HTTP 403) in some sandboxes, while the agent's WebFetch succeeds. Keeping retrieval in the agent and classification in the script preserves portability.

### Step 2: Sanitize

The script strips `author`, `selftext`, `body`, `u/<name>`, and `@name` tokens. Output entries contain only `title`, `flair`, `score`, `permalink`, and `intent`.

> **Why:** Titles and scores are non-identifiable; usernames and bodies are personal data. Excluding them satisfies GDPR data minimization and keeps the digest anonymized.

### Step 3: Classify

`scripts/classify.py` assigns each post to one of `co-founder | compliance | funding | feedback | visibility | hiring | unclassified` via deterministic substring matching after normalization (casefold, umlaut folding, ß→ss, whitespace collapse). Ties break in canonical order; zero matches → `unclassified`.

### Step 4: Compose the digest

Copy `assets/digest-template.md`, fill placeholders with the classified counts, and write ONE new Markdown file. Write 1–2 line summaries per cluster using sanitized titles only. Do NOT edit any existing file.

## Failure Modes

### Level 1 — Local Retry (transient)

WebFetch/curl transient failure, timeout, or 429/5xx. Retry with exponential backoff + jitter, maximum 3 attempts, headers unchanged.

### Level 2 — Local Patch (fixable)

Malformed JSON response or a schema field missing. Inspect the raw payload, correct the parser mapping once, resubmit. Do NOT change the plan.

### Level 3 — Replan / Escalate (structural)

Network unreachable after retries, or Reddit blocks the request persistently. HALT. Report the diagnostic context to the user. Do NOT fabricate posts or loop. Offer: (1) retry later, (2) narrow scope, (3) abort.

### Edge case — fewer than 25 posts

Emit the digest with `fetched < 25` and a note; do NOT fail. The count invariant is `classified + unclassified <= fetched`, never greater.

## Output Contract

A single Markdown file matching `assets/digest-template.md`, containing:

- Header with date, `fetched`, `classified`, `unclassified` counts.
- A `Cluster Counts` table with integer counts for the six clusters plus `unclassified`.
- One section per cluster with 1–2 line sanitized-title summaries.
- An `unclassified` section listing sanitized titles.

Invariants: counts are integers; no `author`, `selftext`, or comment `body` text; no `u/…` or `@…` tokens anywhere.

## Verification Gate

1. `python3 scripts/classify.py --self-test` exits 0 (all golden fixtures pass).
2. `python3 scripts/fetch_and_classify.py` (with JSON on stdin or a file path) exits 0; stdout is valid JSON; `classified_count <= 25`; no entry contains `author`/`selftext`/`body` keys.
3. The digest contains all six cluster headings with counts and no username tokens or post bodies.

> **Why:** These are deterministic, agent-executable checks — no LLM-as-judge. They guard the two failure modes that matter: classifier regression and personal-data leakage.

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| --- | --- | --- | --- |
| GET `hot.json?limit=25` (agent, WebFetch/curl) | Read-only (network) | Low | No |
| Sanitize + classify | Pure | Low | No |
| Print JSON to stdout | Pure | Low | No |
| Write digest Markdown (new file) | Reversible | Low | No |

No irreversible actions. The scripts never write files; only the agent emits the single digest. "Never mutate anything" holds: existing files and the reviewed subreddit are untouched.
