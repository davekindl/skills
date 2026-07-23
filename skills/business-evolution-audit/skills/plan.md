# PLAN -- Gap Analysis + Revenue Modeling + Roadmap

## Purpose
Cross-reference evaluate outputs against benchmark outputs to produce: categorized gaps, revenue impact estimates, and a phased 12-month roadmap.

## Inputs Required
- `site_health.json` (from evaluate)
- `competitor_matrix.json` (from benchmark)
- Industry template if available

## Phase 1: Gap Categorization

Cross-reference the Feature Matrix against the target's capabilities. For each gap:

### Category Assignment

| Category | Definition | Example |
|----------|-----------|---------|
| **Critical** | ALL Tier 3 competitors have this. Target doesn't. Table stakes the target is missing. | Zillow, Rightmove, Idealista ALL have price history charts. Target doesn't. |
| **Opportunity** | 2+ competitors have this. Clear market expectation forming. | 3 of 6 competitors have AI-powered property recommendations. |
| **Differentiation** | NO competitor has this. Would create unique advantage. | None offer AI-generated neighborhood safety analysis from public data. |
| **Parity** | Target has the feature but executes poorly vs competitors. | Target has search filters but they're clunky vs Zillow's instant-filter UX. |

### Effort/Impact Matrix

For each gap, score:
- **Impact** (1-5): Revenue/user impact if fixed
- **Effort** (1-5): Development cost and complexity

Place in quadrant:
- **Quick Win** (high impact, low effort) → Phase 1
- **Strategic** (high impact, high effort) → Phase 2-3
- **Fill Later** (low impact, low effort) → Phase 3 or backlog
- **Ignore** (low impact, high effort) → Don't include in roadmap

## Phase 2: SEO/GEO Audit

Read `references/geo-checklist.md` for the full 47-point checklist. Key checks:

**SEO Baseline:**
- robots.txt configuration (from evaluate Leg 3)
- Sitemap presence and structure
- Meta tags quality (title, description, OG tags)
- Structured data (JSON-LD: Organization, Product, FAQ, BreadcrumbList)
- Internal linking depth
- Page speed indicators
- Mobile-friendliness

**GEO Layer (AI Search Visibility):**
- AI crawler access (GPTBot, ClaudeBot, PerplexityBot)
- llms.txt presence
- Content citability (answer-first structure, standalone paragraphs)
- Brand entity coherence
- Citation test: ask 5 questions about [industry] in [market] to ChatGPT/Perplexity/Claude -- does the target get cited?
- FAQ section presence and extractability

Score both: SEO Score (0-100) + GEO Score (0-100).

## Phase 3: Revenue Opportunity Modeling

For each Critical and Opportunity gap, model revenue impact:

**Inputs:**
- Estimated monthly traffic (from SimilarWeb/public estimates via WebSearch)
- Industry conversion benchmarks (from references or WebSearch)
- Competitor feature → conversion lift data (when available)
- Current monetization model

**Revenue formula per gap:**
```
annual_impact = monthly_users_affected × conversion_lift × avg_revenue_per_conversion × 12
```

**Three scenarios:**
- Conservative (10th percentile of benchmark improvement)
- Moderate (median)
- Aggressive (75th percentile)

**Always use conservative in the teaser.** Moderate in the full report. Aggressive as upside footnote.

**State all assumptions.** "We estimate 2.3M monthly visitors based on SimilarWeb data (±30%). Conversion lift of 0.3% is the median from Baymard Institute's checkout optimization benchmarks."

## Phase 4: Implementation Roadmap

Structure as 3 phases across 12 months:

### Phase 1: Quick Wins (Month 1-3)
- All high-impact, low-effort gaps
- Typically: SEO/GEO fixes, UX improvements, content optimization, mobile fixes
- Cost estimate: €5K-25K
- Expected ROI: positive within 3 months

### Phase 2: Strategic Features (Month 4-6)
- Medium-effort, high-differentiation gaps
- Typically: new functionality, API integrations, data products
- Cost estimate: €25K-100K
- Expected ROI: positive within 6-9 months

### Phase 3: Platform Evolution (Month 7-12)
- Major features, AI capabilities, business model expansion
- Typically: ML-powered features, marketplace extensions, data monetization
- Cost estimate: €50K-250K
- Expected ROI: positive within 12-18 months

Each phase includes: deliverables list, effort estimate, expected revenue impact, success metrics, dependencies on prior phases.

## Phase 5: Integrate Sentiment Data

Overlay user sentiment from evaluate Leg 2 onto the gap analysis:
- Match user complaints to specific gaps ("users complain about slow search" → Gap #3: Search performance)
- Rank gaps by sentiment intensity (more complaints = higher priority)
- Extract quotable user statements for the teaser (sanitized, no PII)
- Flag gaps where users are actively comparing to competitors ("I switched to X because...")

## Output

```json
{
  "gaps": [
    {
      "id": "G01",
      "name": "Price History Charts",
      "category": "critical",
      "competitors_with": ["Zillow", "Rightmove", "Idealista"],
      "effort": 2,
      "impact": 4,
      "quadrant": "quick_win",
      "phase": 1,
      "revenue_estimate": {"conservative": 120000, "moderate": 280000, "aggressive": 450000},
      "sentiment_matches": ["'Why can't I see what the price was last year?' - Reddit user"],
      "implementation_notes": "Historical listing data likely exists in DB. Frontend chart component + API endpoint."
    }
  ],
  "seo_score": 58,
  "geo_score": 31,
  "total_revenue_opportunity": {"conservative": 890000, "moderate": 2100000},
  "roadmap": {
    "phase1": {...},
    "phase2": {...},
    "phase3": {...}
  }
}
```

Save to `evolution-audits/{slug}/reports/gap_analysis.json` and `roadmap.json`.
