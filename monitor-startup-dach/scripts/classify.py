#!/usr/bin/env python3
"""Deterministic intent classifier for r/StartupDACH posts.

Pure, stdlib-only. No network, no file writes, no state. The `classify_post`
function is the single pluggable seam: replace its body with a real ICU call
in the future without changing callers or the workflow.
"""

from __future__ import annotations

import sys
import unicodedata

CLUSTERS = [
    "co-founder",
    "compliance",
    "funding",
    "feedback",
    "visibility",
    "hiring",
]

# Canonical tie-break order == CLUSTERS order (first wins).
KEYWORDS = {
    "co-founder": [
        "mitgrunder", "co-founder", "cofounder", "co founder", "cofounders",
        "grundungspartner", "suche mitgrunder", "cto gesucht",
        "tech-cofounder", "tech cofounder", "ceo gesucht",
    ],
    "compliance": [
        "compliance", "datenschutz", "dsgvo", "gdpr", "rechtsanwalt", "anwalt",
        "anwaltlich", "steuer", "steuerberater", "finanzamt", "umsatzsteuer",
        "impressum", "agb", "versicherung", "regulierung", "zulassung",
        "gewerbe", "haftung", "vertrag", "wettbewerbsverbot", "treuepflicht",
        "rechtlich", "recht",
    ],
    "funding": [
        "funding", "finanzierung", "foerderung", "zuschuss", "grant", "investor",
        "vc", "investment", "bafa", "kfw", "exist", "seed", "pre-seed",
        "preseed", "crowdfunding", "kapital", "fundraising", "round",
        "wettbewerb", "scale",
    ],
    "feedback": [
        "feedback", "review", "meinung", "beta", "ux", "user-test", "usertest",
        "bewertung", "roast", "kritik", "verbesserung", "erste eindruecke",
        "was haltet ihr", "testet", "demo tester", "demo-tester",
    ],
    "visibility": [
        "visibility", "marketing", "sichtbarkeit", "reichweite", "seo",
        "social media", "linkedin", "launch", "pr", "presse", "branding",
        "growth", "werbung", "content", "community", "bekanntheit", "gefunden",
        "auffindbar",
    ],
    "hiring": [
        "hiring", "stellenanzeige", "stellenangebot", "job", "einstellung",
        "bewerbung", "werkstudent", "praktikum", "vollzeit", "remote", "gehalt",
        "recruiting", "mitarbeiter gesucht", "suche entwickler",
        "freelancer gesucht", "cso gesucht", "sales", "vertrieb",
        "suche startup",
    ],
}


def normalize(text: str) -> str:
    """Casefold, strip combining marks (umlauts), fold ß, collapse whitespace."""
    text = text.casefold()
    text = text.replace("ß", "ss")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return " ".join(text.split())


def classify_post(title: str, flair: str = "") -> str:
    """Return one cluster name or 'unclassified' (deterministic)."""
    haystack = normalize(f"{title} {flair}")
    scores = {cluster: 0 for cluster in CLUSTERS}
    for cluster in CLUSTERS:
        for kw in KEYWORDS[cluster]:
            if normalize(kw) in haystack:
                scores[cluster] += 1
    best_cluster = None
    best_score = 0
    for cluster in CLUSTERS:  # iteration order enforces tie-break
        if scores[cluster] > best_score:
            best_score = scores[cluster]
            best_cluster = cluster
    if best_score == 0:
        return "unclassified"
    return best_cluster


GOLDEN_FIXTURES = [
    ("Suche Co-Founder für SaaS-/Tech-Startup", "", "co-founder"),
    ("Treuepflicht und Wettbewerbsverbot in der Anstellung", "", "compliance"),
    ("Wie habt ihr Datenschutz/DSGVO bei eurem ersten SaaS geregelt?", "", "compliance"),
    ("DACH-Startup-Wettbewerb 2025 - by ScaleList.de", "", "funding"),
    ("Dein Produkt ist besser und trotzdem kommen keine Anfragen?", "", "visibility"),
    ("CSO gesucht!", "", "hiring"),
    ("How do you find demo testers for your saas?", "", "feedback"),
    ("Jurehsick Park", "", "unclassified"),
]


def _self_test() -> int:
    failures = 0
    for title, flair, expected in GOLDEN_FIXTURES:
        got = classify_post(title, flair)
        if got != expected:
            failures += 1
            print(f"FAIL: {title!r} -> {got!r} (expected {expected!r})",
                  file=sys.stderr)
    if failures:
        print(f"{failures} self-test failure(s)", file=sys.stderr)
        return 1
    print(f"self-test passed ({len(GOLDEN_FIXTURES)} fixtures)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        sys.exit(_self_test())
    # Otherwise: classify a single post from argv for ad-hoc use.
    title = sys.argv[1] if len(sys.argv) > 1 else ""
    flair = sys.argv[2] if len(sys.argv) > 2 else ""
    print(classify_post(title, flair))
