# GDPR Readiness Checklist

For a one-person Hungarian Kft. acting as both data controller (own marketing/clients) and data processor (client data processed via AI). Supervisory authority: NAIH (Nemzeti Adatvédelmi és Információszabadság Hatóság). Run at setup and review annually.

Last reviewed: [DATE]

## 1. Lawful Basis & Records
- [ ] Record of Processing Activities (Art.30) maintained — even a small entity should keep one
- [ ] Lawful basis identified for each processing purpose (consent / contract / legitimate interest / legal obligation)
- [ ] Legitimate Interest Assessments (LIA) documented where that basis is used (e.g. B2B prospecting)
- [ ] Special category data (Art.9) avoided unless a specific condition applies

## 2. Transparency
- [ ] Privacy Policy published on every public site/product (use `templates/privacy-policy.md`)
- [ ] Cookie Policy + consent banner live (use `templates/cookie-policy.md`)
- [ ] AI usage disclosed to clients and data subjects (AI Act Art.50 overlap)

## 3. Data Subject Rights
- [ ] Process to handle access, rectification, erasure, portability, objection requests within 1 month
- [ ] Identity-verification step before fulfilling requests
- [ ] Contact channel for rights requests published (email is sufficient for a small entity)

## 4. Processor Obligations (when handling client data)
- [ ] DPA signed with every client whose personal data is processed (use `templates/dpa-gdpr.md`)
- [ ] Sub-processor list current (`clauses/sub-processor-list.md`)
- [ ] Sub-processor DPAs in place (Anthropic, OpenAI/kie.ai, Cloudflare, etc.)
- [ ] International transfer mechanism verified for each non-EEA sub-processor (`clauses/data-transfer-scc.md`)

## 5. Security (Art.32)
- [ ] Encryption in transit (TLS) and at rest where feasible
- [ ] Access controls + strong authentication on all systems holding personal data
- [ ] Secrets kept out of source control (.gitignored / vault)
- [ ] Regular backups + tested restore
- [ ] Minimal data retention — delete client data when engagement ends

## 6. Breach Response
- [ ] Breach notification procedure documented (NAIH within 72 hours; data subjects without undue delay if high risk)
- [ ] Incident log maintained
- [ ] Sub-processors contractually required to notify the company without undue delay

## 7. Accountability
- [ ] DPO assessment done (a one-person consultancy is unlikely to require a mandatory DPO under Art.37 — document the reasoning)
- [ ] DPIA performed for any high-risk processing (Art.35) — e.g. large-scale profiling
- [ ] This checklist + supporting docs stored where they can be produced for NAIH on request

## Result

| Area | Status | Gaps |
|------|--------|------|
| Lawful basis & RoPA | ☐ OK / ☐ Gaps | |
| Transparency | ☐ OK / ☐ Gaps | |
| Data subject rights | ☐ OK / ☐ Gaps | |
| Processor obligations | ☐ OK / ☐ Gaps | |
| Security | ☐ OK / ☐ Gaps | |
| Breach response | ☐ OK / ☐ Gaps | |
| Accountability | ☐ OK / ☐ Gaps | |

Next review due: [DATE + 12 months]

> Draft checklist, not legal advice. NAIH guidance and EDPB opinions evolve. Have a qualified data-protection lawyer review your setup, especially the DPO assessment and any DPIA.
