---
name: seo-content-engine
description: "SEO + GEO content engine. Keyword research, content briefs, SEO-optimized articles, meta elements, schema markup, GEO (Generative Engine Optimization) for AI search visibility, and content refresh scheduling. Trigger on: 'write SEO content', 'SEO article', 'content brief', 'keyword research', 'optimize for SEO', 'refresh this content', 'GEO optimize', 'seo content engine', 'what should I write about', 'AI search visibility', 'generative search optimization', 'make this citeable by AI', 'llms.txt'. Also triggers when the user mentions organic traffic, search rankings, or content strategy for their products."
---

# SEO CONTENT ENGINE

> Keyword research -> content brief -> optimized article -> meta elements -> schema markup -> GEO layer -> refresh schedule. Every piece ships with an expiry date.

## Shared Infrastructure
- **GEO core checks (apply to every piece):** valid structured data (JSON-LD schema), clean title + heading hierarchy, a named author with credentials, 3+ internal links, and a visible published/updated date kept fresh
- **Sibling skills:** content-atomizer (repurpose the article into 10 formats after publishing)

## 7-Phase Workflow

### Phase 1: Discovery (2-5 questions)
- Target domain/URL (for internal linking context)
- Target audience segment
- Content goal: traffic | leads | authority | GEO/AI visibility
- Existing content inventory (URL or sitemap)
- Competitive differentiator (what you know that competitors don't)

### Phase 2: Keyword Research
**Tools:** WebSearch

Run these queries:
```
"[topic] + related terms"
"people also ask [topic]"
"[topic] site:reddit.com" (real pain points)
"[topic] vs [alternative]"
"[topic] 2026"
```

Produce: primary keyword, 5-10 secondary keywords, 5-10 question-format queries, intent classification per keyword.

Build topic cluster map: one pillar page + satellite articles.

### Phase 3: Competitive Analysis
**Tools:** WebSearch, WebFetch

Fetch top 3-5 ranking pages for primary keyword. Extract: word count, heading structure, content type, topics covered, gaps. Identify the content gap (what they all miss). Set target word count.

### Phase 4: Content Brief (HUMAN GATE)
Output a structured brief. **you review before Phase 5 begins.**

Contents:
- Primary + secondary keywords with placement rules
- Search intent classification
- Title tag + meta description drafts
- URL slug
- Content outline (H1/H2/H3 hierarchy with question-format headers)
- Target word count per section
- Questions to answer (from PAA + Reddit)
- Internal link targets
- External citation targets (5-8 authoritative sources)
- CTA specification
- Competitive gap to exploit

Save to file. Wait for approval.

### Phase 5: Article Generation
Write article following the approved brief, applying:

- **Answer-first structure:** direct answer in first 40-60 words of each section
- **Question-format H2/H3 headers:** mirror actual search queries
- **Fact density:** 1 statistic per 150-200 words, each cited
- **`[EXPERT QUOTE NEEDED]` markers:** where your personal experience is required
- **`[ORIGINAL DATA NEEDED]` markers:** where AI cannot substitute for real data
- **FAQ section:** 5-10 Q&A pairs (FAQPage schema-ready)
- **Internal links:** minimum 3 from the brief
- **External citations:** 5-8 to authoritative sources

### Phase 6: Quality Audit
Audit the saved article manually against the checklist below. Treat these as FAIL conditions that block Phase 7: keyword stuffing, missing H1, skipped heading level, title >60 chars. Everything else is advisory.

Checks to perform (mechanical, checkable by reading the draft):
- Keyword density (primary 1-2%, warn if >2.5%) + secondary keyword presence
- Heading hierarchy (no skipped levels) + question-format H2/H3 ratio
- Internal links (minimum 3, warn if <3)
- External citations (minimum 5 for pillar content)
- Fact density (flag sections with 0 data points)
- Experience signals (first-person markers present?) + unresolved `[...NEEDED]` markers
- Meta title length (<60 chars)
- Meta description length (140-160 chars)
- Anti-pattern scan: keyword stuffing, generic AI tone, missing E-E-A-T

Judgment checks: answer-first compliance per section, intent match, original-angle quality. Review these by reading the draft.

### Phase 7: Deliverables
Output package:
1. Final article (Markdown)
2. Meta elements (title, description, slug)
3. Schema markup (JSON-LD: Article, FAQPage, BreadcrumbList)
4. Internal linking suggestions with anchor text
5. Content refresh schedule: stats check 3mo, competitive re-analysis 6mo, full rewrite 12mo. **Persist this schedule to a Memory-tool ledger** (one entry per published URL: slug, publish date, and the three due-dates) so content decay is tracked across sessions and surfaced when a refresh comes due — publication is not the finish line (Anti-Pattern #6).
6. GEO readiness checklist (pass/fail per criterion)

## GEO Layer (applied on top of SEO)

GEO = Generative Engine Optimization. Making content citable by ChatGPT, Perplexity, Claude, Gemini.

**Key difference from SEO:** SEO optimizes for ranking in search result lists. GEO optimizes for being CITED inside AI-generated answers. AI engines favor fresh pages — content they cite is on average ~26% fresher than organic results (Ahrefs, 17M-citation study).

**GEO enhancements (Phase 5):**
- Self-contained H2 sections (each works as standalone extraction)
- Quotable definitions (single-sentence, standalone-extractable)
- Direct expert quotes with credentials
- FAQ sections with brief, extractable answers
- AI crawler verification (GPTBot, ClaudeBot, PerplexityBot access)
- llms.txt recommendation

The enhancement list above plus the GEO core checks under Shared Infrastructure are the complete GEO layer for this skill — apply every item in Phase 5 and score them in the Phase 7 readiness checklist.

## Anti-Patterns (NEVER do these)
1. **Scaled content abuse:** Never batch-publish unedited AI articles. 42% traffic decline documented.
2. **Keyword stuffing:** Cap primary keyword at 2% density. AI tends to over-optimize.
3. **Missing experience signals:** Flag when content has zero first-person markers or expert quotes.
4. **Orphan pages:** Never finalize without 3+ internal link suggestions.
5. **Intent mismatch:** Validate content type matches SERP intent before writing.
6. **Ignoring content decay:** Every piece ships with a refresh schedule. Publication is not the finish line.
7. **Generic AI tone:** Check for original angles. "Technically correct but says nothing new" = fail.

## Tool Integration

| Phase | Tool | Purpose |
|-------|------|---------|
| 2 | WebSearch | Keyword discovery, PAA extraction, Reddit pain points |
| 3 | WebSearch, WebFetch | Competitive content analysis |
| 4 | Write | Save content brief for review |
| 5 | Write | Save article as Markdown |
| 5 | WebSearch | Verify stats and citations |
| 6 | Read | Manual audit: keyword density, heading hierarchy, meta, link, fact-density checks |
| 7 | Write | Schema JSON-LD, meta elements, refresh schedule |
| 7 | Memory | Persist per-URL refresh schedule (content-decay ledger) |

## Reference Files
| File | Read When |
|------|-----------|
| `references/schema-templates.md` | Phase 7 JSON-LD generation (Article, FAQPage, BreadcrumbList) |

The Phase 5 writing techniques (answer-first structure, question-format headers, fact density, experience markers) and the GEO enhancements are specified in full in this file — no external reference needed.
