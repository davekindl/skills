# TEASER -- Persuasion-Optimized Email + Preview Package

## Purpose
Produce a teaser email and 3-page PDF preview that makes the target company unable to ignore the audit findings. Uses 4 of 7 Cialdini persuasion principles.

## Inputs Required
- `gap_analysis.json` (from plan)
- `sentiment.json` (from evaluate Leg 2)
- `competitor_matrix.json` (from benchmark)
- Target company name and contact person (if known)
- Language: HU or EN

## Persuasion Framework

Read `D:\.claude\skills\superpowers-evolved\writing-skills\persuasion-principles.md` before generating.

Apply these 4 principles:

| Principle | Application in Teaser |
|-----------|----------------------|
| **Authority** | Position as methodology-driven audit, not opinion. "47-point assessment" + named frameworks. |
| **Scarcity** | Time-sensitive competitive gap. "[Competitor] launched [feature] [date]. Every month without it costs estimated €X." |
| **Social Proof** | Quote their OWN users' complaints. "On [source], your users say: '[actual quote]'." This is unanswerable. |
| **Commitment** | Small ask (20 minutes). The 3-page PDF creates reading investment. Once they see the gaps, they can't unsee them. |

**DO NOT use:** Liking (creates sycophancy), Reciprocity (feels manipulative), Unity (no shared identity yet).

## Email Generation

### Subject Line (max 70 chars)
Pattern: `[Company]'s users are asking for [feature] — [competitor] already has it`

Or: `[N] gaps [company] leaves vs [Tier 3 competitor] — [€X] on the table`

### Body (100-125 words, 4 paragraphs)

```
[AUTHORITY — 1 sentence]
We audited [company] against [Tier 3 competitor] across 47 dimensions —
UX, functionality, SEO, and AI search visibility.

[SOCIAL PROOF — 2 sentences]
Your users notice the gap. On [source], [verbatim user quote about a pain
point]. [Competitor] solved this [timeframe] ago with [specific feature].

[SCARCITY — 2 sentences]
[Competitor X] launched [specific feature] [date]. Each month without
[gap], an estimated €[conservative number] in [metric] is left on the table.

[COMMITMENT — small ask]
I've attached a 3-page preview with the top 5 findings. If [2 specific
findings] resonate, I can walk through the full analysis in 20 minutes —
no pitch, just the data.

[Signature]
```

### Language Rules
- **Hungarian targets:** Read hungarian-content-gate BEFORE writing. Use Ön register (B2B enterprise). Native phrasing, not translated English.
- **English targets:** Direct, consultative, no fluff. British English for European targets.

## PDF Preview Generation (3 pages)

### Page 1: Cover
- Hero visual generated via gpt-image-2-techniques (use your brand kit — see gpt-image-2-techniques/brand_kits/ for examples)
- Prompt: "Professional consulting audit report cover, [industry] sector, modern data visualization aesthetic, dark premium design with [brand accent color], no background, transparent, isolated design element"
- Target company name (text, not logo -- don't use their trademarked assets)
- "Business Evolution Preview" title
- Date + your consulting firm branding

### Page 2: Top 5 Findings
For each of the 5 highest-impact gaps:

```
[SEVERITY BADGE: Critical | High | Medium]

[Gap Name]
[One-line problem statement]

vs. [Competitor]: [What they do instead]
User signal: "[Quote from sentiment data]"
Estimated annual impact: €[conservative number]
```

**Rules:**
- Show WHAT is broken. Never show HOW to fix it.
- Use the competitor comparison to create urgency.
- Use the user quote for social proof.
- Use the revenue number for business case.

### Page 3: Comparison + Full Report Preview
- Radar chart comparing target vs Tier 3 best across 6 axes:
  1. User Experience
  2. Performance
  3. Feature Completeness
  4. SEO
  5. GEO / AI Visibility
  6. Business Model Sophistication

- "What's in the Full Report" table of contents:
  ```
  1. Executive Summary ................. 1 page
  2. Site Audit Report ................. 5 pages
  3. Competitive Landscape ............. 5 pages
  4. Gap Analysis ...................... 5 pages
  5. GEO/SEO Audit .................... 4 pages
  6. Revenue Opportunity Model ......... 4 pages
  7. Implementation Roadmap ............ 4 pages
  8. Next Steps + Pricing .............. 1 page
  ```

## Output Format

Generate as self-contained HTML with inline CSS (print-ready via Ctrl+P → Save as PDF).

Design reference: read `D:\.claude\skills\frontend-design-references\design-systems\linear.app-DESIGN.md` for dark premium aesthetic. Or `stripe-DESIGN.md` for clean professional.

## Output Files

- `evolution-audits/{slug}/teaser/email_draft.txt` -- ready-to-paste email body
- `evolution-audits/{slug}/teaser/preview.html` -- 3-page PDF (print from browser)
- `evolution-audits/{slug}/teaser/hero.png` -- cover image (if generated)
