# GEO Audit Checklist (47 Points)

Based on Princeton KDD 2024 research + AutoGEO ICLR 2026 methodology.

## Crawler Access (5 checks)
- [ ] GPTBot allowed in robots.txt
- [ ] ClaudeBot allowed in robots.txt
- [ ] PerplexityBot allowed in robots.txt
- [ ] Google-Extended allowed in robots.txt
- [ ] No blanket "Disallow: /" for AI crawlers

## llms.txt & AI Metadata (5 checks)
- [ ] llms.txt exists at root
- [ ] llms.txt contains meaningful description (not placeholder)
- [ ] llms.txt lists key pages/sections
- [ ] Schema.org Organization entity present
- [ ] Knowledge Graph entity exists (Google Knowledge Panel)

## Content Citability (10 checks)
- [ ] Pages have answer-first structure (direct answer in first 40-60 words of sections)
- [ ] H2/H3 headers use question format matching real search queries
- [ ] FAQ sections exist with 5+ Q&A pairs
- [ ] FAQ uses FAQPage schema markup
- [ ] Content contains quotable definitions (single-sentence, standalone-extractable)
- [ ] Statistics and data points have inline source citations
- [ ] Content updated within last 13 weeks (50% of AI-cited content is <13 weeks old)
- [ ] Author attribution with credentials present
- [ ] Content has clear topical authority (depth > breadth)
- [ ] Pages are self-contained (each section works as standalone extraction)

## Structured Data (7 checks)
- [ ] Organization JSON-LD present
- [ ] Article/Product/Service schema on relevant pages
- [ ] BreadcrumbList schema for navigation
- [ ] HowTo schema where applicable
- [ ] Local Business schema if applicable
- [ ] Review/AggregateRating schema where applicable
- [ ] Schema validates without errors (Google Rich Results Test)

## Brand Entity Coherence (5 checks)
- [ ] Consistent brand name across all platforms
- [ ] Wikipedia/Wikidata entity exists
- [ ] LinkedIn company page complete and active
- [ ] Google Business Profile claimed and accurate
- [ ] Brand mentions in authoritative third-party sources

## Trust Stack (8 checks)
- [ ] Author bios with credentials on content pages
- [ ] Clear editorial policy or methodology page
- [ ] Source citations in content (outbound links to authoritative sources)
- [ ] Original research or proprietary data published
- [ ] Industry awards, certifications, or partnerships displayed
- [ ] Customer testimonials with specifics (not generic praise)
- [ ] Transparent pricing (if applicable)
- [ ] Contact information easily accessible

## AI Citation Testing (7 checks)
- [ ] Test 5 industry-relevant questions in ChatGPT -- target cited? (Y/N per query)
- [ ] Test 5 industry-relevant questions in Perplexity -- target cited?
- [ ] Test 5 industry-relevant questions in Claude -- target cited?
- [ ] Test 5 industry-relevant questions in Gemini -- target cited?
- [ ] Count total citations across 20 queries
- [ ] Compare citation frequency vs top competitor
- [ ] Identify which queries cite competitors but NOT the target (gap queries)

## Scoring
Each check: 1 point if passed, 0 if failed.
GEO Score = (points earned / 47) × 100
