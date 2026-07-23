---
name: business-evolution-audit
description: "Proactive business/website evolution audit. Crawls a target site, benchmarks against local/domestic/global competitors, identifies gaps, models revenue impact, and produces a teaser package for consultation outreach. Trigger on: 'run evolution audit on [url]', 'business audit [url]', 'analyze [company]', 'generate teaser for [url]', 'what's wrong with [url]', 'benchmark [url]', 'evolution audit', 'proactive audit', 'site audit [url]', 'competitor analysis [url]'. Also trigger when the user mentions evaluating a business for consulting outreach, creating an unsolicited audit, or generating a teaser email for a target company."
---

# BUSINESS EVOLUTION AUDIT

> Proactive audit. Demonstrated expertise. Revenue-backed roadmap. The email doesn't say "hire me" -- it says "I already found what you're leaving on the table."

## Shared Infrastructure
- **Persuasion principles:** Read `references/persuasion-hooks.md` (included in this skill's references/)
- **Sibling skills leveraged:** the-inspector, seo-content-engine, deep-interrogation, gpt-image-2-techniques, grand-slam-offer

## How It Works

5 sub-skills orchestrated by this master file. Steps 1-2 run in parallel, 3-5 are sequential.

```
INPUT: target URL + optional industry hint
         │
    ┌────┴────┬───────────┐
    ▼         ▼           ▼     (parallel)
 EVALUATE  BENCHMARK  UNIQUENESS
    │         │           │
    └────┬────┴───────────┘
         ▼
       PLAN
         │
    ┌────┴────┐
    ▼         ▼         (parallel)
  TEASER    PRICE
    │         │
    └────┬────┘
         ▼
      COMPILE + HUMAN REVIEW
```

## Input

```
Required: target URL (e.g., "ingatlan.com")
Optional: industry hint (e.g., "real-estate-portal")
Optional: output mode — "teaser-only" | "snapshot" | "full-audit"
Optional: language — "hu" | "en" (default: detect from target site)
```

If no industry hint, auto-detect from site content during EVALUATE.

## Orchestration

### Step 1+2: EVALUATE + BENCHMARK (parallel)

Read and invoke:
- `skills/evaluate.md` with the target URL → `site_health.json` + `sentiment.json` + `technical_audit.json`
- `skills/benchmark.md` with the target URL + industry → `competitor_matrix.json`

These have NO dependencies on each other. Run via parallel Agent dispatch.

### Step 2b: UNIQUENESS (parallel with 1+2)

Invoke the **`ai-uniqueness-test`** skill on the target (named competitors from BENCHMARK, JTBD situation-queries from the niche) → `uniqueness_card.json` + an HTML Uniqueness Card. This is the SELECTION axis — whether AI sees the target as a category-of-one or a swappable commodity — the differentiator no competing GEO/AEO tool measures. Two-mode (bare + grounded), local-Claude-compliant. The recommendation probe in EVALUATE measures *presence* (does AI name you); this measures *substitutability* (when AI picks, are you singular or swappable). Both feed PLAN.

### Step 3: PLAN

Read and invoke `skills/plan.md` with all Step 1+2+2b outputs → `gap_analysis.json` + `roadmap.json` + `seo_geo_audit.json`. Fold each low Uniqueness metric into the roadmap as an implementation-ready scope.

### Step 4+5: TEASER + PRICE (parallel)

Read and invoke:
- `skills/teaser.md` with Step 3 outputs → `teaser.html` + `email_draft.txt`
- `skills/price.md` with Step 3 outputs + industry → `pricing.json`

### Step 6: COMPILE

Assemble the full output package:

```
evolution-audits/{target-slug}/
├── reports/
│   ├── site_health.json
│   ├── sentiment.json
│   ├── technical_audit.json
│   ├── competitor_matrix.json
│   ├── gap_analysis.json
│   ├── roadmap.json
│   ├── seo_geo_audit.json
│   ├── uniqueness_card.json   ← substitutability / category-of-one (ai-uniqueness-test)
│   └── pricing.json
├── teaser/
│   ├── email_draft.txt          ← ready to paste/send
│   ├── preview.html             ← 3-page teaser PDF (print from browser)
│   └── hero.png                 ← generated via gpt-image-2
├── full_report.html             ← 25-35 page report (snapshot/full mode only)
└── audit_meta.json              ← timestamp, target, industry, scores summary
```

### Step 7: HUMAN REVIEW GATE

Present to the user:
```
Evolution audit complete for [target].

Scores: Site Health [X/100] | Competitive Position [X%ile] | GEO [X/100] | Uniqueness [X/100 grounded]
Gaps found: [N] (Critical: [N], Opportunity: [N], Differentiation: [N])
Revenue opportunity: €[X] estimated annual impact

REVIEW CHECKLIST (15 min):
□ Facts correct? (company description, business model)
□ Comparisons fair? (competitors are actually comparable)
□ Revenue estimates sane? (right order of magnitude)
□ Tone consultative? (not aggressive or condescending)
□ Legal clean? (no disparagement, no confidential data)

Teaser email ready at: evolution-audits/{slug}/teaser/email_draft.txt
```

Do NOT send anything without the user's explicit approval.

## Output Modes

| Mode | What's Produced | When to Use |
|------|----------------|-------------|
| **teaser-only** | Teaser email + 3-page PDF preview | Outreach / Octopus nightly batch |
| **snapshot** | 10-page focused report + teaser | When prospect responds to teaser |
| **full-audit** | 30-page report + roadmap + revenue model + teaser | Paid engagement deliverable |

## Anti-Patterns

- **Never fabricate metrics.** If Playwright is blocked and we can't measure load time, say "blocked by anti-bot, unable to measure directly" -- don't guess.
- **Never disparage the target.** The tone is "here's what you could gain" not "here's how bad you are." Consultative, not condescending.
- **Never reveal implementation details in the teaser.** Show WHAT's broken, never HOW to fix it. The how is the paid deliverable.
- **Never send without human review.** Even in Octopus nightly mode, teasers go to a review queue, not directly to prospects.
- **Never use the target company's trademarked logos or assets** in the teaser without permission.

## Gotchas (from production runs)

- **Hybrid Firecrawl + custom fetch beats either alone.** Firecrawl for JS rendering, custom fetch for robots.txt/llms.txt/headers. Use both.
- **Free LLMs hallucinate local businesses at ~70% rate** — this IS the selling point, not a bug. Frame it as the diagnostic finding.
- **The Race Card (competitive comparison) is 10x more powerful** than an abstract "you're invisible" pitch. Always include a named competitor who IS visible.
- **GEO score does NOT correlate with AI recommendations** — reputation/training data dominates. Don't oversell GEO as a silver bullet.
- **"You're AI invisible" is misleading for big brands** — ChatGPT knows Helvetic by reputation alone. Frame as "not optimized" instead.
- **A stat without a findable primary artifact is poison.** Cross-check every claim against the source document, not the folklore.
- **Derived sums (29+53=82) ship only with explicit derivation phrasing** — never as a quoted study stat.
- **Real audit scores with relabeled axes beat derived mappings** — when a radar needs filling, find the measurement that already exists.
- **Per-prospect probe cost: ~$0.45 OpenRouter + 6 subagent runs + ~30 min wall time.** Budget accordingly.

## Reference Files

| File | Read When |
|------|-----------|
| `skills/evaluate.md` | Step 1 |
| `skills/benchmark.md` | Step 2 |
| `skills/plan.md` | Step 3 |
| `skills/teaser.md` | Step 4 |
| `skills/price.md` | Step 5 |
| `references/scoring-rubrics.md` | During evaluate + plan |
| `references/geo-checklist.md` | During plan (SEO/GEO audit) |
| `references/persuasion-hooks.md` | During teaser generation |
| `references/pricing-guide.md` | During pricing |
| `references/industry-templates/*.md` | During benchmark + plan (industry-specific gaps) |
| `ai-uniqueness-test` skill | Step 2b — uniqueness / substitutability axis |
