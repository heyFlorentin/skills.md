---
alwaysApply: true
---

# Compliance (GDPR / EU AI Act / German Data Sovereignty)

- **GDPR Art. 28** — ENSURE no personal data, credentials, or client-confidential material is placed in MCP tool arguments without a processing agreement covering that endpoint. Reasoning MCP calls transmit content to `https://mcp.beta.lstr.one/mcp`; strip secrets and PII from `thought`, `content`, and `claim` fields.
- **EU AI Act** — avoid prohibited practices (Art. 5). Do NOT build or operate systems that manipulate, exploit, or perform social scoring of natural persons. Do NOT infer sensitive attributes (race, health, political opinion) without a lawful basis.
- **Data sovereignty (German-first)** — default to on-device / local storage. Prefer local skills and project rules over remote services where functionality is equivalent. Flag any cross-border data egress explicitly.
- **Secrets hygiene** — secrets MUST NOT appear in hooks, memory files, evolution ledger, or reasoning records. Use environment variables or a secrets store.
- **Human oversight** — irreversible or high-blast-radius actions (deploy, destructive delete, financial mutation) MUST require explicit user confirmation before execution.
