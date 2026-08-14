#!/usr/bin/env python3
"""Sanitize + classify r/StartupDACH posts from Reddit JSON; print JSON to stdout.

Read-only with respect to the filesystem: this script writes NO file. The agent
(not the script) writes the Markdown digest. Stdlib only; no API key, no OAuth.

Input: Reddit `hot.json` JSON on stdin, or a file path as argv[1]. Raw outbound
HTTP to reddit.com is blocked in some environments; retrieve the JSON via the
agent's WebFetch/curl and pipe it here. This keeps network retrieval and
classification decoupled.
"""

from __future__ import annotations

import json
import re
import sys

from classify import classify_post

DEFAULT_LIMIT = 25


def _strip_usernames(text: str) -> str:
    """Remove u/<name> and @name tokens to avoid persisting identifiers."""
    text = re.sub(r"\bu/[\w-]+", "", text)
    text = re.sub(r"@[\w-]+", "", text)
    return " ".join(text.split())


def _sanitize(post: dict) -> dict:
    """Return only title, flair, score, permalink, and classification.

    Deliberately EXCLUDES author, selftext, and body (GDPR data minimization).
    """
    title = post.get("title", "")
    flair = (post.get("link_flair_text") or "").strip()
    return {
        "title": _strip_usernames(title),
        "flair": flair,
        "score": post.get("score"),
        "permalink": post.get("permalink"),
        "intent": classify_post(title, flair),
    }


def _read_payload() -> dict:
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
    elif len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as fh:
            raw = fh.read()
    else:
        raise SystemExit(
            "no input: pipe Reddit hot.json to stdin or pass a file path argument"
        )
    return json.loads(raw)


def main() -> int:
    try:
        payload = _read_payload()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"input parse failed: {exc}", file=sys.stderr)
        return 1

    children = payload.get("data", {}).get("children", [])
    posts = [
        _sanitize(child["data"])
        for child in children
        if child.get("kind") == "t3" and "data" in child
    ][:DEFAULT_LIMIT]

    out = {
        "source": "r/StartupDACH/hot.json",
        "fetched": len(children),
        "classified_count": len(posts),
        "posts": posts,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
