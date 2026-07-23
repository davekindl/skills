# Scoring Rubrics

## Site Health Score (0-100)

6 sub-scores, weighted average:

| Sub-Score | Weight | What's Measured | 0 (terrible) | 50 (mediocre) | 100 (excellent) |
|-----------|--------|-----------------|--------------|---------------|-----------------|
| UX | 20% | Navigation clarity, form usability, visual design, CTA effectiveness | Confusing nav, broken forms, dated design | Functional but generic | Intuitive, modern, conversion-optimized |
| Performance | 15% | Load time, CWV proxy, resource optimization | >5s load, layout shifts, bloated JS | 2-4s load, acceptable CWV | <2s load, green CWV, optimized assets |
| Content | 20% | Depth, freshness, quality, multimedia, structure | Thin pages, stale content, no media | Adequate content, some media | Rich content, fresh, multimedia, structured data |
| Technical | 15% | Stack modernity, security, APIs, integrations | Legacy stack, no HTTPS, no API | Functional stack, basic security | Modern stack, CDN, APIs, security headers |
| Mobile | 15% | Responsive design, touch targets, mobile UX | Desktop-only or broken mobile | Responsive but not optimized | Mobile-first, PWA-ready, native-quality |
| Accessibility | 15% | Semantic HTML, alt texts, keyboard nav, ARIA | No semantic markup, images without alt | Partial compliance | WCAG 2.1 AA compliant |

**If Leg 1 (Playwright) is blocked:** Weight UX and Mobile at 0, redistribute to other sub-scores proportionally. Note in report.

## Competitive Position Score (percentile)

```
position = (target_features / tier3_average_features) * 100
```

Capped at 100. Score >80 = market leader. Score <40 = significant gap risk.

## GEO Score (0-100)

See `geo-checklist.md` for full 47-point checklist. Score is percentage of checks passed.

| Range | Rating |
|-------|--------|
| 80-100 | AI-ready: actively optimized for generative search |
| 60-79 | Partially visible: some AI citations likely |
| 40-59 | Minimal visibility: rarely cited by AI |
| 0-39 | AI-invisible: actively blocked or structurally incompatible |

## Business Model Maturity (1-5)

| Level | Name | Characteristics |
|-------|------|-----------------|
| 1 | Startup | Single revenue stream, no data monetization, basic pricing |
| 2 | Growing | 2-3 revenue streams, some premium features, growing user base |
| 3 | Established | Diversified revenue, marketplace dynamics, brand recognition |
| 4 | Optimized | Data products, dynamic pricing, ecosystem of integrations |
| 5 | Market Leader | Platform economics, network effects, industry-standard brand |
