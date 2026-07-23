---
name: legal-toolkit
description: "Generate legal document drafts for a Hungarian AI consultancy (Kft.). Covers: consulting agreements, NDAs, DPAs (GDPR Art.28), SOWs, terms of service, EU AI Act compliance self-assessment, Kft. annual compliance checklist, freelancer contracts, privacy policies, IP assignments. Bilingual HU/EN. Trigger on: 'generate contract', 'NDA for', 'data processing agreement', 'DPA', 'terms of service', 'privacy policy', 'GDPR compliance', 'AI Act compliance', 'Kft. compliance', 'legal toolkit', 'consulting agreement', 'statement of work', 'freelancer contract', 'IP assignment'. Also triggers when you mention needing legal documents for your consultancy, client engagements, or product terms."
---

# LEGAL TOOLKIT

> Draft documents, not legal advice. Every output ships with a "have your lawyer review this" checklist.

## MANDATORY CAVEAT (include in EVERY output)

```
This is a machine-generated draft. It does not constitute legal advice.
Have a qualified Hungarian/EU lawyer review any document before signing
or relying on it. Estimated review cost: €200-500 for a standard contract.
```

## Shared Infrastructure
- **Hungarian writing:** Read your brand-voice reference for ALL Hungarian output
- **Kft. entity details:** Read your company registration details for your consultancy registration data
- **Front Office integration:** Tax calendar, GDPR steward, AI Act officer agents exist at your business files

## 12 Document Types

| # | Document | Hungarian Name | When Needed |
|---|----------|---------------|-------------|
| 1 | Consulting Services Agreement | Tanácsadási szerződés | Every new client |
| 2 | Non-Disclosure Agreement | Titoktartási megállapodás | Before sharing methodologies |
| 3 | Data Processing Agreement (GDPR Art.28) | Adatfeldolgozási megállapodás | When processing personal data |
| 4 | Statement of Work | Részletes munkaterv | Per-project scope |
| 5 | Terms of Service | Általános Szerződési Feltételek (ÁSZF) | SaaS/digital products |
| 6 | EU AI Act Self-Assessment | EU MI jogszabály megfelelési önértékelés | Quarterly internal audit |
| 7 | Kft. Annual Compliance Checklist | Kft. éves ellenőrzőlista | Annual review |
| 8 | Freelancer/Subcontractor Agreement | Alvállalkozói szerződés | Hiring freelancers |
| 9 | Privacy Policy | Adatvédelmi tájékoztató | Every public product/site |
| 10 | Cookie Policy | Sütikre vonatkozó tájékoztató | Every website |
| 11 | AI Output Disclaimer | MI-kimenet felelősségkizáró | Every AI deliverable |
| 12 | IP Assignment | Szellemi tulajdon átruházás | Custom work transfers |

## Workflow

```
"I need a [document type]"
        │
Phase 1: DISCOVERY (3-5 questions)
        │ • Who is the other party?
        │ • Jurisdiction? (Hungarian law / English law / mixed)
        │ • Personal data involved? (triggers GDPR flow)
        │ • AI systems involved? (triggers AI Act clauses)
        │ • Special constraints? (non-compete, exclusivity, rush)
        │
Phase 2: TEMPLATE SELECTION
        │ • Match to document type
        │ • Language: HU only / EN only / bilingual
        │ • Complexity: micro (1-2p) / standard (3-8p) / comprehensive (8+p)
        │
Phase 3: DRAFT GENERATION
        │ • Fill template with discovery answers
        │ • Insert jurisdiction-specific clauses
        │ • Add GDPR/AI Act clauses if triggered
        │ • Pre-fill your consultancy details
        │ • Add modular clauses from clauses/ directory
        │
Phase 4: REVIEW CHECKLIST
        │ • Flag [REVIEW] markers on clauses needing lawyer attention
        │ • List assumptions made
        │ • Estimate lawyer review cost
        │ • Generate "what to ask your lawyer" checklist
        │
Phase 5: EXPORT
          • Clean Markdown (for Word/Google Docs paste)
          • Optional: HTML with print CSS for direct PDF
```

## EU AI Act Compliance (Article 50 Transparency)

Key obligations for your AI consultancy:
- Label ALL AI-generated deliverables as AI-generated
- Classify each AI system used as: prohibited / high-risk / limited-risk / minimal-risk
- Maintain technical documentation for any AI system deployed for clients
- Log incidents
- Review quarterly

The self-assessment checklist at `checklists/eu-ai-act-self-assessment.md` covers this.

## GDPR DPA Requirements (Art.28 mandatory clauses)

Every DPA must include:
1. Subject matter, duration, nature, purpose of processing
2. Types of personal data and data subject categories
3. Controller's processing instructions
4. Confidentiality obligations
5. Security measures (Art.32)
6. Sub-processor approval and flow-down
7. Data subject rights assistance
8. Breach notification (72-hour)
9. Audit and inspection rights
10. Data return/deletion at end
11. International transfer mechanisms (SCCs if data leaves EU/EEA)

you use US-based AI APIs (Anthropic, OpenAI) → must address EU-US data transfers under the Data Privacy Framework.

## Modular Clause Library

Reusable clauses shared across document types:

| Clause | File | Used In |
|--------|------|---------|
| Liability cap | `clauses/liability-cap.md` | Agreements, SOW |
| Force majeure (incl. AI disruption) | `clauses/force-majeure.md` | All contracts |
| AI accuracy disclaimer | `clauses/ai-accuracy-disclaimer.md` | Agreements, deliverables |
| Sub-processor list | `clauses/sub-processor-list.md` | DPA |
| Hungarian jurisdiction | `clauses/hungarian-jurisdiction.md` | All contracts |
| Data transfer SCCs | `clauses/data-transfer-scc.md` | DPA |

## Anti-Patterns (7 legal mistakes to prevent)

1. **Using public AI with client data** without business agreement → include DPA + sub-processor disclosure
2. **No written contract for "quick favors"** → micro-SOW for everything, even 1-hour sessions
3. **Guaranteeing AI accuracy** → always include probabilistic output disclaimer
4. **IP ownership ambiguity** → default: client owns deliverables, consultant retains methodologies
5. **Missing sub-processor disclosure** → maintain living list of all AI/cloud services used
6. **No liability cap** → default: cap at 1-2x project fee
7. **Missing AI Act transparency** → every AI deliverable gets a disclosure footer

## File Structure

```
legal-toolkit/
├── SKILL.md
├── templates/
│   ├── consulting-agreement.md
│   ├── nda-ai.md
│   ├── dpa-gdpr.md
│   ├── sow.md
│   ├── tos-saas.md
│   ├── freelancer-agreement.md
│   ├── privacy-policy.md
│   ├── cookie-policy.md
│   ├── ip-assignment.md
│   └── ai-output-disclaimer.md
├── checklists/
│   ├── kft-annual.md
│   ├── eu-ai-act-self-assessment.md
│   └── gdpr-readiness.md
├── clauses/
│   ├── liability-cap.md
│   ├── force-majeure.md
│   ├── ai-accuracy-disclaimer.md
│   ├── sub-processor-list.md
│   ├── hungarian-jurisdiction.md
│   └── data-transfer-scc.md
└── references/
    ├── ptk-key-sections.md
    ├── gdpr-article-28.md
    ├── ai-act-article-50.md
    └── lawyer-review-guide.md
```

Templates are loaded on-demand (only the relevant one). Clauses are modular -- a consulting agreement pulls liability-cap + ai-accuracy-disclaimer + hungarian-jurisdiction as needed. References are for "why does it say this?" questions, never loaded during generation.
