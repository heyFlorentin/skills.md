# Intent Keyword Tables — L3 Reference

> **L3 Reference for `monitor-startup-dach`.** Load on demand when editing the
> classifier or extending clusters. The `scripts/classify.py` module embeds a
> normalized copy of these tables; keep them in sync.

## Normalization Rules (deterministic)

Applied to both keywords and the input `title + " " + flair` before matching:

1. `str.casefold()` — case-insensitive.
2. Unicode NFD normalization, then strip combining marks (`unicodedata.category(c) == "Mn"`)
   so umlauts collapse: `ü→u`, `ö→o`, `ä→a`.
3. `ß → ss`.
4. Collapse all whitespace runs to a single space; trim ends.

> **Why:** Normalization makes "DSGVO"/"dsgvo", "Mitgründer"/"mitgruender", and
> "Förderung"/"foerderung" match identically, without needing an exhaustive
> keyword-per-inflection list.

## Matching Algorithm

- Substring match of each normalized keyword against the normalized input.
- Per-cluster score = number of matching keywords.
- Highest score wins.
- Tie-break order (deterministic, first wins):
  `co-founder` → `compliance` → `funding` → `feedback` → `visibility` → `hiring`.
- Zero matches → `unclassified`. Do NOT force a cluster.

## Cluster Keyword Tables

### co-founder

mitgrunder, mitgründer, co-founder, cofounder, co founder, cofounders,
grundungspartner, gründungspartner, suche mitgrunder, suche mitgründer,
cto gesucht, tech-cofounder, tech cofounder, ceo gesucht

### compliance

compliance, datenschutz, dsgvo, gdpr, rechtsanwalt, anwalt, anwaltlich,
steuer, steuerberater, finanzamt, umsatzsteuer, impressum, agb,
versicherung, regulierung, zulassung, gewerbe, haftung, vertrag,
wettbewerbsverbot, treuepflicht, rechtlich, recht, gründung rechtlich

### funding

funding, finanzierung, förderung, foerderung, zuschuss, grant, investor,
vc, investment, bafa, kfw, exist, seed, pre-seed, preseed, crowdfunding,
kapital, fundraising, round, wettbewerb, scale

### feedback

feedback, review, meinung, beta, ux, user-test, usertest, bewertung,
roast, kritik, verbesserung, erste eindrücke, erste eindruecke,
was haltet ihr, testet, demo tester, demo-tester

### visibility

visibility, marketing, sichtbarkeit, reichweite, seo, social media,
linkedin, launch, pr, presse, branding, growth, werbung, content,
community, bekanntheit, gefunden, auffindbar

### hiring

hiring, stellenanzeige, stellenangebot, job, einstellung, bewerbung,
werkstudent, praktikum, vollzeit, remote, gehalt, recruiting,
mitarbeiter gesucht, suche entwickler, freelancer gesucht, cso gesucht,
sales, vertrieb, suche startup
