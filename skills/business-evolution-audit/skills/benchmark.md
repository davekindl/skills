# BENCHMARK -- Three-Tier Competitor Analysis

## Purpose
Find and analyze competitors across three tiers, build a Feature Matrix showing what exists where, and identify the target's competitive position.

## Three-Tier Discovery

### Tier 1: Local Competitors (same market, same language)

**Search queries:**
```
WebSearch: "[target industry] [target country/city]"
WebSearch: "[target] versenytárs" (Hungarian: competitor)
WebSearch: "[target] alternative [country]"
WebSearch: "[target industry] site [target country TLD]"
```

Find 3-5 local competitors. For ingatlan.com: jofogas.hu, otthonterkep.hu, ingatlanbazar.hu

### Tier 2: Domestic/Regional Leaders (adjacent markets, comparable scale)

**Search queries:**
```
WebSearch: "[target industry] [neighboring countries]"
WebSearch: "best [target industry] central europe"
WebSearch: "[target industry] Czech OR Slovak OR Romanian OR Polish"
```

Find 3 regional comparables. For ingatlan.com: sreality.cz, nehnutelnosti.sk, imobiliare.ro

### Tier 3: Global Best-in-Class (what the best version looks like)

**Search queries:**
```
WebSearch: "best [target industry] platform world"
WebSearch: "[target industry] market leader global"
WebSearch: "[target industry] most innovative features 2026"
```

Find 3 global leaders. For ingatlan.com: Zillow, Rightmove, Idealista, Hemnet

## Feature Matrix Construction

For each competitor (target + all tiers), assess these dimensions:

| Dimension | What to Check |
|-----------|---------------|
| **Core Features** | The basic table-stakes features for this industry |
| **Search/Discovery** | How users find what they want (filters, maps, AI, recommendations) |
| **Data/Analytics** | What data the platform surfaces (price history, market trends, valuations) |
| **User Experience** | Mobile app quality, page speed, design modernity, accessibility |
| **Content Depth** | Photos, videos, 3D tours, descriptions, neighborhood info |
| **Trust/Social** | Reviews, ratings, verified listings, agent profiles |
| **Monetization** | Revenue model sophistication (ads, premium listings, SaaS, data products) |
| **AI/Innovation** | AI features (chatbots, recommendations, valuations, virtual staging) |
| **Community** | Forums, guides, blog, educational content |
| **Integration** | APIs, partner ecosystems, mortgage calculators, legal tools |

**For each feature found, record:**
- Which competitor has it
- How well implemented (basic / good / excellent)
- When it was launched (if findable -- recency matters)

**Build the matrix as a markdown table** saved to `competitor_matrix.json`.

## Competitive Position Score

Calculate the target's percentile rank within the matrix:
- Count total features across all dimensions
- Count how many the target has vs. Tier 3 average
- Position = (target features / Tier 3 average features) × 100

Example: Target has 45 features, Tier 3 average has 78 → Position = 58th percentile.

## Industry Template Integration

If an industry template exists at `references/industry-templates/{industry}.md`, read it BEFORE starting research. It contains a pre-built gap library with common features for that industry, saving research time.

If no template exists, the benchmark builds the feature list from scratch and the output can be saved as a new industry template for future audits.

## Output

```json
{
  "target": "ingatlan.com",
  "industry": "real-estate-portal",
  "competitors": {
    "tier1_local": [...],
    "tier2_regional": [...],
    "tier3_global": [...]
  },
  "feature_matrix": {
    "dimensions": [...],
    "scores": {...}
  },
  "competitive_position_percentile": 58,
  "standout_gaps": [...],
  "standout_strengths": [...]
}
```

Save to `evolution-audits/{slug}/reports/competitor_matrix.json`.
